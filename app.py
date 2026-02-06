# app.py
"""
Academic Cockpit — Integrated app (single file)
- Modern Streamlit UI: header banner, card layout, nicer sidebar
- Nearby Hub: filters, images, distance calculation
- Navigate Smarter: pydeck map + OSRM route fallback
- Timetable & Assignments: add/list with session_state
- Drop images into /mnt/data (ASSETS_DIR) or update paths
Run:
    pip install streamlit pandas haversine pydeck requests
    streamlit run app.py
"""

from pathlib import Path
from datetime import time
import streamlit as st
import pandas as pd
from haversine import haversine, Unit
import requests
import pydeck as pdk

# ---------------- Page config & constants ----------------
st.set_page_config(page_title="Academic Cockpit", layout="wide", initial_sidebar_state="expanded")
ASSETS_DIR = Path("/mnt/data")  # change if needed

# ---------- Sample Places of Interest (replace with real data) ----------
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
    {
        "id": 4,
        "name": "Book Exchange Stall",
        "category": "Marketplace",
        "lat": 30.9339,
        "lon": 76.5284,
        "rating": 4.0,
        "vibes": ["budget", "bustle"],
        "popularity": 60,
        "img": "book_stall.jpg",
        "desc": "Affordable second-hand textbooks and notes."
    },
    {
        "id": 5,
        "name": "Night Canteen",
        "category": "Eatery",
        "lat": 30.9346,
        "lon": 76.5262,
        "rating": 4.1,
        "vibes": ["late-night", "cheap"],
        "popularity": 80,
        "img": "night_canteen.jpg",
        "desc": "Open late-night, popular with exam-time crowds."
    },
]

# ---------------- Utility functions ----------------
@st.cache_data
def load_places_df():
    return pd.DataFrame(PLACES)

def compute_distance_km(a_latlon, b_latlon):
    return haversine(a_latlon, b_latlon, unit=Unit.KILOMETERS)

def google_maps_url(origin, dest):
    return f"https://www.google.com/maps/dir/{origin[0]},{origin[1]}/{dest[0]},{dest[1]}/"

def osrm_route(origin, dest):
    try:
        lon1, lat1 = origin[1], origin[0]
        lon2, lat2 = dest[1], dest[0]
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        coords = data["routes"][0]["geometry"]["coordinates"]
        return coords
    except Exception:
        return None

def straight_line_route(origin, dest):
    return [[origin[1], origin[0]], [dest[1], dest[0]]]

