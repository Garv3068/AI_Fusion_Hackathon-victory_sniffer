import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Live Timetable", layout="wide")
st.title("📅 Live Timetable")

# =====================================================
# SAFE DATA LOADING
# =====================================================

st.sidebar.header("📂 Timetable Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload timetable CSV",
    type=["csv"]
)

def load_mock_data():
    """Fallback mock timetable so app NEVER crashes"""
    data = {
        "Day": ["Monday", "Monday", "Tuesday", "Tuesday", "Wednesday"],
        "Time": ["9-10", "10-11", "9-10", "10-11", "9-10"],
        "Subject": ["Maths", "Free", "Physics", "Free", "Electronics"]
    }
    return pd.DataFrame(data)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Timetable loaded from uploaded file")
else:
    df = load_mock_data()
    st.info("ℹ️ Using demo timetable (upload CSV to replace)")

# =====================================================
# DISPLAY TIMETABLE
# =====================================================

st.subheader("📘 Your Weekly Schedule")
st.dataframe(df, use_container_width=True)

# =====================================================
# FREE PERIOD FINDER (SIMULATED AI LOGIC)
# =====================================================
# Logic:
# - Any row where Subject == "Free" is treated as a free slot
# - Simple rule-based filtering (transparent + explainable)

st.subheader("🔍 Free Period Finder")

free_slots = df[df["Subject"].str.lower() == "free"]

if free_slots.empty:
    st.warning("No free periods detected.")
else:
    st.success(f"Found {len(free_slots)} free slot(s)")
    st.dataframe(free_slots, use_container_width=True)

# =====================================================
# EXAM COUNTDOWN
# =====================================================
# Simple date arithmetic, no external APIs

st.subheader("⏳ Exam Countdown")

exam_date = st.date_input(
    "Select Exam Date",
    min_value=date.today()
)

days_left = (exam_date - date.today()).days

if days_left > 0:
    st.success(f"📆 {days_left} days left for the exam!")
elif days_left == 0:
    st.warning("📌 Exam is today!")
else:
    st.error("❌ Exam date has already passed")

# =====================================================
# SAFETY / UX NOTE
# =====================================================

st.caption("🔒 Tip: Upload only non-sensitive timetable data.")


