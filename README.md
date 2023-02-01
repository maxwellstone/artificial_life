# Assignment 5

This simulation features a monoped robot trying to hop around through its environment. The robot consists of a torso, two arms, each with an upper and lower part, and a single piece for a leg. The robot learns to use its one leg to propel itself forward, and uses its arms to balance and keep itself from falling down.

## Fitness

The fitness function used to evolve the robot to exhibit such behavior is the squared distance of the torso from the origin (see [here](robot.py#41-45)).