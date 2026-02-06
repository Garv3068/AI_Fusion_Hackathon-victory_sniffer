import streamlit as st
from datetime import datetime, timedelta

# =========================================================
# Student Exchange – Travel Sharing
# Systems-oriented Streamlit app with simulated AI matching
# =========================================================

st.set_page_config(
    page_title="Student Exchange – Travel Sharing",
    layout="wide"
)

st.title("🚗 Student Exchange – Travel Sharing")
st.caption("Find safe, coordinated travel partners on campus")

# =========================================================
# In-memory storage (resets on refresh)
# =========================================================
if "trips" not in st.session_state:
    st.session_state.trips = []

# =========================================================
# Simulated AI / Heuristic Logic
# =========================================================

def time_difference_hours(t1, t2):
    """Return absolute time difference in hours."""
    return abs((t1 - t2).total_seconds()) / 3600


def route_similarity(a, b):
    """
    SIMULATED ROUTE SIMILARITY
    -------------------------
    Very simple heuristic:
    - Same starting point → high similarity
    - Otherwise partial similarity based on keyword overlap
    """
    a = a.lower()
    b = b.lower()

    if a == b:
        return 1.0

    common = set(a.split()) & set(b.split())
    return len(common) / max(len(a.split()), 1)


def estimate_cost_split(passengers):
    """
    SIMULATED COST ESTIMATION
    ------------------------
    Assumes a fixed base trip cost and splits
    it across passengers.
    """
    BASE_COST = 600  # mock average cab/bus cost
    return round(BASE_COST / max(passengers, 1), 2)


def find_matches(current_trip, time_window=3):
    """
    SIMULATED AI MATCHING ENGINE
    ----------------------------
    Rules:
    1. Same destination
    2. Time difference within X hours
    3. Rank using:
       - Time closeness
       - Route similarity
    """
    matches = []

    for trip in st.session_state.trips:
        if trip is current_trip:
            continue

        if trip["destination"].lower() == current_trip["destination"].lower():
            time_diff = time_difference_hours(
                trip["datetime"], current_trip["datetime"]
            )

            if time_diff <= time_window:
                route_score = route_similarity(
                    trip["start"], current_trip["start"]
                )

                # Combined score: lower time diff + higher route similarity
                score = (1 / (1 + time_diff)) + route_score

                matches.append({
                    "trip": trip,
                    "score": score,
                    "time_diff": time_diff,
                    "route_score": route_score
                })

    # Rank best matches first
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches


# =========================================================
# Travel Entry Form
# =========================================================

st.subheader("➕ Add a Travel Plan")

with st.form("travel_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input("Destination (e.g. Chandigarh, Delhi)")
        start = st.text_input("Starting Point")
        date = st.date_input("Date")
        time = st.time_input("Time")

    with col2:
        seats = st.number_input(
            "Seats Available (+) or Seats Needed (-)",
            min_value=-5,
            max_value=5,
            value=1
        )

    submit = st.form_submit_button("Add Travel Entry")

    if submit and destination and start:
        trip_datetime = datetime.combine(date, time)

        new_trip = {
            "destination": destination,
            "start": start,
            "datetime": trip_datetime,
            "seats": seats
        }

        st.session_state.trips.append(new_trip)
        st.success("Travel plan added successfully!")

# =========================================================
# Display All Travel Entries
# =========================================================

st.divider()
st.subheader("🧳 All Travel Plans")

if not st.session_state.trips:
    st.info("No travel plans yet.")
else:
    for trip in st.session_state.trips:
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #ddd;border-radius:10px;padding:15px;">
                <h4>📍 {trip['destination']}</h4>
                <b>From:</b> {trip['start']}<br>
                <b>Date & Time:</b> {trip['datetime'].strftime('%d %b %Y, %H:%M')}<br>
                <b>Seats:</b> {"+" if trip['seats']>0 else ""}{trip['seats']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ================= AI MATCH SUGGESTIONS =================
            matches = find_matches(trip)

            if matches:
                st.markdown("🤖 **Suggested travel matches:**")
                for m in matches[:3]:
                    matched_trip = m["trip"]
                    passengers = abs(trip["seats"]) + abs(matched_trip["seats"])
                    cost = estimate_cost_split(passengers)

                    st.markdown(
                        f"""
                        - **From {matched_trip['start']}**  
                          ⏱ Time difference: `{m['time_diff']:.1f} hrs`  
                          🛣 Route similarity: `{m['route_score']:.2f}`  
                          💰 Estimated cost/person: `₹{cost}`
                        """
                    )

            st.markdown(
                "<small>🔒 Safety Tip: Share contact details carefully and meet at public locations.</small>",
                unsafe_allow_html=True
            )

            st.write("")
