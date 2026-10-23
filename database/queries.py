
import pandas as pd
from database.db import get_connection


def get_top_run_scorers():
    conn = get_connection()
    try:
        query = """
            SELECT player_name, team, runs
            FROM player_stats
            ORDER BY runs DESC
            LIMIT 5;
        """
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def get_top_wicket_takers():
    conn = get_connection()
    try:
        query = """
            SELECT player_name, team, wickets
            FROM player_stats
            ORDER BY wickets DESC
            LIMIT 5;
        """
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
