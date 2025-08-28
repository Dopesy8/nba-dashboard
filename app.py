import streamlit as st
import pandas as pd
import plotly.express as px
from etl import get_today_scoreboard, get_team_stats, get_player_stats, normalize

st.set_page_config(page_title="NBA Matchup Dashboard", layout="wide")
st.title("🏀 NBA 赛前对阵分析看板")

# ================== 今日赛程 ==================
st.header("今日赛程")
scoreboard = get_today_scoreboard()
if scoreboard.empty:
    st.info("今天没有比赛。")
else:
    games = scoreboard[["GAME_DATE_EST","GAME_ID","HOME_TEAM_ABBREVIATION","VISITOR_TEAM_ABBREVIATION"]]
    game_options = [f"{row['VISITOR_TEAM_ABBREVIATION']} @ {row['HOME_TEAM_ABBREVIATION']}" for _, row in games.iterrows()]
    game_choice = st.selectbox("选择一场比赛", game_options)

    if game_choice:
        row = games.iloc[game_options.index(game_choice)]
        home, away = row["HOME_TEAM_ABBREVIATION"], row["VISITOR_TEAM_ABBREVIATION"]

        st.subheader(f"对阵分析: {away} @ {home}")

        # ========== 球队对比 ==========
        st.markdown("### 球队对比 (全赛季平均)")
        teams = normalize(get_team_stats())
        sub = teams[teams["TEAM_ABBREVIATION"].isin([home, away])]

        if not sub.empty:
            metrics = ["PACE","OFF_RATING","DEF_RATING","NET_RATING"]
            fig = px.bar(sub, x="TEAM_ABBREVIATION", y=metrics, barmode="group", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

        # ========== 近期表现 ==========
        st.markdown("### 近期表现 (最近 5 场)")
        recent = normalize(get_team_stats(last_n="5"))
        sub_recent = recent[recent["TEAM_ABBREVIATION"].isin([home, away])]
        if not sub_recent.empty:
            st.dataframe(sub_recent[["TEAM_ABBREVIATION","GP","W_PCT","OFF_RATING","DEF_RATING","NET_RATING"]], use_container_width=True)

        # ========== 球员近况 ==========
        st.markdown("### 主要球员近况 (最近 5 场平均)")
        players = normalize(get_player_stats(last_n="5"))
        sub_players = players[players["TEAM_ABBREVIATION"].isin([home, away])]
        top = sub_players.sort_values("PTS", ascending=False).groupby("TEAM_ABBREVIATION").head(5)
        st.dataframe(top[["TEAM_ABBREVIATION","PLAYER_NAME","PTS","REB","AST","MIN"]], use_container_width=True)
