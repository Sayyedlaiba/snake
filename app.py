import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Streamlit Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 Mobile-Friendly Snake Game")
st.write("Play with Arrow keys on Desktop or Touch buttons/Swipes on Mobile!")

snake_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
            touch-action: manipulation; /* Prevents double-tap zoom delay */
        }
        #score-board {
            font-size: 22px;
            margin: 5px 0;
            font-weight: bold;
        }
        #game-container {
            position: relative;
            width: 320px; /* Reduced slightly to fit mobile screens better */
            height: 320px;
        }
        canvas {
            border: 4px solid #4feb34;
            background-color: #1a1c23;
            box-shadow: 0px 0px 15px rgba(79, 235, 52, 0.3);
            width: 100%;
            height: 100%;
        }
        #game-over {
            display: none;
            color: #ff4b4b;
            font-size: 18px;
            margin-top: 10px;
            text-align: center;
            cursor: pointer;
        }
        /* Popup Menu Styles */
        #menu-overlay {
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
        }
        #menu-overlay h2 {
            margin-bottom: 15px;
            color: #4feb34;
            font-size: 20px;
        }
        .menu-btn {
            background-color: #1a1c23;
            color: white;
            border: 2px solid #4feb34;
            padding: 8px 16px;
            margin: 6px;
            font-size: 14px;
            cursor: pointer;
            width: 130px;
            border-radius: 5px;
        }
        /* Touch Controls D-PAD */
        #mobile-controls {
            display: grid;
            grid-template-columns: repeat(3, 60px);
            grid-template-rows: repeat(3, 60px);
            gap: 10px;
            margin-top: 15px;
        }
        .control-btn {
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
        }
        .control-btn:active {
            background-color: #4feb34;
            color: #0e1117;
        }
        .empty-space {
            visibility: hidden;
        }
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

        let snake = [{x: 10, y: 10}];
        let food = {x: 15, y: 7};
        let dx = 1;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;
        let gameSpeed = 100;

        function setDifficulty(mode) {
            if (mode === 'easy') gameSpeed = 200;
            else if (mode === 'medium') gameSpeed = 100;
            else if (mode === 'hard') gameSpeed = 50;
            
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

            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                endGame();
                return;
            }

            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    endGame();
                    return;
                }
            }

            snake.unshift(head);

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

            snake.forEach((part, index) => {
                ctx.fillStyle = index === 0 ? "#3db828" : "#4feb34";
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 1, gridSize - 1);
            });

            ctx.fillStyle = "#ff4b4b";
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 1, gridSize - 1);
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
        }

        function endGame() {
            gameOver = true;
            clearInterval(gameInterval);
            document.getElementById("game-over").style.display = "block";
        }

        function restartGame() {
            snake = [{x: 10, y: 10}];
            dx = 1; dy = 0; score = 0; gameOver = false;
            document.getElementById("score").innerText = score;
            document.getElementById("game-over").style.display = "none";
            generateFood();
            startGame();
        }

        function showMenu() {
            document.getElementById("game-over").style.display = "none";
            document.getElementById("menu-overlay").style.display = "flex";
            ctx.fillStyle = "#1a1c23";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Direction changes shared by both keyboards and touchpads
        function goUp() { if (dy === 0 && !gameOver) { dx = 0; dy = -1; } }
        function goDown() { if (dy === 0 && !gameOver) { dx = 0; dy = 1; } }
        function goLeft() { if (dx === 0 && !gameOver) { dx = -1; dy = 0; } }
        function goRight() { if (dx === 0 && !gameOver) { dx = 1; dy = 0; } }

        // Physical Keyboard Event Handling
        window.addEventListener("keydown", e => {
            if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
                e.preventDefault();
            }
            switch(e.key.toLowerCase()) {
                case "arrowup": case "w": goUp(); break;
                case "arrowdown": case "s": goDown(); break;
                case "arrowleft": case "a": goLeft(); break;
                case "arrowright": case "d": goRight(); break;
                case " ": if (gameOver) showMenu(); break;
            }
        });

        // Mobile Touch D-Pad Handling
        document.getElementById("btn-up").addEventListener("touchstart", (e) => { e.preventDefault(); goUp(); });
        document.getElementById("btn-down").addEventListener("touchstart", (e) => { e.preventDefault(); goDown(); });
        document.getElementById("btn-left").addEventListener("touchstart", (e) => { e.preventDefault(); goLeft(); });
        document.getElementById("btn-right").addEventListener("touchstart", (e) => { e.preventDefault(); goRight(); });

        // Simple Mobile Swipe Detection on Canvas
        let touchStartX = 0;
        let touchStartY = 0;

        canvas.addEventListener("touchstart", e => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, {passive: true});

        canvas.addEventListener("touchend", e => {
            let diffX = e.changedTouches[0].screenX - touchStartX;
            let diffY = e.changedTouches[0].screenY - touchStartY;

            // Threshold checking to avoid accidental tiny twitches
            if (Math.abs(diffX) > Math.abs(diffY)) {
                if (Math.abs(diffX) > 30) {
                    if (diffX > 0) goRight(); else goLeft();
                }
            } else {
                if (Math.abs(diffY) > 30) {
                    if (diffY > 0) goDown(); else goUp();
                }
            }
        }, {passive: true});

        // Initialize display context
        ctx.fillStyle = "#1a1c23";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    </script>
</body>
</html>
"""

# Embed component layout with enough vertical headspace for the virtual D-Pad buttons
components.html(snake_game_html, height=640, scrolling=False)