# ---------------- Styling (inline CSS) ----------------
st.markdown(
    """
    <style>
    /* page background */
    .reportview-container .main { background-color: #f5f7fb; }
    .block-container { padding-top: 1.8rem; padding-left: 1.5rem; padding-right: 1.5rem; }
    .header-banner {
        background: linear-gradient(135deg, #4F46E5, #9333EA);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 8px 30px rgba(16,24,40,0.06);
    }
    .metric-card {
        background: white;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(2,6,23,0.04);
    }
    .place-card {
        background: white;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(2,6,23,0.04);
        margin-bottom: 12px;
    }
    .small-muted { color: #6b7280; font-size: 13px; }
    .pill { display:inline-block; padding:6px 10px; border-radius:999px; background:#eef2ff; color:#4f46e5; font-weight:600; font-size:12px; margin-right:6px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.markdown(
    """
    <div class="header-banner">
      <h1 style="margin:0;">🎓 Academic Cockpit</h1>
      <p style="margin:4px 0 0 0; opacity:0.95">Your intelligent academic command center — Nearby Hub, routing, timetable & assignments.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- Sidebar ----------------
st.sidebar.title("📚 Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📍 Nearby Hub", "🗺 Navigate Smarter", "📅 Timetable", "📝 Assignments", "⚙ Settings"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Sample campus center (default)**")
sample_lat, sample_lon = 30.9320, 76.5269
st.sidebar.markdown(f"- Latitude: `{sample_lat}`  \n- Longitude: `{sample_lon}`")

with st.sidebar.expander("Your location", expanded=True):
    loc_mode = st.radio("Location input", ["Use sample campus location", "Enter coordinates"], index=0)
    if loc_mode == "Use sample campus location":
        user_lat, user_lon = sample_lat, sample_lon
    else:
        user_lat = st.number_input("Latitude", value=sample_lat, format="%.6f")
        user_lon = st.number_input("Longitude", value=sample_lon, format="%.6f")

# Optional theme (visual only)
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        "<style> .reportview-container .main { background-color: #0b1020; color: #e6eef8 } </style>",
        unsafe_allow_html=True,
    )

# ---------------- Home ----------------
if menu == "🏠 Home":
    st.subheader("Dashboard Overview")
    df_all = load_places_df()
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="metric-card"><h3 style="margin:0">📍 Total POIs</h3><h2 style="margin-top:6px">{len(df_all)}</h2></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card"><h3 style="margin:0">🔥 Trending Spots</h3><h2 style="margin-top:6px">{sum(1 for p in PLACES if p['popularity'] > 70)}</h2></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card"><h3 style="margin:0">📝 Assignments</h3><h2 style="margin-top:6px">{len(st.session_state.get('assignments', []))}</h2></div>""", unsafe_allow_html=True)

    st.markdown("### Quick actions")
    a1, a2, a3 = st.columns(3)
    if a1.button("🔎 Open Nearby Hub"):
        st.experimental_set_query_params(page="nearby")  # not necessary but hint
        st.experimental_rerun()
    if a2.button("🗺 Open Navigate"):
        st.experimental_set_query_params(page="navigate")
        st.experimental_rerun()
    if a3.button("➕ Add assignment"):
        st.session_state.setdefault("show_add_assignment", True)
        st.experimental_rerun()

    st.markdown("---")
    st.markdown("### Your campus snapshot")
    # show top 3 popular places
    df_all["popularity"] = df_all["popularity"].astype(int)
    top3 = df_all.sort_values("popularity", ascending=False).head(3)
    cols = st.columns(3)
    for i, (_, p) in enumerate(top3.iterrows()):
        with cols[i]:
            img_path = ASSETS_DIR / p["img"]
            if img_path.exists():
                st.image(str(img_path), use_column_width=True)
            st.markdown(f"**{p['name']}**")
            st.write(p["category"], "•", f"{p['rating']}★")
            st.write(f"<span class='small-muted'>{p['desc']}</span>", unsafe_allow_html=True)

# ---------------- Nearby Hub ----------------
elif menu == "📍 Nearby Hub":
    st.header("Nearby Hub — discover study spots & campus places")
    df = load_places_df()
    user_loc = (user_lat, user_lon)

    # Filters (multi-column)
    f1, f2, f3 = st.columns([2, 2, 2])
    radius_km = f1.slider("Search radius (km)", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
    vibes_available = sorted({v for p in PLACES for v in p["vibes"]})
    vibe_filter = f2.multiselect("Vibe tags (match any)", options=vibes_available, default=[])
    sort_by = f3.selectbox("Sort by", ["distance", "rating", "popularity"])

    s1, s2 = st.columns([3,1])
    search_term = s1.text_input("Search by name or category")
    trending_only = s2.checkbox("Trending only (popularity > 70)")

    # compute distances
    df["distance_km"] = df.apply(lambda r: compute_distance_km(user_loc, (r["lat"], r["lon"])), axis=1)

    # filters
    mask = df["distance_km"] <= radius_km
    if vibe_filter:
        mask &= df["vibes"].apply(lambda vs: any(v in vs for v in vibe_filter))
    if search_term:
        s = search_term.lower()
        mask &= df.apply(lambda r: s in r["name"].lower() or s in str(r["category"]).lower(), axis=1)
    if trending_only:
        mask &= df["popularity"] > 70

    df_filtered = df[mask].copy()

    # sorting
    if sort_by == "distance":
        df_filtered = df_filtered.sort_values("distance_km")
    elif sort_by == "rating":
        df_filtered = df_filtered.sort_values("rating", ascending=False)
    else:
        df_filtered = df_filtered.sort_values("popularity", ascending=False)

    st.subheader(f"Places ({len(df_filtered)})")
    if df_filtered.empty:
        st.info("No places match your filters. Try expanding the radius or clearing filters.")
    else:
        for _, place in df_filtered.iterrows():
            st.markdown('<div class="place-card">', unsafe_allow_html=True)
            cols = st.columns([1, 3])
            thumb_path = ASSETS_DIR / place["img"]
            if thumb_path.exists():
                cols[0].image(str(thumb_path), width=140)
            else:
                cols[0].empty()
            with cols[1]:
                st.markdown(f"### {place['name']}")
                st.caption(f"{place['category']} • ⭐ {place['rating']} • 📏 {place['distance_km']:.2f} km")
                st.write(place["desc"])
                # vibes pill list
                vibes_html = " ".join([f"<span class='pill'>{v}</span>" for v in place["vibes"]])
                st.markdown(vibes_html, unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if b1.button("🧭 Navigate", key=f"nav_{place['id']}"):
                    st.session_state["selected_place"] = int(place["id"])
                    st.success(f"Selected {place['name']} for routing (open Navigate Smarter).")
                if b2.button("🌍 Open Maps", key=f"gmaps_{place['id']}"):
                    url = google_maps_url(user_loc, (place["lat"], place["lon"]))
                    st.markdown(f"[Open directions in Google Maps]({url})")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Navigate Smarter ----------------
elif menu == "🗺 Navigate Smarter":
    st.header("Navigate Smarter — map & routing")
    df = load_places_df()
    user_loc = (user_lat, user_lon)
    df["distance_km"] = df.apply(lambda r: compute_distance_km(user_loc, (r["lat"], r["lon"])), axis=1)

    selected_id = st.session_state.get("selected_place", None)

    st.subheader("Map view")
    if df.empty:
        st.info("No places to show on the map.")
    else:
        viewport = pdk.ViewState(latitude=user_lat, longitude=user_lon, zoom=15, pitch=0)
        scatter = pdk.Layer(
            "ScatterplotLayer",
            data=df.to_dict(orient="records"),
            get_position='[lon, lat]',
            get_color='[200, 60, 0, 160]',
            get_radius=40,
            pickable=True,
            radius_scale=10,
        )
        user_df = pd.DataFrame([{"lon": user_lon, "lat": user_lat, "name": "You"}])
        user_marker = pdk.Layer(
            "ScatterplotLayer",
            data=user_df.to_dict(orient="records"),
            get_position='[lon, lat]',
            get_color='[0, 120, 200, 255]',
            get_radius=60,
            radius_scale=10
        )
        deck = pdk.Deck(layers=[scatter, user_marker], initial_view_state=viewport,
                        tooltip={"text": "{name}\n{category}\n{rating}★\n{distance_km} km"})
        st.pydeck_chart(deck)

    st.subheader("Selected place & route")
    if selected_id is None:
        st.info("Select a place from Nearby Hub (click Navigate) or pick one here.")
        pick = st.selectbox("Pick a place to preview route", df["name"].tolist())
        if st.button("Preview route"):
            sel_row = df[df["name"] == pick].iloc[0]
            st.session_state["selected_place"] = int(sel_row["id"])
            st.experimental_rerun()
    else:
        sel = df[df["id"] == selected_id].iloc[0]
        st.markdown(f"### {sel['name']} — {sel['category']}")
        st.write(sel["desc"])
        st.write("🎯 Vibes:", ", ".join(sel["vibes"]))
        st.write(f"Distance: **{sel['distance_km']:.2f} km** • Rating: **{sel['rating']}★**")

        use_osrm = st.checkbox("Use OSRM routing (internet required)", value=True)
        route_coords = None
        if use_osrm:
            with st.spinner("Querying OSRM route..."):
                route_coords = osrm_route(user_loc, (sel["lat"], sel["lon"]))
            if route_coords is None:
                st.warning("OSRM routing failed or is unreachable — showing straight-line fallback.")

        if route_coords is None:
            route_coords = straight_line_route(user_loc, (sel["lat"], sel["lon"]))

        path_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords, "name": sel["name"]}],
            get_path="path",
            get_width=6,
            get_color=[2, 126, 209],
            width_min_pixels=3,
        )

        route_deck = pdk.Deck(layers=[path_layer, scatter, user_marker], initial_view_state=viewport)
        st.pydeck_chart(route_deck)

        gmaps = google_maps_url(user_loc, (sel["lat"], sel["lon"]))
        st.markdown(f"[Open full directions in Google Maps]({gmaps})")

# ---------------- Timetable ----------------
elif menu == "📅 Timetable":
    st.header("Timetable")
    st.session_state.setdefault("timetable", [])

    with st.form("add_slot", clear_on_submit=True):
        cols = st.columns(4)
        course = cols[0].text_input("Course", value="Intro to AI")
        day = cols[1].selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        start = cols[2].time_input("Start", value=time(hour=9, minute=0))
        end = cols[3].time_input("End", value=time(hour=10, minute=0))
        submitted = st.form_submit_button("Add slot")
    if submitted:
        st.session_state["timetable"].append({
            "course": course,
            "day": day,
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M")
        })
        st.success("Timetable slot added.")

    st.subheader("Your timetable")
    if st.session_state["timetable"]:
        st.dataframe(pd.DataFrame(st.session_state["timetable"]), use_container_width=True)
    else:
        st.info("No timetable entries yet. Add slots using the form above.")

    # Quick suggestion for nearest study spot (simple heuristic)
    if st.session_state["timetable"]:
        next_slot = st.session_state["timetable"][0]
        st.markdown("**Quick suggestion**: nearest study spot for your next class")
        df2 = load_places_df()
        df2["distance_km"] = df2.apply(lambda r: compute_distance_km((user_lat, user_lon), (r["lat"], r["lon"])), axis=1)
        nearest = df2.sort_values("distance_km").iloc[0]
        st.write(f"For **{next_slot['course']}** (on {next_slot['day']}):")
        st.write(f"- Recommended spot: **{nearest['name']}** — {nearest['category']} ({nearest['distance_km']:.2f} km away)")

# ---------------- Assignments ----------------
elif menu == "📝 Assignments":
    st.header("Assignments & Grades")
    st.session_state.setdefault("assignments", [])

    with st.form("assign_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        title = col1.text_input("Title")
        course = col2.text_input("Course")
        due = col3.date_input("Due date")
        weight = st.number_input("Weight (%)", min_value=0, max_value=100, value=10)
        added = st.form_submit_button("Add assignment")
    if added:
        st.session_state["assignments"].append({
            "title": title,
            "course": course,
            "due": due.isoformat(),
            "weight": weight,
            "status": "pending"
        })
        st.success("Assignment added.")

    st.subheader("Your assignments")
    if st.session_state["assignments"]:
        df_as = pd.DataFrame(st.session_state["assignments"])
        st.table(df_as)
    else:
        st.info("No assignments yet. Add one above.")

# ---------------- Settings ----------------
elif menu == "⚙ Settings":
    st.header("Settings & advanced")
    st.markdown("Change app behavior (demo only).")
    show_assets = st.checkbox("Show images available in /mnt/data")
    if show_assets:
        files = sorted([f for f in ASSETS_DIR.glob("*") if f.is_file()])
        if files:
            for f in files:
                st.write(f.name)
        else:
            st.info("No files found in assets directory.")

    st.markdown("**Routing provider**")
    st.markdown("- This prototype uses the public OSRM server for route lookup. For production use a paid provider or your own OSRM instance.")
    st.markdown("**Developer notes**")
    st.code(
        "- To replace PLACES load from CSV/DB or call a Places API.\n"
        "- To persist timetable/assignments connect to a DB (SQLite/Postgres/Firebase).\n"
        "- To authenticate users integrate OAuth / identity provider."
    )

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Prototype built for Academic Cockpit — Nearby Hub + Navigate Smarter demo.")
