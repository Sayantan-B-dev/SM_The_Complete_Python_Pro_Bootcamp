import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_SPEED = 10

BULLET_WIDTH = 4
BULLET_HEIGHT = 5
PLAYER_BULLET_SPEED = -10
ENEMY_BULLET_SPEED = 3
MAX_PLAYER_BULLETS = 3

ALIEN_ROWS = 5
ALIEN_COLS = 15
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 30
ALIEN_SPACING = 7
ALIEN_BASE_SPEED = 5
ALIEN_DROP_STEP = 5
ALIEN_SHOOT_BASE_PROB = 0.001
ALIEN_COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']

USE_BARRIERS = True
BARRIER_COUNT = 4
BARRIER_WIDTH = 80
BARRIER_HEIGHT = 40
BARRIER_Y = 450
BARRIER_COLOR = '#22c55e'

# Hitbox expansion (pixels added on each side)
PLAYER_HITBOX_EXPANSION = 5


class SpaceInvadersGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = {
            'x': SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2,
            'y': SCREEN_HEIGHT - 60,
            'width': PLAYER_WIDTH,
            'height': PLAYER_HEIGHT
        }
        self.aliens = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.barriers = []
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.game_win = False

        self.alien_direction = 1
        self.alien_move_counter = 0
        self.alien_move_delay = 40

        # Input states
        self.left_pressed = False
        self.right_pressed = False

        self._create_aliens()
        self._create_barriers()

    def _create_aliens(self):
        start_x = 100
        start_y = 80
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLS):
                self.aliens.append({
                    'x': start_x + col * (ALIEN_WIDTH + ALIEN_SPACING),
                    'y': start_y + row * (ALIEN_HEIGHT + ALIEN_SPACING),
                    'width': ALIEN_WIDTH,
                    'height': ALIEN_HEIGHT,
                    'active': True,
                    'row': row,
                    'col': col,
                    'color': ALIEN_COLORS[row % len(ALIEN_COLORS)]
                })

    def _create_barriers(self):
        if not USE_BARRIERS:
            return
        spacing = SCREEN_WIDTH / (BARRIER_COUNT + 1)
        for i in range(BARRIER_COUNT):
            x = (i + 1) * spacing - BARRIER_WIDTH / 2
            blocks = []
            for row in range(3):
                for col in range(3):
                    blocks.append({
                        'x': x + col * (BARRIER_WIDTH / 3),
                        'y': BARRIER_Y + row * (BARRIER_HEIGHT / 3),
                        'width': BARRIER_WIDTH / 3,
                        'height': BARRIER_HEIGHT / 3,
                        'active': True
                    })
            self.barriers.append(blocks)

    def _player_hitbox(self):
        """Return an expanded rectangle for collision detection."""
        exp = PLAYER_HITBOX_EXPANSION
        return {
            'x': self.player['x'] - exp,
            'y': self.player['y'] - exp,
            'width': self.player['width'] + 1 * exp,
            'height': self.player['height'] + 1 * exp
        }

    def handle_input(self, left=False, right=False, shoot=False):
        self.left_pressed = left
        self.right_pressed = right
        if shoot and len(self.player_bullets) < MAX_PLAYER_BULLETS:
            self.player_bullets.append({
                'x': self.player['x'] + self.player['width'] / 2 - BULLET_WIDTH / 2,
                'y': self.player['y'] - BULLET_HEIGHT,
                'width': BULLET_WIDTH,
                'height': BULLET_HEIGHT
            })

    def update(self):
        if self.game_over:
            return

        # Player movement
        if self.left_pressed:
            self.player['x'] = max(0, self.player['x'] - PLAYER_SPEED)
        if self.right_pressed:
            self.player['x'] = min(SCREEN_WIDTH - self.player['width'],
                                    self.player['x'] + PLAYER_SPEED)

        # Move player bullets
        for bullet in self.player_bullets[:]:
            bullet['y'] += PLAYER_BULLET_SPEED
            if bullet['y'] + bullet['height'] < 0:
                self.player_bullets.remove(bullet)

        # Alien movement (only every few frames)
        self.alien_move_counter += 1
        if self.alien_move_counter >= self.alien_move_delay / self.level:
            self.alien_move_counter = 0
            edge_hit = False
            for alien in self.aliens:
                if not alien['active']:
                    continue
                alien['x'] += self.alien_direction * ALIEN_BASE_SPEED * self.level
                if alien['x'] <= 0 or alien['x'] + alien['width'] >= SCREEN_WIDTH:
                    edge_hit = True
            if edge_hit:
                self.alien_direction *= -1
                for alien in self.aliens:
                    if alien['active']:
                        alien['y'] += ALIEN_DROP_STEP

        # Alien shooting
        for alien in self.aliens:
            if alien['active'] and random.random() < ALIEN_SHOOT_BASE_PROB * self.level:
                self.enemy_bullets.append({
                    'x': alien['x'] + alien['width'] / 2 - BULLET_WIDTH / 2,
                    'y': alien['y'] + alien['height'],
                    'width': BULLET_WIDTH,
                    'height': BULLET_HEIGHT
                })

        # Move enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet['y'] += ENEMY_BULLET_SPEED
            if bullet['y'] > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)

        # Collisions
        self._check_collisions()

    def _check_collisions(self):
        # Player bullets vs aliens
        for bullet in self.player_bullets[:]:
            for alien in self.aliens:
                if alien['active'] and self._rect_collide(bullet, alien):
                    alien['active'] = False
                    self.player_bullets.remove(bullet)
                    self.score += 10
                    break

        # Player bullets vs barriers
        if USE_BARRIERS:
            for bullet in self.player_bullets[:]:
                for barrier in self.barriers:
                    for block in barrier:
                        if block['active'] and self._rect_collide(bullet, block):
                            block['active'] = False
                            self.player_bullets.remove(bullet)
                            break
                    else:
                        continue
                    break

        # Enemy bullets vs player (using hitbox)
        hitbox = self._player_hitbox()
        for bullet in self.enemy_bullets[:]:
            if self._rect_collide(bullet, hitbox):
                self.lives -= 1
                self.enemy_bullets.remove(bullet)
                if self.lives <= 0:
                    self.game_over = True
                break

        # Enemy bullets vs barriers
        if USE_BARRIERS:
            for bullet in self.enemy_bullets[:]:
                for barrier in self.barriers:
                    for block in barrier:
                        if block['active'] and self._rect_collide(bullet, block):
                            block['active'] = False
                            self.enemy_bullets.remove(bullet)
                            break
                    else:
                        continue
                    break

        # Aliens vs player (using hitbox)
        for alien in self.aliens:
            if alien['active'] and self._rect_collide(alien, hitbox):
                self.game_over = True
                return

        # Aliens reaching bottom (visual player position, not hitbox)
        for alien in self.aliens:
            if alien['active'] and alien['y'] + alien['height'] >= self.player['y']:
                self.game_over = True
                return

        # All aliens destroyed → next level
        if all(not a['active'] for a in self.aliens):
            self.level += 1
            self._create_aliens()

    @staticmethod
    def _rect_collide(r1, r2):
        return (r1['x'] < r2['x'] + r2['width'] and
                r1['x'] + r1['width'] > r2['x'] and
                r1['y'] < r2['y'] + r2['height'] and
                r1['y'] + r1['height'] > r2['y'])

    def to_dict(self):
        """Serialize the game state for sending to the client."""
        return {
            'player': self.player,
            'aliens': [a for a in self.aliens if a['active']],
            'playerBullets': self.player_bullets,
            'enemyBullets': self.enemy_bullets,
            'barriers': self.barriers,
            'score': self.score,
            'level': self.level,
            'lives': self.lives,
            'gameOver': self.game_over,
            'gameWin': self.game_win,
        }