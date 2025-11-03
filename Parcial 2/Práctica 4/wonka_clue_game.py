""" Wonka Clue - Minimal Pygame Prototype Single-file Python (pygame) prototype for your Clue-style game.

Features:

Loads sprite "idle" frames for 6 characters (Charlie, Augustus, Veruca, Violet, Mike, Wonka)

Characters are clickable to open a simple interrogation dialog

5 background rooms (pan between them)

A simple weapons panel with 5 murder-weapon icons

Placeholder asset paths (you must provide PNGs in ./assets/...)

Graceful fallback drawing if assets are missing


How to run:

1. Install pygame: pip install pygame


2. Create an assets folder following the structure below (see README comments in code)


3. python wonka_clue_game.py



Note: This is a prototype. Expand with your game logic, audio, and animations as needed. """

import os import sys import pygame from pygame.locals import *

-------- CONFIG -------------------------------------------------

SCREEN_WIDTH = 1280 SCREEN_HEIGHT = 720 FPS = 60

ASSET_DIR = os.path.join(os.path.dirname(file), 'assets') CHAR_DIR = os.path.join(ASSET_DIR, 'characters') ROOM_DIR = os.path.join(ASSET_DIR, 'rooms') WEAPON_DIR = os.path.join(ASSET_DIR, 'weapons')

CHARACTER_NAMES = ['charlie', 'augustus', 'veruca', 'violet', 'mike', 'wonka'] ROOM_NAMES = ['chocolate_river', 'inventing_room', 'nut_sorting', 'tv_room', 'fizzy_lift'] WEAPON_NAMES = ['candy_cane', 'golden_ticket_knife', 'exploding_gum', 'fizzy_gas_tank', 'nutcracker_arm']

FONT_NAME = None  # default pygame font

--- Helper: safe image loader with fallback rect

def load_image(path): try: return pygame.image.load(path).convert_alpha() except Exception: return None

-------- CLASSES ------------------------------------------------

class SpriteCharacter(pygame.sprite.Sprite): """Character with idle animation frames and click interaction."""

def __init__(self, name, pos):
    super().__init__()
    self.name = name
    self.pos = pygame.Vector2(pos)
    self.frames = []
    self.frame_index = 0
    self.frame_timer = 0.0
    self.frame_delay = 0.25  # seconds per frame
    self.image = None
    self.rect = pygame.Rect(pos[0], pos[1], 80, 140)
    self.load_frames()
    self.is_selected = False

def load_frames(self):
    # Expecting ./assets/characters/<name>_idle_0.png, _1.png, ...
    i = 0
    while True:
        path = os.path.join(CHAR_DIR, f"{self.name}_idle_{i}.png")
        img = load_image(path)
        if img is None:
            break
        self.frames.append(img)
        i += 1
    if not self.frames:
        # try single file
        path = os.path.join(CHAR_DIR, f"{self.name}.png")
        img = load_image(path)
        if img:
            self.frames.append(img)
    if self.frames:
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=self.pos)
    else:
        # fallback: create plain surface
        surf = pygame.Surface((80, 140), pygame.SRCALPHA)
        surf.fill((180, 180, 180, 255))
        pygame.draw.rect(surf, (100, 100, 100), surf.get_rect(), 4)
        self.image = surf
        self.rect = surf.get_rect(topleft=self.pos)

def update(self, dt):
    if len(self.frames) > 1:
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer -= self.frame_delay
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
    # hover scale effect for selection

def draw(self, surface):
    surface.blit(self.image, self.rect.topleft)
    if self.is_selected:
        pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)

def on_click(self, game):
    # open interrogation dialog
    game.open_dialogue(self.name)

class Room: def init(self, key): self.key = key self.image = None self.load()

def load(self):
    path = os.path.join(ROOM_DIR, f"{self.key}.png")
    img = load_image(path)
    if img:
        # scale to screen while preserving aspect ratio
        self.image = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        # fallback background
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill((30, 20, 10))
        pygame.draw.rect(surf, (80, 40, 20), surf.get_rect(), 8)
        font = pygame.font.Font(FONT_NAME, 36)
        text = font.render(self.key.replace('_', ' ').title(), True, (200, 200, 200))
        surf.blit(text, (40, 40))
        self.image = surf

