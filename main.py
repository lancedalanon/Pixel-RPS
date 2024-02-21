"""
Computer Programming 3 Project - Modified Rock, Paper, Scissors

This project is about a more visual version of the traditional
rock, paper, scissors game. It is akin to than of a fighter game
where characters have their own ability to add damage towards their
opponents. Players and/or CPU attack each other up until one is defeated.
The winner is determined by who is not at 0 health points at the end
of the battle. The game is very luck-based. The mechanics of the rock, paper,
scissors itself was not changed for the game except for when both players and cpu
are tied with their choice. If that were the case, then the system flips a coin and
determine who will attack and guard in the battlefield. The opponent who guards from
the attack receives half the expected damage and this is decided by a random chance
whether the opponent could block the attack or not. If the game reaches beyond 12 turns
it will start to reduce 20 health points for each player.

Pygame and Random module are required for this program to work properly.

Group 7 - Prog 3 Project

Members:

Artillagas, Lorenz
Casincac, Kristine
Cosio, Vincent
Dalanon, Lance
Ramirez, Dan
"""
import pygame
import random
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game Window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pixel RPS')

# Define fonts
font_titles = pygame.font.SysFont('Times New Roman', 48, bold=True)
font_game_title = pygame.font.SysFont('Times New Roman', 100, bold=True)
font_others = pygame.font.SysFont('Times New Roman', 36)
font_turn_count = pygame.font.SysFont('Times New Roman', 80, bold=True)

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
BG = (50, 50, 50)
CYAN = (47, 95, 115)

# Load Images
# Background Image
background_image = pygame.image.load('Assets/Background/Background.png').convert_alpha()
logo_rps = pygame.image.load('Assets/Icons/LogoRPS.png').convert_alpha()

# Menu Buttons
play_image = pygame.image.load('Assets/Icons/Play1.png').convert_alpha()
quit_image = pygame.image.load('Assets/Icons/Quit1.png').convert_alpha()
pvp_image = pygame.image.load('Assets/Icons/Pvp1.png').convert_alpha()
ai_image = pygame.image.load('Assets/Icons/Ai1.png').convert_alpha()

# HUD
hp_image = pygame.image.load('Assets/HUD/Upper Screen/HealthBarFrame.png')
hp_image = pygame.transform.scale(hp_image, (525, 35*2))
full_hud_image = pygame.image.load('Assets/HUD/Upper Screen/FullBattleHUD.png')
full_hud_image = pygame.transform.scale(full_hud_image, (640*2, 111*2))
gold_hp_image = pygame.image.load('Assets/HUD/Upper Screen/GoldHealthBar.png')
red_hp_image = pygame.image.load('Assets/HUD/Upper Screen/RedHealthBar.png')

# RPS Image
rock_image = pygame.image.load('Assets/Icons/Rock.png').convert_alpha()
paper_image = pygame.image.load('Assets/Icons/Paper.png').convert_alpha()
scissors_image = pygame.image.load('Assets/Icons/Scissors.png').convert_alpha()
chose_rock = pygame.image.load('Assets/Icons/RockCopy.png').convert_alpha()
chose_rock = pygame.transform.scale(chose_rock, (200*1.3, 196*1.3))
chose_paper = pygame.image.load('Assets/Icons/PaperCopy.png').convert_alpha()
chose_paper = pygame.transform.scale(chose_paper, (200*1.3, 196*1.3))
chose_scissors = pygame.image.load('Assets/Icons/ScissorsCopy.png').convert_alpha()
chose_scissors = pygame.transform.scale(chose_scissors, (200*1.3, 196*1.3))

# Ready Button
ready_image = pygame.image.load('Assets/Icons/Play1.png').convert_alpha()

# Yes Button
yes_image = pygame.image.load('Assets/Icons/Play1.png').convert_alpha()

# No Button
no_image = pygame.image.load('Assets/Icons/Quit1.png').convert_alpha()

# Abilities Button
swordsman_ability_img = pygame.image.load('Assets/Icons/swordsmanability.png').convert_alpha()
mage_ability_img = pygame.image.load('Assets/Icons/mageability.png').convert_alpha()
rouge_ability_img = pygame.image.load('Assets/Icons/rougeability.png').convert_alpha()
cancel_ability_img = pygame.image.load('Assets/Icons/cancel.png').convert_alpha()

# Character Portraits
select_swordsman = pygame.image.load('Assets/Swordsman/Portrait/SwordsmanPortrait.png').convert_alpha()
select_swordsman = pygame.transform.scale(select_swordsman, (488*0.8, 466*0.8))
select_rouge = pygame.image.load('Assets/Rouge/Portrait/RougePortrait.png').convert_alpha()
select_rouge = pygame.transform.scale(select_rouge, (428*0.8, 480*0.8))
select_mage = pygame.image.load('Assets/Mage/Portrait/MagePortrait.png').convert_alpha()
select_mage = pygame.transform.scale(select_mage, (458*0.8, 473*0.8))

# Character Upper Portraits
swordsman_portrait_upper = pygame.image.load('Assets/Swordsman/Portrait/SwordsmanUpperPortrait.png').convert_alpha()
swordsman_portrait_upper = pygame.transform.scale(swordsman_portrait_upper, (249*0.8, 99*0.8))
mage_portrait_upper = pygame.image.load('Assets/Mage/Portrait/MageUpperPortrait.png').convert_alpha()
mage_portrait_upper = pygame.transform.scale(mage_portrait_upper, (249*0.8, 99*0.8))
rouge_portrait_upper = pygame.image.load('Assets/Rouge/Portrait/RougeUpperPortrait.png').convert_alpha()
rouge_portrait_upper = pygame.transform.scale(rouge_portrait_upper, (249*0.8, 99*0.8))

# Background Music
pygame.mixer.music.load('Assets/Sounds/BGM.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
pygame.mixer.music.set_volume(0.1)

# Sound Effects
ability_sfx = pygame.mixer.Sound('Assets/Sounds/Ability.wav')
cancel_sfx = pygame.mixer.Sound('Assets/Sounds/Cancel.wav')
cancel_sfx.set_volume(0.5)
guard_sfx = pygame.mixer.Sound('Assets/Sounds/Guard.wav')
heal_sfx = pygame.mixer.Sound('Assets/Sounds/Heal.wav')
normal_damage_sfx = pygame.mixer.Sound('Assets/Sounds/NormalDamage.wav')
opt_select_sfx = pygame.mixer.Sound('Assets/Sounds/OptSelect.wav')
opt_select_sfx.set_volume(0.5)
select_sfx = pygame.mixer.Sound('Assets/Sounds/Select.wav')
select_sfx.set_volume(0.5)

# Loads Sprite Sheet
class SpriteSheet(object):
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, color):
        image = pygame.Surface((120, 150)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * 120), 0, 120, 150))
        image = pygame.transform.scale(image, (120 * 3.5, 150 * 3.5))
        image.set_colorkey(color)
        return image

# Creates Health Bars
class HealthBar():
    def __init__(self, x, y, baseHealth, maxHealth):
        self.x = x
        self.y = y
        self.baseHealth = baseHealth
        self.maxHealth = maxHealth

    def draw(self, baseHealth):
        #Update with new health
        self.baseHealth = baseHealth
        #Calculate health ratio
        ratio = self.baseHealth / self.maxHealth
        if ratio <= 0:
            ratio = 0
        width = 501
        height = 43
        current_hp = width * ratio
        screen.blit(pygame.transform.scale(gold_hp_image, (current_hp, height)), (self.x, self.y))

# Creates Rock, Paper, Scissors buttons
class RPSButtons():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Checks if Left click has been done
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    # Checks if Left click has been done
    def draw2(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Creates Ready Button
class Ready():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Checks if Left click has been done
    def draw_ready(self):
        ready = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                ready = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return ready

    # Checks if Left click has been done
    def draw_ready2(self):
        ready = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                ready = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return ready

# Creates Ability Buttons for selection
class AbilityButton():
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (175, 175))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Checks if Left click has been done
    def draw_ability(self):
        chose_ability = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                chose_ability = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return chose_ability

    # Checks if Left click has been done
    def draw_ability2(self):
        chose_ability = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                chose_ability = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return chose_ability

# Creates Play, Quit, PvP, PvComp, Yes and No buttons
class SelectionButton():
    def __init__(self, x, y, image, width, height):
        self.image = pygame.transform.scale(image, (width * 0.6, height * 0.6))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # Checks if Left click has been done
    def draw_play(self):
        play = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                play = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return play

