import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Campus Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    /* Main layout */
    .block-container {
        padding-top: 1.8rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #4F46E5, #9333EA);
        padding: 22px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(16,24,40,0.08);
    }

    /* FIXED metric cards */
    .metric-card {
        background: white;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(2,6,23,0.05);
        color: #111827 !important;
        text-align: center;
    }

    .metric-card h2 {
        color: #111827 !important;
        font-size: 32px;
        margin: 0;
        font-weight: 800;
    }

    .metric-card h3 {
        color: #374151 !important;
        font-size: 15px;
        margin-top: 6px;
        font-weight: 600;
    }

    /* Cards */
    .place-card {
        background: white;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(2,6,23,0.06);
        margin-bottom: 14px;
        color: #111827;
    }

    .small-muted {
        color: #6b7280;
        font-size: 13px;
    }

    .pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #eef2ff;
        color: #4f46e5;
        font-weight: 600;
        font-size: 12px;
        margin-right: 6px;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="header-banner">
        <h1>🎓 Campus Intelligence Dashboard</h1>
        <p>Smart insights for students — meals, events, skills & updates</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <h2>5</h2>
            <h3>📍 Total POIs</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <h2>3</h2>
            <h3>🔥 Trending Spots</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="metric-card">
            <h2>0</h2>
            <h3>📝 Assignments Due</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ---------------- SAMPLE CONTENT ----------------
st.subheader("📌 Today’s Highlights")

st.markdown(
    """
    <div class="place-card">
        <h4>🍽 Mess Menu Update</h4>
        <p class="small-muted">Lunch • 12:30 PM – 2:30 PM</p>
        <span class="pill">Dal</span>
        <span class="pill">Rice</span>
        <span class="pill">Paneer</span>
        <span class="pill">Salad</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="place-card">
        <h4>🤝 Skill Exchange Activity</h4>
        <p class="small-muted">
        New coding & tutoring requests are available today.
        </p>
        <span class="pill">Coding</span>
        <span class="pill">Design</span>
        <span class="pill">Tutoring</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("💡 Tip: Switch between Light/Dark mode — cards will stay readable.")
