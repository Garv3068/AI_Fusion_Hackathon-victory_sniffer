import streamlit as st

def init_menu():
    if "mess_menu" not in st.session_state:
        st.session_state.mess_menu = {
            "Monday": {
                "Breakfast": "Poha, Tea",
                "Lunch": "Rajma, Rice",
                "Dinner": "Roti, Paneer"
            },
            "Tuesday": {
                "Breakfast": "Idli, Sambhar",
                "Lunch": "Chole, Rice",
                "Dinner": "Roti, Mix Veg"
            },
            "Wednesday": {
                "Breakfast": "Upma, Coffee",
                "Lunch": "Dal, Rice",
                "Dinner": "Roti, Aloo Sabzi"
            }
        }

def show_mess_menu():
    init_menu()
    st.header("🍽 Live Mess Menu")

    day = st.selectbox("📅 Select Day", list(st.session_state.mess_menu.keys()))

    col1, col2, col3 = st.columns(3)

    col1.metric("🍳 Breakfast", st.session_state.mess_menu[day]["Breakfast"])
    col2.metric("🍛 Lunch", st.session_state.mess_menu[day]["Lunch"])
    col3.metric("🍽 Dinner", st.session_state.mess_menu[day]["Dinner"])

    st.divider()

    # ---- Admin Section ----
    with st.expander("🔐 Admin: Update Menu"):
        admin_pass = st.text_input("Enter Admin Password", type="password")

        if admin_pass == "admin123":  # demo password
            meal = st.selectbox("Select Meal", ["Breakfast", "Lunch", "Dinner"])
            new_menu = st.text_input(f"Update {meal} Menu")

            if st.button("Update Menu"):
                st.session_state.mess_menu[day][meal] = new_menu
                st.success(f"{meal} updated successfully for {day} ✅")
        elif admin_pass:
            st.error("Incorrect password ❌")
