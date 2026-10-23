
from database.queries import (
    get_top_run_scorers,
    get_top_wicket_takers
)

print("\n🏏 TOP RUN SCORERS")
print(get_top_run_scorers().to_string(index=False))

print("\n🎯 TOP WICKET TAKERS")
print(get_top_wicket_takers().to_string(index=False))
