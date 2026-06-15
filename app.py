import streamlit as st
import streamlit.components.v1 as components

# Set up the Streamlit page layout
st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Classic Snake Game")
st.write("Built with Python & Streamlit, powered by JavaScript.")

# HTML/JavaScript code for the Snake Game
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
        }
        .controls-hint {
            color: #808495;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <div id="score-board">Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <div id="game-over">Game Over! Press 'Space' to Restart</div>
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

        // Main game loop control
        function startGame() {
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(update, 100); // 100ms per frame
        }

        function update() {
            if (gameOver) return;

            // Move Snake Head
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};

            // Game Over Conditions (Wall collisions)
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                endGame();
                return;
            }

            // Game Over Conditions (Self collision)
            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    endGame();
                    return;
                }
            }

            // Add new head
            snake.unshift(head);

            // Check Food Collision
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                document.getElementById("score").innerText = score;
                generateFood();
            } else {
                // Remove tail if no food eaten
                snake.pop();
            }

            draw();
        }

        function draw() {
            // Clear Canvas
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Snake
            ctx.fillStyle = "#4feb34";
            snake.forEach((part, index) => {
                // Make the head slightly darker green
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

            // Ensure food doesn't spawn on top of snake
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

        // Handle Controls
        window.addEventListener("keydown", e => {
            // Prevent scrolling with arrows/space keys
            if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
                e.preventDefault();
            }

            switch(e.key.toLowerCase()) {
                case "arrowup":
                case "w":
                    if (dy === 0) { dx = 0; dy = -1; }
                    break;
                case "arrowdown":
                case "s":
                    if (dy === 0) { dx = 0; dy = 1; }
                    break;
                case "arrowleft":
                case "a":
                    if (dx === 0) { dx = -1; dy = 0; }
                    break;
                case "arrowright":
                case "d":
                    if (dx === 0) { dx = 1; dy = 0; }
                    break;
                case " ":
                    if (gameOver) restartGame();
                    break;
            }
        });

        // Initialize
        startGame();
    </script>
</body>
</html>
"""

# Embed the HTML game inside Streamlit frame
components.html(snake_game_html, height=520, scrolling=False)

# Footer instructions
st.markdown("---")
st.caption("Tip: If the snake isn't moving, click inside the game box to give it keyboard focus!")
