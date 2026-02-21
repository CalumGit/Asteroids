import pygame
import random
import json
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Screen:
    def update(self, surface):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass


class Button:
    def __init__(self, text, x, y, width, height, font_size=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.hovered = False

    def draw(self, surface):
        colour = "yellow" if self.hovered else "white"
        pygame.draw.rect(surface, colour, self.rect, 2)
        text_surface = self.font.render(self.text, True, colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Menu(Screen):
    def __init__(self):
        self.buttons = [
            Button("Start", SCREEN_WIDTH//2 - 100, 200, 200, 50),
            Button("High Scores", SCREEN_WIDTH//2 - 100, 270, 200, 50),
            Button("Settings", SCREEN_WIDTH//2 - 100, 340, 200, 50),
            Button("Exit", SCREEN_WIDTH//2 - 100, 410, 200, 50)
        ]
        self.next_state = "menu"

        self.stars = [pygame.Vector2(random.randint(0, SCREEN_WIDTH),
                                     random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]


    def update(self, surface):
        for star in self.stars:
            star.y += 50 * 0.016
            if star.y > SCREEN_HEIGHT:
                star.y = 0
                star.x = random.randint(0, SCREEN_WIDTH)

        self.draw(surface)
        return self.next_state


    def handle_event(self, event):
        for i, button in enumerate(self.buttons):
            if button.handle_event(event):
                if i == 0:
                    self.next_state = "game"
                if i == 1:
                    self.next_state = "highscores"
                if i == 2:
                    self.next_state = "settings"
                if i == 3:
                    self.next_state = "exit"


    def draw(self, surface):
        surface.fill("black")
        for star in self.stars:
            pygame.draw.circle(surface, "white", star, 2)

        font = pygame.font.SysFont(None, 80)
        title_surface = font.render("ASTEROIDS", True, "white")
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(title_surface, title_rect)

        for button in self.buttons:
            button.draw(surface)


# --- High Scores Screen ---
class HighScoreScreen(Screen):
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()
        self.back_button = Button("Back", SCREEN_WIDTH//2 - 100, 500, 200, 50)
        self.next_state = "highscores"

    def load_scores(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f)

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.next_state = "menu"

    def update(self, surface):
        self.draw(surface)
        return self.next_state

    def draw(self, surface):
        surface.fill("black")
        font = pygame.font.SysFont(None, 60)
        title = font.render("HIGH SCORES", True, "white")
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        font = pygame.font.SysFont(None, 40)
        for i, score in enumerate(sorted(self.scores, reverse=True)[:10]):
            text = font.render(f"{i+1}. {score}", True, "white")
            surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*40))

        self.back_button.draw(surface)

# --- Settings Screen ---
class SettingsScreen(Screen):
    def __init__(self):
        self.back_button = Button("Back", SCREEN_WIDTH//2 - 100, 500, 200, 50)
        self.next_state = "settings"

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.next_state = "menu"

    def update(self, surface):
        self.draw(surface)
        return self.next_state

    def draw(self, surface):
        surface.fill("black")
        font = pygame.font.SysFont(None, 60)
        title = font.render("SETTINGS", True, "white")
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        # Example placeholder text
        font = pygame.font.SysFont(None, 40)
        text = font.render("Volume / Controls / etc.", True, "white")
        surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200))

        self.back_button.draw(surface)
