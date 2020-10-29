import brain
import math

class Rocket:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        ## -- Each rocket has a brain which stores the vectors
        self.brain = brain.Brain(500)
        self.fitness = 0

        self.alive = True
        self.at_goal = False

    ## -- Function called every loop, updates position and does checks
    def update(self,target,obsticles):
        next_vector = self.brain.get_next_vector()
        ## -- If you've reached the end of the brain
        if next_vector == None:
            self.alive = False
        else:
            ## -- Updates the position
            self.x += next_vector[0]
            self.y += next_vector[1]

            ## -- Check if they hit the wall
            if self.x < 0 or self.x > 500:
                self.alive = False
            if self.y < 0 or self.y > 800:
                self.alive = False

            ## -- Check if the they hit an obsticle
            for o in obsticles:
                if self.x > o[0] and self.x < o[0] + o[2]:
                    if self.y > o[1] and self.y < o[1] + o[3]:
                        self.alive = False

            ## -- Check if they have reached the target
            if self.x > target[0] - 25 and self.x < target[0] + 25:
                if self.y > target[1] - 25 and self.y < target[1] + 25:
                    self.at_goal = True


    def calculate_fitness(self,target):
        ## -- is dead, distance from target, number of steps
        self.fitness = 0

        #if self.alive:
        #    self.fitness += 50

        dx = self.x - target[0]
        dy = self.y - target[1]
        distance = math.sqrt(dx**2 + dy**2)

        self.fitness += (700 - distance) // 10

        if self.alive:
            self.fitness += 50
            self.fitness += (250 - self.brain.pos) // 10

            if self.at_goal:
                self.fitness *= 2

        if self.fitness < 0:
            self.fitness = 0

        return self.fitness
