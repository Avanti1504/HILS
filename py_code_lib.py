import numpy as np
import pygad
import subprocess
import numpy

warnings.filterwarnings('ignore')
min_fitness=1000
# Define the target outputs
desired_outputs = numpy.loadtxt("D:\Avanti\SSP\Parameter_tuning\ORION\output.txt", dtype=float)
desired_outputs = desired_outputs.reshape(50, 4)

# Define the C program command
c_program_command_1 = "gcc -o D:\Avanti\SSP\Parameter_tuning\ORION\main.exe D:\Avanti\SSP\Parameter_tuning\ORION\main.c"
c_program_command_2 = "D:\Avanti\SSP\Parameter_tuning\ORION\main.exe "
# Define the genetic algorithm parameters
population_size = 5
mutation_rate = 1
max_generations = 2

# Define the number of constants (genes) to generate number of
num_constants = 3

# Define the gene bounds
gene_bounds = [
    np.linspace(1e-15, 3e-15),  # epsilon stepsize e-15
    np.linspace(0.00010, 0.00020),  # delta (1e-4 2e-4) stepsize
    np.linspace(1e-4 , 1e-2) ,#EPSILON_SEQ_ERROR
    #(0.99999999999, 0.999999999999),  # ymax
    #(0.93, 0.95),  # ymin
    
]

# Convert gene_bounds to a NumPy array
gene_space = numpy.array(gene_bounds)





# Define the fitness function
def fitness_func(ga_instance, solution, solution_idx):
    individual = solution[:num_constants]

  

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
        file.write("#define Y_MAX 0.9999999999926209\n")
        file.write("#define Y_MIN 0.9900261208247870\n")
        file.write("#define TOL 0.5\n")
        file.write("#define P1 35 \n")
        file.write("#define P2 80 \n")
        file.write("#define EPSILON_SEQ_ERROR {} \n".format(individual[2])) # 1e-4 to 1e-2
        file.write("#define EPSILON_EST 0.001 \n")

  # Evaluate the fitness for each test case
    # Run the C program and collect the output
    result = subprocess.run(c_program_command_1, shell=True, capture_output=True, text=True)
    process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    print("EPSILON:", individual[0]," DELTA:", individual[1], " y_max:" , individual[2], "y-min", individual[3])
    print("Output:", output)
    output = list(filter(None, output.split('\r\n')))
# Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = numpy.array([list(map(float, line.split())) for line in output])

    # Check the shapes of the arrays
    if desired_outputs.shape != output_coordinates.shape:
        raise ValueError("Shape mismatch between desired_outputs and output_coordinates")

    # Calculate the fitness based on the differences between desired and obtained coordinates
    fitness = numpy.sum(numpy.abs(desired_outputs - output_coordinates))
    #fitness=numpy.abs(sim_error(desired_outputs,output_coordinates))
    return fitness

# Convert gene_bounds to a list
gene_space = gene_space.tolist()

# Create an instance of the pygad.GA class
ga_instance = pygad.GA(num_generations=max_generations,
                       num_parents_mating=population_size,
                       fitness_func=fitness_func,
                       sol_per_pop=population_size,
                       num_genes=num_constants,
                       gene_type=float,
                       gene_space=gene_space,
                       mutation_type=mutation_func,
                       crossover_type=crossover_func,
                       mutation_percent_genes=mutation_rate,
                       parent_selection_type=parent_selection_func)

# Run the genetic algorithm
ga_instance.run()

# Get the best solution and its fitness
best_solution, best_fitness = ga_instance.best_solution(), ga_instance.best_fitness()

# Print the best solution and its fitness
print("Best solution:", best_solution[:num_constants])
print("Fitness:", best_fitness)
# plot the error on test sample

