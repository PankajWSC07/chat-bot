# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1",
# )

# response = client.responses.create(
#     input="explain quantum computer",
#     model="llama-3.1-8b-instant",
# )


system_prompt = """
    pankaj makvana
    makvana pankaj 
"""
print(system_prompt)