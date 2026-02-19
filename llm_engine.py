import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_evaluate(prompt):

    evaluation_prompt = f"""
You are a prompt engineering evaluator.

Score the following prompt from 0 to 10 for:

1. Clarity
2. Specificity
3. Constraint Definition
4. Output Format Definition

Return STRICT JSON only like:

{{
  "clarity": 0,
  "specificity": 0,
  "constraints": 0,
  "format": 0,
  "feedback": "text",
  "improved_prompt": "rewritten version"
}}

Prompt:
{prompt}
"""

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": "You are a strict evaluator."},
            {"role": "user", "content": evaluation_prompt}
        ]
    )

    return response.choices[0].message.content
