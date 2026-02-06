# components/academic.py
import streamlit as st
import pandas as pd
from datetime import datetime

def show_academic():
    st.header("Academic Cockpit — Timetable & Assignments")
    if "timetable" not in st.session_state:
        st.session_state["timetable"] = []
    with st.form("slot"):
        course = st.text_input("Course", value="Course name")
        day = st.selectbox("Day", ["Mon","Tue","Wed","Thu","Fri"])
        start = st.time_input("Start", value=datetime.strptime("09:00","%H:%M").time())
        end = st.time_input("End", value=datetime.strptime("10:00","%H:%M").time())
        if st.form_submit_button("Add slot"):
            st.session_state["timetable"].append({"course":course,"day":day,"start":start,"end":end})
    st.table(pd.DataFrame(st.session_state["timetable"]))

    if "assignments" not in st.session_state:
        st.session_state["assignments"] = []
    with st.form("assign"):
        title = st.text_input("Title")
        due = st.date_input("Due")
        if st.form_submit_button("Add assignment"):
            st.session_state["assignments"].append({"title":title,"due":due,"status":"pending"})
    st.table(pd.DataFrame(st.session_state["assignments"]))
