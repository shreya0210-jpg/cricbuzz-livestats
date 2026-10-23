
from database.db import get_connection


def seed_db():
    players = [
        ("Virat Kohli", "India", 85, 0, 1),
        ("Rohit Sharma", "India", 62, 0, 1),
        ("Jasprit Bumrah", "India", 10, 3, 1),
        ("Travis Head", "Australia", 74, 0, 1),
        ("Pat Cummins", "Australia", 12, 2, 1),
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for player in players:
        cursor.execute(
            """
            INSERT INTO player_stats
                (player_name, team, runs, wickets, matches_played)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM player_stats
                WHERE player_name = ? AND team = ?
            );
            """,
            (*player, player[0], player[1])
        )
    matches = [
        ("India", "Australia", "Mumbai", "2026-10-25", "Upcoming"),
        ("England", "South Africa", "London", "2026-10-26", "Upcoming"),
        ("Pakistan", "New Zealand", "Lahore", "2026-10-20", "Completed"),
    ]

    for match in matches:
        cursor.execute(
            """
            INSERT INTO matches
                (team1, team2, venue, match_date, match_status)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM matches
                WHERE team1 = ? AND team2 = ? AND match_date = ?
            );
            """,
            (*match, match[0], match[1], match[3])
        )

    conn.commit()
    conn.close()
