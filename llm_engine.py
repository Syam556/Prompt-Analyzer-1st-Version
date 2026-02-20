import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def llm_evaluate(prompt):

    evaluation_prompt = f"""
You are a strict prompt engineering evaluator.

Score the following prompt from 0 to 10 for:

1. Clarity
2. Specificity
3. Constraint Definition
4. Output Format Definition

Return ONLY valid JSON in this format:

{{
  "clarity": 0,
  "specificity": 0,
  "constraints": 0,
  "format": 0,
  "feedback": "text explanation",
  "improved_prompt": "rewritten optimized prompt"
}}

Prompt:
{prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=evaluation_prompt,
    )

    text = response.text.strip()

    # Clean markdown formatting if Gemini wraps JSON
    if text.startswith("```"):
        text = text.split("```")[1]

    return text