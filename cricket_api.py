
import requests


def get_live_matches():
    """Fetch cricket match data from the sports feed."""

    url = "https://sportscore.com/api/widget/matches/"

    try:
        response = requests.get(
            url,
            params={"sport": "cricket", "limit": 10},
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError) as error:
        return {"error": str(error)}
