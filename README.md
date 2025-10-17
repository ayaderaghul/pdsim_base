# Repeated Prisoner's Dilemma Game - simulation of agent based model - in C
This is the base model in which the agent responds to the previous outcome of each round. I build this to later build upon it another extended version where agents can have an initial phase of testing the opponents. I would like to see what behavior emerge when they are able to sustain cooperation in society.
# Mini database of structs in .bin
In each cycle, I would save the struct of the agents into a binary file, then I would write interface to get back from this database the agents.
# Welcome for discussion and contribution

# How to run

Change the output data file names

gcc main.c -o simulation
simulation
py plot.py

Check the cycle that you like to inspect
Load them with load.c, parse the agents with parser.c, plot the agents and propensity to cooperate in the population using plot3.py

