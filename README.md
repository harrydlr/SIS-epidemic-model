# SIS-epidemic-model

This work is about a Monte Carlo simulation of SIS (Susceptible-Infected-Susceptible) epidemic models.

An SIS model is an epidemiology Compartmental model, characterized by 2 parameters:
  - µ: spontaneous recovery probability.
  - β: infection probability of a susceptible (S) individual when it is contacted by an infected (I) one.
  
For an SIS dynamics in a complex network we suppose that every node is an individual which can be in either state S or state I, the time is discrete, and at each time step each node contacts (synchronously) with all of its neighbors.

We are interested in the calculation of <ρ>, the average fraction of infected node in the network, that requires 2 kind of averages:
  - For one simulation, average of ρ(t) over many time steps, when the systems has reached the stationary state.
  - Repeat the simulation many times to average over initial conditions and temporal evolutions.

Setup:

  The following python packages were used:
  
    - networkx: to create/manipulate and save the networks
    - random: to generate random numbers from a uniform distribution
    - multiproccessing: to parallelize the repetitions of the simulations
    - pickle: to save the results in a python dictionary

Pipeline:

  - First, we create the network (or load an existing one). Once loaded we create 2 node attributes for the network:

      - State: It indicates the state of the node: either Infected(I) or Susceptible(S)
      - Neighbors: It’s a list that contains the neighbors of a node

  - Second, we define the parameters we want to evaluate:

      - beta: 51 values from 0 to 1
      - mu: 0.1, 0.5 and 0.9
      - rho_0:  initial fraction of infected nodes = 0.2
      - T_max : maximum number of time steps of each simulation = 1000
      - T_trans : number of steps of the transitory = 900
      - N_rep: number of repetitions of each simulation = 50

  Then, the SIS_MC() function will perform the systematic study. There we parallelize the repetitions of each simulation.

  Each simulation is carried on using epidemic_sim() function

  The results of every specific set of parameters are saved in a python dictionary like:
  {mu: {beta: value}}

  and finally it is saved using the pickle package.
  
  As example, we performed the study over an Erdös-Rényi network (500 nodes, p=0.02).
