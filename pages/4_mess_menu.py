import streamlit as st

menu = {
    "Monday": {
        "Breakfast": "Poha, Tea",
        "Lunch": "Rajma, Rice",
        "Dinner": "Roti, Paneer"
    },
    "Tuesday": {
        "Breakfast": "Idli, Sambhar",
        "Lunch": "Chole, Rice",
        "Dinner": "Roti, Mix Veg"
    }
}

def show_mess_menu():
    st.header("🍽 Live Mess Menu")

    day = st.selectbox("Select Day", menu.keys())

    col1, col2, col3 = st.columns(3)

    col1.metric("Breakfast", menu[day]["Breakfast"])
    col2.metric("Lunch", menu[day]["Lunch"])
    col3.metric("Dinner", menu[day]["Dinner"])
