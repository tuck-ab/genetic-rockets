import pygame
import random
import brain

import rocket as r

pygame.init()

clock = pygame.time.Clock()

screen_size = (500,800)
screen = pygame.display.set_mode(screen_size)
myfont = pygame.font.SysFont('Comic Sans MS', 30)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

rockets = []
gen_size = 500
for i in range(0,gen_size):
    rockets.append(r.Rocket(250,750))

target = [250,50]
max_height = 800
gen_num = 1
best_previous = rockets[0]

def shape_one():
    obsticles = []
    obsticles.append([200,500,300,10])
    obsticles.append([0,300,300,10])
    return obsticles

def shape_two():
    obsticles = []
    obsticles.append([150,500,350,10])
    obsticles.append([150,400,10,100])
    obsticles.append([0,300,300,10])
    obsticles.append([300,300,10,100])
    return obsticles

obsticles = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ## --- UPDATE
    all_dead = True
    for rocket in rockets:
        if rocket.alive and not rocket.at_goal:
            all_dead = False
            rocket.update(target,obsticles)
        if rocket.y < max_height:
            max_height = rocket.y

    if all_dead:
        ## -- Create new Generation

        weights = []
        for rocket in rockets:
            weights.append(rocket.calculate_fitness(target))
            if rocket.fitness > best_previous.fitness:
                best_previous = rocket

        parent_list = random.choices(rockets, weights=weights, k=gen_size*2-2)

        new_rockets = []
        temp = r.Rocket(250,750)
        temp.brain = best_previous.brain
        temp.brain.pos = 0
        best_previous = temp
        new_rockets.append(best_previous)
        for i in range(0,gen_size-1):
            new_rocket = r.Rocket(250,750)
            new_rocket.brain = brain.combine_brains(parent_list[2*i].brain,parent_list[2*i+1].brain)
            new_rockets.append(new_rocket)

        rockets = new_rockets
        gen_num += 1

    ## --- DRAW

    if gen_num % 10 == 1:
        screen.fill(WHITE)

        for rocket in rockets:
            pygame.draw.rect(screen,BLACK,[rocket.x,rocket.y,4,10])
        pygame.draw.rect(screen,RED,[best_previous.x,best_previous.y,4,10])

        for obsticle in obsticles:
            pygame.draw.rect(screen,BLACK,obsticle)

        pygame.draw.rect(screen,RED,[target[0]-25,target[1]-25,50,50])
        pygame.draw.line(screen,BLACK,[0,max_height],[500,max_height])

        my_string = "Generation: " + str(gen_num)
        text = myfont.render(my_string, False,BLACK)
        screen.blit(text,(0,0))


        pygame.display.flip()
        clock.tick(60)


pygame.quit()