def draw(self, surface):
    surface.blit(self.image, (0, 0))

class WeaponIcon: def init(self, key, pos): self.key = key self.pos = pos self.image = None self.rect = pygame.Rect(pos[0], pos[1], 64, 64) self.load() self.selected = False

def load(self):
    path = os.path.join(WEAPON_DIR, f"{self.key}.png")
    img = load_image(path)
    if img:
        self.image = pygame.transform.smoothscale(img, (64, 64))
        self.rect = self.image.get_rect(topleft=self.pos)
    else:
        surf = pygame.Surface((64, 64))
        surf.fill((90, 0, 0))
        pygame.draw.rect(surf, (180, 180, 180), surf.get_rect(), 3)
        font = pygame.font.Font(FONT_NAME, 12)
        text = font.render(self.key.split('_')[0].upper(), True, (255, 255, 255))
        surf.blit(text, (4, 24))
        self.image = surf
        self.rect = surf.get_rect(topleft=self.pos)

def draw(self, surf):
    surf.blit(self.image, self.rect.topleft)
    if self.selected:
        pygame.draw.rect(surf, (0, 200, 0), self.rect, 3)

-------- MAIN GAME CLASS ----------------------------------------

class WonkaClueGame: def init(self): pygame.init() pygame.display.set_caption('Wonka Clue - Prototype') self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) self.clock = pygame.time.Clock() self.font = pygame.font.Font(FONT_NAME, 20) self.big_font = pygame.font.Font(FONT_NAME, 28)

# load rooms
    self.rooms = [Room(k) for k in ROOM_NAMES]
    self.current_room_index = 0

    # characters
    self.characters = pygame.sprite.Group()
    # layout positions for panoramic distant view
    start_x = 140
    gap_x = 180
    y = SCREEN_HEIGHT - 220
    for i, name in enumerate(CHARACTER_NAMES):
        pos = (start_x + i * gap_x, y)
        char = SpriteCharacter(name, pos)
        self.characters.add(char)

    # weapons panel
    self.weapons = []
    for i, key in enumerate(WEAPON_NAMES):
        pos = (SCREEN_WIDTH - 90, 40 + i * 80)
        w = WeaponIcon(key, pos)
        self.weapons.append(w)

    # UI state
    self.running = True
    self.dialogue_open = False
    self.dialogue_lines = []
    self.dialogue_title = ''
    self.selected_weapon = None

    # preload dialogues using the content you provided earlier
    self.dialogues = self._build_dialogues()

def _build_dialogues(self):
    # A tiny mapping for interrogation replies. Expand as needed.
    return {
        'charlie': [
            "I was standing by the chocolate river... I thought I heard him laugh.",
            "We had words earlier about the factory. He should have trusted me.",
            "I found his cane floating."
        ],
        'augustus': [
            "I was inspecting the machines — I only want what I make to be perfect.",
            "My boots got muddy in the river earlier. It was humiliating the last time.",
            "I saw someone near the riverbank before the alarm." 
        ],
        'veruca': [
            "I was looking at the egg sorter. I couldn't stand his attitude.",
            "My glove was ruined by grease. I didn't kill him!",
            "I swear I smelled perfume near the lever."
        ],
        'violet': [
            "I was testing the gum formula — it was volatile.",
            "He said things to me... I won't be mocked.",
            "There were purple fingerprints on a lever."
        ],
        'mike': [
            "I was checking the monitors. The feeds glitched before the scream.",
            "His notebook had my name on it — like he was watching me.",
            "There was a power surge right when he fell."
        ],
        'wonka': [
            "(silent body - investigation target)"
        ]
    }

def open_dialogue(self, name):
    self.dialogue_open = True
    self.dialogue_title = name.title()
    self.dialogue_lines = self.dialogues.get(name, ["No response."])

