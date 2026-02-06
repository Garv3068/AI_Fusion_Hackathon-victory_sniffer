import streamlit as st
import pandas as pd

st.title("📘 LMS Lite")

# Load data
assignments = pd.read_csv("data/assignments.csv")
grades = pd.read_csv("data/grades.csv")

# Assignments section
st.subheader("📝 Assignments")
st.dataframe(assignments, use_container_width=True)

# Grades section
st.subheader("📊 Grades")
st.dataframe(grades, use_container_width=True)

# GPA Calculator
st.subheader("🎯 GPA Calculator")
gpa = (grades["Grade"] * grades["Credits"]).sum() / grades["Credits"].sum()
st.metric("Current GPA", round(gpa / 10, 2))

# Performance Analytics
st.subheader("📈 Performance Analytics")
st.bar_chart(grades.set_index("Course")["Grade"])

