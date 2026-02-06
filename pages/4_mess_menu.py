import streamlit as st

st.set_page_config(page_title="Mess Menu", layout="wide")

# ---------------- INIT DATA ----------------
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

# ---------------- UI ----------------
st.title("🍽 Live Mess Menu")

day = st.selectbox(
    "📅 Select Day",
    list(st.session_state.mess_menu.keys())
)

col1, col2, col3 = st.columns(3)

col1.metric("🍳 Breakfast", st.session_state.mess_menu[day]["Breakfast"])
col2.metric("🍛 Lunch", st.session_state.mess_menu[day]["Lunch"])
col3.metric("🍽 Dinner", st.session_state.mess_menu[day]["Dinner"])

st.divider()

# ---------------- ADMIN PANEL ----------------
with st.expander("🔐 Admin: Update Menu"):
    admin_pass = st.text_input("Admin Password", type="password")

    if admin_pass == "admin123":
        meal = st.selectbox("Select Meal", ["Breakfast", "Lunch", "Dinner"])
        new_item = st.text_input("Enter Updated Menu")

        if st.button("Update Menu"):
            st.session_state.mess_menu[day][meal] = new_item
            st.success(f"{meal} updated for {day} ✅")

    elif admin_pass:
        st.error("Wrong password ❌")
