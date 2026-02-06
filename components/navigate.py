import streamlit as st
import pydeck as pdk
import pandas as pd
import math
from components.nearby import load_df

# =================================================
# Distance calculation (Pure Python – Cloud Safe)
# =================================================
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# =================================================
# Navigate Smarter UI
# =================================================
def show_navigate():
    st.header("🗺️ Navigate Smarter")
    st.caption("Visualize nearby places and preview routes instantly")

    df = load_df()

    # ---------------- Sidebar Controls ----------------
    with st.sidebar.expander("📍 Your Location", expanded=True):
        user_lat = st.number_input("Latitude", value=30.9320, format="%.6f")
        user_lon = st.number_input("Longitude", value=76.5269, format="%.6f")

    user_loc = (user_lat, user_lon)

    # ---------------- Distance Calculation ----------------
    df["distance_km"] = df.apply(
        lambda r: haversine_km(user_lat, user_lon, r["lat"], r["lon"]),
        axis=1
    )

    df = df.sort_values("distance_km")

    # ---------------- Map View ----------------
    st.subheader("📌 Map View")

    view = pdk.ViewState(
        latitude=user_lat,
        longitude=user_lon,
        zoom=15,
        pitch=45
    )

    places_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_radius=50,
        get_color='[255, 80, 80, 180]',
        pickable=True
    )

    user_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame([{
            "lon": user_lon,
            "lat": user_lat,
            "name": "You"
        }]),
        get_position='[lon, lat]',
        get_radius=80,
        get_color='[0, 120, 255, 255]'
    )

    deck = pdk.Deck(
        layers=[places_layer, user_layer],
        initial_view_state=view,
        tooltip={
            "text": "{name}\nDistance: {distance_km} km"
        }
    )

    st.pydeck_chart(deck)

    # ---------------- Route Preview ----------------
    st.subheader("🧭 Route Preview")

    place_names = df["name"].tolist()
    selected_place = st.selectbox("Choose a destination", place_names)

    sel = df[df["name"] == selected_place].iloc[0]

    st.info(
        f"📍 **{sel['name']}** is "
        f"**{sel['distance_km']:.2f} km** away"
    )

    route_coords = [
        [user_lon, user_lat],
        [sel["lon"], sel["lat"]]
    ]

    route_layer = pdk.Layer(
        "PathLayer",
        data=[{"path": route_coords}],
        get_path="path",
        get_width=6,
        get_color=[0, 150, 255],
        width_min_pixels=4
    )

    route_deck = pdk.Deck(
        layers=[places_layer, user_layer, route_layer],
        initial_view_state=view
    )

    st.pydeck_chart(route_deck)

    # ---------------- Extra UX ----------------
    st.markdown("### 🚶 Quick Actions")
    cols = st.columns(2)

    with cols[0]:
        st.metric("Distance (km)", round(sel["distance_km"], 2))

    with cols[1]:
        maps_url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{sel['lat']},{sel['lon']}"
        st.link_button("Open in Google Maps", maps_url)
