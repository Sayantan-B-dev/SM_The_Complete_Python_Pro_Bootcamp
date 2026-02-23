from flask import Blueprint, render_template, request
from flask_socketio import emit, disconnect
from . import socketio          # ✅ changed from .. import socketio
from .game_logic import SpaceInvadersGame

bp = Blueprint('main', __name__)

# Store active games per socket id
games = {}
# Store background tasks per socket id
game_tasks = {}

@bp.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    games[sid] = SpaceInvadersGame()
    task = socketio.start_background_task(game_loop, sid)
    game_tasks[sid] = task
    emit('connected', {'message': 'Game started'})

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in games:
        del games[sid]
    if sid in game_tasks:
        # The task will stop when it detects the game is gone
        pass

@socketio.on('input')
def handle_input(data):
    sid = request.sid
    if sid not in games:
        return
    game = games[sid]
    game.handle_input(
        left=data.get('left', False),
        right=data.get('right', False),
        shoot=data.get('shoot', False)
    )

@socketio.on('reset')
def handle_reset():
    sid = request.sid
    if sid in games:
        games[sid].reset()

def game_loop(sid):
    """Run at ~60 FPS for a specific client."""
    import time
    frame_time = 1.0 / 60
    while sid in games:
        start = time.time()
        game = games[sid]
        game.update()
        socketio.emit('game_state', game.to_dict(), room=sid)
        elapsed = time.time() - start
        sleep_time = max(0, frame_time - elapsed)
        time.sleep(sleep_time)