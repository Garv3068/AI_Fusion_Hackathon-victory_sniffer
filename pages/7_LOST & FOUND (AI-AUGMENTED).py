import streamlit as st
from datetime import date
from difflib import SequenceMatcher

# =========================================================
# Student Exchange – Lost & Found
# Streamlit-only app with simulated AI features
# =========================================================

st.set_page_config(
    page_title="Student Exchange – Lost & Found",
    layout="wide"
)

st.title("🎒 Student Exchange – Lost & Found")
st.caption("Simple campus lost & found system with **simulated AI matching**")

# =========================================================
# In-memory storage (resets on refresh)
# =========================================================
if "items" not in st.session_state:
    st.session_state.items = []

# =========================================================
# Simulated AI Logic
# =========================================================

def auto_tag(description: str):
    """
    SIMULATED AI TAGGING (Keyword-based)
    -----------------------------------
    This mimics an AI classifier by checking for
    presence of certain keywords in the description.
    """
    desc = description.lower()

    if any(k in desc for k in ["phone", "laptop", "charger", "earbuds", "tablet"]):
        return "Electronics"
    if any(k in desc for k in ["id", "card", "aadhar", "pan", "license", "passport"]):
        return "ID"
    if any(k in desc for k in ["shirt", "jacket", "hoodie", "shoes", "cap", "jeans"]):
        return "Clothing"
    return "Other"


def text_similarity(a: str, b: str):
    """
    SIMULATED AI SIMILARITY CHECK
    -----------------------------
    Uses simple string similarity to mimic
    NLP-based semantic matching.
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matches(current_item, threshold=0.6):
    """
    SIMULATED AI MATCHING
    ---------------------
    Compares LOST vs FOUND items using description similarity.
    """
    matches = []

    for item in st.session_state.items:
        if item["status"] != current_item["status"]:
            score = text_similarity(
                current_item["description"], item["description"]
            )
            if score >= threshold:
                matches.append((item, score))

    return matches


# =========================================================
# Submission Forms
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Report Lost Item")
    with st.form("lost_form", clear_on_submit=True):
        lost_name = st.text_input("Item Name")
        lost_desc = st.text_area("Description")
        lost_location = st.text_input("Last Seen Location")
        lost_date = st.date_input("Date Lost", value=date.today())

        submit_lost = st.form_submit_button("Submit Lost Item")

        if submit_lost and lost_name and lost_desc:
            tag = auto_tag(lost_desc)

            new_item = {
                "name": lost_name,
                "description": lost_desc,
                "location": lost_location,
                "date": lost_date,
                "status": "Lost",
                "category": tag
            }

            st.session_state.items.append(new_item)
            st.success("Lost item submitted successfully!")

with col2:
    st.subheader("🟢 Report Found Item")
    with st.form("found_form", clear_on_submit=True):
        found_name = st.text_input("Item Name ")
        found_desc = st.text_area("Description ")
        found_location = st.text_input("Found At Location")
        found_date = st.date_input("Date Found", value=date.today())

        submit_found = st.form_submit_button("Submit Found Item")

        if submit_found and found_name and found_desc:
            tag = auto_tag(found_desc)

            new_item = {
                "name": found_name,
                "description": found_desc,
                "location": found_location,
                "date": found_date,
                "status": "Found",
                "category": tag
            }

            st.session_state.items.append(new_item)
            st.success("Found item submitted successfully!")

# =========================================================
# Search & Display
# =========================================================

st.divider()
st.subheader("📋 All Submissions")

search = st.text_input("🔍 Search by name, description, or location")

filtered_items = []
for item in st.session_state.items:
    combined = f"{item['name']} {item['description']} {item['location']}".lower()
    if search.lower() in combined:
        filtered_items.append(item)

# =========================================================
# Display Cards with AI Match Highlighting
# =========================================================

if not filtered_items:
    st.info("No items found.")
else:
    for idx, item in enumerate(filtered_items):
        with st.container():
            st.markdown(
                f"""
                <div style="border-radius:10px;padding:15px;border:1px solid #ddd;">
                <h4>{'🔴' if item['status']=='Lost' else '🟢'} {item['name']}</h4>
                <b>Status:</b> {item['status']}<br>
                <b>Category (AI-tagged):</b> {item['category']}<br>
                <b>Location:</b> {item['location']}<br>
                <b>Date:</b> {item['date']}<br>
                <b>Description:</b> {item['description']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ---------------- AI MATCH SUGGESTIONS ----------------
            matches = find_matches(item)

            if matches:
                st.markdown("🤖 **AI-suggested possible matches:**")
                for m, score in matches:
                    st.markdown(
                        f"- **{m['name']}** ({m['status']}) — Similarity: `{score:.2f}`"
                    )

            st.write("")  # spacing
