import streamlit as st
from difflib import SequenceMatcher

# =========================================================
# Student Exchange – Skill & Service Hub
# Campus collaboration platform with simulated AI matching
# =========================================================

st.set_page_config(
    page_title="Student Exchange – Skill & Service Hub",
    layout="wide"
)

st.title("🤝 Student Exchange – Skill & Service Hub")
st.caption("Offer skills. Request help. Barter smartly.")

# =========================================================
# In-memory mock storage
# =========================================================
if "listings" not in st.session_state:
    st.session_state.listings = []

# =========================================================
# SIMULATED AI / MATCHING LOGIC
# =========================================================

def text_similarity(a, b):
    """
    SIMULATED NLP SIMILARITY
    -----------------------
    Uses simple string similarity to approximate
    relevance between skills/services.
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def relevance_score(listing, target):
    """
    SIMULATED AI RELEVANCE SCORE
    ----------------------------
    Factors:
    1. Skill/Service text similarity
    2. Same category boost
    3. Availability bonus
    """
    score = text_similarity(listing["title"], target["title"])

    if listing["category"] == target["category"]:
        score += 0.3

    if listing["availability"] == "Available":
        score += 0.2

    return round(score, 2)


def find_recommendations(current):
    """
    SIMULATED MATCH ENGINE
    ---------------------
    Matches:
    - Offer ↔ Request
    - Ranked by relevance score
    """
    matches = []

    for item in st.session_state.listings:
        if item is current:
            continue

        if item["type"] != current["type"]:
            score = relevance_score(item, current)
            if score > 0.4:
                matches.append((item, score))

    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def barter_suggestion(category):
    """
    SIMULATED AI BARTER ADVISOR
    --------------------------
    Suggests fair exchange options based on category.
    """
    suggestions = {
        "Tutoring": "📘 Exchange for notes, printing credits, or book rental",
        "Design": "🎨 Exchange for coding help or social media promotion",
        "Coding": "💻 Exchange for tutoring, design, or project collaboration",
        "Repair": "🔧 Exchange for meals, transport help, or small payments",
        "Services": "🔄 Exchange for time-based help or skill swap"
    }
    return suggestions.get(category, "🔄 Open to mutual agreement")

# =========================================================
# LISTING FORM
# =========================================================

st.subheader("➕ Create a Listing")

with st.form("listing_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        listing_type = st.radio("Type", ["Offer", "Request"])
        title = st.text_input("Skill / Service Title")
        category = st.selectbox(
            "Category",
            ["Tutoring", "Design", "Coding", "Repair", "Services"]
        )

    with col2:
        tags = st.text_input("Tags (comma-separated)")
        availability = st.selectbox(
            "Availability",
            ["Available", "Limited", "Unavailable"]
        )

    submit = st.form_submit_button("Post Listing")

    if submit and title:
        st.session_state.listings.append({
            "type": listing_type,
            "title": title,
            "category": category,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "availability": availability
        })
        st.success("Listing posted successfully!")

# =========================================================
# TOGGLE VIEW
# =========================================================

st.divider()
view_mode = st.radio("View", ["Offers", "Requests"], horizontal=True)

filtered = [
    l for l in st.session_state.listings
    if l["type"] == ("Offer" if view_mode == "Offers" else "Request")
]

# =========================================================
# DISPLAY LISTINGS + AI RECOMMENDATIONS
# =========================================================

if not filtered:
    st.info(f"No {view_mode.lower()} available yet.")
else:
    for item in filtered:
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd;border-radius:10px;padding:15px;">
                    <h4>{'🟢' if item['type']=='Offer' else '🔵'} {item['title']}</h4>
                    <b>Category:</b> {item['category']}<br>
                    <b>Availability:</b> {item['availability']}<br>
                    <b>Tags:</b> {', '.join(item['tags']) if item['tags'] else 'None'}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ================= AI RECOMMENDATIONS =================
            recommendations = find_recommendations(item)

            if recommendations:
                st.markdown("🤖 **Recommended matches:**")
                for rec, score in recommendations[:3]:
                    st.markdown(
                        f"- **{rec['title']}** ({rec['type']}) — Relevance: `{score}`"
                    )

            st.markdown(
                f"💡 **Barter suggestion:** {barter_suggestion(item['category'])}"
            )

            st.markdown(
                "<small>🔒 Tip: Agree on expectations clearly before exchanging skills or services.</small>",
                unsafe_allow_html=True
            )

            st.write("")
