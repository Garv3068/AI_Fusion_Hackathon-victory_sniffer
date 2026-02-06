# app.py
"""
Academic Cockpit — Integrated app:
- Header (Academic Cockpit)
- Explorer's Guide: Nearby Hub + Navigate Smarter
- Timetable & Assignments
- Route lookup via OSRM (fallback to straight-line)
Drop images into /mnt/data (or edit ASSETS_DIR).
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from haversine import haversine, Unit
import pydeck as pdk
import requests
from datetime import datetime, time

# ---------------- Page config & constants ----------------
st.set_page_config(page_title="Academic Cockpit", layout="wide", initial_sidebar_state="expanded")

ASSETS_DIR = Path("/mnt/data")  # adjust if needed

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
    """Return DataFrame for POIs (cached)."""
    return pd.DataFrame(PLACES)

def compute_distance_km(a_latlon, b_latlon):
    """Haversine distance (km). Expect tuples: (lat, lon)."""
    return haversine(a_latlon, b_latlon, unit=Unit.KILOMETERS)

def google_maps_url(origin, dest):
    """Return Google Maps directions URL (origin/dest are (lat,lon))."""
    return f"https://www.google.com/maps/dir/{origin[0]},{origin[1]}/{dest[0]},{dest[1]}/"

def osrm_route(origin, dest):
    """
    Query OSRM public demo server for a route.
    origin/dest: (lat, lon)
    Returns: list of [lon, lat] coordinates or None on failure.
    Note: production apps should run their own routing instance or use a paid provider.
    """
    try:
        lon1, lat1 = origin[1], origin[0]
        lon2, lat2 = dest[1], dest[0]
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        coords = data["routes"][0]["geometry"]["coordinates"]  # list of [lon, lat]
        return coords
    except Exception:
        return None

def straight_line_route(origin, dest, steps=2):
    """Fallback route: simple polyline between origin & dest."""
    # return list of [lon, lat] pairs
    return [[origin[1], origin[0]], [dest[1], dest[0]]]

# ---------------- Page header (your snippet integrated) ----------------
st.title("🎓 Academic Cockpit")
st.subheader("Your command center for academic success")
st.markdown("""
Welcome to **Academic Cockpit**:
- 📅 Manage your timetable
- 📚 Track assignments & grades
- 🧠 Use AI to study smarter

---

