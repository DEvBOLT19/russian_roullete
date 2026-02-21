import pygame
import random
import sys
import math

# theme fo gui
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface = pygame.Surface((WIDTH, HEIGHT)) 
pygame.display.set_caption("Aura Roulette: Definitive Edition")
clock = pygame.time.Clock()

# Colors for DIDIY 
BG_COLOR    = (10, 10, 12)
CARD_COLOR  = (25, 25, 30)
ACCENT_GOLD = (255, 215, 0)
ACCENT_RED  = (255, 45, 85)
TEXT_WHITE  = (240, 240, 240)
GRAY        = (60, 60, 70)
FLASH_COLOR = (255, 255, 255)

# Fonts by pygame library
TITLE_FONT = pygame.font.SysFont("Verdana", 48, bold=True)
MAIN_FONT  = pygame.font.SysFont("Verdana", 24, bold=True)
UI_FONT    = pygame.font.SysFont("Verdana", 18)

# logic variables
players = []
input_text = ""
game_log = "Add 2+ players to start."
is_spinning = False
spin_angle = 0
flash_timer = 0
shake_intensity = 0
chamber = [0, 0, 0, 0, 0, 1]
random.shuffle(chamber)
winner_declared = False

def draw_text(surf, text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=(x, y))
    if center: rect.center = (x, y)
    surf.blit(surface, rect)

def draw_button(surf, text, x, y, w, h, active):
    color = ACCENT_RED if active else GRAY
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surf, color, rect, border_radius=12)
    pygame.draw.rect(surf, (255,255,255), rect, 2, border_radius=12)
    draw_text(surf, text, MAIN_FONT, TEXT_WHITE, x + w//2, y + h//2, center=True)
    return rect

def draw_revolver(surf, x, y, angle):
    pygame.draw.circle(surf, (40, 40, 45), (x, y), 95)
    pygame.draw.circle(surf, GRAY, (x, y), 90, 8)
    for i in range(6):
        rad = math.radians(angle + (i * 60))
        cx = x + 60 * math.cos(rad)
        cy = y + 60 * math.sin(rad)
        pygame.draw.circle(surf, BG_COLOR, (int(cx), int(cy)), 18)
        pygame.draw.circle(surf, ACCENT_GOLD, (int(cx), int(cy)), 18, 2)

# MAIN FUCTION
running = True
while running:
    display_surface.fill(BG_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # DIDDY MAKE THIS
        if not is_spinning and not winner_declared:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    clean_name = input_text.strip().upper()
                    if clean_name and len(players) < 10:
                        players.append({"name": clean_name, "aura": 1000})
                        input_text = ""
                        game_log = f"{clean_name} joined the lobby."
                    elif len(players) >= 10:
                        game_log = "Lobby is full!"
                
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

            # text inout (FUCK PYTORCH)
            elif event.type == pygame.TEXTINPUT:
                if len(input_text) < 12:
                    input_text += event.text

        # CLCIK
        if event.type == pygame.MOUSEBUTTONDOWN:
            trigger_rect = pygame.Rect(350, 480, 500, 60)
            if trigger_rect.collidepoint(event.pos):
                if winner_declared:
                    # Reset Game
                    players = []
                    winner_declared = False
                    game_log = "New game started. Add players."
                    chamber = [0, 0, 0, 0, 0, 1]
                    random.shuffle(chamber)
                elif len(players) >= 2 and not is_spinning:
                    is_spinning = True
                    spin_timer = pygame.time.get_ticks()

    # ANIMATION
    if is_spinning:
        spin_angle += 25
        game_log = "HOLD YOUR BREATH..."
        
        if pygame.time.get_ticks() - spin_timer > 1800:
            is_spinning = False
            current_p = players[0]
            
            if chamber.pop(0) == 1:
                game_log = f"LOST AURA: {current_p['name']} ELIMINATED"
                players.pop(0)
                flash_timer = 6     
                shake_intensity = 15 
                # Reset Chamber
                chamber = [0, 0, 0, 0, 0, 1]
                random.shuffle(chamber)
            else:
                game_log = f"RESPECT+: {current_p['name']} SURVIVED"
                current_p['aura'] += 500
                players.append(players.pop(0))
                chamber.append(0)
            
            if len(players) == 1:
                game_log = f"👑 {players[0]['name']} IS THE AURA KING!"
                winner_declared = True

    # LAYOUT
    # Sidebar: Squad List
    pygame.draw.rect(display_surface, CARD_COLOR, (30, 80, 280, 480), border_radius=15)
    draw_text(display_surface, "THE SQUAD", MAIN_FONT, ACCENT_GOLD, 50, 100)
    for i, p in enumerate(players):
        color = ACCENT_GOLD if i == 0 else TEXT_WHITE
        prefix = "► " if i == 0 else "  "
        draw_text(display_surface, f"{prefix}{p['name']}", UI_FONT, color, 50, 150 + (i*35))
        draw_text(display_surface, f"{p['aura']}", UI_FONT, ACCENT_GOLD, 230, 150 + (i*35))

    # Main Center
    draw_text(display_surface, "AURA ROULETTE", TITLE_FONT, TEXT_WHITE, WIDTH//2 + 100, 50, center=True)
    draw_revolver(display_surface, WIDTH//2 + 100, HEIGHT//2 - 20, spin_angle)
    
    # Input Field with Flashing Cursor
    pygame.draw.rect(display_surface, CARD_COLOR, (350, 410, 500, 40), border_radius=8)
    cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 and not winner_declared else ""
    draw_text(display_surface, f"New Player: {input_text}{cursor}", UI_FONT, TEXT_WHITE, 360, 420)
    
    # Game Log
    log_color = ACCENT_RED if "ELIMINATED" in game_log else ACCENT_GOLD
    draw_text(display_surface, game_log, UI_FONT, log_color, WIDTH//2 + 100, 370, center=True)
    
    # RESET 
    if winner_declared:
        draw_button(display_surface, "NEW GAME", 350, 480, 500, 60, True)
    else:
        btn_active = len(players) >= 2 and not is_spinning
        draw_button(display_surface, "PULL TRIGGER", 350, 480, 500, 60, btn_active)

    # SHake and flash in the end
    render_offset = [0, 0]
    if shake_intensity > 0:
        render_offset = [random.randint(-shake_intensity, shake_intensity), 
                         random.randint(-shake_intensity, shake_intensity)]
        shake_intensity -= 1

    if flash_timer > 0:
        flash_surf = pygame.Surface((WIDTH, HEIGHT))
        flash_surf.fill(FLASH_COLOR)
        flash_surf.set_alpha(flash_timer * 40)
        display_surface.blit(flash_surf, (0, 0))
        flash_timer -= 1

    # Final diddy Flip
    screen.fill((0, 0, 0))
    screen.blit(display_surface, render_offset)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
