const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;

const socket = io();

let gameState = {
    player: { x: 0, y: 0, width: 50, height: 30 },
    aliens: [],
    playerBullets: [],
    enemyBullets: [],
    barriers: [],
    score: 0,
    level: 1,
    lives: 3,
    gameOver: false,
    gameWin: false
};

let leftPressed = false;
let rightPressed = false;

function updateDisplay() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('level').textContent = gameState.level;
    document.getElementById('lives').textContent = gameState.lives;
}

socket.on('game_state', (state) => {
    gameState = state;
    updateDisplay();
});

function sendInput() {
    socket.emit('input', {
        left: leftPressed,
        right: rightPressed
    });
}

window.addEventListener('keydown', (e) => {
    const key = e.key;
    if (key === 'ArrowLeft' || key === 'a' || key === 'A') {
        leftPressed = true;
        e.preventDefault();
    } else if (key === 'ArrowRight' || key === 'd' || key === 'D') {
        rightPressed = true;
        e.preventDefault();
    } else if (key === ' ' || key === 'Space') {
        socket.emit('input', { shoot: true });
        e.preventDefault();
    } else if (key === 'r' || key === 'R') {
        socket.emit('reset');
        e.preventDefault();
    }
    sendInput();
});

window.addEventListener('keyup', (e) => {
    const key = e.key;
    if (key === 'ArrowLeft' || key === 'a' || key === 'A') {
        leftPressed = false;
        e.preventDefault();
    } else if (key === 'ArrowRight' || key === 'd' || key === 'D') {
        rightPressed = false;
        e.preventDefault();
    }
    sendInput();
});

canvas.addEventListener('mousedown', (e) => {
    if (e.button === 0) {
        e.preventDefault();
        socket.emit('input', { shoot: true });
    }
});
canvas.addEventListener('contextmenu', (e) => e.preventDefault());

socket.on('connect', () => {
    console.log('Connected to server');
    sendInput();
});

function draw() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    ctx.fillStyle = '#fff';
    for (let i = 0; i < 50; i++) {
        if (i % 2 === 0) continue;
        ctx.fillRect(Math.random() * SCREEN_WIDTH, Math.random() * SCREEN_HEIGHT, 2, 2);
    }

    ctx.fillStyle = '#4ade80';
    ctx.fillRect(gameState.player.x, gameState.player.y, gameState.player.width, gameState.player.height);
    ctx.fillStyle = '#fff';
    ctx.fillRect(gameState.player.x + gameState.player.width/2 - 3, gameState.player.y - 5, 6, 5);

    ctx.fillStyle = '#fbbf24';
    for (let bullet of gameState.playerBullets) {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    }

    ctx.fillStyle = '#ef4444';
    for (let bullet of gameState.enemyBullets) {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    }

    for (let alien of gameState.aliens) {
        ctx.fillStyle = alien.color;
        ctx.fillRect(alien.x, alien.y, alien.width, alien.height);
        ctx.fillStyle = '#000';
        ctx.fillRect(alien.x + 10, alien.y + 8, 5, 5);
        ctx.fillRect(alien.x + 25, alien.y + 8, 5, 5);
    }

    if (gameState.barriers) {
        ctx.fillStyle = '#22c55e';
        for (let barrier of gameState.barriers) {
            for (let block of barrier) {
                if (block.active) {
                    ctx.fillRect(block.x, block.y, block.width, block.height);
                }
            }
        }
    }

    if (gameState.gameOver) {
        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.fillStyle = '#ef4444';
        ctx.font = 'bold 48px "Courier New", monospace';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', SCREEN_WIDTH/2, SCREEN_HEIGHT/2);
        ctx.font = '24px "Courier New", monospace';
        ctx.fillStyle = '#fff';
        ctx.fillText('Press R to restart', SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50);
    }
}

function gameLoop() {
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();