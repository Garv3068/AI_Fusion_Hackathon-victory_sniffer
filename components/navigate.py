# components/navigate.py
import streamlit as st
import pydeck as pdk
import pandas as pd
from components.nearby import load_df
from haversine import haversine, Unit

def show_navigate():
    st.header("Navigate Smarter")
    df = load_df()
    user_loc = (30.9320,76.5269)
    df["distance_km"] = df.apply(lambda r: haversine(user_loc, (r["lat"],r["lon"]), unit=Unit.KILOMETERS), axis=1)
    view = pdk.ViewState(latitude=user_loc[0], longitude=user_loc[1], zoom=15)
    scatter = pdk.Layer("ScatterplotLayer", data=df, get_position='[lon, lat]', get_radius=40)
    user_df = pd.DataFrame([{"lon":user_loc[1],"lat":user_loc[0],"name":"You"}])
    user_marker = pdk.Layer("ScatterplotLayer", data=user_df, get_position='[lon, lat]', get_radius=60, get_color='[0,120,200]')
    deck = pdk.Deck(layers=[scatter,user_marker], initial_view_state=view)
    st.pydeck_chart(deck)
    sel_id = st.session_state.get("selected_place", None)
    if sel_id:
        sel = df[df["id"]==sel_id].iloc[0]
        st.write("Routing to", sel["name"])
        coords = [[user_loc[1],user_loc[0]],[sel["lon"],sel["lat"]]]
        path_layer = pdk.Layer("PathLayer", data=[{"path":coords}], get_path="path", get_width=6)
        st.pydeck_chart(pdk.Deck(layers=[path_layer], initial_view_state=view))
