import streamlit as st

st.title("🧠 Academic Intelligence")

st.subheader("📅 AI Study Planner")
subjects = st.multiselect("Select Subjects", ["Math", "Physics", "CS", "Chemistry"])
hours = st.slider("Daily Study Hours", 1, 10)

if st.button("Generate Study Plan"):
    for sub in subjects:
        st.write(f"📘 {sub}: {hours//len(subjects)} hrs/day")

st.subheader("🧪 Topic Difficulty Predictor")
topic = st.text_input("Enter topic name")
if topic:
    st.warning(f"Predicted difficulty for **{topic}**: Medium")

st.subheader("🧠 Flashcard Generator")
notes = st.text_area("Paste your notes")
if st.button("Generate Flashcards"):
    st.success("Flashcards generated successfully!")
