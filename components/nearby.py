# components/nearby.py
import streamlit as st
import pandas as pd
from haversine import haversine, Unit
from pathlib import Path

ASSETS_DIR = Path("/mnt/data")
PLACES = [
    {"id":1,"name":"Campus Cafe","category":"Eatery","lat":30.9315,"lon":76.5278,"rating":4.4,"vibes":["study-friendly","budget"],"popularity":78,"img":"campus_cafe.jpg","desc":"Cozy cafe."},
    {"id":2,"name":"Central Library","category":"Library","lat":30.9326,"lon":76.5267,"rating":4.8,"vibes":["quiet","study-friendly"],"popularity":95,"img":"library.jpg","desc":"24/7 study halls."},
]

def load_df():
    return pd.DataFrame(PLACES)

def show_nearby():
    st.header("Nearby Hub")
    df = load_df()
    user_loc = (30.9320,76.5269)
    radius = st.slider("Radius (km)", 0.5, 5.0, 2.0)
    vibes = sorted({v for p in PLACES for v in p["vibes"]})
    sel_vibes = st.multiselect("Vibes", vibes)
    df["distance_km"] = df.apply(lambda r: haversine(user_loc, (r["lat"],r["lon"]), unit=Unit.KILOMETERS), axis=1)
    mask = df["distance_km"] <= radius
    if sel_vibes:
        mask &= df["vibes"].apply(lambda vs: any(v in vs for v in sel_vibes))
    res = df[mask].sort_values("distance_km")
    for _, r in res.iterrows():
        cols = st.columns([1,4])
        img = ASSETS_DIR / r["img"]
        if img.exists():
            cols[0].image(str(img), width=100)
        cols[1].markdown(f"**{r['name']}** — {r['category']}")
        cols[1].write(r["desc"])
        if cols[1].button("Navigate", key=f"nav_{r['id']}"):
            st.session_state["selected_place"] = int(r["id"])
