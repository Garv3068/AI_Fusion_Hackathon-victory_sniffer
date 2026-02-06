import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mail Summarizer",
    layout="wide"
)

# ---------------- GEMINI SETUP ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- UI ----------------
st.title("📧 AI Mail Summarizer (Gemini)")
st.caption("Paste any official college mail and get a clear, student-friendly summary.")

mail_text = st.text_area(
    "Paste College Mail Here",
    height=250,
    placeholder="Paste official college mail / notice..."
)

if st.button("Summarize Mail"):
    if not mail_text.strip():
        st.warning("Please paste a mail first.")
    else:
        with st.spinner("Summarizing using Gemini AI..."):
            prompt = f"""
You are a college assistant AI.

Summarize the following mail in simple student-friendly language.

Return:
1. 3–5 bullet point summary
2. Important dates (if any)
3. Action required (Yes/No)

Mail:
{mail_text}
"""
            response = model.generate_content(prompt)

            st.subheader("📌 Summary")
            st.success(response.text)