# Main Game with different states
class GameState():
    def __init__(self):
        self.state = 'title_screen'
        self.game_type = None
        self.transition_delay = 0
        self.p1_character = None
        self.p2_character = None
        self.fighter = Character
        self.p1_fighter_delay = 0
        self.p2_fighter_delay = 0
        self.start = 0
        self.quit = 0
        self.pvp = 0
        self.ai = 0
        # Player 1
        self.player1_turn = 1
        self.p1_ability_turn = 1
        self.player1_status = 0
        self.player1_option = None
        self.p1_ability_option = None
        self.p1_selection = 0
        self.p1_ability_selection = 0
        self.p1_heal = None
        # Player 2 / CPU
        self.player2_turn = 1
        self.p2_ability_turn = 1
        self.player2_status = 0
        self.player2_option = None
        self.p2_ability_option = None
        self.p2_selection = 0
        self.p2_ability_selection = 0
        self.p2_heal = None
        # Battle Statistics
        self.turn_count = 1
        self.battle_delay = 0
        self.hit_delay = 0
        self.hit_delay2 = 0
        self.hit_done = False
        self.hit_done2 = False
        self.heal_delay = 0
        self.heal_delay2 = 0
        self.heal_done = False
        self.heal_done2 = False
        self.battle_end = False  # If True, Battle animations are finished
        self.battle_finished = False  # If True, Battle itself is done and goes to Battle results next
        self.action_cooldown = 0
        self.action_wait_time = 180
        self.choice_results_delay = 0
        self.choice_results_displayed = 0
        self.results_shown = False
        self.selection_delay = 0
        self.result_delay = 0
        self.question_delay = 0
        self.reset = 0
        self.backToMain = 0
        self.restarting_count = 0
        self.restarting = False

    # Initializes Title Screen
    def title_screen(self):

        draw_bg()
        draw_title_screen()
        draw_logo()
        self.start = (play())
        self.quit = (quit())
        # Starts the Game
        if self.start == 1:
            self.state = 'fighter_selection'
        # Terminates the Game
        if self.quit == 1:
            global gameIsRunning
            gameIsRunning = False

    # Initializes Fighter Selection
    def fighter_selection(self):

        draw_bg()

        # Game Type Selection
        if self.game_type == None:
            self.transition_delay += 1
        if self.transition_delay >= 10:
            draw_gamemode_screen()
            self.pvp = (pvp())
            self.ai = (ai())
            if self.pvp == 1:
                self.game_type = 'pvp'
                self.transition_delay = 0
            if self.ai == 1:
                self.game_type = 'pvai'
                self.transition_delay = 0

        # Player 1 Fighter Selection
        if self.game_type != None and self.p1_character == None:
            self.p1_fighter_delay += 1
            if self.p1_fighter_delay >= 10:
                self.p1_character = (p1_fighter())
                draw_fighter_screen()
                if self.p1_character == "A":
                    self.player1 = self.fighter('Swordsman', 500, 500)
                if self.p1_character == "B":
                    self.player1 = self.fighter('Mage', 500, 500)
                if self.p1_character == "C":
                    self.player1 = self.fighter('Rouge', 500, 500)

        # Player 2 Fighter Selection
        if self.p1_character != None:
            self.p2_fighter_delay += 1
        if self.p2_fighter_delay >= 10 and self.game_type == 'pvp':
            self.p2_character = (p2_fighter())
            draw_fighter_screen2()
            if self.p2_character == "A":
                self.player2 = self.fighter('Swordsman', 500, 500)
            if self.p2_character == "B":
                self.player2 = self.fighter('Mage', 500, 500)
            if self.p2_character == "C":
                self.player2 = self.fighter('Rouge', 500, 500)

        # Player 2 (CPU) Fighter Selection
        if self.p2_fighter_delay >= 10 and self.game_type == 'pvai':
            self.p2_character = (cpu_fighter())
            if self.p2_character == "A":
                self.player2 = self.fighter('Swordsman', 500, 500)
            if self.p2_character == "B":
                self.player2 = self.fighter('Mage', 500, 500)
            if self.p2_character == "C":
                self.player2 = self.fighter('Rouge', 500, 500)

        # Initiates RPS if Player 1 and Player 2 have finished selecting a character
        if self.p1_character and self.p2_character:
            self.state = 'rps'
            self.player1_health_bar = HealthBar(25, 83, self.player1.baseHealth, self.player1.maxHealth)
            self.player2_health_bar = HealthBar(752, 83, self.player1.baseHealth, self.player1.maxHealth)
            self.p1_fighter_delay = 0
            self.p2_fighter_delay = 0

    # Initializes Rock, Paper, Scissors and Abilities Selection
    def rps(self):

        # Delay selection for 150ms
        if self.player1_turn == 1 or self.player2_turn == 1:
            self.selection_delay += 1

        if self.selection_delay < 150:

            self.reset_skill()
            draw_bg()
            draw_hud()
            self.determine_choices2()
            self.draw_turn_count()
            self.player1_health_bar.draw(self.player1.baseHealth)
            self.player2_health_bar.draw(self.player2.baseHealth)
            self.player1.update1()
            self.player2.update2()
            self.player1.draw1()
            self.player2.draw2()

            # Checks if one of the Players has 0 Health Points
            if self.player1.baseHealth <= 0 or self.player2.baseHealth <= 0:
                if self.player1.baseHealth <= 0:
                    self.player1.baseHealth = 0
                if self.player2.baseHealth <= 0:
                    self.player2.baseHealth = 0
                self.battle_finished = True
            if self.battle_finished:
                self.result_delay += 1
            if self.result_delay >= 60:
                self.state = 'battle_result'
                self.result_delay = 0

        # Starts selection for ability and skill to use by both Players
        if self.selection_delay >= 150 and self.battle_finished == False:

            draw_bg()
            draw_hud()
            self.determine_choices2()
            self.draw_turn_count()
            self.player1_health_bar.draw(self.player1.baseHealth)
            self.player2_health_bar.draw(self.player2.baseHealth)
            self.player1.update1()
            self.player2.update2()
            self.player1.draw1()
            self.player2.draw2()
            draw_dark_bg()

            # Start of Player 1's Selection
            if self.player1_status == 0:
                draw_ask_ready1()
                self.player1_status = (self.player1_ready())
            if self.player1_status == 1:
                self.p1_selection += 1
            if self.player1_turn == 1 and self.player1_status == 1 and self.p1_selection >= 10:
                self.draw_skill_turns1()
                self.player1_option = (self.player1_choice())
                if self.player1_option != None:
                    self.player1_turn = 0
            # 50% Chance To Heal P1
            healChance = random.randint(0, 1)
            if healChance == 1:
                if all(value == 1 for value in self.player1.heal.values()):
                    self.p1_heal = 'A'
            else:
                self.p1_heal = 'B'
            if all(value == 1 for value in self.player1.hit.values()):
                self.p1_hit = 'A'
            if self.p1_ability_turn == 1 and self.player1_turn == 0:
                self.p1_ability_selection += 1
            if self.p1_ability_selection >= 10 and self.p1_ability_turn == 1:
                self.draw_ability_turns1()
                self.p1_ability_option = (self.player1_ability())
                if self.p1_ability_option != None:
                    self.p1_ability_turn = 0

        # Start of Player 2's Selection
        if self.game_type == 'pvp':
            if self.player2_status == 0 and self.player1_turn == 0 and self.p1_ability_turn == 0:
                draw_ask_ready2()
                self.player2_status = (self.player2_ready())
            if self.player2_status == 1:
                self.p2_selection += 1
            if self.player2_turn == 1 and self.player2_status == 1 and self.p2_selection >= 10:
                self.draw_skill_turns2()
                self.player2_option = (self.player2_choice())
                if self.player2_option != None:
                    self.player2_turn = 0
            # 50% Chance To Heal P2/CPU
            healChance2 = random.randint(0, 1)
            if healChance2 == 1:
                if all(value == 1 for value in self.player2.heal.values()):
                    self.p2_heal = 'A'
            else:
                self.p2_heal = 'B'
            if all(value == 1 for value in self.player2.hit.values()):
                self.p2_hit = 'A'
            if self.p2_ability_turn == 1 and self.player2_turn == 0:
                self.p2_ability_selection += 1
            if self.p2_ability_selection >= 10 and self.p2_ability_turn == 1:
                self.draw_ability_turns2()
                self.p2_ability_option = (self.player2_ability())
                if self.p2_ability_option != None:
                    self.p2_ability_turn = 0

        # Start of Player 2 (CPU)'s Selection
        elif self.game_type == 'pvai':
            if self.player1_turn == 0 and self.player1_turn == 0 and self.p1_ability_turn == 0:
                self.p2_selection += 1
            if self.player2_turn == 1 and self.p2_selection >= 10:
                self.player2_option = (self.cpu_choice())
                if self.player2_option != None:
                    self.player2_turn = 0
            # 50% Chance To Heal P2/CPU
            healChance2 = random.randint(0, 1)
            if healChance2 == 1:
                if all(value == 1 for value in self.player2.heal.values()):
                    self.p2_heal = 'A'
            else:
                self.p2_heal = 'A'
            if all(value == 1 for value in self.player2.hit.values()):
                self.p2_hit = 'A'
            if self.p2_ability_turn == 1 and self.player2_turn == 0:
                self.p2_ability_option = (self.cpu_ability())
                if self.p2_ability_option != None:
                    self.p2_ability_turn = 0

        # Initiates Choice Results if Player 1 and Player 2 have finished selecting
        if self.p1_ability_turn == 0 and self.p2_ability_turn == 0:
            self.selection_delay = 0
            self.p1_selection = 0
            self.p2_selection = 0
            self.p1_ability_selection = 0
            self.p2_ability_selection = 0
            self.state = 'choice_results'

    # Reveals the Players' choices for a brief moment
    def choice_results(self):

        draw_bg()
        draw_hud()
        self.determine_choices2()
        self.draw_turn_count()
        self.player1_health_bar.draw(self.player1.baseHealth)
        self.player2_health_bar.draw(self.player2.baseHealth)
        self.player1.update1()
        self.player2.update2()
        self.player1.draw1()
        self.player2.draw2()
        draw_dark_bg()

        # Temporarily displays randomized selection effect
        if self.results_shown == False:
            self.choice_results_delay += 1
            draw_choice_result()
            choices = ['R', 'P', 'S']
            temp_p1 = random.choice(choices)
            choices2 = ['R', 'P', 'S']
            temp_p2 = random.choice(choices2)
            if temp_p1 == "R":
                self.p1_display_rock()
            elif temp_p1 == "P":
                self.p1_display_paper()
            elif temp_p1 == "S":
                self.p1_display_scissors()
            if temp_p2 == "R":
                self.p2_display_rock()
            elif temp_p2 == "P":
                self.p2_display_paper()
            elif temp_p2 == "S":
                self.p2_display_scissors()

        # Displays final selection effect of both players after 2 seconds
        if self.choice_results_delay >= 60:
            draw_choice_result()
            self.determine_choices()
            self.results_shown = True
            self.choice_results_displayed += 1

        # Transitions into a battle state after 1 second
        if self.choice_results_displayed >= 60 and self.results_shown:
            self.choice_results_delay = 0
            self.choice_results_displayed = 0
            self.results_shown = False
            self.state = 'battle'

    # Initializes Battle Animations
    def battle(self):

        draw_bg()
        draw_hud()
        self.determine_choices2()
        self.draw_turn_count()
        self.player1_health_bar.draw(self.player1.baseHealth)
        self.player2_health_bar.draw(self.player2.baseHealth)
        self.player1.update1()
        self.player2.update2()
        self.player1.draw1()
        self.player2.draw2()

        # Player 1 Heal
        self.heal_delay += 1
        # Check if player 1 can heal
        if 350 >= self.player1.baseHealth and self.p1_heal == "A" and all(value == 1 for value in self.player1.heal.values()):
            if self.heal_delay >= 180:
                self.player1.heal1()
                self.player1.baseHealth += sum(self.player1.healPower.values())
                self.player1.heal[self.p1_heal] -= 1
                if self.player1.baseHealth > 500:
                    self.player1.baseHealth = 500  # Healing caps at 500 HP
                    self.heal_done = True
                else:
                    self.heal_done = True
        else:
            self.heal_done = True

        # Player 2/CPU Heal
        if self.heal_done:
            self.heal_delay2 += 1
            # Check if player 2/cpu can heal
            if 350 >= self.player2.baseHealth and self.p2_heal == "A" and all(value == 1 for value in self.player2.heal.values()):
                if self.heal_delay2 >= 180:
                    self.heal_done2 = True
                    self.player2.heal2()
                    self.player2.baseHealth += sum(self.player2.healPower.values())
                    self.player2.heal[self.p2_heal] -= 1
                    if self.player2.baseHealth > 500:
                        self.player2.baseHealth = 500  # Healing caps at 500 HP
                        self.heal_done2 = True
                    else:
                        self.heal_done2 = True
            else:
                self.heal_done2 = True

        # Player 1 Hit
        if self.heal_done and self.heal_done2:
            self.hit_delay += 1
            # Check if player 1 can hit
            if self.p1_hit == "A" and all(value == 1 for value in self.player1.hit.values()):
                if self.hit_delay >= 180:
                    self.player1.skill1(self.player2)
                    self.player2.baseHealth -= sum(self.player1.hitPower.values())
                    self.player1.hit[self.p1_hit] -= 1
                    self.hit_done = True
            else:
                self.hit_done = True

            # Player 2/CPU Hit
            if self.hit_done:
                self.hit_delay2 += 1
                # Check if player 2 can hit
                if self.p2_hit == "A" and all(value == 1 for value in self.player2.hit.values()):
                    if self.hit_delay2 >= 180:
                        self.player2.skill2(self.player1)
                        self.player1.baseHealth -= sum(self.player2.hitPower.values())
                        self.player2.hit[self.p2_hit] -= 1
                        self.hit_done2 = True
                else:
                    self.hit_done2 = True

        if self.hit_done and self.hit_done2:
            # If Tie
            if self.player1_option == self.player2_option:
                rand_chance = random.randint(0, 1)
                # Flips a coin to decide who will attack
                if rand_chance == 0:
                    # If Player 1 will attack next
                    p2_block_chance = random.randint(0, 1)
                    if self.p1_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        if p2_block_chance == 0:
                            # If P1 uses ability next and P2 does not block
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player1.ability1(self.player2)
                                totalAttack = self.player1.skillPower.get(
                                    self.player1_option) + self.player1.abilityPower.get(
                                    self.p1_ability_option) + self.crit()
                                self.player2.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                        else:
                            # If P1 uses ability next and P2 blocks
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player1.abilityguard1(self.player2)
                                totalAttack = (self.player1.skillPower.get(
                                    self.player1_option) + self.player1.abilityPower.get(
                                    self.p1_ability_option) + self.crit()) / 2
                                self.player2.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                    else:
                        if p2_block_chance == 0:
                            # If P1 attacks next and P2 does not block
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player1.attack1(self.player2)
                                totalAttack = self.player1.skillPower.get(self.player1_option) + self.crit()
                                self.player2.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                        else:
                            # If P1 uses attack next and P2 blocks
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player1.atkguard1(self.player2)
                                totalAttack = (self.player1.skillPower.get(self.player1_option) + self.crit()) / 2
                                self.player2.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True

                else:
                    # If Player 2 will attack next
                    p1_block_chance = random.randint(0, 1)
                    if self.p2_ability_option == "A" and all(
                            value == 1 for value in self.player2.ability.values()):
                        if p1_block_chance == 0:
                            # If P2 uses ability next and P1 does not block
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player2.ability2(self.player1)
                                totalAttack = self.player2.skillPower.get(
                                    self.player2_option) + self.player2.abilityPower.get(
                                    self.p2_ability_option) + self.crit()
                                self.player1.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                        else:
                            # If P2 uses ability next and P1 blocks
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player2.abilityguard2(self.player1)
                                totalAttack = (self.player2.skillPower.get(
                                    self.player2_option) + self.player2.abilityPower.get(
                                    self.p2_ability_option) + self.crit()) / 2
                                self.player1.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                    else:
                        if p1_block_chance == 0:
                            # If P2 attacks next and P1 does not block
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player2.attack2(self.player1)
                                totalAttack = self.player2.skillPower.get(self.player2_option) + self.crit()
                                self.player1.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True
                        else:
                            # If P2 uses attack next and P1 blocks
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                self.player2.atkguard2(self.player1)
                                totalAttack = (self.player2.skillPower.get(self.player2_option) + self.crit()) / 2
                                self.player1.baseHealth -= totalAttack
                                self.action_cooldown = 0
                                self.battle_end = True

            # If P1 chose Rock and P2 chose scissors
            elif self.player1_option == "R":
                if self.player2_option == "S":

                    # If P1 activated ability and hits
                    if self.p1_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.ability1(self.player2)
                            totalAttack = self.player1.skillPower.get(
                                self.player1_option) + self.player1.abilityPower.get(self.p1_ability_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P1 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.attack1(self.player2)
                            totalAttack = self.player1.skillPower.get(self.player1_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                else:
                    # If P2 activated ability and hits
                    if self.p2_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.ability2(self.player1)
                            totalAttack = self.player2.skillPower.get(
                                self.player1_option) + self.player2.abilityPower.get(self.p2_ability_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P2 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.attack2(self.player1)
                            totalAttack = self.player2.skillPower.get(self.player2_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

            # If P1 chose Paper and P2 chose Rock
            elif self.player1_option == "P":
                if self.player2_option == "R":

                    # If P1 activated ability and hits
                    if self.p1_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.ability1(self.player2)
                            totalAttack = self.player1.skillPower.get(
                                self.player1_option) + self.player1.abilityPower.get(self.p1_ability_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P1 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.attack1(self.player2)
                            totalAttack = self.player1.skillPower.get(self.player1_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                else:
                    # If P2 activated ability and hits
                    if self.p2_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.ability2(self.player1)
                            totalAttack = self.player2.skillPower.get(
                                self.player2_option) + self.player2.abilityPower.get(self.p2_ability_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P2 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.attack2(self.player1)
                            totalAttack = self.player2.skillPower.get(self.player2_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

            # If P1 chose Scissors and P2 chose Paper
            elif self.player1_option == "S":
                if self.player2_option == "P":

                    # If P1 activated ability and hits
                    if self.p1_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.ability1(self.player2)
                            totalAttack = self.player1.skillPower.get(
                                self.player1_option) + self.player1.abilityPower.get(self.p1_ability_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P1 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player1.attack1(self.player2)
                            totalAttack = self.player1.skillPower.get(self.player1_option) + self.crit()
                            self.player2.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                else:
                    # If P2 activated ability and hits
                    if self.p2_ability_option == "A" and all(
                            value == 1 for value in self.player1.ability.values()):
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.ability2(self.player1)
                            totalAttack = self.player2.skillPower.get(
                                self.player1_option) + self.player2.abilityPower.get(self.p2_ability_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

                    # If P2 did not activate ability, but normal attack hits
                    else:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            self.player2.attack2(self.player1)
                            totalAttack = self.player2.skillPower.get(self.player2_option) + self.crit()
                            self.player1.baseHealth -= totalAttack
                            self.action_cooldown = 0
                            self.battle_end = True

        # Reset when battle has ended
        if self.battle_end:

            # Reduces usage of Skill and Ability
            if self.p1_ability_option == "A" and all(
                    value == 1 for value in self.player1.ability.values()):
                self.player1.ability[self.p1_ability_option] -= 1
            if self.p2_ability_option == "A" and all(
                    value == 1 for value in self.player2.ability.values()):
                self.player2.ability[self.p2_ability_option] -= 1
            self.player1.skill[self.player1_option] -= 1
            self.player2.skill[self.player2_option] -= 1

            # Checking and updating ability cooldowns
            if all(value == 0 for value in self.player1.abilityCD.values()):
                playerOneResetA = {"A": 1}
                self.player1.ability.update(playerOneResetA)
                self.player1.abilityCD['A'] = 5
            if all(value == 0 for value in self.player1.ability.values()):
                self.player1.abilityCD['A'] -= 1
            if all(value == 0 for value in self.player2.abilityCD.values()):
                playerTwoResetA = {"A": 1}
                self.player2.ability.update(playerTwoResetA)
                self.player2.abilityCD['A'] = 5
            if all(value == 0 for value in self.player2.ability.values()):
                self.player2.abilityCD['A'] -= 1

            # Check for hit cooldown
            if all(value == 0 for value in self.player1.hitCD.values()):
                playerOneResetA = {"A": 1}
                self.player1.hit.update(playerOneResetA)
                self.player1.hitCD['A'] = 5
            if all(value == 0 for value in self.player2.hitCD.values()):
                playerTwoResetA = {"A": 1}
                self.player2.hit.update(playerTwoResetA)
                self.player2.hitCD['A'] = 5
            if all(value == 0 for value in self.player1.hit.values()):
                self.player1.hitCD['A'] -= 1
            if all(value == 0 for value in self.player2.hit.values()):
                self.player2.hitCD['A'] -= 1

            # Check for heal cooldown
            if all(value == 0 for value in self.player1.healCD.values()):
                playerOneResetA = {"A": 1}
                self.player1.heal.update(playerOneResetA)
                self.player1.healCD['A'] = 10
            if all(value == 0 for value in self.player2.healCD.values()):
                playerTwoResetA = {"A": 1}
                self.player2.heal.update(playerTwoResetA)
                self.player2.healCD['A'] = 10
            if all(value == 0 for value in self.player1.heal.values()):
                self.player1.healCD['A'] -= 1
            if all(value == 0 for value in self.player2.heal.values()):
                self.player2.healCD['A'] -= 1

            # Starts decreasing both Player's HP 12 turns and beyond
            if self.turn_count >= 12:
                self.player1.baseHealth -= 20
                self.player2.baseHealth -= 20

            # Reset Players and CPU Options
            self.player1_option = None
            self.player2_option = None
            self.p1_ability_option = None
            self.p2_ability_option = None
            self.player1_status = 0
            self.player2_status = 0
            self.player1_turn = 1
            self.player2_turn = 1
            self.p1_ability_turn = 1
            self.p2_ability_turn = 1
            self.hit_done = False
            self.hit_delay = 0
            self.hit_done2 = False
            self.hit_delay2 = 0
            self.heal_done = False
            self.heal_delay = 0
            self.heal_done2 = False
            self.heal_delay2 = 0
            self.battle_end = False
            self.turn_count += 1
            self.state = 'rps'

    # Initializes Battle Results and Draws Menu Options
    def battle_result(self):

        done = False

        draw_bg()
        draw_hud()
        self.determine_choices2()
        self.draw_turn_count()
        self.player1_health_bar.draw(self.player1.baseHealth)
        self.player2_health_bar.draw(self.player2.baseHealth)
        self.player1.update1()
        self.player2.update2()
        self.player1.draw1()
        self.player2.draw2()
        pygame.mixer.music.stop()

        # Shows after battle results after 1 second
        self.result_delay += 1
        if self.result_delay >= 60 and done == False:

            draw_bg()
            draw_hud()
            self.determine_choices2()
            self.player1_health_bar.draw(self.player1.baseHealth)
            self.player2_health_bar.draw(self.player2.baseHealth)
            self.player1.update1()
            self.player2.update2()
            self.player1.draw1()
            self.player2.draw2()
            draw_dark_bg()

            # Show which one of the players won the battle
            if self.player1.baseHealth > self.player2.baseHealth:
                draw_victory1()
                self.question_delay += 1
            elif self.player1.baseHealth < self.player2.baseHealth:
                draw_victory2()
                self.question_delay += 1
            elif self.player1.baseHealth <= 0 and self.player2.baseHealth <= 0:
                draw_tie()
                self.question_delay += 1

        # Delays for reset or quit options
        if self.question_delay >= 90:
            done = True

        # Initiates reset and quit options
        if self.reset != 1 and self.backToMain != 1 and done:

            draw_bg()
            draw_hud()
            self.determine_choices2()
            self.player1_health_bar.draw(self.player1.baseHealth)
            self.player2_health_bar.draw(self.player2.baseHealth)
            self.player1.update1()
            self.player2.update2()
            self.player1.draw1()
            self.player2.draw2()
            draw_dark_bg()

            # Resets all player stats
            draw_restart_screen1()
            self.reset = (yes())
            self.backToMain = (no())
            playerOneResetR1 = {"R": 1}
            playerOneResetP1 = {"P": 1}
            playerOneResetS1 = {"S": 1}
            self.player1.skill.update(playerOneResetR1)
            self.player1.skill.update(playerOneResetP1)
            self.player1.skill.update(playerOneResetS1)
            playerTwoResetR2 = {"R": 1}
            playerTwoResetP2 = {"P": 1}
            playerTwoResetS2 = {"S": 1}
            self.player2.skill.update(playerTwoResetR2)
            self.player2.skill.update(playerTwoResetP2)
            self.player2.skill.update(playerTwoResetS2)
            playerOneResetA = {"A": 1}
            self.player1.ability.update(playerOneResetA)
            self.player1.abilityCD['A'] = 5
            playerTwoResetB = {"A": 1}
            self.player2.ability.update(playerTwoResetB)
            self.player2.abilityCD['A'] = 5
            playerOneResetC = {"A": 1}
            self.player1.hit.update(playerOneResetC)
            self.player1.hitCD['A'] = 3
            playerTwoResetD = {"A": 1}
            self.player2.hit.update(playerTwoResetD)
            self.player2.hitCD['A'] = 3
            playerOneResetE = {"A": 1}
            self.player1.heal.update(playerOneResetE)
            self.player1.healCD['A'] = 7
            playerTwoResetF = {"A": 1}
            self.player2.heal.update(playerTwoResetF)
            self.player2.healCD['A'] = 7

            # If reset is selected, will reset stats and keep characters
            if self.reset == 1:

                self.player1.baseHealth = 500
                self.player2.baseHealth = 500
                self.battle_finished = False
                self.question_delay = 0
                self.result_delay = 0
                self.reset = 0
                self.turn_count = 1
                self.state = 'rps'
                pygame.mixer.music.play(-1, 0.0, 5000)

            # If quit is selected, will be brought back to the main menu
            if self.backToMain == 1:

                self.start = 0
                self.quit = 0
                self.pvp = 0
                self.ai = 0
                self.backToMain = 0
                self.player1.baseHealth = 500
                self.player2.baseHealth = 500
                self.p1_character = None
                self.p2_character = None
                self.battle_finished = False
                self.game_type = None
                self.result_delay = 0
                self.question_delay = 0
                self.turn_count = 1
                self.restarting = True

        # Delay setup for transitioning back to the main menu
        if self.restarting:
            self.restarting_count += 1
        if self.restarting_count >= 20:
            self.restarting_count = 0
            self.restarting = False
            self.turn_count = 1
            self.state = 'title_screen'
            pygame.mixer.music.play(-1, 0.0, 5000)

    # Contains different game states
    def game_manager(self):
        if self.state == 'title_screen':
            self.title_screen()
        if self.state == 'fighter_selection':
            self.fighter_selection()
        if self.state == 'choice_results':
            self.choice_results()
        if self.state == 'rps':
            self.rps()
        if self.state == 'battle':
            self.battle()
        if self.state == 'battle_result':
            self.battle_result()

    # Draws Player 1's Characters Ability and Cancel Option
    def draw_ability_turns1(self):
        draw_text2(f'Pick an ability Player 1!', font_titles, white, 200)
        draw_text(f'Use: {self.player1.ability["A"]}', font_others, white, 428, 460)
        draw_text(f'Cancel', font_others, white, 754, 465)

    # Draws Player 2's Characters Ability and Cancel Option
    def draw_ability_turns2(self):
        draw_text2(f'Pick an ability Player 2!', font_titles, white, 200)
        draw_text(f'Use: {self.player2.ability["A"]}', font_others, white, 428, 460)
        draw_text(f'Cancel', font_others, white, 754, 465)

    # Draws Player 1's Rock, Paper, Scissors Options
    def draw_skill_turns1(self):
        draw_text2(f'Choose a pick Player 1!', font_titles, white, 200)
        draw_text(f'Use: {self.player1.skill["R"]}', font_others, white, 305, 470)
        draw_text(f'Use: {self.player1.skill["P"]}', font_others, white, 576, 470)
        draw_text(f'Use: {self.player1.skill["S"]}', font_others, white, 855, 470)

    # Draws Player 2's Rock, Paper, Scissors Options
    def draw_skill_turns2(self):
        draw_text2(f'Choose a pick Player 2!', font_titles, white, 200)
        draw_text(f'Use: {self.player2.skill["R"]}', font_others, white, 305, 470)
        draw_text(f'Use: {self.player2.skill["P"]}', font_others, white, 576, 470)
        draw_text(f'Use: {self.player2.skill["S"]}', font_others, white, 855, 470)

    # Draws Turn Counts
    def draw_turn_count(self):
        draw_text3(f'{self.turn_count}', font_turn_count, red, 90)

    # CPU Choice of Rock, Paper Scissors randomized
    def cpu_choice(self):
        while True:
            rand_select = random.randint(0, 2)
            if rand_select == 0 and self.player2.role == "Swordsman":
                cpuChoice = "R"
            elif rand_select == 1 and self.player2.role == "Swordsman":
                cpuChoice = "P"
            elif rand_select == 2 and self.player2.role == "Swordsman":
                cpuChoice = "S"
            elif rand_select == 0 and self.player2.role == "Mage":
                cpuChoice = "R"
            elif rand_select == 1 and self.player2.role == "Mage":
                cpuChoice = "P"
            elif rand_select == 2 and self.player2.role == "Mage":
                cpuChoice = "S"
            elif rand_select == 0 and self.player2.role == "Rouge":
                cpuChoice = "R"
            elif rand_select == 1 and self.player2.role == "Rouge":
                cpuChoice = "P"
            elif rand_select == 2 and self.player2.role == "Rouge":
                cpuChoice = "S"
            if cpuChoice in self.player2.skill:
                if self.player2.skill[cpuChoice] > 0:
                    return cpuChoice
                else:
                    continue

    # CPU Choice of Ability randomized
    def cpu_ability(self):
        while True:
            rand_ability_select = random.randint(0, 1)
            if rand_ability_select == 0 and self.player2.role == "Swordsman":
                cpuAbilityChoice = "A"
            elif rand_ability_select == 1 and self.player2.role == "Swordsman":
                cpuAbilityChoice = "B"
            elif rand_ability_select == 0 and self.player2.role == "Mage":
                cpuAbilityChoice = "A"
            elif rand_ability_select == 1 and self.player2.role == "Mage":
                cpuAbilityChoice = "B"
            elif rand_ability_select == 0 and self.player2.role == "Rouge":
                cpuAbilityChoice = "A"
            elif rand_ability_select == 1 and self.player2.role == "Rouge":
                cpuAbilityChoice = "B"
            if cpuAbilityChoice == "B":
                return cpuAbilityChoice
            elif cpuAbilityChoice in self.player2.ability:
                if self.player2.ability[cpuAbilityChoice] > 0:
                    return cpuAbilityChoice
                else:
                    break

    # Returns value of Player 1's Choice of Rock, Paper, Scissors
    def player1_choice(self):
        if rock_button.draw():
            if self.player1.skill['R'] > 0:
                select_sfx.play()
                PlayerOneChoice = "R"
                return PlayerOneChoice
        if paper_button.draw():
            if self.player1.skill['P'] > 0:
                select_sfx.play()
                PlayerOneChoice = "P"
                return PlayerOneChoice
        if scissors_button.draw():
            if self.player1.skill['S'] > 0:
                select_sfx.play()
                PlayerOneChoice = "S"
                return PlayerOneChoice

    # Returns value of Player 1's Choice of Ability whether activated or canceled
    def player1_ability(self):
        if self.player1.role == 'Swordsman':
            if swordsman_ability.draw_ability():
                if self.player1.ability['A'] > 0:
                    select_sfx.play()
                    PlayerOneAbility = "A"
                    return PlayerOneAbility
            if cancel_ability.draw_ability():
                select_sfx.play()
                PlayerOneAbility = "B"
                return PlayerOneAbility

        elif self.player1.role == 'Mage':
            if mage_ability.draw_ability():
                if self.player1.ability['A'] > 0:
                    select_sfx.play()
                    PlayerOneAbility = "A"
                    return PlayerOneAbility
            if cancel_ability.draw_ability():
                select_sfx.play()
                PlayerOneAbility = "B"
                return PlayerOneAbility

        elif self.player1.role == 'Rouge':
            if rouge_ability.draw_ability():
                if self.player1.ability['A'] > 0:
                    select_sfx.play()
                    PlayerOneAbility = "A"
                    return PlayerOneAbility
            if cancel_ability.draw_ability():
                select_sfx.play()
                PlayerOneAbility = "B"
                return PlayerOneAbility

    # If Player 1 selects Ready button, it transitions into Rock, Paper, Scissors selection
    def player1_ready(self):
        if ready_button.draw_ready():
            select_sfx.play()
            player1_stat = 1
            return player1_stat
        else:
            player1_stat = 0
            return player1_stat

    # Returns value of Player 2's Choice of Rock, Paper Scissors
    def player2_choice(self):
        if rock_button.draw2():
            if self.player2.skill['R'] > 0:
                select_sfx.play()
                PlayerTwoChoice = "R"
                return PlayerTwoChoice
        if paper_button.draw2():
            if self.player2.skill['P'] > 0:
                select_sfx.play()
                PlayerTwoChoice = "P"
                return PlayerTwoChoice
        if scissors_button.draw2():
            if self.player2.skill['S'] > 0:
                select_sfx.play()
                PlayerTwoChoice = "S"
                return PlayerTwoChoice

    # Returns value of Player 2's Choice of Ability whether activated or canceled
    def player2_ability(self):
        if self.player2.role == 'Swordsman':
            if swordsman_ability.draw_ability2():
                if self.player2.ability['A'] > 0:
                    select_sfx.play()
                    PlayerTwoAbility = "A"
                    return PlayerTwoAbility
            if cancel_ability.draw_ability2():
                select_sfx.play()
                PlayerTwoAbility = "B"
                return PlayerTwoAbility

        elif self.player2.role == 'Mage':
            if mage_ability.draw_ability2():
                if self.player2.ability['A'] > 0:
                    select_sfx.play()
                    PlayerTwoAbility = "A"
                    return PlayerTwoAbility
            if cancel_ability.draw_ability2():
                select_sfx.play()
                PlayerTwoAbility = "B"
                return PlayerTwoAbility

        elif self.player2.role == 'Rouge':
            if rouge_ability.draw_ability2():
                if self.player2.ability['A'] > 0:
                    select_sfx.play()
                    PlayerTwoAbility = "A"
                    return PlayerTwoAbility
            if cancel_ability.draw_ability2():
                select_sfx.play()
                PlayerTwoAbility = "B"
                return PlayerTwoAbility

    # If Player 2 selects Ready button, it transitions into Rock, Paper, Scissors selection
    def player2_ready(self):
        if ready_button.draw_ready2():
            select_sfx.play()
            player2_stat = 1
            return player2_stat
        else:
            player2_stat = 0
            return player2_stat

    # Random chance of critical hit for any player
    def crit(self):
        randomCritChance = random.randint(0, 5)
        if randomCritChance == 1:
            criticalDamage = 50
            return criticalDamage
        else:
            criticalDamage = 0
            return criticalDamage

    # If Player 1 Chose Rock
    def p1_display_rock(self):
        screen.blit(chose_rock, (150, 250))

    # If Player 1 Chose Paper
    def p1_display_paper(self):
        screen.blit(chose_paper, (150, 250))

    # If Player 1 Chose Scissors
    def p1_display_scissors(self):
        screen.blit(chose_scissors, (150, 250))

    # If Player 2 Chose Rock
    def p2_display_rock(self):
        screen.blit(pygame.transform.flip(chose_rock, True, False), (875, 250))

    # If Player 2 Chose Paper
    def p2_display_paper(self):
        screen.blit(pygame.transform.flip(chose_paper, True, False), (875, 250))

    # If Player 2 Chose Scissors
    def p2_display_scissors(self):
        screen.blit(pygame.transform.flip(chose_scissors, True, False), (875, 250))

    # If Player 1 Chose Rock
    def p1_display_char1(self):
        screen.blit(swordsman_portrait_upper, (0, 0))

    # If Player 1 Chose Mage as Character
    def p1_display_char2(self):
        screen.blit(mage_portrait_upper, (0, 0))

    # If Player 1 Chose Rouge as Character
    def p1_display_char3(self):
        screen.blit(rouge_portrait_upper, (0, 0))

    # If Player 2 Chose Swordsman as Character
    def p2_display_char1(self):
        screen.blit(pygame.transform.flip(swordsman_portrait_upper, True, False), (1075, 0))

    # If Player 2 Chose Mage as Character
    def p2_display_char2(self):
        screen.blit(pygame.transform.flip(mage_portrait_upper, True, False), (1075, 0))

    # If Player 2 Chose Rouge as Character
    def p2_display_char3(self):
        screen.blit(pygame.transform.flip(rouge_portrait_upper, True, False), (1075, 0))

    # Conditional Master Function of Rock, Paper, Scissors
    def determine_choices(self):
        if self.player1_option == "R":
            self.p1_display_rock()
        elif self.player1_option == "P":
            self.p1_display_paper()
        elif self.player1_option == "S":
            self.p1_display_scissors()
        if self.player2_option == "R":
            self.p2_display_rock()
        elif self.player2_option == "P":
            self.p2_display_paper()
        elif self.player2_option == "S":
            self.p2_display_scissors()

    # Conditional Master Function of Swordsman, Rouge, and Mage Upper Portraits
    def determine_choices2(self):
        if self.p1_character == "A":
            self.p1_display_char1()
        elif self.p1_character == "B":
            self.p1_display_char2()
        elif self.p1_character == "C":
            self.p1_display_char3()
        if self.p2_character == "A":
            self.p2_display_char1()
        elif self.p2_character == "B":
            self.p2_display_char2()
        elif self.p2_character == "C":
            self.p2_display_char3()

    # Resets Rock, Paper, Scissors Options if all are 0
    def reset_skill(self):
        if all(value == 0 for value in self.player1.skill.values()):
            playerOneResetR = {"R": 1}
            playerOneResetP = {"P": 1}
            playerOneResetS = {"S": 1}
            self.player1.skill.update(playerOneResetR)
            self.player1.skill.update(playerOneResetP)
            self.player1.skill.update(playerOneResetS)
        if all(value == 0 for value in self.player2.skill.values()):
            playerTwoResetR = {"R": 1}
            playerTwoResetP = {"P": 1}
            playerTwoResetS = {"S": 1}
            self.player2.skill.update(playerTwoResetR)
            self.player2.skill.update(playerTwoResetP)
            self.player2.skill.update(playerTwoResetS)

# Creates character objects through Object Oriented Programming
class Character():
    def __init__(self, role, baseHealth, maxHealth):
        self.role = role
        self.baseHealth = baseHealth
        self.maxHealth = maxHealth
        self.animation_list = []
        self.animation_list2 = self.animation_list
        self.action = 0 #0: Idle, 1: Ability, 2: Normal Attack, 3: Skill, 4: Heal, 5:Guard, 6: Hurt
        self.frame_index = 0
        self.action2 = 0 #0: Idle, 1: Ability, 2: Normal Attack, 3: Skill, 4: Heal, 5:Guard, 6: Hurt
        self.frame_index2 = 0
        self.update_time = pygame.time.get_ticks()
        self.update_time2 = pygame.time.get_ticks()
        self.delay = 0
        self.delay2 = 0
        self.isHurt = False
        self.isHurt2 = False
        self.hasGuard = False
        self.hasGuard2 = False

        # If "Swordsman" is the Role that the player/cpu chose
        if role == "Swordsman":

            # Swordsman Idle Sprite
            temp_list = []
            swordsman_idle_sprite = pygame.image.load(f'Assets/{self.role}/Idle.png').convert_alpha()
            self.idle_sprite = SpriteSheet(swordsman_idle_sprite)
            idle_animation = 8
            for x in range(idle_animation):
                temp_list.append(self.idle_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Ability Sprite
            temp_list = []
            swordsman_ability_sprite = pygame.image.load(f'Assets/{self.role}/Ability.png').convert_alpha()
            self.ability_sprite = SpriteSheet(swordsman_ability_sprite)
            ability_animation = 14
            for x in range(ability_animation):
                temp_list.append(self.ability_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Normal Attack Sprite
            temp_list = []
            swordsman_normal_sprite = pygame.image.load(f'Assets/{self.role}/NormalAttack.png').convert_alpha()
            self.normal_attack_sprite = SpriteSheet(swordsman_normal_sprite)
            normal_attack_animation = 13
            for x in range(normal_attack_animation):
                temp_list.append(self.normal_attack_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Skill Sprite
            temp_list = []
            swordsman_skill_sprite = pygame.image.load(f'Assets/{self.role}/Skill.png').convert_alpha()
            self.skill_sprite = SpriteSheet(swordsman_skill_sprite)
            skill_animation = 11
            for x in range(skill_animation):
                temp_list.append(self.skill_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Heal Sprite
            temp_list = []
            swordsman_heal_sprite = pygame.image.load(f'Assets/{self.role}/Heal.png').convert_alpha()
            self.heal_sprite = SpriteSheet(swordsman_heal_sprite)
            heal_animation = 11
            for x in range(heal_animation):
                temp_list.append(self.heal_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Guard Sprite
            temp_list = []
            swordsman_guard_sprite = pygame.image.load(f'Assets/{self.role}/Guard.png').convert_alpha()
            self.guard_sprite = SpriteSheet(swordsman_guard_sprite)
            guard_animation = 3
            for x in range(guard_animation):
                temp_list.append(self.guard_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Swordsman Hurt Sprite
            temp_list = []
            swordsman_hurt_sprite = pygame.image.load(f'Assets/{self.role}/Hurt.png').convert_alpha()
            self.hurt_sprite = SpriteSheet(swordsman_hurt_sprite)
            hurt_animation = 3
            for x in range(hurt_animation):
                temp_list.append(self.hurt_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (270, 380)
            self.image2 = self.animation_list2[self.action2][self.frame_index2]
            self.rect2 = self.image2.get_rect()
            self.rect2.center = (1000, 380)

            self.skill = {
                "R": 1,
                "P": 1,
                "S": 1
            }

            self.skillPower = {
                "R": 50,
                "P": 50,
                "S": 50
            }

            self.abilityName = "Dual Wield"

            self.ability = {
                "A": 1
            }

            self.abilityPower = {
                "A": 100
            }

            self.abilityCD = {
                "A": 7
            }

            self.healName = "Regenerate"

            self.heal = {
                "A": 1
            }

            self.healPower = {
                "A": 100
            }

            self.healCD = {
                "A": 5
            }

            self.hitName = "Slash"

            self.hit = {
                "A": 1
            }

            self.hitPower = {
                "A": 50
            }

            self.hitCD = {
                "A": 3
            }

        # If "Mage" is the Role that the player/cpu chose
        if role == "Mage":

            # Mage Idle Sprite
            temp_list = []
            mage_idle_sprite = pygame.image.load(f'Assets/{self.role}/Idle.png').convert_alpha()
            self.idle_sprite = SpriteSheet(mage_idle_sprite)
            idle_animation = 18
            for x in range(idle_animation):
                temp_list.append(self.idle_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Ability Sprite
            temp_list = []
            mage_ability_sprite = pygame.image.load(f'Assets/{self.role}/Ability.png').convert_alpha()
            self.ability_sprite = SpriteSheet(mage_ability_sprite)
            ability_animation = 18
            for x in range(ability_animation):
                temp_list.append(self.ability_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Normal Attack Sprite
            temp_list = []
            mage_normal_sprite = pygame.image.load(f'Assets/{self.role}/NormalAttack.png').convert_alpha()
            self.normal_attack_sprite = SpriteSheet(mage_normal_sprite)
            normal_attack_animation = 12
            for x in range(normal_attack_animation):
                temp_list.append(self.normal_attack_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Skill Sprite
            temp_list = []
            mage_skill_sprite = pygame.image.load(f'Assets/{self.role}/Skill.png').convert_alpha()
            self.skill_sprite = SpriteSheet(mage_skill_sprite)
            skill_animation = 6
            for x in range(skill_animation):
                temp_list.append(self.skill_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Heal Sprite
            temp_list = []
            mage_heal_sprite = pygame.image.load(f'Assets/{self.role}/Heal.png').convert_alpha()
            self.heal_sprite = SpriteSheet(mage_heal_sprite)
            heal_animation = 8
            for x in range(heal_animation):
                temp_list.append(self.heal_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Guard Sprite
            temp_list = []
            mage_guard_sprite = pygame.image.load(f'Assets/{self.role}/Guard.png').convert_alpha()
            self.guard_sprite = SpriteSheet(mage_guard_sprite)
            guard_animation = 2
            for x in range(guard_animation):
                temp_list.append(self.guard_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Mage Hurt Sprite
            temp_list = []
            mage_hurt_sprite = pygame.image.load(f'Assets/{self.role}/Hurt.png').convert_alpha()
            self.hurt_sprite = SpriteSheet(mage_hurt_sprite)
            hurt_animation = 2
            for x in range(hurt_animation):
                temp_list.append(self.hurt_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (370, 370)
            self.image2 = self.animation_list2[self.action2][self.frame_index2]
            self.rect2 = self.image2.get_rect()
            self.rect2.center = (910, 370)

            self.skill = {
                "R": 1,
                "P": 1,
                "S": 1
            }

            self.skillPower = {
                "R": 50,
                "P": 50,
                "S": 50
            }

            self.abilityName = "Incinerate"

            self.ability = {
                "A": 1
            }

            self.abilityPower = {
                "A": 100
            }

            self.abilityCD = {
                "A": 7
            }

            self.healName = "Regenerate"

            self.heal = {
                "A": 1
            }

            self.healPower = {
                "A": 100
            }

            self.healCD = {
                "A": 5
            }

            self.hitName = "Fireball"

            self.hit = {
                "A": 1
            }

            self.hitPower = {
                "A": 50
            }

            self.hitCD = {
                "A": 3
            }

        # If "Rouge" is the Role that the player/cpu chose
        if role == "Rouge":

            # Rouge Idle Sprite
            temp_list = []
            rouge_idle_sprite = pygame.image.load(f'Assets/{self.role}/Idle.png').convert_alpha()
            self.idle_sprite = SpriteSheet(rouge_idle_sprite)
            idle_animation = 6
            for x in range(idle_animation):
                temp_list.append(self.idle_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Ability Sprite
            temp_list = []
            rouge_ability_sprite = pygame.image.load(f'Assets/{self.role}/Ability.png').convert_alpha()
            self.ability_sprite = SpriteSheet(rouge_ability_sprite)
            ability_animation = 24
            for x in range(ability_animation):
                temp_list.append(self.ability_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Normal Attack Sprite
            temp_list = []
            rouge_normal_sprite = pygame.image.load(f'Assets/{self.role}/NormalAttack.png').convert_alpha()
            self.normal_attack_sprite = SpriteSheet(rouge_normal_sprite)
            normal_attack_animation = 7
            for x in range(normal_attack_animation):
                temp_list.append(self.normal_attack_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Skill Sprite
            temp_list = []
            rouge_skill_sprite = pygame.image.load(f'Assets/{self.role}/Skill.png').convert_alpha()
            self.skill_sprite = SpriteSheet(rouge_skill_sprite)
            skill_animation = 7
            for x in range(skill_animation):
                temp_list.append(self.skill_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Heal Sprite
            temp_list = []
            rouge_heal_sprite = pygame.image.load(f'Assets/{self.role}/Heal.png').convert_alpha()
            self.heal_sprite = SpriteSheet(rouge_heal_sprite)
            heal_animation = 9
            for x in range(heal_animation):
                temp_list.append(self.heal_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Guard Sprite
            temp_list = []
            rouge_guard_sprite = pygame.image.load(f'Assets/{self.role}/Guard.png').convert_alpha()
            self.guard_sprite = SpriteSheet(rouge_guard_sprite)
            guard_animation = 3
            for x in range(guard_animation):
                temp_list.append(self.guard_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            # Rouge Hurt Sprite
            temp_list = []
            rouge_hurt_sprite = pygame.image.load(f'Assets/{self.role}/Hurt.png').convert_alpha()
            self.hurt_sprite = SpriteSheet(rouge_hurt_sprite)
            hurt_animation = 3
            for x in range(hurt_animation):
                temp_list.append(self.hurt_sprite.get_image(x, CYAN))
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (360, 380)
            self.image2 = self.animation_list2[self.action2][self.frame_index2]
            self.rect2 = self.image2.get_rect()
            self.rect2.center = (900, 380)

            self.skill = {
                "R": 1,
                "P": 1,
                "S": 1
            }

            self.skillPower = {
                "R": 50,
                "P": 50,
                "S": 50
            }

            self.abilityName = "Dagger Flurry"

            self.ability = {
                "A": 1
            }

            self.abilityPower = {
                "A": 100
            }

            self.abilityCD = {
                "A": 7
            }

            self.healName = "Regenerate"

            self.heal = {
                "A": 1
            }

            self.healPower = {
                "A": 100
            }

            self.healCD = {
                "A": 5
            }

            self.hitName = "Throw"

            self.hit = {
                "A": 1
            }

            self.hitPower = {
                "A": 50
            }

            self.hitCD = {
                "A": 3
            }

    # Draws Player 1 selected character
    def draw1(self):
        screen.blit(self.image, self.rect)

    # Draws Player 2 selected character mirrored in position
    def draw2(self):
        screen.blit(pygame.transform.flip(self.image2.convert_alpha(), True, False), self.rect2)

    # Manages animation of Player 1's character
    def update1(self):
        animation_cooldown = 75
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 6:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.isHurt = True
            elif self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.hasGuard = True
            else:
                self.idle1()
        if self.isHurt or self.hasGuard:
            self.delay += 1
        if self.delay >= 40 and self.isHurt:
            self.isHurt = False
            self.delay = 0
            self.idle1()
        if self.delay >= 40 and self.hasGuard:
            self.hasGuard = False
            self.delay = 0
            self.idle1()

    # Manages animation of Player 2's character
    def update2(self):
        animation_cooldown2 = 75
        # Update image
        self.image2 = self.animation_list2[self.action2][self.frame_index2]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time2 > animation_cooldown2:
            self.update_time2 = pygame.time.get_ticks()
            self.frame_index2 += 1
        # If the animation has run out then reset back to the start
        if self.frame_index2 >= len(self.animation_list2[self.action2]):
            if self.action2 == 6:
                self.frame_index2 = len(self.animation_list2[self.action2]) - 1
                self.isHurt2 = True
            elif self.action2 == 5:
                self.frame_index2 = len(self.animation_list2[self.action2]) - 1
                self.hasGuard2 = True
            else:
                self.idle2()
        if self.isHurt2 or self.hasGuard2:
            self.delay2 += 1
        if self.delay2 >= 40 and self.isHurt2:
            self.isHurt2 = False
            self.delay2 = 0
            self.idle2()
        if self.delay2 >= 40 and self.hasGuard2:
            self.hasGuard2 = False
            self.delay2 = 0
            self.idle2()

    def idle1(self):
        # Set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def ability1(self, target):
        # Enemy hurt
        ability_sfx.play()
        target.hurt2()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to ability animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack1(self, target):
        # Enemy hurt
        target.hurt2()
        normal_damage_sfx.play()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to attack animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def atkguard1(self, target):
        # Enemy guard
        target.guard2()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def abilityguard1(self, target):
        # Enemy ability guard
        target.guard2()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def skill1(self, target):
        # Enemy hurt
        target.hurt2()
        normal_damage_sfx.play()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to skill animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def heal1(self):
        # Set variables to heal animation
        heal_sfx.play()
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def guard1(self):
        # Set variables to guard animation
        guard_sfx.play()
        self.action = 5
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt1(self):
        # Set variables to hurt animation
        self.action = 6
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def idle2(self):
        # Set variables to idle animation
        self.action2 = 0
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def ability2(self, target):
        # Enemy hurt
        ability_sfx.play()
        target.hurt1()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to ability animation
        self.action2 = 1
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def attack2(self, target):
        # Enemy hurt
        target.hurt1()
        normal_damage_sfx.play()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to attack animation
        self.action2 = 2
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def atkguard2(self, target):
        # Enemy ability guard
        target.guard1()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        self.action2 = 2
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def abilityguard2(self, target):
        # Enemy ability guard
        target.guard1()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        self.action2 = 1
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def skill2(self, target):
        # Enemy hurt
        target.hurt1()
        normal_damage_sfx.play()
        # Check if target has died
        if target.baseHealth < 1:
            target.baseHealth = 0
        # Set variables to skill animation
        self.action2 = 3
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def heal2(self):
        # Set variables to heal animation
        heal_sfx.play()
        self.action2 = 4
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def guard2(self):
        # Set variables to guard animation
        guard_sfx.play()
        self.action2 = 5
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

    def hurt2(self):
        # Set variables to hurt animation
        self.action2 = 6
        self.frame_index2 = 0
        self.update_time2 = pygame.time.get_ticks()

# Menu Buttons
play_button = SelectionButton(455, 250, play_image, 503, 221)
quit_button = SelectionButton(455, 420, quit_image, 500, 220)
pvp_button = SelectionButton(375, 230, pvp_image, 750, 220)
ai_button = SelectionButton(375, 400, ai_image, 750, 220)
yes_button = SelectionButton(465, 250, yes_image, 503, 221)
no_button = SelectionButton(465, 420, no_image, 500, 220)

# Rock, Paper, Scissors Buttons
rock_button = RPSButtons(250, 260, rock_image)
paper_button = RPSButtons(525, 260, paper_image)
scissors_button = RPSButtons(800, 260, scissors_image)

# Ready Button
ready_button = Ready(360, 250, ready_image)

# Buttons of each characters' abilities and Cancel button
swordsman_ability = AbilityButton(380, 260, swordsman_ability_img)
mage_ability = AbilityButton(380, 260, mage_ability_img)
rouge_ability = AbilityButton(380, 260, rouge_ability_img)
cancel_ability = AbilityButton(715, 260, cancel_ability_img)

# Character Portrait Buttons
swordsman_portrait = RPSButtons(50, 220, select_swordsman)
mage_portrait = RPSButtons(460, 220, select_mage)
rouge_portrait = RPSButtons(900, 220, select_rouge)

# Player 1 Fighter selection
def p1_fighter():
    if swordsman_portrait.draw():
        opt_select_sfx.play()
        PlayerOneChoice = "A"
        return PlayerOneChoice
    if mage_portrait.draw():
        opt_select_sfx.play()
        PlayerOneChoice = "B"
        return PlayerOneChoice
    if rouge_portrait.draw():
        opt_select_sfx.play()
        PlayerOneChoice = "C"
        return PlayerOneChoice

# Player 2 Fighter selection
def p2_fighter():
    if swordsman_portrait.draw():
        opt_select_sfx.play()
        PlayerTwoChoice = "A"
        return PlayerTwoChoice
    if mage_portrait.draw():
        opt_select_sfx.play()
        PlayerTwoChoice = "B"
        return PlayerTwoChoice
    if rouge_portrait.draw():
        opt_select_sfx.play()
        PlayerTwoChoice = "C"
        return PlayerTwoChoice

# CPU Fighter selection
def cpu_fighter():
    choices = ['A', 'B', 'C']
    playerTwoChoice = random.choice(choices)
    return playerTwoChoice

# Function made as a base for drawing game texts
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function made as a base for drawing game texts (centered only)
def draw_text2(text, font, text_col, y):
    text = font.render(text, True, text_col)
    text_rect = text.get_rect(center=((screen_width / 2) - 20, y))
    screen.blit(text, text_rect)

# Function made as a base for drawing game texts (turn count only)
def draw_text3(text, font, text_col, y):
    text = font.render(text, True, text_col)
    text_rect = text.get_rect(center=((screen_width / 2), y))
    screen.blit(text, text_rect)

# Function for drawing background
def draw_bg():
    screen.blit(background_image, (0, 0))

# Function for drawing game title image
def draw_logo():
    screen.blit(logo_rps, (365, 5))

# Draws a darker contrast of the background
def draw_dark_bg():
    dark_bg = background_image.copy()
    dark_bg.set_alpha(170)
    dark_bg.fill((0, 0, 0))
    screen.blit(dark_bg, (0, 0))

def draw_choice_result():
    draw_text(f'Player 1 Chose', font_titles, white, 130, 150)
    draw_text(f'Player 2 Chose', font_titles, white, 865, 150)

# Draws Game HUD
def draw_hud():
    screen.blit(full_hud_image, (0, 0))
    screen.blit(hp_image, (10, 75))
    screen.blit(pygame.transform.flip(hp_image, True, False), (745, 75))

# Draws Title Text
def draw_title_screen():
    draw_text2(f'Pixel RPS', font_game_title, white, 150)

# Draws Game Mode Text
def draw_gamemode_screen():
    draw_text2(f'Select Game Mode', font_game_title, white, 110)

# Draws Fighter Selection Text for Player 1
def draw_fighter_screen():
    draw_text2(f'Select Fighter Player 1', font_game_title, white, 110)

# Draws Fighter Selection Text for Player 2
def draw_fighter_screen2():
    draw_text2(f'Select Fighter Player 2', font_game_title, white, 110)

# Draws "Continue ?" at the battle results
def draw_restart_screen1():
    draw_text2(f'Continue?', font_titles, white, 200)

# Draws play button
def play():
    if play_button.draw_play():
        opt_select_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws quit button
def quit():
    if quit_button.draw_play():
        opt_select_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws PvP button
def pvp():
    if pvp_button.draw_play():
        opt_select_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws PvAI button
def ai():
    if ai_button.draw_play():
        opt_select_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws Yes button
def yes():
    if yes_button.draw_play():
        opt_select_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws No Button
def no():
    if no_button.draw_play():
        cancel_sfx.play()
        confirm = 1
        return confirm
    else:
        confirm = 0
        return confirm

# Draws a "Player 1 Ready?" text
def draw_ask_ready1():
    draw_text2(f'Player 1 Ready?', font_titles, white, 200)

# Draws a "Player 2 Ready?" text
def draw_ask_ready2():
    draw_text2(f'Player 2 Ready?', font_titles, white, 200)

# Draws a "Player 1 Wins!" text
def draw_victory1():
    draw_text2(f'Player 1 Wins!', font_titles, white, 200)

# Draws a "Player 2 Wins!" text
def draw_victory2():
    draw_text2(f'Player 2 Wins!', font_titles, white, 200)

# Draws a "Tie!" text
def draw_tie():
    draw_text2(f'Tie!', font_titles, white, 200)

# Makes GameState class methods callable
game_state = GameState()

# Pygame game loop
gameIsRunning = True
while gameIsRunning:

    clock.tick(fps)
    # Calls game_manager method from GameState
    game_state.game_manager()

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameIsRunning = False

    pygame.display.update()

pygame.quit()