
from database.db import get_connection

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

conn.commit()
conn.close()

print("Player sample data checked and restored.")
