from config import *
from assets import Firework

from main import ImageCapture

trails = []
fade_p = []

def update(win: pygame.Surface, fireworks: list, trails: list):
    if TRAILS:
        for t in trails:
            t.show(win)
            if t.decay():
                trails.remove(t)
                
    for fw in fireworks:
        fw.update(win)
        if fw.remove():
            fireworks.remove(fw)
    pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Fireworks in Pygame")
    win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT - 150))
    clock = pygame.time.Clock()

    fireworks = []  # create the first fireworks
    
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, (win.get_width(), 600))

    running = True

    while running:
        clock.tick(60)
        imageCapture = ImageCapture()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Meow") 
                    fireworks.append(Firework(position = vector2(pygame.mouse.get_pos()[0], DISPLAY_HEIGHT), particle_type = ["defaultspread"]))
                    
                if event.key == pygame.K_2:
                    fireworks.append(Firework(position = vector2(pygame.mouse.get_pos()[0], DISPLAY_HEIGHT), particle_type = ["circle"]))
                    
                if event.key == pygame.K_3:
                    fireworks.append(Firework(position = vector2(pygame.mouse.get_pos()[0], DISPLAY_HEIGHT), particle_type = ["heart"]))
                    
                elif event.key == pygame.K_4:
                    fireworks.append(Firework(position = vector2(120, DISPLAY_HEIGHT), particle_type = ["heart_5_45", "defaultspread"]))
                    fireworks.append(Firework(position = vector2(690, DISPLAY_HEIGHT), particle_type = ["heart_3_-45", "defaultspread"]))
                    fireworks.append(Firework(position = vector2(120 + 50, DISPLAY_HEIGHT), particle_type = ["heart_3_45"]))
                    fireworks.append(Firework(position = vector2(690 - 50, DISPLAY_HEIGHT), particle_type = ["heart_3_-45"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))
                    fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = ["circle"]))

        win.fill(BACKGROUND_COLOR)  # draw background
        win.blit(bg, (0, 0))

        if randint(0, 70) == 1:  # create new firework
            fireworks.append(Firework(position = vector2(randint(150, DISPLAY_WIDTH - 150), DISPLAY_HEIGHT), particle_type = [choice(["defaultspread", "default", "circle"])]))
        
        
        update(win, fireworks, trails)
        
        
        # print(imageCapture._is_match_found())

        # stats for fun
        # total_particles = 0
        # for f in fireworks:
        #    total_particles += len(f.particles)

        # print(f"Fireworks: {len(fireworks)}\nParticles: {total_particles}\n\n")

    pygame.quit()
    quit()


main()
