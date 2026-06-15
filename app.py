import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

st.set_page_config(page_title="Streamlit Snake Leaderboard", page_icon="🐍", layout="centered")

st.title("🐍 Snake Game with Leaderboard")

# 1. Initialize Leaderboard in Streamlit Session State
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {
        "Player": ["AlphaSnake", "Chomper", "Slytherin"],
        "High Score": [120, 80, 40]
    }

# 2. Get Player Name Before Starting
if "player_name" not in st.session_state or not st.session_state.player_name:
    st.subheader("Welcome! Please enter your name to start:")
    name_input = st.text_input("Name", placeholder="Enter your player name...")
    if st.button("Start Game"):
        if name_input.strip():
            st.session_state.player_name = name_input.strip()
            st.rerun()
        else:
            st.warning("Please enter a valid name!")
    st.stop() 

player_name = st.session_state.player_name
st.write(f"🎮 **Playing as:** `{player_name}`")

if st.button("Change Player"):
    st.session_state.player_name = ""
    st.rerun()

# 3. Streamlit Query Parameter Catch Hook
query_params = st.query_params
if "last_score" in query_params and "last_player" in query_params:
    p_name = query_params["last_player"]
    p_score = int(query_params["last_score"])
    
    df = pd.DataFrame(st.session_state.leaderboard)
    if p_name in df["Player"].values:
        current_hi = df.loc[df["Player"] == p_name, "High Score"].values[0]
        if p_score > current_hi:
            df.loc[df["Player"] == p_name, "High Score"] = p_score
    else:
        new_row = pd.DataFrame([{"Player": p_name, "High Score": p_score}])
        df = pd.concat([df, new_row], ignore_index=True)
    
    st.session_state.leaderboard = df.to_dict(orient="list")
    st.query_params.clear()
    st.rerun()

# 4. Load the game layout safely from disk
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        raw_html = f.read()
    
    # Inject user dynamic data safely
    final_game_html = raw_html.replace("PLAYER_NAME_PLACEHOLDER", player_name)
    
    # 5. Render Component
    components.html(final_game_html, height=620, scrolling=False)
else:
    st.error("Error: Could not find `index.html` file in your repository!")

# 6. Render Leaderboard Table
st.markdown("---")
st.subheader("🏆 Leaderboard (Highest Scores)")

leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
leaderboard_df = leaderboard_df.sort_values(by="High Score", ascending=False).reset_index(drop=True)

st.table(leaderboard_df)
