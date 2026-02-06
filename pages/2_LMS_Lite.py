import streamlit as st
import pandas as pd

st.title("📘 LMS Lite")

assignments = pd.read_csv("data/assignments.csv")
grades = pd.read_csv("data/grades.csv")

st.subheader("📝 Assignments")
st.dataframe(assignments)

st.subheader("📊 Grades")
st.dataframe(grades)

st.subheader("🎯 GPA Calculator")
gpa = (grades["Grade"] * grades["Credits"]).sum() / grades["Credits"].sum()
st.metric("Current GPA", round(gpa, 2))

st.subheader("📈 Performance Analytics")
st.bar_chart(grades.set_index("Course")["Grade"])
