
import streamlit as st
import pandas as pd
from database.db import get_connection

st.title("👥 Player Management")
st.write("Add, edit, and delete player statistics.")


def load_players():
    conn = get_connection()
    players = pd.read_sql_query(
        "SELECT * FROM player_stats",
        conn
    )
    conn.close()
    return players


# Display current players
players = load_players()

st.subheader("Current Players")
st.dataframe(players, use_container_width=True, hide_index=True)


# Add a player
st.subheader("➕ Add Player")

with st.form("add_player_form"):
    player_name = st.text_input("Player Name")
    team = st.text_input("Team")
    runs = st.number_input("Runs", min_value=0, step=1)
    wickets = st.number_input("Wickets", min_value=0, step=1)
    matches_played = st.number_input(
        "Matches Played", min_value=0, step=1
    )

    submitted = st.form_submit_button("Add Player")

    if submitted:
        if not player_name.strip():
            st.error("Please enter a player name.")
        else:
            conn = get_connection()
            conn.execute(
                """
                INSERT INTO player_stats
                (player_name, team, runs, wickets, matches_played)
                VALUES (?, ?, ?, ?, ?)
                """,
                (player_name.strip(), team.strip(), runs, wickets, matches_played)
            )
            conn.commit()
            conn.close()
            st.success("Player added successfully!")
            st.rerun()


# Edit a player
st.subheader("✏️ Edit Player")

players = load_players()

if not players.empty:
    player_id = st.selectbox(
        "Select Player ID to Edit",
        players["stat_id"].tolist()
    )

    selected_player = players[
        players["stat_id"] == player_id
    ].iloc[0]

    with st.form("edit_player_form"):
        edit_name = st.text_input(
            "Player Name",
            value=selected_player["player_name"]
        )
        edit_team = st.text_input(
            "Team",
            value=selected_player["team"] or ""
        )
        edit_runs = st.number_input(
            "Runs",
            min_value=0,
            value=int(selected_player["runs"]),
            step=1
        )
        edit_wickets = st.number_input(
            "Wickets",
            min_value=0,
            value=int(selected_player["wickets"]),
            step=1
        )
        edit_matches = st.number_input(
            "Matches Played",
            min_value=0,
            value=int(selected_player["matches_played"]),
            step=1
        )

        update = st.form_submit_button("Update Player")

        if update:
            if not edit_name.strip():
                st.error("Player name cannot be empty.")
            else:
                conn = get_connection()
                conn.execute(
                    """
                    UPDATE player_stats
                    SET player_name = ?, team = ?, runs = ?,
                        wickets = ?, matches_played = ?
                    WHERE stat_id = ?
                    """,
                    (
                        edit_name.strip(),
                        edit_team.strip(),
                        edit_runs,
                        edit_wickets,
                        edit_matches,
                        player_id
                    )
                )
                conn.commit()
                conn.close()
                st.success("Player updated successfully!")
                st.rerun()


# Delete a player
st.subheader("🗑️ Delete Player")

players = load_players()

if not players.empty:
    delete_id = st.selectbox(
        "Select Player ID to Delete",
        players["stat_id"].tolist(),
        key="delete_player_id"
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this player."
    )

    if st.button("Delete Player", type="primary"):
        if confirm_delete:
            conn = get_connection()
            conn.execute(
                "DELETE FROM player_stats WHERE stat_id = ?",
                (delete_id,)
            )
            conn.commit()
            conn.close()
            st.success("Player deleted successfully!")
            st.rerun()
        else:
            st.warning("Please confirm before deleting.")