def close_dialogue(self):
    self.dialogue_open = False
    self.dialogue_lines = []

def draw_ui(self):
    # top-left room name
    room_name = ROOM_NAMES[self.current_room_index].replace('_', ' ').title()
    txt = self.font.render(room_name, True, (255, 255, 255))
    self.screen.blit(txt, (20, 20))

    # weapons panel title
    wtxt = self.font.render('Weapons', True, (255, 255, 255))
    self.screen.blit(wtxt, (SCREEN_WIDTH - 180, 10))

    # draw weapons
    for w in self.weapons:
        w.draw(self.screen)

    # bottom help
    help_txt = self.font.render('Click characters to interrogate • Arrow keys to change room • Click weapons to select', True, (200, 200, 200))
    self.screen.blit(help_txt, (20, SCREEN_HEIGHT - 40))

    # selected weapon label
    if self.selected_weapon:
        sw_txt = self.font.render('Selected: ' + self.selected_weapon.key.replace('_', ' ').title(), True, (255, 200, 50))
        self.screen.blit(sw_txt, (SCREEN_WIDTH - 420, 20))

def draw_dialogue(self):
    if not self.dialogue_open:
        return
    # dialog box
    box_w = SCREEN_WIDTH - 120
    box_h = 180
    box_x = 60
    box_y = SCREEN_HEIGHT - box_h - 60
    rect = pygame.Rect(box_x, box_y, box_w, box_h)
    pygame.draw.rect(self.screen, (10, 10, 10), rect)
    pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)

    title = self.big_font.render(self.dialogue_title, True, (255, 220, 180))
    self.screen.blit(title, (box_x + 12, box_y + 12))

    for i, line in enumerate(self.dialogue_lines):
        txt = self.font.render(line, True, (220, 220, 220))
        self.screen.blit(txt, (box_x + 12, box_y + 56 + i * 28))

    close_hint = self.font.render('Press ESC to close', True, (150, 150, 150))
    self.screen.blit(close_hint, (box_x + box_w - 170, box_y + box_h - 30))

def handle_mouse_click(self, pos):
    # weapons
    for w in self.weapons:
        if w.rect.collidepoint(pos):
            # toggle selection
            for other in self.weapons:
                other.selected = False
            w.selected = True
            self.selected_weapon = w
            return

    # characters (front to back)
    for char in reversed(self.characters.sprites()):
        if char.rect.collidepoint(pos):
            char.on_click(self)
            return

    # click elsewhere closes dialogue
    if self.dialogue_open:
        self.close_dialogue()

def change_room(self, delta):
    self.current_room_index = (self.current_room_index + delta) % len(self.rooms)

def run(self):
    while self.running:
        dt = self.clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.dialogue_open:
                        self.close_dialogue()
                    else:
                        self.running = False
                elif event.key == K_RIGHT:
                    self.change_room(1)
                elif event.key == K_LEFT:
                    self.change_room(-1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)

        # update
        for c in self.characters:
            c.update(dt)

        # draw
        self.rooms[self.current_room_index].draw(self.screen)

        # draw characters as a distant panoramic row (adjust opacity for depth if desired)
        for c in self.characters:
            c.draw(self.screen)

        # UI overlays
        self.draw_ui()
        self.draw_dialogue()

        pygame.display.flip()

    pygame.quit()

--------- RUN --------------------------------------------------

if name == 'main': # create asset folders if missing to help user for path in (ASSET_DIR, CHAR_DIR, ROOM_DIR, WEAPON_DIR): os.makedirs(path, exist_ok=True) print('Please place your image assets in the following folders:') print(' -', CHAR_DIR, '   (character idle frames: name_idle_0.png, name_idle_1.png, ... OR name.png)') print(' -', ROOM_DIR, '   (room background: <room_key>.png)') print(' -', WEAPON_DIR, ' (weapon icons: <weapon_key>.png)') print('\nRunning game...') WonkaClueGame().run()