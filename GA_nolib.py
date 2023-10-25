import numpy as np
import subprocess

# Define the number of constants (genes) to generate number of
num_constants = 5

# Define the gene bounds
gene_bounds = [
    np.linspace(-7, 0),  # log delta
    np.linspace(0.1, 1),  # TOL
    np.linspace(25, 50),  # P1
    np.linspace(70, 90),  # P2
    np.linspace(0.004, 0.006)  # EPSILON_SEQ_ERROR
]

# Define the target outputs
desired_outputs = np.loadtxt("out_ideal.txt", dtype=float)
desired_outputs = desired_outputs.reshape(5, 4)

# Define the C program command
c_program_command_1 = "gcc main.c -o exe -lm"
c_program_command_2 = "./exe"

# Convert gene_bounds to a np array
gene_space = np.array(gene_bounds)

# Define the fitness function
def cal_fitness(Q1, Q2):
    # Compute the quaternion conjugate of Q1
    conj_Q1 = np.array([-Q1[0], -Q1[1], -Q1[2], -Q1[3]])

    # Compute the quaternion product Q12
    Q12 = np.array([
        conj_Q1[0] * Q2[0] - conj_Q1[1] * Q2[1] - conj_Q1[2] * Q2[2] - conj_Q1[3] * Q2[3],
        conj_Q1[0] * Q2[1] + conj_Q1[1] * Q2[0] + conj_Q1[2] * Q2[3] - conj_Q1[3] * Q2[2],
        conj_Q1[0] * Q2[2] - conj_Q1[1] * Q2[3] + conj_Q1[2] * Q2[0] + conj_Q1[3] * Q2[1],
        conj_Q1[0] * Q2[3] + conj_Q1[1] * Q2[2] - conj_Q1[2] * Q2[1] + conj_Q1[3] * Q2[0]
    ])

    # Compute the norm of Q12
    norm_Q12 = np.linalg.norm(Q12)

    # Calculate the angle using atan2
    angle = 2 * np.arctan2(norm_Q12, Q12[0])

    # Convert the angle from radians to degrees, if desired
    angle_degrees = np.degrees(angle)
    error_quat = (angle_degrees - 90) * 1e5

    # Calculate fitness based on the difference from the desired value
    return abs(error_quat)  # Adjust this for your fitness function


# Evaluate the fitness for each test case
def fitness_func(solution):
    # Create a header file with the current solution's parameters
    with open("constants.h", "w") as file:
        file.write("#include <stdio.h>\n")
        # Write constants based on the solution
        for i, param_range in enumerate(gene_bounds):
            file.write("#include <stdio.h>\n")
            file.write("#include <stdlib.h>\n")
            file.write("#include <math.h>\n")
            file.write("#include <string.h>\n")
            # Generate multiple constants based on the solution's genes
            #file.write("#define THRESHOLD 3\n")
            file.write("#define STAR_MIN_PIXEL 3\n")
            file.write("#define STAR_MAX_PIXEL 150\n")
            file.write("#define MAX_STARS 100\n")
            file.write("#define SKIP_PIXELS 2\n")
            file.write("#define LENGTH 2028\n")
            file.write("#define BREADTH 1520\n")     
            file.write("#define PIXEL_WIDTH 0.0000031\n")
            file.write("#define NUM_MAX_STARS 13\n")
            file.write("//SM constants\n")
            file.write("#define FOCAL_LENGTH 0.0175\n")
            #file.write("#define EPSILON 2.2e-15\n")
            file.write("#define EPSILON 2.22e-15\n")
            file.write("#define DELTA {}\n".format(10**solution[0]))
            file.write("#define ANG_DIST_TOLERANCE 1.2\n")
            file.write("#define N_GC 8876\n")
            file.write("#define N_KVEC_PAIRS 224792\n")
            file.write("#define Y_MAX 0.9999999999926209\n")
            file.write("#define Y_MIN 0.9900261208247870\n")
            file.write("#define TOL {}\n".format(solution[1]))
            file.write("#define P1 {}\n".format(solution[2]))
            file.write("#define P2 {} \n".format(solution[3]))
            file.write("#define EPSILON_SEQ_ERROR {} \n".format(solution[4])) 
            file.write("#define EPSILON_EST 0.001 \n")
    
    subprocess.run(c_program_command_1, shell=True)

    # Run the C program and collect the output
    process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    output = list(filter(None, output.split('\n')))
    print(output)

    # Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = np.array([list(map(float, line.split())) for line in output])

    fitness =[]
    for i in range(desired_outputs.shape[0]):
        desired_row = desired_outputs[i, :]
        obtained_row = output_coordinates[i, :]
        fitness.append(cal_fitness(desired_row, obtained_row))

    least_fitness=min(fitness)
    return least_fitness

# Define uniform crossover function
def uniform_crossover(parent1, parent2):
    child = np.empty(len(parent1))
    for i in range(len(parent1)):
        if np.random.rand() < 0.5:
            child[i] = parent1[i]
        else:
            child[i] = parent2[i]
    return child

def rank_based_selection(population, fitness_values, num_parents):
    ranked_indices = np.argsort(fitness_values)
    selected_parents_indices = ranked_indices[:num_parents]
    parents = population[selected_parents_indices]
    return parents
# Define gene-wise mutation function
def mutate_adaptive(solution, mutation_rate):
    mutated_solution = solution.copy()
    for i in range(len(solution)):
        if np.random.rand() < mutation_rate:
            mutated_solution[i] = np.random.choice(gene_bounds[i])
    return mutated_solution

# Hyperparameters
population_size = 10
num_generations = 10
initial_mutation_rate = 0.1
final_mutation_rate = 0.01
#mutation_rate=[final_mutation_rate,initial_mutation_rate]
# Initialize the population with random solutions within the gene bounds
population = np.random.rand(population_size, num_constants)
for i in range(population_size):
    for j in range(num_constants):
        population[i, j] = np.random.choice(gene_bounds[j])
mutation_rate=initial_mutation_rate
# Main genetic algorithm loop
for generation in range(num_generations):
    # Evaluate the fitness of the current population
    fitness_values = [fitness_func(solution) for solution in population]

    # Rank-based selection of parents
    num_parents = int(population_size / 2)
    parents = rank_based_selection(population, fitness_values, num_parents)

    # Create the next generation through crossover and adaptive mutation
    offspring = np.empty((population_size, num_constants))
    for i in range(num_parents):
        parent1 = parents[i]
        parent2 = parents[(i + 1) % num_parents]  # Circular selection of parents
        child = uniform_crossover(parent1, parent2)
        child = mutate_adaptive(child, mutation_rate)
        offspring[i] = child
    population[num_parents:, :] = offspring[:population_size - num_parents]

    # Report the best fitness in this generation    
    best_fitness_idx = np.argmin(fitness_values)
    best_solution = population[best_fitness_idx]
    best_fitness = fitness_values[best_fitness_idx]
    print(f"Generation {generation+1}: Best Fitness = {best_fitness}")

   

# Print the best solution found
print("Best Solution:")
print(best_solution)
print("Best Fitness:", best_fitness)
