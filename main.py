import pygame
import random

import brain
import levels
import rocket as r

pygame.init()

clock = pygame.time.Clock()

## -- Setting the screen up
screen_size = (500,800)
screen = pygame.display.set_mode(screen_size)
myfont = pygame.font.SysFont('Comic Sans MS', 30)

## -- Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

## -- Setting up the population
rockets = []
gen_size = 500
for i in range(0,gen_size):
    rockets.append(r.Rocket(250,750))

## -- Setting up the target and tracking of best rocket
target = [250,50]
max_height = 800
gen_num = 1
best_previous = rockets[0]

obsticles = [levels.shape_one()]

## -- Main Loop
running = True
while running:
    for event in pygame.event.get():
        ## -- If the window is closed
        if event.type == pygame.QUIT:
            running = False

    ## --- UPDATE

    ## -- Looping through all the rockets and updating them
    all_dead = True
    for rocket in rockets:
        ## -- Only updating the alive rockets
        if rocket.alive and not rocket.at_goal:
            all_dead = False
            rocket.update(target,obsticles)
        ## -- Checking if the rocket has broken a height record
        if rocket.y < max_height:
            max_height = rocket.y

    if all_dead:
        ## -- Createing a new Generation
        ## -- Calculating the weights of all the rockets
        weights = []
        for rocket in rockets:
            weights.append(rocket.calculate_fitness(target))
            ## -- Working out the best rocket
            if rocket.fitness > best_previous.fitness:
                best_previous = rocket

        ## -- Weighted random pick of "parents" for the rockets
        parent_list = random.choices(rockets, weights=weights, k=gen_size*2-2)

        ## -- Actually creating the new generation
        new_rockets = []
        ## -- The best rocket added first to ensure the generation
        ## -- doesnt get worse
        temp = r.Rocket(250,750)
        temp.brain = best_previous.brain
        temp.brain.pos = 0
        best_previous = temp
        new_rockets.append(best_previous)

        ## -- Using the parents to fill the rest of the generation
        for i in range(0,gen_size-1):
            new_rocket = r.Rocket(250,750)
            new_rocket.brain = brain.combine_brains(parent_list[2*i].brain,parent_list[2*i+1].brain)
            new_rockets.append(new_rocket)

        rockets = new_rockets
        gen_num += 1

    ## --- DRAW

    if gen_num % 10 == 1: ## -- Only displays every 10 generations
        screen.fill(WHITE)

        ## -- Draw Rockets
        for rocket in rockets:
            pygame.draw.rect(screen,BLACK,[rocket.x,rocket.y,4,10])
        pygame.draw.rect(screen,RED,[best_previous.x,best_previous.y,4,10])

        ## -- Draw Obsticles
        for obsticle in obsticles:
            pygame.draw.rect(screen,BLACK,obsticle)

        ## -- Drawing Target
        pygame.draw.rect(screen,RED,[target[0]-25,target[1]-25,50,50])
        ## -- Drawing the line for the highest point reached
        pygame.draw.line(screen,BLACK,[0,max_height],[500,max_height])

        ## -- Displaying the generation number
        my_string = "Generation: " + str(gen_num)
        text = myfont.render(my_string, False,BLACK)
        screen.blit(text,(0,0))


        pygame.display.flip()
        clock.tick(60)


pygame.quit()
