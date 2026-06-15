import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Streamlit Snake Leaderboard", page_icon="🐍", layout="centered")

st.title("🐍 Snake Game with Leaderboard")

# 1. Initialize Leaderboard in Streamlit Session State
# This acts as a tiny temporary database while the app runs
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
    st.stop() # Stops execution here until they submit a name

player_name = st.session_state.player_name
st.write(f"🎮 **Playing as:** `{player_name}`")

# Button to switch players if needed
if st.button("Change Player"):
    st.session_state.player_name = ""
    st.rerun()

# 3. HTML Game Code with High Score Reporting System
snake_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Snake Game</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #0e1117;
            color: #ffffff;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            touch-action: manipulation;
        }}
        #score-board {{
            font-size: 22px;
            margin: 5px 0;
            font-weight: bold;
        }}
        #game-container {{
            position: relative;
            width: 320px;
            height: 320px;
        }}
        canvas {{
            border: 4px solid #4feb34;
            background-color: #1a1c23;
            box-shadow: 0px 0px 15px rgba(79, 235, 52, 0.3);
            width: 100%;
            height: 100%;
        }}
        #game-over {{
            display: none;
            color: #ff4b4b;
            font-size: 18px;
            margin-top: 10px;
            text-align: center;
            cursor: pointer;
        }}
        #menu-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(14, 17, 23, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
        }}
        #menu-overlay h2 {{
            margin-bottom: 15px;
            color: #4feb34;
            font-size: 20px;
        }}
        .menu-btn {{
            background-color: #1a1c23;
            color: white;
            border: 2px solid #4feb34;
            padding: 8px 16px;
            margin: 6px;
            font-size: 14px;
            cursor: pointer;
            width: 130px;
            border-radius: 5px;
        }}
        #mobile-controls {{
            display: grid;
            grid-template-columns: repeat(3, 60px);
            grid-template-rows: repeat(3, 60px);
            gap: 10px;
            margin-top: 15px;
        }}
        .control-btn {{
            background-color: #1a1c23;
            border: 2px solid #4feb34;
            color: white;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            user-select: none;
            -webkit-user-select: none;
        }}
        .control-btn:active {{
            background-color: #4feb34;
            color: #0e1117;
        }}
        .empty-space {{
            visibility: hidden;
        }}
    </style>
</head>
<body>

    <div id="score-board">Score: <span id="score">0</span></div>
    
    <div id="game-container">
        <div id="menu-overlay">
            <h2>Select Difficulty</h2>
            <button class="menu-btn" onclick="setDifficulty('easy')">Easy</button>
            <button class="menu-btn" onclick="setDifficulty('medium')">Medium</button>
            <button class="menu-btn" onclick="setDifficulty('hard')">Hard</button>
        </div>
        <canvas id="gameCanvas" width="320" height="320"></canvas>
    </div>

    <div id="game-over" onclick="showMenu()">Game Over!<br><span style="font-size:14px; color:#4feb34;">Tap here to restart</span></div>

    <div id="mobile-controls">
        <div class="empty-space"></div>
        <div class="control-btn" id="btn-up">▲</div>
        <div class="empty-space"></div>
        
        <div class="control-btn" id="btn-left">◀</div>
        <div class="empty-space"></div>
        <div class="control-btn" id="btn-right">▶</div>
        
        <div class="empty-space"></div>
        <div class="control-btn" id="btn-down">▼</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const gridSize = 16; 
        const tileCount = canvas.width / gridSize;

        let snake = [{{x: 10, y: 10}}];
        let food = {{x: 15, y: 7}};
        let dx = 1;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;
        let gameSpeed = 100;

        function setDifficulty(mode) {{
            if (mode === 'easy') gameSpeed = 200;
            else if (mode === 'medium') gameSpeed = 100;
            else if (mode === 'hard') gameSpeed = 50;
            
            document.getElementById("menu-overlay").style.display = "none";
            restartGame();
        }}

        function startGame() {{
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(update, gameSpeed); 
        }}

        function update() {{
            if (gameOver) return;
            const head = {{x: snake[0].x + dx, y: snake[0].y + dy}};

            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {{
                endGame();
                return;
            }

            for (let i = 0; i < snake.length; i++) {{
                if (head.x === snake[i].x && head.y === snake[i].y) {{
                    endGame();
                    return;
                }}
            }}

            snake.unshift(head);

            if (head.x === food.x && head.y === food.y) {{
                score += 10;
                document.getElementById("score").innerText = score;
                generateFood();
            }} else {{
                snake.pop();
            }}

            draw();
        }

        function draw() {{
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            snake
