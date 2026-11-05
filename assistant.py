
from ollama import chat
import memory
import memory_manager
import vector_memory


MODEL = "Astolfo"

memory.initialize()
vector_memory.sync_sqlite_memories()

SYSTEM_PROMPT = """
Você é um assistente virtual inteligente, prestativo e confiável.

REGRAS DE COMPORTAMENTO:

1. Interprete cuidadosamente a pergunta antes de responder.
2. Responda exatamente ao que o usuário perguntou.
3. Não invente informações, dados ou acontecimentos.
4. Se não souber algo, admita que não sabe.
5. Utilize o histórico da conversa para compreender o contexto.
6. Evite respostas repetitivas ou desnecessariamente longas.
7. Explique conceitos técnicos de maneira simples e didática.
8. Diferencie fatos, opiniões e hipóteses.
9. Responda em português brasileiro, salvo solicitação contrária.
10. Seu nome é Astolfo. Não troque de nome se não for solicitado.

Seu objetivo é fornecer respostas corretas, coerentes e naturais.
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# Recupera histórico anterior
messages.extend(memory.get_recent_messages(limit=10))

# Recupera memórias permanentes
def load_memories():

    saved_memories = memory.get_memories()

    if saved_memories:

        context = "\n".join(
            f"- {item[1]}"
            for item in reversed(saved_memories[:30])
        )

        messages[0]["content"] = (
            SYSTEM_PROMPT
            + "\n\nInformações sobre o usuário:\n"
            + context
        )


load_memories()


def retrieve_memory_context(query):

    results = vector_memory.search_memories(
        query=query,
        limit=5,
        max_distance=0.75
    )

    if not results:
        return ""

    context = "\n".join(
        f"- {item['content']}"
        for item in results
    )

    print(
        f"\n[VECTOR] {len(results)} memórias relevantes encontradas."
    )

    return (
        "Informações relevantes recuperadas da memória "
        "de longo prazo:\n"
        + context
        + "\nUtilize essas informações apenas quando "
          "forem pertinentes à pergunta. "
          "Não invente fatos adicionais."
    )



def show_memories():

    memories = memory.get_memories()

    if not memories:
        print("\nNenhuma memória cadastrada.\n")
        return

    print("\n===== MINHAS MEMÓRIAS =====")

    for item in memories:
        print(f"[{item[0]}] {item[1]}")

    print("===========================\n")


print("=" * 50)
print("          MINHA IA LOCAL")
print("          MEMORIA AUTOMATICA")
print("=" * 50)

print("""
Comandos:
/sair       - Encerrar
/reset      - Limpar histórico
/memorias   - Consultar memórias
/lembrar    - Salvar memória manualmente
/esquecer   - Excluir memória]
/reset_memory - Reseta a memória
/buscar - Busca a memória no banco de dados
""")


while True:

    try:

        user_input = input("\nVocê: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "/sair":
            print("Encerrando assistente...")
            break

        elif user_input.lower() == "/reset":

            memory.clear_history()

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            load_memories()

            print("\nHistórico apagado!\n")
            continue

        elif user_input.lower() == "/memorias":
            show_memories()
            continue

        elif user_input.lower().startswith("/lembrar "):

            content = user_input[9:].strip()

            if content and not memory.memory_exists(content):
                memory_id = memory.save_memory(content)
                vector_memory.index_memory(memory_id, content)
                print("\nMemória salva!\n")
            else:
                print("\nInformação vazia ou já cadastrada.\n")

            continue

        elif user_input.lower().startswith("/esquecer "):

            try:
                memory_id = int(user_input[10:].strip())

                if memory.delete_memory(memory_id):
                    vector_memory.delete_vector_memory(memory_id)
                    print("\nMemória excluída dos bancos!\n")

                else:
                    print("\nMemória não encontrada.\n")

            except ValueError:
                print("\nInforme um ID válido.\n")

            continue

        elif user_input.lower().startswith("/buscar "):

            query = user_input[8:].strip()

            results = vector_memory.search_memories(
                query,
                limit=5,
                max_distance=0.45
            )

            print("\n===== RESULTADOS DA BUSCA =====")

            if results:
                for item in results:
                    print(f"\nMemória: {item['content']}")
                    print(f"Distância: {item['distance']:.4f}")
            else:
                print("Nenhuma memória relevante encontrada.")

            print("\n===============================\n")
            continue

        elif user_input.lower() == "/reset_memory":

            memory.reset_memory()
            print("\nMemória reiniciada!\n")
            continue

        # Registra mensagem
        messages.append({
            "role": "user",
            "content": user_input
        })

        memory.save_message("user", user_input)

        print("\nAstolfo: ", end="", flush=True)

        # Pesquisa memórias relacionadas à pergunta
        memory_context = retrieve_memory_context(user_input)

        # Prepara o contexto sem alterar o histórico permanente
        request_messages = [messages[0]]

        if memory_context:
            request_messages.append({
                "role": "system",
                "content": memory_context
            })

        request_messages.extend(messages[1:])

        response = chat(
            model=MODEL,
            messages=request_messages,
            stream=True
        )
        
        answer = ""

        for chunk in response:
            content = chunk.message.content
            print(content, end="", flush=True)
            answer += content

        print("\n")

        messages.append({
            "role": "assistant",
            "content": answer
        })

        memory.save_message("assistant", answer)

        # Analisa a conversa e salva novas memórias
        extracted = memory_manager.process_conversation(user_input)

        if extracted:
            load_memories()

    except KeyboardInterrupt:
        print("\nEncerrando...")
        break

    except Exception as error:
        print(f"\nErro: {error}\n")
