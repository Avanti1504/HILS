import numpy as np
import pygad
import subprocess
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')
min_fitness=100000000
best_parameters=[0,0,0,0,0]
# Define the number of constants (genes) to generate number of
num_constants = 5
no_of_epochs=0
errors_per_epoch=[]
def cal_fitness(Q1,Q2):
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
    error_quat=(angle_degrees-90)*1e5
    return (error_quat)
    

# Define the gene bounds
gene_bounds = [
    
    np.linspace(-6,-2),  # log delta 
    np.linspace(0.1,1), #TOL
    np.linspace(25,50), #P1
    np.linspace(70,90), #P2
    np.linspace(0.004, 0.006) #EPSILON_SEQ_ERROR
    
]



    # Define the target outputs
desired_outputs = np.loadtxt("/mnt/d/Avanti/SSP/Parameter_tuning/ORION_RPI/out_ideal.txt", dtype=float)
desired_outputs = desired_outputs.reshape(5, 4)
    #print(desired_outputs)

    # Define the C program command
c_program_command_1 = "gcc /mnt/d/Avanti/SSP/Parameter_tuning/ORION_RPI/main.c  -o /mnt/d/Avanti/SSP/Parameter_tuning/ORION_RPI/exe -lm"
c_program_command_2 = "/mnt/d/Avanti/SSP/Parameter_tuning/ORION_RPI/exe"
    
    # Convert gene_bounds to a np array
gene_space = np.array(gene_bounds)


    # Define the fitness function
def fitness_func(ga_instance, solution, solution_idx):
    #
    # solution = solution[:num_constants]
    
        # Generate random values for each gene within the bounds
        #solution = np.random.uniform(low=gene_bounds[0][0], high=gene_bounds[0][1])
        #for i in range(1, num_constants):
        #    solution = np.append(solution, np.random.uniform(low=gene_bounds[i][0], high=gene_bounds[i][1]))
    

        # Save the solution's genes in a header file as constants
    with open("/mnt/d/Avanti/SSP/Parameter_tuning/ORION_RPI/constants.h", "w") as file:
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
         file.write("#define EPSILON 2.22e-15")
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
   # Evaluate the fitness for each test case
    # Run the C program and collect the output
    result = subprocess.run(c_program_command_1, shell=True, capture_output=True, text=True)
    process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      #process = subprocess.Popen(c_program_command_2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    print(" DELTA:", 10**solution[0], " TOL:",solution[1], " P1:",solution[2], " P2:",solution[3], " EsE:",solution[4] )
    #print("Output:", output)
    output = list(filter(None, output.split('\n')))
    # Calculate the fitness based on the differences between desired and obtained coordinates
    output_coordinates = np.array([list(map(float, line.split())) for line in output])

        # Check the shapes of the arrays
    if desired_outputs.shape != output_coordinates.shape:
        raise ValueError("Shape mismatch between desired_outputs and output_coordinates")

        # Calculate the fitness based on the differences between desired and obtained coordinates
       # fitness = np.sum(np.abs(desired_outputs - output_coordinates))
        #fitness=np.abs(sim_error(desired_outputs,output_coordinates))
    best_fitness_val=10000000
    

    for i in range(desired_outputs.shape[0]):
         desired_row = desired_outputs[i, :]
         obtained_row = output_coordinates[i, :]
         curr_fitness=cal_fitness(desired_row,obtained_row)
         best_fitness_val=min(best_fitness_val,curr_fitness)
         #fitness += np.sum(np.linalg.norm(desired_row - obtained_row))
    
    global min_fitness
    if best_fitness_val < min_fitness:
        
        for i in range(0,5):
            
            best_parameters[i]=solution[i]
        min_fitness=best_fitness_val
        global no_of_epochs
        global errors_per_epoch
        no_of_epochs=no_of_epochs+1
        errors_per_epoch.append(min_fitness)
    print(min_fitness)
    return (min_fitness)

    # Convert gene_bounds to a list
gene_space = gene_space.tolist()
initial_mutation_percent = 1 #0.0001
final_mutation_percent = 5 #0.05
mutation_percent_genes = [initial_mutation_percent, final_mutation_percent]
keep_parents = 5
num_generations = 5
num_parents_mating = 5
sol_per_pop = 5


while min_fitness>500:
        # Create an instance of the pygad.GA class
    ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            fitness_func=fitness_func,
                            sol_per_pop=sol_per_pop,
                            num_genes=num_constants,
                            gene_type=float,
                            gene_space=gene_space,
                            mutation_type="adaptive",
                            keep_elitism=1,
                            mutation_percent_genes=mutation_percent_genes,
                            crossover_type="uniform",
                            parent_selection_type="rank")


    ga_instance.run()# Run the genetic algorithm
    ga_instance.plot_fitness()
    gene_bounds = [
    np.linspace(best_parameters[0]*0.9,best_parameters[0]*1.1),  # epsilon 
    np.linspace(best_parameters[1]*0.9,best_parameters[1]*1.1),  # delta 
    np.linspace(best_parameters[2]*0.9,best_parameters[2]*1.1), #TOL
    np.linspace(best_parameters[3]*0.9,best_parameters[3]*1.1), #P1
    np.linspace(best_parameters[4]*0.9,best_parameters[4]*1.1), #P2
    #np.linspace(best_parameters[5]*0.9,best_parameters[5]*1.1) #EPSILON_SEQ_ERROR
    ]


    # Get the best solution and its fitness
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(solution)
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))



