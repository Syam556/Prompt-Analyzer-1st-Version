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

        try:
            llm_data = json.loads(llm_result)
        except:
            st.error("LLM response formatting error.")
            st.write(llm_result)
            st.stop()

        llm_total = (
            llm_data["clarity"] +
            llm_data["specificity"] +
            llm_data["constraints"] +
            llm_data["format"]
        )

        final_score = rule_score + llm_total

        st.subheader("📊 Final Score")
        st.success(f"{final_score} / 100")

        st.subheader("📝 Feedback")
        st.write(llm_data["feedback"])

        if rule_feedback:
            st.subheader("⚠ Rule-Based Suggestions")
            for f in rule_feedback:
                st.write("-", f)

        st.subheader("🚀 Improved Prompt")
        st.write(llm_data["improved_prompt"])
