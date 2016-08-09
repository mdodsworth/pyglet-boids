# Overview #

A simple Boid simulation, based on Craig Reynolds [seminal paper](http://www.cs.toronto.edu/~dt/siggraph97-course/cwr87/).
The intent of this project was to scratch a long-time itch, and (re)learn a few things along the way (although, the number of times I found myself on "GCSE Physics" and "Fun with Maths!" sites was somewhat depressing). For simplicity, Python and [Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home) were used; Numpy was *not* used deliberately (as where would be the fun in that).

## Boid Behaviour ##

A boid's motion is a function of multiple, simple behavioural rules. Each rule uses information of _that_ boid's perceived local environment, meaning that each boid acts independently and selfishly. 

> "The aggregate motion of the simulated flock is the result of the dense interaction of the relatively simple behaviors of the individual simulated birds" -- Craig Reynolds

### Cohesion ###

Each boid attempts to move itself towards the [geometric center](https://en.wikipedia.org/wiki/Centroid) of all nearby boids. In this simulation, "nearby" is defined as being within a specified distance and angle, relative to a boids position and direction respectively. The cohesion change vector is simply `boid_position -> mean_position(nearby_boids)`.

### Alignment ###

### Collision Avoidance ###

### Object Attraction ###


![Boids demo](docs/boids-demo.gif)

# Setup #

This project was built against python3 -- as somewhat of an outsider, the 2 vs. 3 discussion appears to be a mess of biblical proportions.

`make init` will fetch the required packages. `make run` will run the simulation. Simples.

# Controls #

- `Q`: Quit
- `A`: Add Attractor (at the current mouse position)
- `O`: Add Obstacle (at the current mouse position)
- `+`: Add Boid
- `-`: Remove Boid
- `D`: Show debug (incl. each boid's direction and visible range)
- `V`: Show change vectors (displays a line for each behavioural rule's contribution)
