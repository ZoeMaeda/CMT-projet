import numpy as np
import matplotlib.pyplot as plt
import csv


# for iron
with open('fixed_data_iron.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data_iron = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data_iron)
distance_iron = data_iron[:,0]
X_distance_iron = np.column_stack((distance_iron,np.ones(len(distance_iron))))
iron = data_iron[:,1]

# for log of iron
with open('fixed_data_iron_log.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data_iron_log = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data_iron)
iron_log = data_iron_log[:,1]


# for cadmium
with open('fixed_data_cadmium.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data_cadmium = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data_iron)
distance_cadmium = data_cadmium[:,0]
X_distance_cadmium = np.column_stack((distance_cadmium,np.ones(len(distance_cadmium))))
cadmium = data_cadmium[:,1]


# for log of iron
with open('fixed_data_cadmium_log.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data_cadmium_log = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data_iron)
cadmium_log = data_cadmium_log[:,1]


# implementing linear model
def model(X,param):   #model : y = param[0]*x + param[1]
    return X@param.T


# # defining mean squared error function
def mean_squared_error(X,Y,param):
    m = len(Y)
    sum = np.sum((model(X,param)-Y)**2)
    return 1/(2*m) *sum


# # derivating the mean squared error function by the parameter
def gradient(X,Y,param):
    m = len(Y)
    return 1/m* ((X.T)@(model(X,param)-Y))


# # implementing the gradient descent function
def gradient_descent(X,Y,param,learning_rate, tol):
    blocked = 0
    while mean_squared_error(X,Y,param) > tol and blocked < 20:
        mse_init = mean_squared_error(X_distance_iron,iron,param)
        param_temp = param - learning_rate*(gradient(X,Y,param))
        # print(f"mae = {mean_squared_error(X,Y,param_temp)}")
        if mean_squared_error(X,Y,param_temp)<mse_init:
            blocked = 0
            param = param_temp
            learning_rate *= 1.5
        else:
            blocked += 1
            learning_rate *= 0.5
    return param


# # after analysing the graphs, we gave a first estimation of the parameters by finding an approximative slope and intercept
initial_param_iron = np.array([-0.5,400])
initial_param_iron_log = np.array([-0.003,5.9])
initial_param_cadmium = np.array([-0.03,65])
initial_param_cadmium_log = np.array([-0.001,4])


# finding adjusted parameters
final_param_iron = gradient_descent(X_distance_iron,iron,initial_param_iron,0.01,745)
# final_param_cadmium = gradient_descent(X_distance_cadmium,cadmium,initial_param_cadmium,0.01,90)
# final_param_iron_log = gradient_descent(X_distance_iron,iron_log,initial_param_iron_log,0.01,0.02)
# final_param_cadmium_log = gradient_descent(X_distance_cadmium,cadmium_log,initial_param_cadmium_log,0.001,0.2)

print(mean_squared_error(X_distance_iron,iron,initial_param_iron))
print(f"iron : y = a*x + b with \na = {final_param_iron[0]}\nb = {final_param_iron[1]}")
# print(f"cadmium : y = a*x + b with \na = {final_param_cadmium[0]}\nb = {final_param_cadmium[1]}")
# print(f"log(iron) : y = a*x + b with \na = {final_param_iron_log[0]}\nb = {final_param_iron_log[1]}")
# print(f"log(cadmium) : y = a*x + b with \na = {final_param_cadmium_log[0]}\nb = {final_param_cadmium_log[1]}")