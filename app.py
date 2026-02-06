# app.py
"""
Academic Cockpit — Integrated app (single file)
"""

from pathlib import Path
from datetime import time
import streamlit as st
import pandas as pd
from haversine import haversine, Unit
import requests
import pydeck as pdk

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Academic Cockpit",
    layout="wide",
    initial_sidebar_state="expanded"
)

ASSETS_DIR = Path("/mnt/data")

# ---------------- Sample data ----------------
PLACES = [
    {
        "id": 1,
        "name": "Campus Cafe",
        "category": "Eatery",
        "lat": 30.9315,
        "lon": 76.5278,
        "rating": 4.4,
        "vibes": ["study-friendly", "budget"],
        "popularity": 78,
        "img": "campus_cafe.jpg",
        "desc": "Cozy cafe, quiet corners, reliable Wi-Fi."
    },
    {
        "id": 2,
        "name": "Central Library",
        "category": "Library",
        "lat": 30.9326,
        "lon": 76.5267,
        "rating": 4.8,
        "vibes": ["quiet", "study-friendly"],
        "popularity": 95,
        "img": "library.jpg",
        "desc": "24/7 study halls, group rooms, printer access."
    },
    {
        "id": 3,
        "name": "Riverside Park",
        "category": "Outdoor",
        "lat": 30.9308,
        "lon": 76.5250,
        "rating": 4.2,
        "vibes": ["outdoor", "date-spot"],
        "popularity": 66,
        "img": "park.jpg",
        "desc": "Open lawn, morning joggers, benches and kiosks."
    },
]

# ---------------- Utilities ----------------
@st.cache_data
def load_places_df():
    return pd.DataFrame(PLACES)

def compute_distance_km(a, b):
    return haversine(a, b, unit=Unit.KILOMETERS)

def google_maps_url(origin, dest):
    return f"https://www.google.com/maps/dir/{origin[0]},{origin[1]}/{dest[0]},{dest[1]}/"

# ---------------- Styling (FIXED TEXT VISIBILITY) ----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
    }

    .header-banner {
        background: linear-gradient(135deg, #4F46E5, #9333EA);
        padding: 20px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
    }

    .metric-card {
        background: #ffffff;
        color: #111827;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }

    .place-card {
        background: #ffffff;
        color: #111827;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 14px;
    }

    .pill {
        display:inline-block;
        padding:6px 12px;
        border-radius:999px;
        background:#eef2ff;
        color:#4f46e5;
        font-weight:600;
        font-size:12px;
        margin-right:6px;
    }

    .small-muted {
        color: #6b7280;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.markdown(
    """
    <div class="header-banner">
        <h1>🎓 Academic Cockpit</h1>
        <p>Your intelligent academic command center</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- Sidebar ----------------
menu = st.sidebar.radio(
    "📚 Navigation",
    ["🏠 Home", "📍 Nearby Hub", "🗺 Navigate Smarter", "📅 Timetable", "📝 Assignments"]
)

sample_lat, sample_lon = 30.9320, 76.5269
user_lat = sample_lat
user_lon = sample_lon

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.subheader("Dashboard Overview")

    df = load_places_df()

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""
        <div class="metric-card">
            <h3>📍 Total POIs</h3>
            <h2>{len(df)}</h2>
        </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Trending Spots</h3>
            <h2>{len(df[df["popularity"] > 70])}</h2>
        </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
        <div class="metric-card">
            <h3>📝 Assignments</h3>
            <h2>{len(st.session_state.get("assignments", []))}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Quick Actions")
    a1, a2 = st.columns(2)

    if a1.button("🔎 Open Nearby Hub"):
        st.session_state["goto"] = "📍 Nearby Hub"
        st.rerun()

    if a2.button("🗺 Open Navigate"):
        st.session_state["goto"] = "🗺 Navigate Smarter"
        st.rerun()

# ---------------- NEARBY HUB ----------------
elif menu == "📍 Nearby Hub":
    st.header("Nearby Hub")

    df = load_places_df()
    user_loc = (user_lat, user_lon)

    df["distance_km"] = df.apply(
        lambda r: compute_distance_km(user_loc, (r["lat"], r["lon"])), axis=1
    )

    for _, p in df.sort_values("distance_km").iterrows():
        st.markdown('<div class="place-card">', unsafe_allow_html=True)
        st.markdown(f"### {p['name']}")
        st.write(f"{p['category']} • ⭐ {p['rating']} • 📏 {p['distance_km']:.2f} km")
        st.write(p["desc"])

        vibes = " ".join([f"<span class='pill'>{v}</span>" for v in p["vibes"]])
        st.markdown(vibes, unsafe_allow_html=True)

        if st.button("🧭 Navigate", key=f"nav_{p['id']}"):
            st.session_state["selected_place"] = p["id"]
            st.session_state["goto"] = "🗺 Navigate Smarter"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
elif menu == "🗺 Navigate Smarter":
    st.header("Navigate Smarter")

    df = load_places_df()
    selected_id = st.session_state.get("selected_place")

    if not selected_id:
        st.info("Select a place from Nearby Hub")
    else:
        place = df[df["id"] == selected_id].iloc[0]
        st.subheader(place["name"])
        st.write(place["desc"])

        url = google_maps_url((user_lat, user_lon), (place["lat"], place["lon"]))
        st.markdown(f"[🌍 Open in Google Maps]({url})")

# ---------------- TIMETABLE ----------------
elif menu == "📅 Timetable":
    st.header("Timetable")

    st.session_state.setdefault("timetable", [])

    with st.form("add_class"):
        c1, c2, c3, c4 = st.columns(4)
        course = c1.text_input("Course")
        day = c2.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri"])
        start = c3.time_input("Start", time(9, 0))
        end = c4.time_input("End", time(10, 0))
        submit = st.form_submit_button("Add")

    if submit:
        st.session_state["timetable"].append({
            "course": course,
            "day": day,
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M")
        })
        st.success("Class added")

    if st.session_state["timetable"]:
        st.dataframe(pd.DataFrame(st.session_state["timetable"]))

# ---------------- ASSIGNMENTS ----------------
elif menu == "📝 Assignments":
    st.header("Assignments")

    st.session_state.setdefault("assignments", [])

    with st.form("add_assignment"):
        title = st.text_input("Title")
        course = st.text_input("Course")
        due = st.date_input("Due date")
        submit = st.form_submit_button("Add")

    if submit:
        st.session_state["assignments"].append({
            "title": title,
            "course": course,
            "due": due.isoformat()
        })
        st.success("Assignment added")

    if st.session_state["assignments"]:
        st.table(pd.DataFrame(st.session_state["assignments"]))

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Academic Cockpit • Streamlit Prototype")
