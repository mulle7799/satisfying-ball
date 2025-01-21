import pygame
import random
import math
import tkinter as tk
from tkinter import filedialog
import pygame_gui
import os

# Initialize Pygame modules
pygame.init()
pygame.mixer.init()

# --- Window Setup ---
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

# --- Ball Parameters ---
ball_radius = 15 # Initial radius of the ball
gravity = 0.08 # Gravity applied to the ball
damping = 0.92 # Speed reduction after collision
bounce_strength = 4 # Strength of the bounce effect
speed_multiplier = 2 # Multiplier for speed changes
fps = 60 # Frames per second
initial_ball_speed = 2 # Default starting speed of the ball
initial_ball_radius = 15  # Default ball radius
min_ball_speed = 1  # Minimum speed of the ball

# --- Circular Space Parameters ---
center_x = width // 2  # X-coordinate of the circle's center
center_y = height // 2  # Y-coordinate of the circle's center
radius = 250 # Radius of the circle
initial_radius = radius # Storing initial circle radius
shrink_speed = 1.5 # How fast circle shrinks
return_radius = 15 # Return speed of radius

pulse_radius = radius  # Initial radius for pulse effect
pulse_alpha = 0  # Initial transparency of pulse
pulse_speed = 2  # Speed of pulse expansion
pulse_fade_speed = 4  # Speed of pulse fading
pulse_active = False  # Whether pulse effect is active
pulse_color = (200, 200, 200) # Color of the pulse

# --- Settings ---
enable_color_change = True # Enables ball color change
enable_pulse = False # Enables pulse effect on collisions
sound_volume = 1.0 # Initial sound volume
current_ball_radius = initial_ball_radius  # Current ball radius
current_ball_speed = initial_ball_speed # Current ball speed
game_mode = "classic" # Default game mode
mode_menu_open = False # Is mode menu open?

# --- Functions ---
# Function to generate random colors
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Ball class
class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

# Initial ball setup
ball = Ball(width // 2, height // 2, current_ball_radius, get_random_color(),
            random.uniform(-3, 3) * current_ball_speed, random.uniform(-3, 3) * current_ball_speed)

# Sound Setup
collision_sound = None

# Sound loading function
def load_sound():
    global collision_sound
    root = tk.Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(title="Select sound file",
                                           filetypes=(("Audio Files", "*.wav *.mp3"),
                                                      ("all files", "*.*")))  # Show file selection dialog
    if file_path:
        try:
            collision_sound = pygame.mixer.Sound(file_path) # Load the sound
            print("Sound Loaded Successfully")
        except pygame.error as e:
            print(f"Error loading sound {file_path}: {e}")
    else:
        print("No sound file selected.")

