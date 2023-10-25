import random
import subprocess
import numpy
import os

# Define thetarget outputs
desired_outputs= numpy.loadtxt("D:\Avanti\SSP\Parameter_tuning\ORION\output.txt", dtype=float)




# Reshape the array to have the desired shape of 100x4
desired_outputs= desired_outputs.reshape(100, 4)

# Print the array
#print(desired_outputs)


# Define the C program command

c_program_command = "gcc -o D:\Avanti\SSP\Parameter_tuning\ORION\main.exe D:\Avanti\SSP\Parameter_tuning\ORION\main.c; D:\Avanti\SSP\Parameter_tuning\ORION\main.exe"

# Define the genetic algorithm parameters
population_size = 100
mutation_rate = 0.01
max_generations = 100

# Define the number of constants (genes) to generate
num_constants = 4
#put bounds
gene_bounds = [
    (1e-15, 3e-15),  # epsilon
    (0.00010, 0.00020),  # delta
    (0.99999999999, 0.999999999999),  # ymax
    (0.93, 0.95),  # ymin
]
def evaluate_individual(individual):
    # Save the individual's genes in a header file as constants
    with open("D:/Avanti/SSP/Parameter_tuning/ORION/constants.h", "w") as file:
        file.write("#include <stdio.h>\n")
        file.write("#include <stdlib.h>\n")
        file.write("#include <math.h>\n")
        file.write("#include <string.h>\n")
        # Generate multiple constants based on the individual's genes
        file.write("#define THRESHOLD 3\n")
        file.write("#define STAR_MIN_PIXEL 3\n")
        file.write("#define STAR_MAX_PIXEL 150\n")
        file.write("#define MAX_STARS 100\n")
        file.write("#define SKIP_PIXELS 2\n")
        file.write("#define LENGTH 808\n")
        file.write("#define BREADTH 608\n")
        file.write("#define PIXEL_WIDTH 0.0000048\n")
        file.write("#define NUM_MAX_STARS 13\n")
        file.write("//SM constants\n")
        file.write("#define FOCAL_LENGTH 0.036\n")
        file.write("#define EPSILON {}\n".format(individual[0]))
        file.write("#define DELTA {}\n".format(individual[1]))
        file.write("#define ANG_DIST_TOLERANCE 1.2\n")
        file.write("#define N_GC 8876\n")
        file.write("#define N_KVEC_PAIRS 224792\n")
        file.write("#define Y_MAX {}\n".format(individual[2]))
        file.write("#define Y_MIN {}\n".format(individual[3]))
        file.write("#define TOL 0.5\n")
        file.write("#define P1 35 \n")
        file.write("#define P2 80 \n")

    fitness = 0
    # Evaluate the fitness for each test case
    # Run the C program and collect the output
    process = subprocess.Popen(c_program_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    print("Output:", output)  # Print the output for debugging purposes

    # Remove empty strings from the output list
    output = list(filter(None, output.split('\r\n')))

    # Convert the output to a NumPy array
    output_array = numpy.array([list(map(float, line.split())) for line in output])
    process = subprocess.Popen(c_program_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    print("Output:", output)  # Print the output for debugging purposes

    # Remove empty strings from the output list
    output = list(filter(None, output.split('\r\n')))

    # Convert the output to a 100x4 array of coordinates
    output_coordinates = numpy.array([list(map(float, line.split())) for line in output])

    # Check the shapes of the arrays
    if desired_outputs.shape != output_coordinates.shape:
        raise ValueError("Shape mismatch between desired_outputs and output_coordinates")

    # Calculate the fitness based on the differences between desired and obtained coordinates
    fitness = numpy.sum(numpy.abs(desired_outputs - output_coordinates))

    return fitness


# Define the function to generate a random individual
def generate_individual():
    return [random.uniform(bounds[0], bounds[1]) for bounds in gene_bounds]



#mutate
def mutate_individual(individual):
    mutated_individual = individual.copy()
    for i in range(num_constants):
        if random.random() < mutation_rate:
            bounds = gene_bounds[i]
            mutated_individual[i] = random.randint(bounds[0], bounds[1])
    return mutated_individual

# Create the initial population
population = [generate_individual() for _ in range(population_size)]

# Run the genetic algorithm
for generation in range(max_generations):
    # Evaluate the fitness of each individual
    fitness_scores = [evaluate_individual(individual) for individual in population]

    # Find the best individual in the population
    best_individual_index = min(range(population_size), key=lambda i: fitness_scores[i])
    best_individual = population[best_individual_index]
    best_fitness = fitness_scores[best_individual_index]

    # Terminate if the best individual matches the desired outputs
    if best_fitness <= 0.01:
        break

    # Create a new population by selecting and mutating the best individuals
    new_population = [best_individual]

    while len(new_population) < population_size:
        # Select two parents from the population using tournament selection
        parents = random.choices(population, k=2, weights=[1 / fitness_scores[i] for i in range(population_size)])

        # Create a new individual by crossover
        child = [random.choice(gene_pair) for gene_pair in zip(parents[0], parents[1])]

        # Mutate the new individual
        child = mutate_individual(child)

        # Add the new individual to the new population
        new_population.append(child)

    population = new_population

# Print the best individual and its fitness
print("Best individual:", best_individual)
print("Fitness:", best_fitness)
