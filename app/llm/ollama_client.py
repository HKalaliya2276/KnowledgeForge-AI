import ollama

from app.config.settings import OLLAMA_MODEL


class OllamaClient:

    @staticmethod
    def generate(
        query,
        context
    ):

        prompt = f"""
You are a cybersecurity assistant.

Use ONLY the provided context.

Rules:
- Answer in under 120 words
- Be direct and concise
- Focus only on the user's question
- Do not repeat information
- Do not explain unrelated concepts
- Use English only
- If partial answer exists in context, answer it

QUESTION:
{query}

CONTEXT:
{context}

SHORT ANSWER:
"""

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.1,
                "num_predict": 80
            }
        )

        return response["message"]["content"]