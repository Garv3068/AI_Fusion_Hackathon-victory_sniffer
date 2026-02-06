import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📅 Live Timetable")

df = pd.read_csv("data/timetable.csv")

st.subheader("Your Weekly Schedule")
st.dataframe(df, use_container_width=True)

st.subheader("🔍 Free Period Finder")
free_slots = df[df["Subject"] == "Free"]
st.write(free_slots)

st.subheader("⏳ Exam Countdown")
exam_date = st.date_input("Select Exam Date")
days_left = (exam_date - datetime.today().date()).days
st.success(f"{days_left} days left for the exam!")
