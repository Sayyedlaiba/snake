import streamlit as st
import streamlit.components.v1 as components

# Set up the Streamlit page layout
st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Classic Snake Game")
st.write("Select a difficulty mode to begin playing!")

# HTML/JavaScript code for the Snake Game with Difficulty Pop-up
snake_game_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Snake Game</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #0e1117;
            color: #ffffff;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            position: relative;
        }
        #game-container {
            position: relative;
            width: 400px;
            height: 400px;
        }
        canvas {
            border: 4px solid #4feb34;
            background-color: #1a1c23;
            box-shadow: 0px 0px 15px rgba(79, 235, 52, 0.3);
        }
        #score-board {
            font-size: 24px;
            margin: 10px 0;
            font-weight: bold;
        }
        #game-over {
            display: none;
            color: #ff4b4b;
            font-size: 20px;
            margin-top: 10px;
            text-align: center;
        }
        .controls-hint {
            color: #808495;
            font-size: 14px;
            margin-top: 10px;
        }
        /* Popup Menu Styles */
        #menu-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 400px;
            height: 400px;
            background-color: rgba(14, 17, 23, 0.9);
            border: 4px solid #4feb34;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10;
        }
        #menu-overlay h2 {
            margin-bottom: 20px;
            color: #4feb34;
        }
        .menu-btn {
            background-color: #1a1c23;
            color: white;
            border: 2px solid #4feb34;
            padding: 10px 20px;
            margin: 8px;
            font-size: 16px;
            cursor: pointer;
            width: 150px;
            border-radius: 5px;
            transition: all 0.2s ease;
        }
        .menu-btn:hover {
            background-color: #4feb34;
            color: #0e1117;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div id="score-board">Score: <span id="score">0</span></div>
    
    <div id="game-container">
        <!-- The Pop-up Menu -->
        <div id="menu-overlay">
            <h2>Select Difficulty</h2>
            <button class="menu-btn" onclick="setDifficulty('easy')">Easy</button>
            <button class="menu-btn" onclick="setDifficulty('medium')">Medium</button>
            <button class="menu-btn" onclick="setDifficulty('hard')">Hard</button>
        </div>
        
        <canvas id="gameCanvas" width="400" height="400"></canvas>
    </div>

    <div id="game-over">Game Over!<br><span style="font-size:16px; color:#fff;">Press 'Space' to return to menu</span></div>
    <div class="controls-hint">Use Arrow Keys or WASD to move.</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{x: 10, y: 10}];
        let food = {x: 15, y: 7};
        let dx = 1;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;
        let gameSpeed = 100; // default interval in ms

        // This triggers when a user clicks a difficulty button
        function setDifficulty(mode) {
            if (mode === 'easy') {
                gameSpeed = 200;  // Half speed (slower tick rate)
            } else if (mode === 'medium') {
                gameSpeed = 100;  // Original speed
            } else if (mode === 'hard') {
                gameSpeed = 50;   // Double speed (faster tick rate)
            }
            
            // Hide the popup overlay and start the game execution
            document.getElementById("menu-overlay").style.display = "none";
            restartGame();
        }

        function startGame() {
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(update, gameSpeed); 
        }

        function update() {
            if (gameOver) return;

            const head = {x: snake[0].x + dx, y: snake[0].y + dy};

            // Wall collisions
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                endGame();
                return;
            }

            // Self collision
            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    endGame();
                    return;
                }
            }

            snake.unshift(head);

            // Food Collision
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                document.getElementById("score").innerText = score;
                generateFood();
            } else {
                snake.pop();
            }

            draw();
        }

        function draw() {
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Snake
            snake.forEach((part, index) => {
                if (index === 0) ctx.fillStyle = "#3db828";
                else ctx.fillStyle = "#4feb34";
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            });

            // Draw Food
            ctx.fillStyle = "#ff4b4b";
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);

            snake.forEach(part => {
                if (part.x === food.x && part.y === food.y) {
                    generateFood();
                }
            });
        }

        function endGame() {
            gameOver = true;
            clearInterval(gameInterval);
            document.getElementById("game-over").style.display = "block";
        }

        function restartGame() {
            snake = [{x: 10, y: 10}];
            dx = 1;
            dy = 0;
            score = 0;
            gameOver = false;
            document.getElementById("score").innerText = score;
            document.getElementById("game-over").style.display = "none";
            generateFood();
            startGame();
        }

        function showMenu() {
            document.getElementById("game-over").style.display = "none";
            document.getElementById("menu-overlay").style.display = "flex";
            // Clear the canvas space while menu is up
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Handle Controls
        window.addEventListener("keydown", e => {
            if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
                e.preventDefault();
            }

            switch(e.key.toLowerCase()) {
                case "arrowup":
                case "w":
                    if (dy === 0 && !gameOver) { dx = 0; dy = -1; }
                    break;
                case "arrowdown":
                case "s":
                    if (dy === 0 && !gameOver) { dx = 0; dy = 1; }
                    break;
                case "arrowleft":
                case "a":
                    if (dx === 0 && !gameOver) { dx = -1; dy = 0; }
                    break;
                case "arrowright":
                case "d":
                    if (dx === 0 && !gameOver) { dx = 1; dy = 0; }
                    break;
                case " ":
                    if (gameOver) showMenu();
                    break;
            }
        });

        // Initialize by wiping background canvas and letting overlay display first
        ctx.fillStyle = "#1a1c23";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    </script>
</body>
</html>
"""

# Embed the HTML game inside Streamlit frame
components.html(snake_game_html, height=540, scrolling=False)

st.markdown("---")
st.caption("Tip: If your keyboard presses aren't registering, click inside the game field to focus your browser window.")
