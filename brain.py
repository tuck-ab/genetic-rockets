import random

## -- Creates a random vector with values between -7.5 and 7.5
def get_random_vector():
    return [(random.random()-0.5)*15,(random.random()-0.5)*15]

## -- Takes 2 brain objects and combines their vectors to create a new
## -- brain object
def combine_brains(brain1,brain2):
    new_brain = Brain(brain1.size)

    ## -- Loop through all the vectors and add them together
    for i in range(0,new_brain.size):
        vector = [(brain1.vectors[i][0] + brain2.vectors[i][0])/2,
                  (brain1.vectors[i][1] + brain2.vectors[i][1])/2]

        ## -- Mutate the vectors for the genetic algorithm to work
        vector[0] += (random.random() - 0.5) * 6
        vector[1] += (random.random() - 0.5) * 6

        new_brain.vectors[i] = vector
    return new_brain


## -- Brain object contains the list of vectors as well as an attribute
## -- to store which step the brain is on
class Brain:
    def __init__(self,size):
        self.vectors = [get_random_vector() for i in range(0,size)]
        self.pos = 0
        self.size = size

    ## -- Returns the vector and updates the step counter
    def get_next_vector(self):
        if self.pos < self.size:
            self.pos += 1
            return self.vectors[self.pos-1]
        else:
            return None
