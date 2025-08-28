import requests
import pandas as pd
import time
import logging

log = logging.getLogger(nba-etl)
logging.basicConfig(level=logging.INFO, format=%(asctime)s  %(levelname)s  %(message)s)

BASE = httpsstats.nba.comstats
HEADERS = {
    User-Agent Mozilla5.0,
    x-nba-stats-origin stats,
    x-nba-stats-token true,
    Referer httpswww.nba.com,
    Origin httpswww.nba.com
}

def _get(endpoint, params, retries=5)
    url = f{BASE}{endpoint}
    for i in range(retries)
        try
            r = requests.get(url, headers=HEADERS, params=params, timeout=15)
            if r.status_code == 200
                js = r.json()
                sets = js.get(resultSets) or js.get(resultSet)
                if isinstance(sets, dict)
                    return pd.DataFrame(sets[rowSet], columns=sets[headers])
                else
                    return pd.DataFrame(sets[0][rowSet], columns=sets[0][headers])
        except Exception as e
            log.warning(fError {endpoint} {e})
        time.sleep(1.5)
    return pd.DataFrame()

def get_today_scoreboard()
    params = {LeagueID 00, DayOffset 0}
    return _get(scoreboardv2, params)

def get_team_stats(season=2024-25, season_type=Regular Season, last_n=0)
    params = {
        LeagueID 00,
        Season season,
        SeasonType season_type,
        LastNGames last_n,
        PerMode PerGame,
        MeasureType Advanced
    }
    return _get(leaguedashteamstats, params)

def get_player_stats(season=2024-25, season_type=Regular Season, last_n=5)
    params = {
        LeagueID 00,
        Season season,
        SeasonType season_type,
        LastNGames last_n,
        PerMode PerGame,
        MeasureType Base
    }
    return _get(leaguedashplayerstats, params)

def normalize(df)
    return df.rename(columns={c c.strip().upper().replace( , _) for c in df.columns})
