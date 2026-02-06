# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
from haversine import haversine, Unit
from PIL import Image
from pathlib import Path

# --------------------- Page config & header (your snippet integrated) ---------------------
st.set_page_config(page_title="Academic Cockpit", layout="wide")
st.title("🎓 Academic Cockpit")
st.subheader("Your command center for academic success")

st.markdown("""
Welcome to **Academic Cockpit**:
- 📅 Manage your timetable
- 📚 Track assignments & grades
- 🧠 Use AI to study smarter
""")

st.markdown("---")
st.markdown("Below is the **Explorer's Guide** (Nearby Hub + Navigate Smarter) demo integrated inside the Academic Cockpit shell.")
# ------------------------------------------------------------------------------------------

# ---------- Sample dataset ----------
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
        "vibes": ["vibes", "date-spot", "outdoor"],
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

ASSETS_DIR = Path("/mnt/data")

# ---------- Utility functions ----------
@st.cache_data
def load_places_df():
    df = pd.DataFrame(PLACES)
    return df

def compute_distance(user_latlon, place_latlon):
    return haversine(user_latlon, place_latlon, unit=Unit.KILOMETERS)

def google_maps_url(origin, dest):
    return f"https://www.google.com/maps/dir/{origin[0]},{origin[1]}/{dest[0]},{dest[1]}/"

# ---------- Sidebar: user controls (Nearby Hub) ----------
with st.sidebar:
    st.header("Explorer's Hub Controls")
    # location mode
    loc_mode = st.radio("Your location mode", ["Use sample campus location", "Enter coordinates"])
    if loc_mode == "Use sample campus location":
        user_lat, user_lon = 30.9320, 76.5269
    else:
        user_lat = st.number_input("Your latitude", value=30.9320, format="%.6f")
        user_lon = st.number_input("Your longitude", value=76.5269, format="%.6f")

    radius_km = st.slider("Search radius (km)", 0.1, 5.0, 2.0, step=0.1)
    vibes_available = sorted({v for p in PLACES for v in p["vibes"]})
    vibe_filter = st.multiselect("Vibe tags", options=vibes_available, default=[])
    sort_by = st.selectbox("Sort by", ["distance", "rating", "popularity"])
    search_term = st.text_input("Search by name or category")
    trending_only = st.checkbox("Trending (popularity > 70)")

# ---------- Data processing ----------
df = load_places_df()
user_loc = (user_lat, user_lon)
df["distance_km"] = df.apply(lambda r: compute_distance(user_loc, (r["lat"], r["lon"])), axis=1)

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

# ---------- Main layout ----------
left, right = st.columns((1, 2))

with left:
    st.subheader(f"Places ({len(df_filtered)})")
    if df_filtered.empty:
        st.info("No places match your filters. Try expanding radius or clearing filters.")
    for _, place in df_filtered.iterrows():
        st.markdown("---")
        cols = st.columns([1, 3])
        thumb_path = ASSETS_DIR / place["img"]
        if thumb_path.exists():
            with cols[0]:
                st.image(str(thumb_path), width=120)
        else:
            with cols[0]:
                st.empty()

        with cols[1]:
            st.markdown(f"**{place['name']}**  \n"
                        f"{place['category']} • {place['rating']}★  • {place['distance_km']:.2f} km away")
            st.markdown(f"{place['desc']}")
            st.write(" ".join([f"`{v}`" for v in place["vibes"]]))
            c1, c2 = st.columns([1, 1])
            if c1.button("Navigate", key=f"nav_{place['id']}"):
                st.session_state["selected_place"] = int(place["id"])
            if c2.button("Open in Google Maps", key=f"gmaps_{place['id']}"):
                url = google_maps_url(user_loc, (place["lat"], place["lon"]))
                st.markdown(f"[Open directions in Google Maps]({url})")

with right:
    st.subheader("Map")
    if not df_filtered.empty:
        viewport = pdk.ViewState(latitude=user_lat, longitude=user_lon, zoom=15, pitch=0)

        scatter = pdk.Layer(
            "ScatterplotLayer",
            data=df_filtered,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=40,
            pickable=True,
            radius_scale=10,
        )

        user_df = pd.DataFrame([{"lon": user_lon, "lat": user_lat}])
        user_marker = pdk.Layer(
            "ScatterplotLayer",
            data=user_df,
            get_position='[lon, lat]',
            get_color='[0, 120, 200, 255]',
            get_radius=60,
            radius_scale=10
        )

        r = pdk.Deck(layers=[scatter, user_marker], initial_view_state=viewport,
                     tooltip={"text": "{name}\n{category}\n{rating}★\n{distance_km} km"})
        st.pydeck_chart(r)

    selected_id = st.session_state.get("selected_place", None)
    if selected_id:
        sel = df[df["id"] == selected_id].iloc[0]
        st.markdown("### Selected place")
        st.markdown(f"**{sel['name']}** — {sel['category']}")
        st.markdown(f"{sel['desc']}")
        st.write("Vibes:", ", ".join(sel["vibes"]))
        st.write(f"Distance: **{sel['distance_km']:.2f} km** • Rating: **{sel['rating']}★**")

        route_coords = [
            [user_lon, user_lat],
            [sel["lon"], sel["lat"]]
        ]
        line_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords, "name": sel["name"]}],
            get_path="path",
            get_width=6,
            get_color=[2, 126, 209],
            width_min_pixels=3,
        )
        route_deck = pdk.Deck(layers=[line_layer, user_marker, scatter], initial_view_state=viewport)
        st.pydeck_chart(route_deck)

        gmaps = google_maps_url(user_loc, (sel["lat"], sel["lon"]))
        st.markdown(f"[Open full directions in Google Maps]({gmaps})")

st.markdown("---")
st.markdown("#### Next steps (production-ready):")
st.markdown("""
- Connect Academic Cockpit's scheduling/assignments data with the Nearby Hub to recommend study spots based on your calendar.
- Replace sample dataset with a Places API or campus DB.
- Use a Directions API for turn-by-turn navigation polylines.
- Add authentication so students can save preferences & favorites.
""")