# Button Class for simple UI elements
class Button:
    def __init__(self, rect, text, font, action, color=(200, 200, 200)):
        self.rect = rect
        self.text = text
        self.font = font
        self.action = action
        self.color = color  # Regular state color
        self.hover_color = (150, 150, 150)  # Hover state color
        self.text_color = (255, 255, 255)  # Text color

    def draw(self, screen):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10) # Rounded corners
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Settings Menu class
class SettingsMenu:
    def __init__(self, game, ui_manager):
        self.game = game
        self.font = pygame.font.Font(None, 20) # Reduced font size
        self.manager = ui_manager
        self.buttons = {
            "Change Sound": Button(pygame.Rect(20, 80, 150, 40), "Change Sound", self.font, lambda: load_sound()),
            "Toggle Color Change": Button(pygame.Rect(20, 130, 150, 40), "Toggle Color Change", self.font,
                                          lambda: self.toggle_color()),
            "Toggle Pulse Effect": Button(pygame.Rect(20, 180, 150, 40), "Toggle Pulse Effect", self.font,
                                          lambda: self.toggle_pulse()),
            "Reset Settings": Button(pygame.Rect(20, 450, 150, 40), "Reset Settings", self.font,
                                     lambda: self.reset_settings()),
            "Back": Button(pygame.Rect(20, 500, 150, 40), "Back", self.font, lambda: self.game.set_menu_state(False)),
        }
        button_width = 150
        slider_x = width // 2 + 50
        slider_width = 200
        label_x_offset = 5
        label_y_offset = 5

        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(slider_x, 280, slider_width, 30),
                                                                    start_value=sound_volume,
                                                                    value_range=(0.0, 1.0),
                                                                    manager=self.manager)
        self.ball_size_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(slider_x, 330, slider_width, 30),
                                                                       start_value=current_ball_radius,
                                                                       value_range=(5.0, 30.0),
                                                                       manager=self.manager)
        self.ball_speed_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(slider_x, 380, slider_width, 30),
                                                                        start_value=current_ball_speed,
                                                                        value_range=(0.5, 5.0),
                                                                        manager=self.manager)
        self.fps_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect(slider_x, 430, slider_width, 30),
                                                                 start_value=fps,
                                                                 value_range=(30, 120),
                                                                 manager=self.manager)

        # Creating text labels
        self.label_volume = self.font.render("Effect Volume", True, (255, 255, 255))
        self.label_ball_size = self.font.render("Ball Size", True, (255, 255, 255))
        self.label_ball_speed = self.font.render("Ball Speed", True, (255, 255, 255))
        self.label_fps = self.font.render("FPS", True, (255, 255, 255))
        self.labels = {
            self.volume_slider: self.label_volume,
            self.ball_size_slider: self.label_ball_size,
            self.ball_speed_slider: self.label_ball_speed,
            self.fps_slider: self.label_fps
        }

    # Reset all settings to default
    def reset_settings(self):
        global sound_volume, current_ball_radius, current_ball_speed, enable_color_change, enable_pulse, game_mode, fps, radius
        enable_color_change = True
        enable_pulse = False
        sound_volume = 1.0
        current_ball_radius = initial_ball_radius
        current_ball_speed = initial_ball_speed
        game_mode = "classic"
        fps = 60
        radius = initial_radius
        self.volume_slider.set_current_value(sound_volume)
        self.ball_size_slider.set_current_value(current_ball_radius)
        self.ball_speed_slider.set_current_value(current_ball_speed)
        self.fps_slider.set_current_value(fps)
        self.game.update_ball() # Update ball settings

    def toggle_color(self):
        global enable_color_change
        enable_color_change = not enable_color_change

    def toggle_pulse(self):
        global enable_pulse
        enable_pulse = not enable_pulse

    def draw(self):
        screen.fill((50, 50, 50))
        for button in self.buttons.values():
            button.draw(screen)
        # Draw text labels
        for slider, label in self.labels.items():
            text_rect = label.get_rect(center=slider.rect.center)
            text_rect.x = slider.rect.left - label.get_width() - 10  # Set x with offset
            screen.blit(label, text_rect)

    def handle_input(self, event):
        for button in self.buttons.values():
            button.handle_input(event)


# Game Class
class Game:
    def __init__(self):
        self.in_settings = False
        self.ui_manager = pygame_gui.UIManager((width, height))
        self.settings_menu = SettingsMenu(self, self.ui_manager)
        self.menu_font = pygame.font.Font(None, 30)
        self.menu_button = Button(pygame.Rect(10, 10, 100, 30), "Settings", self.menu_font,
                                  lambda: self.set_menu_state(True))
        self.mode_font = pygame.font.Font(None, 24)
        self.mode_button = Button(pygame.Rect(120, 10, 100, 30), "Modes", self.menu_font,
                                  lambda: self.toggle_mode_menu())
        self.mode_buttons = {
            "classic": Button(pygame.Rect(120, 50, 100, 40), "Classic", self.mode_font,
                              lambda: self.switch_mode("classic"), color=(150, 150, 150)),
            "paint_map": Button(pygame.Rect(120, 100, 100, 40), "Paint Map", self.mode_font,
                                lambda: self.switch_mode("paint_map"), color=(150, 150, 150)),
            "duplication": Button(pygame.Rect(120, 150, 100, 40), "Duplication", self.mode_font,
                                  lambda: self.switch_mode("duplication"), color=(150, 150, 150)),
            "merge": Button(pygame.Rect(120, 200, 100, 40), "Merge", self.mode_font, lambda: self.switch_mode("merge"),
                            color=(150, 150, 150)),
            "shrinking_space": Button(pygame.Rect(120, 250, 100, 40), "Shrink", self.mode_font,
                                      lambda: self.switch_mode("shrinking_space"), color=(150, 150, 150))
        }

    def toggle_mode_menu(self):
        global mode_menu_open
        mode_menu_open = not mode_menu_open

    def switch_mode(self, new_mode):
        global game_mode, mode_menu_open, balls, radius
        game_mode = new_mode
        radius = initial_radius  # Reset radius for new mode
        if game_mode == "paint_map":
            global paint_map_surface, paint_map_color
            paint_map_surface = pygame.Surface((width, height), pygame.SRCALPHA) # Create surface for painting
            paint_map_color = (0, 0, 0, 0) # Transparent color
        elif game_mode == "merge":
            balls = [Ball(width // 2, height // 2, current_ball_radius, get_random_color(),
                          random.uniform(-3, 3) * current_ball_speed, random.uniform(-3, 3) * current_ball_speed)
                , Ball(width // 2 - 50, height // 2 - 50, current_ball_radius, get_random_color(),
                       random.uniform(-3, 3) * current_ball_speed, random.uniform(-3, 3) * current_ball_speed)]
        else:
            balls = [Ball(width // 2, height // 2, current_ball_radius, get_random_color(),
                          random.uniform(-3, 3) * current_ball_speed, random.uniform(-3, 3) * current_ball_speed)]
        mode_menu_open = False # Close menu after selection

    def set_menu_state(self, state):
        self.in_settings = state

    def handle_menu_input(self, event):
        self.menu_button.handle_input(event)

    def draw_menu_button(self):
        self.menu_button.draw(screen)

    def draw_mode_button(self):
        self.mode_button.draw(screen)

    def draw_mode_buttons(self):
        if mode_menu_open:
            for button in self.mode_buttons.values():
                button.draw(screen)

    def handle_mode_input(self, event):
        if not self.in_settings:  # If not in the settings menu
            self.mode_button.handle_input(event)
            if mode_menu_open:
                for button in self.mode_buttons.values():
                    button.handle_input(event)

    def update_ball(self):
        global ball, current_ball_radius, current_ball_speed
        current_ball_radius = self.settings_menu.ball_size_slider.get_current_value()
        current_ball_speed = self.settings_menu.ball_speed_slider.get_current_value()
        ball = Ball(width // 2, height // 2, current_ball_radius, ball.color,
                    random.uniform(-3, 3) * current_ball_speed, random.uniform(-3, 3) * current_ball_speed)

