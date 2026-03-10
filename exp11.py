import numpy as np

fuel_efficiency = np.array([22, 25, 27, 30, 24, 28])

# Average fuel efficiency
average_efficiency = np.mean(fuel_efficiency)

# Compare two models
model_A = fuel_efficiency[1]
model_B = fuel_efficiency[3]

percentage_improvement = ((model_B - model_A) / model_A) * 100

print("Average Fuel Efficiency:", average_efficiency, "mpg")
print("Percentage Improvement:", percentage_improvement, "%")