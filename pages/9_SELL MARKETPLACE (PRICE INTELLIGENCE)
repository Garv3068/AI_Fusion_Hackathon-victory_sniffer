import streamlit as st

# =========================================================
# Student Exchange – Buy/Sell Marketplace
# Streamlit-only app with simulated AI pricing
# =========================================================

st.set_page_config(
    page_title="Student Exchange – Buy/Sell Marketplace",
    layout="wide"
)

st.title("🛒 Student Exchange – Buy/Sell Marketplace")
st.caption("Campus marketplace with **AI-simulated price recommendations**")

# =========================================================
# In-memory storage
# =========================================================
if "listings" not in st.session_state:
    st.session_state.listings = []

# =========================================================
# Mock historical price data (SIMULATED AI KNOWLEDGE)
# =========================================================
# These act like learned averages from past data
HISTORICAL_AVG = {
    "Books": {"New": 600, "Good": 400, "Used": 250},
    "Electronics": {"New": 8000, "Good": 5500, "Used": 3500},
    "Furniture": {"New": 5000, "Good": 3500, "Used": 2000},
    "Cycles": {"New": 7000, "Good": 4500, "Used": 3000},
}

def recommend_price(category, condition):
    """
    SIMULATED AI PRICE RECOMMENDER
    ------------------------------
    Uses mocked historical averages based on
    category + condition.
    """
    return HISTORICAL_AVG[category][condition]

def price_flag(user_price, recommended):
    """
    SIMULATED AI PRICE EVALUATION
    -----------------------------
    Flags listings based on deviation
    from recommended price.
    """
    if user_price > recommended * 1.25:
        return "🔴 Overpriced"
    elif user_price < recommended * 0.75:
        return "🟡 Underpriced"
    return "🟢 Fairly priced"

def negotiation_tip(flag):
    """
    SIMULATED AI NEGOTIATION ADVICE
    -------------------------------
    """
    if "Overpriced" in flag:
        return "💬 Expect 15–20% negotiation"
    if "Underpriced" in flag:
        return "💬 Price may sell quickly (5–10% room)"
    return "💬 10–15% negotiable"

# =========================================================
# Item Listing Form
# =========================================================

st.subheader("➕ List an Item for Sale")

with st.form("list_item", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Item Name")
        category = st.selectbox(
            "Category", ["Books", "Electronics", "Furniture", "Cycles"]
        )
        condition = st.selectbox(
            "Condition", ["New", "Good", "Used"]
        )

    with col2:
        price = st.number_input("Expected Price (₹)", min_value=0, step=100)

    submit = st.form_submit_button("List Item")

    if submit and name and price > 0:
        rec_price = recommend_price(category, condition)
        flag = price_flag(price, rec_price)
        negotiation = negotiation_tip(flag)

        st.session_state.listings.append({
            "name": name,
            "category": category,
            "condition": condition,
            "price": price,
            "recommended": rec_price,
            "flag": flag,
            "negotiation": negotiation
        })

        st.success("Item listed successfully!")

# =========================================================
# Sidebar Filters
# =========================================================

st.sidebar.header("🔍 Filters")

filter_category = st.sidebar.multiselect(
    "Category",
    ["Books", "Electronics", "Furniture", "Cycles"],
    default=["Books", "Electronics", "Furniture", "Cycles"]
)

max_price = st.sidebar.slider(
    "Maximum Price (₹)",
    min_value=0,
    max_value=10000,
    value=10000,
    step=500
)

# =========================================================
# Marketplace Display
# =========================================================

st.divider()
st.subheader("📦 Marketplace Listings")

filtered = [
    item for item in st.session_state.listings
    if item["category"] in filter_category and item["price"] <= max_price
]

if not filtered:
    st.info("No items match the selected filters.")
else:
    for item in filtered:
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd;border-radius:10px;padding:15px;margin-bottom:10px;">
                    <h4>🧾 {item['name']}</h4>
                    <b>Category:</b> {item['category']}<br>
                    <b>Condition:</b> {item['condition']}<br>
                    <b>Listed Price:</b> ₹{item['price']}<br>
                    <b>AI Recommended Price:</b> ₹{item['recommended']}<br>
                    <b>Status:</b> {item['flag']}<br>
                    <b>Negotiation Tip:</b> {item['negotiation']}
                </div>
                """,
                unsafe_allow_html=True
            )