### The Explorer's Guide
This app contains:
- **Nearby Hub** — filter & discover campus spots (vibes, radius, trending)
- **Navigate Smarter** — map + route preview (OSRM or straight-line fallback)
""")

# ---------------- Sidebar: global controls & nav ----------------
menu = st.sidebar.selectbox("Go to", ["Home", "Nearby Hub", "Navigate Smarter", "Timetable", "Assignments", "Settings"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Sample campus center** (used when not entering coordinates):")
sample_lat, sample_lon = 30.9320, 76.5269
st.sidebar.markdown(f"- Latitude: `{sample_lat}`  \n- Longitude: `{sample_lon}`")

# Allow user to set their location
with st.sidebar.expander("Your location"):
    loc_mode = st.radio("Location input", ["Use sample campus location", "Enter coordinates"])
    if loc_mode == "Use sample campus location":
        user_lat, user_lon = sample_lat, sample_lon
    else:
        user_lat = st.number_input("Latitude", value=sample_lat, format="%.6f")
        user_lon = st.number_input("Longitude", value=sample_lon, format="%.6f")

# ---------------- Home (summary) ----------------
if menu == "Home":
    st.header("Welcome — Quick dashboard")
    df_all = load_places_df()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("POIs in dataset", len(df_all))
    with col2:
        st.metric("Trending spots", sum(1 for p in PLACES if p["popularity"] > 70))
    with col3:
        st.metric("Saved assignments", len(st.session_state.get("assignments", [])))
    st.markdown("Use the sidebar to navigate between Nearby Hub, Navigate Smarter, Timetable, and Assignments.")

# ---------------- Nearby Hub ----------------
elif menu == "Nearby Hub":
    st.header("Nearby Hub — discover study spots & campus places")
    df = load_places_df()
    user_loc = (user_lat, user_lon)

    # Filters
    radius_km = st.slider("Search radius (km)", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
    vibes_available = sorted({v for p in PLACES for v in p["vibes"]})
    vibe_filter = st.multiselect("Vibe tags (match any)", options=vibes_available, default=[])
    sort_by = st.selectbox("Sort by", ["distance", "rating", "popularity"])
    search_term = st.text_input("Search by name or category")
    trending_only = st.checkbox("Trending only (popularity > 70)")

    # compute distances
    df["distance_km"] = df.apply(lambda r: compute_distance_km(user_loc, (r["lat"], r["lon"])), axis=1)

    # apply filters
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

    # Results list
    st.subheader(f"Places ({len(df_filtered)})")
    if df_filtered.empty:
        st.info("No places match your filters. Try expanding the radius or clearing filters.")
    else:
        for _, place in df_filtered.iterrows():
            st.markdown("---")
            cols = st.columns([1, 3])
            thumb_path = ASSETS_DIR / place["img"]
            if thumb_path.exists():
                cols[0].image(str(thumb_path), width=120)
            else:
                cols[0].empty()

            with cols[1]:
                st.markdown(f"**{place['name']}**  \n"
                            f"{place['category']} • {place['rating']}★  • {place['distance_km']:.2f} km away")
                st.write(place["desc"])
                st.write("Vibes: " + ", ".join(place["vibes"]))
                c1, c2 = st.columns([1, 1])
                if c1.button("Navigate", key=f"nav_{place['id']}"):
                    # mark selected place in session_state to be picked up by Navigate view
                    st.session_state["selected_place"] = int(place["id"])
                if c2.button("Open in Google Maps", key=f"gmaps_{place['id']}"):
                    url = google_maps_url(user_loc, (place["lat"], place["lon"]))
                    st.markdown(f"[Open directions in Google Maps]({url})")

# ---------------- Navigate Smarter ----------------
elif menu == "Navigate Smarter":
    st.header("Navigate Smarter — map & routing")
    df = load_places_df()
    user_loc = (user_lat, user_lon)
    df["distance_km"] = df.apply(lambda r: compute_distance_km(user_loc, (r["lat"], r["lon"])), axis=1)

    selected_id = st.session_state.get("selected_place", None)

    # Map view (pydeck)
    st.subheader("Map")
    if df.empty:
        st.info("No places to show on the map.")
    else:
        # Prepare pydeck view
        viewport = pdk.ViewState(latitude=user_lat, longitude=user_lon, zoom=15, pitch=0)

        scatter = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 60, 0, 160]',
            get_radius=40,
            pickable=True,
            radius_scale=10,
        )

        user_df = pd.DataFrame([{"lon": user_lon, "lat": user_lat, "name": "You"}])
        user_marker = pdk.Layer(
            "ScatterplotLayer",
            data=user_df,
            get_position='[lon, lat]',
            get_color='[0, 120, 200, 255]',
            get_radius=60,
            radius_scale=10
        )

        deck = pdk.Deck(layers=[scatter, user_marker], initial_view_state=viewport,
                        tooltip={"text": "{name}\n{category}\n{rating}★\n{distance_km} km"})
        st.pydeck_chart(deck)

    # Selected place details + route
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
        st.markdown(f"**{sel['name']}** — {sel['category']}")
        st.write(sel["desc"])
        st.write("Vibes:", ", ".join(sel["vibes"]))
        st.write(f"Distance: **{sel['distance_km']:.2f} km** • Rating: **{sel['rating']}★**")

        # Try OSRM first
        use_osrm = st.checkbox("Use OSRM routing (internet required)", value=True)
        route_coords = None
        if use_osrm:
            route_coords = osrm_route(user_loc, (sel["lat"], sel["lon"]))
            if route_coords is None:
                st.warning("OSRM routing failed or is unreachable — showing straight-line fallback.")

        if route_coords is None:
            route_coords = straight_line_route(user_loc, (sel["lat"], sel["lon"]))

        # PathLayer expects list of coords in [lon, lat] pairs
        path_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords, "name": sel["name"]}],
            get_path="path",
            get_width=6,
            get_color=[2, 126, 209],
            width_min_pixels=3,
        )

        # show map with route
        route_deck = pdk.Deck(layers=[path_layer, scatter, user_marker], initial_view_state=viewport)
        st.pydeck_chart(route_deck)

        # Open in Google Maps link
        gmaps = google_maps_url(user_loc, (sel["lat"], sel["lon"]))
        st.markdown(f"[Open full directions in Google Maps]({gmaps})")

# ---------------- Timetable ----------------
elif menu == "Timetable":
    st.header("Timetable")
    if "timetable" not in st.session_state:
        st.session_state["timetable"] = []

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
        st.table(pd.DataFrame(st.session_state["timetable"]))
    else:
        st.info("No timetable entries yet. Add slots using the form above.")

    # Quick suggestion: recommend nearest study place for next class (simple heuristic)
    if st.session_state["timetable"]:
        # pick first upcoming slot (naive)
        next_slot = st.session_state["timetable"][0]
        st.markdown("**Quick suggestion**: nearest study spot for your next class")
        # find nearest place (using sample user_loc)
        df = load_places_df()
        df["distance_km"] = df.apply(lambda r: compute_distance_km((user_lat, user_lon), (r["lat"], r["lon"])), axis=1)
        nearest = df.sort_values("distance_km").iloc[0]
        st.write(f"For **{next_slot['course']}** (on {next_slot['day']}):")
        st.write(f"- Recommended spot: **{nearest['name']}** — {nearest['category']} ({nearest['distance_km']:.2f} km away)")

# ---------------- Assignments ----------------
elif menu == "Assignments":
    st.header("Assignments & Grades")
    if "assignments" not in st.session_state:
        st.session_state["assignments"] = []

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
elif menu == "Settings":
    st.header("Settings & advanced")
    st.markdown("You can change app behavior here (demo only).")
    show_assets = st.checkbox("Show images available in /mnt/data")
    if show_assets:
        files = list(ASSETS_DIR.glob("*"))
        for f in files:
            st.write(f.name)

    st.markdown("Routing provider")
    st.markdown("- By default this prototype uses the public OSRM server for route polyline lookup. For production, use a paid provider or your own OSRM instance.")
    st.markdown("Developer notes:")
    st.code("""
- To replace PLACES, load from a CSV / DB or call a Places API.
- To persist timetable/assignments, connect to a DB (SQLite/Postgres/Firebase).
- To authenticate users, integrate OAuth / your identity provider.
""")

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Prototype built for Academic Cockpit — Nearby Hub + Navigate Smarter demo.")
