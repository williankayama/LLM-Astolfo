
import json
from ollama import chat
import memory
import vector_memory

MODEL = "Astolfo"


def extract_memories(user_message):

    prompt = f"""
Você é um sistema de extração de memórias.

Sua única fonte de informação é a mensagem escrita pelo usuário.

Extraia apenas informações pessoais explícitas que o usuário
declarou sobre si mesmo.

Regras:
- Ignore qualquer informação que não esteja na mensagem.
- Não utilize conhecimentos externos.
- Não invente informações.
- Não transforme perguntas em fatos pessoais.
- Não salve hipóteses ou suposições.
- Não salve informações escritas pelo assistente.
- Se não houver informação relevante, retorne uma lista vazia.

Retorne exclusivamente JSON neste formato:

{{
    "memories": [
        "Informação declarada pelo usuário"
    ]
}}

Mensagem do usuário:
{user_message}
"""

    try:
        response = chat(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            format="json",
            stream=False
        )

        result = json.loads(response.message.content)

        memories = result.get("memories", [])

        if not isinstance(memories, list):
            return []

        return [
            item.strip()
            for item in memories
            if isinstance(item, str) and item.strip()
        ]

    except Exception as error:
        print(f"[MEMORY ERROR] {error}")
        return []

    prompt = f"""
Você é um sistema de extração de memória de um
assistente pessoal.

Analise a mensagem do usuário e identifique
informações que possam ser úteis em conversas futuras.

Priorize:
- Nome e preferências declaradas.
- Estudos e profissão.
- Projetos em andamento.
- Objetivos de longo prazo.
- Preferências recorrentes.
- Informações importantes sobre o contexto do usuário.

Não salve:
- Perguntas genéricas.
- Informações temporárias.
- Curiosidades sem relevância pessoal.
- Suposições ou informações inventadas.
- Senhas, tokens ou dados de autenticação.
- Informações sensíveis.

Não transforme uma pergunta em um fato sobre o usuário.

Retorne somente JSON neste formato:

{{
    "memories": [
        "Informação importante"
    ]
}}

Se não houver informações relevantes:

{{
    "memories": []
}}

Mensagem do usuário:
{user_message}

Resposta do assistente:
{assistant_response}
"""

    try:
        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json",
            stream=False
        )

        result = json.loads(response.message.content)

        memories = result.get("memories", [])

        if not isinstance(memories, list):
            return []

        return [
            item.strip()
            for item in memories
            if isinstance(item, str) and item.strip()
        ]

    except (ValueError, TypeError, KeyError) as error:
        print(f"[MEMORIA] Erro ao interpretar JSON: {error}")
        return []

    except Exception as error:
        print(f"[MEMORIA] Erro na extração: {error}")
        return []



def process_conversation(user_message):

    extracted = extract_memories(user_message)

    for item in extracted:

        if memory.memory_exists(item):
            continue

        memory_id = memory.save_memory(item)

        print(f"\n[MEMORY] Nova memória salva: {item}")

        try:
            vector_memory.index_memory(memory_id, item)

        except Exception as error:
            print(f"[VECTOR ERROR] {error}")

    return extracted