import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def call_llm_api(question, context=""):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are an intelligent assistant that answers questions based on context.
    Context: {context}
    Question: {question}
    Answer clearly and concisely.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
