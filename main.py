import pygame
import sys
import ui
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot

#Define States
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_HIGHSCORES = "highscores"
STATE_SETTINGS = "settings"
STATE_EXIT = "exit"

def main():
#Print startup info for debugging
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

#Initialises all imported pygame modules
    pygame.init()

#Creates a clock to control frame rate
    clock = pygame.time.Clock()
    dt = 0

#Initialises score and font for rendering score text
    score = 0
    font = pygame.font.SysFont(None, 36)

#Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Sprite group
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

#Player
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

#Asteroids
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

#Asteroid Field
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()

#Shots
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

#Game loop
    running = True
    game_state = STATE_MENU
    menu = ui.Menu()
    highscores = ui.HighScoreScreen()
    settings = ui.SettingsScreen()

    while running:
    #Cap game at 60FPS and calculate delta time
        dt = clock.tick(60) / 1000

    #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #State Handling
            if game_state == STATE_MENU:
                menu.handle_event(event)
            elif game_state == STATE_GAME:
                player.handle_event(event)

        if game_state == STATE_MENU:
            game_state = menu.update(screen)
        elif game_state == STATE_HIGHSCORES:
            game_state = highscores.update(screen)
        elif game_state == STATE_SETTINGS:
            game_state = settings.update(screen)
        elif game_state == STATE_GAME:
        #Update all objects
            updatable.update(dt)
            log_state()

        #Collision: player and asteroids
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    print("Game over!")
                    running = False

        #Collision: shots and asteroids
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                    #Score based on asteroid size
                        if asteroid.radius > 40:
                            score += 20
                        elif asteroid.radius > 20:
                            score += 50
                        else:
                            score += 100
                    #asteroid split and destruction
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()

    #Render everything
        screen.fill("black")
        if game_state == STATE_MENU:
            menu.draw(screen)
        elif game_state == STATE_GAME:
            for obj in drawable:
                obj.draw(screen)
        #Displays Score
            score_surface = font.render(f"Score: {score}", True, "white")
            screen.blit(score_surface, (10, 10))

    #Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
