
import streamlit as st
import pandas as pd
from services.cricket_api import get_live_matches
from database.queries import (
    get_top_run_scorers,
    get_top_wicket_takers
)
from database.db import get_connection

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.header("🏏 Live Cricket Matches")

api_data = get_live_matches()

if "error" in api_data:
    st.warning("Live match data is temporarily unavailable.")
else:
    matches = api_data.get("matches", [])

    
    if matches:
        status_filter = st.selectbox(
            "Filter Live Matches by Status",
            ["All Matches", "Live", "Upcoming", "Finished"]
        )

        if status_filter != "All Matches":
            matches = [
                match for match in matches
                if match.get("status", "").lower() == status_filter.lower()
            ]

        if matches:
            for match in matches:
                home = match.get("home", "Unknown")
                away = match.get("away", "Unknown")
                status = match.get("status", "unknown").title()
                competition = match.get("competition", "Cricket")
                home_score = match.get("home_score") or "—"
                away_score = match.get("away_score") or "—"

                with st.container(border=True):
                    st.subheader(f"{home} vs {away}")
                    st.write(f"**Competition:** {competition}")
                    st.write(f"**Score:** {home_score} — {away_score}")
                    st.write(f"**Status:** {status}")
        else:
            st.info("No matches found for this status.")
    else:
        st.info("No matches are available right now.")



st.info("Currently displaying sample database data.")

conn = get_connection()

matches = pd.read_sql_query(
    "SELECT * FROM matches",
    conn
)

players = pd.read_sql_query(
    "SELECT * FROM player_stats",
    conn
)

conn.close()

# Dashboard summary
col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(matches))
col2.metric("Total Players", len(players))
col3.metric(
    "Total Runs",
    int(players["runs"].sum()) if not players.empty else 0
)

# Matches section

# Matches section
st.header("📅 Cricket Matches")

statuses = ["All Matches"] + sorted(
    matches["match_status"].dropna().unique().tolist()
)

selected_status = st.selectbox(
    "Filter by Match Status",
    statuses
)

if selected_status == "All Matches":
    filtered_matches = matches
else:
    filtered_matches = matches[
        matches["match_status"] == selected_status
    ]

st.dataframe(
    filtered_matches,
    use_container_width=True,
    hide_index=True
)



# Player statistics section
st.header("🏆 Player Statistics")

teams = ["All Teams"] + sorted(players["team"].dropna().unique().tolist())

selected_team = st.selectbox("Filter by Team", teams)

if selected_team == "All Teams":
    filtered_players = players
else:
    filtered_players = players[players["team"] == selected_team]

st.dataframe(
    filtered_players,
    use_container_width=True,
    hide_index=True
)


st.subheader("📊 Top Run Scorers")

top_scorers = players.sort_values(
    by="runs",
    ascending=False
).head(5)

st.bar_chart(
    top_scorers,
    x="player_name",
    y="runs",
    x_label="Player",
    y_label="Runs"
)


# SQL Analytics
st.header("🧮 SQL Analytics")

st.subheader("🏏 Top Run Scorers")
st.dataframe(
    get_top_run_scorers(),
    use_container_width=True,
    hide_index=True
)

st.subheader("🎯 Top Wicket Takers")
st.dataframe(
    get_top_wicket_takers(),
    use_container_width=True,
    hide_index=True
)