# Initialize game
game = Game()
paint_map_surface = None
paint_map_color = None
balls = [ball]
clock = pygame.time.Clock()

# --- Main Game Loop ---
running = True
while running:
    time_delta = clock.tick(fps) / 1000.0  # delta time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game.in_settings:
            game.handle_menu_input(event)
            game.handle_mode_input(event)
        else:
            game.settings_menu.handle_input(event)
            game.settings_menu.manager.process_events(event) # pass event to gui manager

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == game.settings_menu.volume_slider:
                sound_volume = game.settings_menu.volume_slider.get_current_value()
            elif event.ui_element == game.settings_menu.ball_size_slider:
                game.update_ball() # update size
            elif event.ui_element == game.settings_menu.ball_speed_slider:
                game.update_ball()  # update speed
            elif event.ui_element == game.settings_menu.fps_slider:
                fps = int(game.settings_menu.fps_slider.get_current_value())
                clock = pygame.time.Clock()  # update clock if fps changed

    if not game.in_settings:
        # Clear screen
        screen.fill((0, 0, 0))

        # Draw circle
        pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), int(radius), width=1)

        # Shrinking space game mode
        if game_mode == "shrinking_space":
            # Shrink the radius
            radius -= shrink_speed
            if radius < ball.radius:
                radius = ball.radius

            # Ball movement logic
            ball.speed_y += gravity
            ball.x += ball.speed_x
            ball.y += ball.speed_y

            # Check for collision with the circle
            dist_from_center = math.sqrt((ball.x - center_x) ** 2 + (ball.y - center_y) ** 2)
            if dist_from_center > radius - ball.radius:
                # Change color on collision
                if enable_color_change:
                    ball.color = get_random_color()

                # Calculate normal vector at the point of collision
                nx = (ball.x - center_x) / dist_from_center
                ny = (ball.y - center_y) / dist_from_center

                # Calculate reflected speed
                dot_prod = ball.speed_x * nx + ball.speed_y * ny
                ball.speed_x -= 2 * dot_prod * nx
                ball.speed_y -= 2 * dot_prod * ny

                # Add a bounce effect
                ball.speed_y -= bounce_strength

                ball.speed_x *= damping
                ball.speed_y *= damping

                # Correct ball position to prevent clipping
                ball.x = center_x + (radius - ball.radius) * nx
                ball.y = center_y + (radius - ball.radius) * ny

                # Increase circle radius
                radius = min(radius + return_radius, initial_radius)
                # Activate pulse on collision
                if enable_pulse:
                    pulse_radius = radius
                    pulse_alpha = 255
                    pulse_active = True
                # Play collision sound if loaded
                if collision_sound:
                    collision_sound.set_volume(sound_volume)
                    collision_sound.play()

            # Keep speed above minimum
            if math.sqrt(ball.speed_x ** 2 + ball.speed_y ** 2) < min_ball_speed:
                ball.speed_x = random.uniform(-1, 1) * min_ball_speed
                ball.speed_y = random.uniform(-1, 1) * min_ball_speed
            # Slight speed changes on each collision
            if dist_from_center > radius - ball.radius:
                ball.speed_x += random.uniform(-0.5, 0.5) * current_ball_speed
                ball.speed_y += random.uniform(-0.5, 0.5) * current_ball_speed
            # Draw the ball
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))

        # Merge mode logic
        elif game_mode == "merge":
            i = 0
            while i < len(balls):
                ball = balls[i]
                # Ball movement logic
                ball.speed_y += gravity
                ball.x += ball.speed_x
                ball.y += ball.speed_y
                # Collision check with the circle
                dist_from_center = math.sqrt((ball.x - center_x) ** 2 + (ball.y - center_y) ** 2)
                if dist_from_center > radius - ball.radius:
                    # Color change on collision
                    if enable_color_change:
                        ball.color = get_random_color()

                    # Calculate normal vector at point of collision
                    nx = (ball.x - center_x) / dist_from_center
                    ny = (ball.y - center_y) / dist_from_center

                    # Calculate reflected speed
                    dot_prod = ball.speed_x * nx + ball.speed_y * ny
                    ball.speed_x -= 2 * dot_prod * nx
                    ball.speed_y -= 2 * dot_prod * ny

                    # Add a bounce effect
                    ball.speed_y -= bounce_strength

                    ball.speed_x *= damping
                    ball.speed_y *= damping

                    # Correct ball position to prevent clipping
                    ball.x = center_x + (radius - ball.radius) * nx
                    ball.y = center_y + (radius - ball.radius) * ny

                    # Activate pulse on collision
                    if enable_pulse:
                        pulse_radius = radius
                        pulse_alpha = 255
                        pulse_active = True
                    # Play collision sound if loaded
                    if collision_sound:
                        collision_sound.set_volume(sound_volume)
                        collision_sound.play()
                # Collision check with other balls
                j = i + 1
                while j < len(balls):
                    other_ball = balls[j]
                    dist = math.sqrt((ball.x - other_ball.x) ** 2 + (ball.y - other_ball.y) ** 2)
                    if dist < ball.radius + other_ball.radius:
                        new_radius = math.sqrt(ball.radius ** 2 + other_ball.radius ** 2)
                        new_speed_x = (ball.speed_x + other_ball.speed_x) / 2
                        new_speed_y = (ball.speed_y + other_ball.speed_y) / 2
                        balls[i] = Ball(ball.x, ball.y, new_radius, get_random_color(), new_speed_x,
                                        new_speed_y)  # Replacing the current ball
                        balls.pop(j)
                        balls.append(Ball(width // 2, height // 2, current_ball_radius, get_random_color(),
                                          random.uniform(-3, 3) * current_ball_speed,
                                          random.uniform(-3, 3) * current_ball_speed)) # spawn in center
                        break
                    j += 1
                # Keep speed above minimum
                if math.sqrt(ball.speed_x ** 2 + ball.speed_y ** 2) < min_ball_speed:
                    ball.speed_x = random.uniform(-1, 1) * min_ball_speed
                    ball.speed_y = random.uniform(-1, 1) * min_ball_speed
                # Slight speed changes on each collision
                if dist_from_center > radius - ball.radius:
                    ball.speed_x += random.uniform(-0.5, 0.5) * current_ball_speed
                    ball.speed_y += random.uniform(-0.5, 0.5) * current_ball_speed
                pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))
                i += 1
        # Duplication mode
        elif game_mode == "duplication":
            for i, ball in enumerate(balls):
                # Ball movement logic
                ball.speed_y += gravity
                ball.x += ball.speed_x
                ball.y += ball.speed_y
                # Check collision with the circle
                dist_from_center = math.sqrt((ball.x - center_x) ** 2 + (ball.y - center_y) ** 2)
                if dist_from_center > radius - ball.radius:
                    # Change color on collision
                    if enable_color_change:
                        ball.color = get_random_color()

                    # Calculate normal vector at the collision point
                    nx = (ball.x - center_x) / dist_from_center
                    ny = (ball.y - center_y) / dist_from_center

                    # Calculate reflected speed
                    dot_prod = ball.speed_x * nx + ball.speed_y * ny
                    ball.speed_x -= 2 * dot_prod * nx
                    ball.speed_y -= 2 * dot_prod * ny

                    # Add a bounce effect
                    ball.speed_y -= bounce_strength

                    ball.speed_x *= damping
                    ball.speed_y *= damping

                    # Correct ball position to avoid clipping
                    ball.x = center_x + (radius - ball.radius) * nx
                    ball.y = center_y + (radius - ball.radius) * ny

                    # Check collision with other balls
                    collision = False
                    for j, other_ball in enumerate(balls):
                         if i != j: # Check if the ball collided with other ball
                             dist = math.sqrt((ball.x - other_ball.x) ** 2 + (ball.y - other_ball.y) ** 2)
                             if dist < ball.radius + other_ball.radius:
                                 collision = True
                                 break
                    if not collision: # duplicate ball if no collision
                        new_speed_x = random.uniform(-3, 3) * current_ball_speed
                        new_speed_y = random.uniform(-3, 3) * current_ball_speed
                        new_ball = Ball(ball.x, ball.y, ball.radius, get_random_color(), new_speed_x, new_speed_y)
                        balls.append(new_ball)
                    # Activate pulse effect on collision
                    if enable_pulse:
                        pulse_radius = radius
                        pulse_alpha = 255
                        pulse_active = True
                    # Play collision sound
                    if collision_sound:
                        collision_sound.set_volume(sound_volume)
                        collision_sound.play()
                # Keep speed above minimum
                if math.sqrt(ball.speed_x ** 2 + ball.speed_y ** 2) < min_ball_speed:
                    ball.speed_x = random.uniform(-1, 1) * min_ball_speed
                    ball.speed_y = random.uniform(-1, 1) * min_ball_speed
                # Add speed changes after collision
                if dist_from_center > radius - ball.radius:
                    ball.speed_x += random.uniform(-0.5, 0.5) * current_ball_speed
                    ball.speed_y += random.uniform(-0.5, 0.5) * current_ball_speed

                pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))
                # Remove small balls
                if ball.radius < 3:
                   balls.pop(i)
                   continue
        # Classic mode
        else:
            # Ball movement logic
            ball.speed_y += gravity
            ball.x += ball.speed_x
            ball.y += ball.speed_y
            # Check collision with the circle
            dist_from_center = math.sqrt((ball.x - center_x) ** 2 + (ball.y - center_y) ** 2)
            if dist_from_center > radius - ball.radius:
                # Change color on collision
                if enable_color_change:
                    ball.color = get_random_color()

                # Calculate normal vector
                nx = (ball.x - center_x) / dist_from_center
                ny = (ball.y - center_y) / dist_from_center

                # Calculate reflected speed
                dot_prod = ball.speed_x * nx + ball.speed_y * ny
                ball.speed_x -= 2 * dot_prod * nx
                ball.speed_y -= 2 * dot_prod * ny

                # Add bounce effect
                ball.speed_y -= bounce_strength

                ball.speed_x *= damping
                ball.speed_y *= damping

                # Correct ball position
                ball.x = center_x + (radius - ball.radius) * nx
                ball.y = center_y + (radius - ball.radius) * ny

                # Activate pulse on collision
                if enable_pulse:
                    pulse_radius = radius
                    pulse_alpha = 255
                    pulse_active = True

                # Play sound on collision
                if collision_sound:
                    collision_sound.set_volume(sound_volume)
                    collision_sound.play()

            # Draw the ball
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))

        # Draw pulse effect
        if pulse_active:
            pulse_surface = pygame.Surface((width, height), pygame.SRCALPHA) # transparent surface
            pygame.draw.circle(pulse_surface, (*pulse_color, pulse_alpha), (center_x, center_y), int(pulse_radius))
            screen.blit(pulse_surface, (0, 0))

            pulse_radius += pulse_speed  # increase pulse radius
            pulse_alpha -= pulse_fade_speed # reduce transparency

            if pulse_alpha <= 0:  # deactivate pulse
                pulse_active = False

        if game_mode == "paint_map" and paint_map_surface is not None:
            # Paint the circle in paint map mode
            pygame.draw.circle(paint_map_surface, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))
            screen.blit(paint_map_surface, (0, 0))

        # Draw the game menus
        game.draw_menu_button()
        game.draw_mode_button()
        game.draw_mode_buttons()
    else:
        screen.fill((50, 50, 50)) # set background color
        game.settings_menu.draw()
        game.settings_menu.manager.update(time_delta)
        game.settings_menu.manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()

    # Frame delay
    # pygame.time.delay(1000 // fps)

pygame.quit()
