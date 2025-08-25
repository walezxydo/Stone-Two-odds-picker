import streamlit as st
import pandas as pd
from api_football import get_fixtures, get_odds

st.title("2-Odds Daily Picker (Live Football)")

league_ids_input = st.text_input("Enter league IDs separated by commas (e.g., 39,140)", "39,140")
days_ahead = st.slider("Days ahead to fetch fixtures", 1, 7, 2)
api_key = st.text_input("API-Football Key", "", type="password")

if st.button("Fetch Live Fixtures & Odds"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        from api_football import HEADERS
        HEADERS["x-apisports-key"] = api_key

        league_ids_list = [int(x.strip()) for x in league_ids_input.split(",") if x.strip().isdigit()]
        fixtures_df = get_fixtures(league_ids_list, days_ahead)

        if fixtures_df.empty:
            st.info("No upcoming fixtures found.")
        else:
            st.subheader("Upcoming Fixtures")
            st.dataframe(fixtures_df)

            fixture_ids = fixtures_df["fixture_id"].tolist()
            odds_df = get_odds(fixture_ids[:5])
            if not odds_df.empty:
                st.subheader("Bookmaker Odds")
                st.dataframe(odds_df)
            else:
                st.info("Odds not available yet for selected fixtures.")