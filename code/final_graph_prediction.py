import matplotlib.pyplot as plt
import numpy as np
import csv

# for iron
with open('fixed_data_iron.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data)
distance_iron = data[:,0]
iron = data[:,1]

# for log of iron
with open('fixed_data_iron_log.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data)
iron_log = data[:,1]

# for cadmium
with open('fixed_data_cadmium.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data2 = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data)
distance_cadmium = data2[:,0]
cadmium = data2[:,1]

# for log of iron
with open('fixed_data_cadmium_log.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data)
cadmium_log = data[:,1]

# linear model
def model_linear(X,param):   #model : y = param[0]*x + param[1]
    X_distance = np.column_stack((X,np.ones(len(X))))
    return X_distance@param.T

# exponential model
def model_exponential(X,param):
    return np.exp(param[0]*X+param[1])


param_iron = np.array([-0.13943797693009258,399.5628873382527])
param_cadmium = np.array([-0.03302932951766946,64.91546252060607])    
param_iron_log = np.array([-0.0005229823440951592,5.900010486786221])
param_cadmium_log = np.array([-0.0010932963799059892,4.064043239933688])

# plotting data and model
# for iron
plt.plot(distance_iron,iron,'o') #pas mal
plt.plot(distance_iron,model_linear(distance_iron,np.array([-0.13943797693009258,399.5628873382527])))
plt.title('iron concentration as a function of distance')
plt.xlabel('distance to emissary in m')
plt.ylabel('iron concentration in 10^-2 g/L')
plt.savefig('prediction_iron.png')
plt.show()

# for cadmium
plt.plot(distance_cadmium,cadmium,'o')
plt.plot(distance_cadmium,model_linear(distance_cadmium,np.array([-0.03302932951766946,64.91546252060607])))
plt.title('cadmium concentration as a function of distance')
plt.xlabel('distance to emissary in m')
plt.ylabel('cadmium concentration in 10^-2 g/L')
plt.savefig('prediction_cadmium.png')
plt.show()

# for log of iron
plt.plot(distance_iron,iron,'o') #pas mal
plt.plot(np.arange(0,2000,100),model_exponential(np.arange(0,2000,100),param_iron_log))
plt.title('iron concentration as a function of distance with exponential model')
plt.xlabel('distance to emissary in m')
plt.ylabel('iron concentration in 10^-2 g/L')
plt.savefig('prediction_iron_log.png')
plt.show()

# for log of cadmium
plt.plot(distance_cadmium,cadmium,'o') #pas mal
plt.plot(np.arange(0,2000,100),model_exponential(np.arange(0,2000,100),param_cadmium_log))
plt.title('cadmium concentration as a function of distance with exponential model')
plt.xlabel('distance to emissary in m')
plt.ylabel('cadmium concentration in 10^-2 g/L')
plt.savefig('prediction_cadmium_log.png')
plt.show()

# comparison of models 
# for iron 
plt.plot(distance_iron,iron,'o') #pas mal
plt.plot(distance_iron,model_linear(distance_iron,param_iron),label='linear model')
plt.plot(np.arange(0,2000,100),model_exponential(np.arange(0,2000,100),param_iron_log),label='exponential model')
plt.legend()
plt.title('comparison of exponential and linéar model for iron concentration')
plt.xlabel('distance to emissary in m')
plt.ylabel('iron concentration in 10^-2 g/L')
plt.savefig('comparision_iron.png')
plt.show()

# for cadmium 
plt.plot(distance_cadmium,cadmium,'o') #pas mal
plt.plot(distance_cadmium,model_linear(distance_cadmium,param_cadmium),label='linear model')
plt.plot(np.arange(0,2000,100),model_exponential(np.arange(0,2000,100),param_cadmium_log),label='exponential model')
plt.legend()
plt.title('comparison of exponential and linéar model for cadmium concentration')
plt.xlabel('distance to emissary in m')
plt.ylabel('cadmium concentration in 10^-2 g/L')
plt.savefig('comparision_cadmium.png')
plt.show()


# prediction
def distance_prediction(concentration,param):
    return (concentration-param[1])/param[0]

def distance_prediction_exponential_model(concentration,param):
    return (np.log(concentration)-param[1])/param[0]

# starting the Ennui-sur-Blasé case
# using the concentration of the trouts catched to determine the distance to the pollution emmiter by applying our linear model for iron and then calculating the average distance

with open('ennui_sur_blase.csv', newline = '') as file:
    csvreader = csv.reader(file,delimiter=';')
    concentrations = np.array([float(row[0]) for row in csvreader])
    print(concentrations)

distances_linear = distance_prediction(concentrations,param_iron)
print(distances_linear)
distance_esb_linear = np.mean(distances_linear)
print(distance_esb_linear)

distances_exp = distance_prediction_exponential_model(concentrations,param_iron_log)
print(distances_exp)
distance_esb_exp = np.mean(distances_exp)
print(distance_esb_exp)


# uncertanty of final distances 
def uncertainty(concentrations,iron,distance_iron,param,model,model_prediction):
    variance_distance = np.sum((distance_iron-model_prediction(iron,param))**2)/(len(iron)-2)
    variance_a = variance_distance/(np.sum((distance_iron-np.mean(distance_iron))**2))
    variance_b = variance_distance*(1/len(iron)+(np.mean(iron))**2/(np.sum((distance_iron-np.mean(distance_iron))**2)))
    variance_prediction = variance_distance*(1+1/len(iron)+np.sum((concentrations-np.mean(iron))**2)/(np.sum((distance_iron-np.mean(distance_iron))**2)))
    return np.sqrt(variance_prediction)



print(f"For linear model :\nsigma = {uncertainty(concentrations,iron,distance_iron,param_iron,model_linear,distance_prediction)}m")
print(f"For exponential model :\nsigma = {uncertainty(concentrations,iron,distance_iron,param_iron_log,model_exponential,distance_prediction_exponential_model)}m")
