import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📘 LMS Lite")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

assignments_path = DATA_DIR / "assignments.csv"
grades_path = DATA_DIR / "grades.csv"

assignments = pd.read_csv(assignments_path)
grades = pd.read_csv(grades_path)

st.subheader("📝 Assignments")
st.dataframe(assignments)

st.subheader("📊 Grades")
st.dataframe(grades)

st.subheader("🎯 GPA Calculator")
gpa = (grades["Grade"] * grades["Credits"]).sum() / grades["Credits"].sum()
st.metric("Current GPA", round(gpa, 2))

st.subheader("📈 Performance Analytics")
st.bar_chart(grades.set_index("Course")["Grade"])
