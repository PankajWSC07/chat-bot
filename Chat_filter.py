from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def refine_answer(question, context_docs):

    context = "\n".join(context_docs)

    prompt = f"""Based on the following context, answer the question accurately and concisely.
Be helpful and provide clear information. Do not add information not in the context.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on provided context.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        refined_answer = response.choices[0].message.content
        return refined_answer

    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        return None
