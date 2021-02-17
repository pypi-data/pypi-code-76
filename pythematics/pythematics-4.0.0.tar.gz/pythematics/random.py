"""
    \tRandom submodule
    This is a custom made random submodule,
    that includes all trivial random operations (nothing more than the builtin),
    - random() #Pseudorandom number between 0,1
    - randendint(end : int) #Random in range (0,end)
    - choices(array : list,num_choice : int) #Gives an list of num_choice lenght containing random choices from the passed in list
    - randrange(start,end) #Returns a random floating point number in range(start,end)
    - randint(start,end) #Returns int(randrange(start,end))
    - random_complex() #Returns random() * complex(1,1)

"""
from time import time #for seed generation
from .trigonometric import sin #Acting as an 'activation' function for squishing values to (0,1)
from typing import Union

seed = time()
addition = 2.718281828459045 + 3.141592653589793
modulus = 50.12

TEMP_MEMORY = [int(str(seed)[-3:].replace(".",'1'))]

def random() -> float:
    """
        Generates a pseudo-random number between zero and one
    """
    # 0.008620870113372803 for 1k iterations
    val =  (TEMP_MEMORY[-1] + addition) % modulus
    TEMP_MEMORY[0] = val
    return abs(sin(val,iterations=10,degrees=True))

def randendint(end : int):
    """Returns a random integer in range (0,end)"""
    return round(random() * end)

def choice(array : list) -> list:
    """
    Returns a pseudo-randomly chosen element from the input array 
    """
    return array[randendint(len(array))]

def choices(array : list,num_choice : int) -> list:
    """Given an array and a variable 'num_choice' it gives back\n
       a new list containing a total of num_choice,\n
       pseudo-randomly chosen elements\n
    """
    choice_array = []
    for _ in range(num_choice):
        choice_array.append(choice(array))
    return choice_array

def randrange(start : Union[float,int],end : Union[float,int]) -> float:
    """Returns a random floating point number
       given a start and an end
    """
    return random() * (end-start) + start

def randint(start : Union[float,int],end : Union[float,int]) -> float:
    """Returns a random integer given a minimun and a maximun value"""
    return round(randrange(start,end))

def random_complex(factor : Union[float,int] = 1) -> complex:
    """Returns a random complex number scaled by a factor"""
    return random() * complex(1,1) * factor

#Get random modulus and addition
modulus = randrange(1,69969)
addition = randrange(5,96958)

if __name__ == "__main__": 
    for i in range(100):
        print(random())