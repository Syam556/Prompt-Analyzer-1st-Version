import streamlit as st
import json
from scorer import rule_based_score
from llm_engine import llm_evaluate

st.title("🧠 Prompt Analyzer – AI Evaluation System")

user_prompt = st.text_area("Enter your prompt here:", height=200)

if st.button("Analyze Prompt"):

    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        # Rule-based score
        rule_score, rule_feedback = rule_based_score(user_prompt)

        # LLM evaluation
        llm_result = llm_evaluate(user_prompt)

        # 🔹 Clean Gemini output
        cleaned = llm_result.strip()

        # Remove markdown formatting
        if "```" in cleaned:
            cleaned = cleaned.split("```")[1]

        # Remove leading 'json'
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        # Extract only JSON object
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        cleaned = cleaned[start:end]

        try:
            llm_data = json.loads(cleaned)
        except Exception:
            st.error("LLM response formatting error.")
            st.write("Raw Response:")
            st.code(llm_result)
            st.stop()

        # 🔹 Calculate LLM score
        llm_total = (
            llm_data.get("clarity", 0) +
            llm_data.get("specificity", 0) +
            llm_data.get("constraints", 0) +
            llm_data.get("format", 0)
        )

        # 🔹 Scale rule score to 40 and LLM to 60
        final_score = (rule_score * 0.4) + (llm_total * 0.6)

        st.subheader("📊 Final Score")
        st.success(f"{round(final_score, 2)} / 100")

        st.subheader("📝 AI Feedback")
        st.write(llm_data.get("feedback", "No feedback provided."))

        if rule_feedback:
            st.subheader("⚠ Rule-Based Suggestions")
            for f in rule_feedback:
                st.write("-", f)

        st.subheader("🚀 Improved Prompt")
        st.write(llm_data.get("improved_prompt", "No improved version generated."))