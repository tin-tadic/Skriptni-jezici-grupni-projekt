import pygame
import sys
import random
import time


class Blavor():
    def __init__(self, screen):
        self.length = 3
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (240, 240, 240)
        self.score = 0
        self.screen = screen

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ( ( (cur[0] + (x * gridsize)) % screen_width ), ( cur[1] + (y * gridsize) ) % screen_height )

        #Ako smo udarili u sebe onda pozovi reset funkciju
        if new in self.positions:
            self.reset(self.screen)
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self, screen):
        death_sound = pygame.mixer.Sound('Ded.mp3')
        death_sound.play()

        #prikazi da je blavor poginuo i trenutni score
        myfont = pygame.font.SysFont("sans serif", 32)
        dead = myfont.render("Blavor je poginuo :c", 1, (255, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 118, screen_width, 40))
        screen.blit(dead, (145, 125))

        text = myfont.render("Trenutni score: {0}".format(self.score), 1, (255, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 200, screen_width, 40))
        screen.blit(text, (155, 210))

        pygame.display.update()
        time.sleep(4)

        #reset
        start_sound = pygame.mixer.Sound('Start.mp3')
        start_sound.play()
        self.length = 3
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for tijelo in self.positions:
            #Crtanje blavora na ekran
            clanak = pygame.Rect((tijelo[0], tijelo[1]), (gridsize, gridsize))
            tocka = pygame.Rect((tijelo[0] + 8, tijelo[1] + 8), (gridsize - 16, gridsize - 16))
            pygame.draw.rect(surface, self.color, clanak)
            pygame.draw.rect(surface, (211, 211, 211), clanak, 1)
            pygame.draw.rect(surface, (105, 105, 105), tocka)
        
        #Glava da bude zasebne boje radi vece preglednosti
        glava = pygame.Rect((self.positions[0][0] + 3, self.positions[0][1] + 3), (gridsize - 6, gridsize - 6))
        pygame.draw.rect(surface, (0, 0, 0), glava)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (250, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        food = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, food)
        pygame.draw.rect(surface, (93, 216, 228), food, 1)

def drawGrid(surface):
    for i in range(0, int(grid_height)):
        for j in range(0, int(grid_width)):
            if (i + j) % 2 == 0:
                pod_1 = pygame.Rect((j * gridsize, i * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (0, 255, 0), pod_1)
            else:
                pod_2 = pygame.Rect((j * gridsize, i * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (50, 205, 50), pod_2)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

#Vektori kretanja
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)



def main():
    #Odabir tezine (brzine) igre
    difficulty = input("Koji difficulty zelite igrati? Opcije su easy, normal, i hard: ")
    while (difficulty not in {"easy", "normal", "hard"}):
        difficulty = input("Pogresan unos.\nKoji difficulty zelite igrati? Opcije su easy, normal, i hard: ")
    
    if difficulty == "easy":
        difficulty = 5
    elif difficulty == "normal":
        difficulty = 10
    else:
        difficulty = 20
    
    pygame.init()


    start_sound = pygame.mixer.Sound('Start.mp3')
    start_sound.play()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('The Blavor Game: Snake of the Year Edition')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    blavor = Blavor(screen)
    food = Food()
    
    while (True):
        clock.tick(difficulty)
        blavor.handle_keys()
        drawGrid(surface)
        blavor.move()

        if blavor.get_head_position() == food.position:
            collect_sound = pygame.mixer.Sound('Collected.mp3')
            collect_sound.play()
            blavor.length += 1
            blavor.score += 1
            food.randomize_position()
        
        blavor.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()

main()