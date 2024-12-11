import matplotlib.pyplot as plt
import numpy as np
import csv


# reading file
with open('data.csv', newline = '') as file:
    csvreader = csv.reader(file, delimiter = ';')
    data = np.array([[float(elem) for elem in row] for row in csvreader])
    print(data)


# seperating data into 1D arrays for each pollutant
weight = data[:,0]
calcium = data[:,1]
cadmium = data[:,2]
copper = data[:,3]
iron = data[:,4]
zinc = data[:,5]
distance = data[:,6]

# for calcium
# the calcium data was part of the given data but it is not typically considered as a pollutant, so we will skip the data for calcium


# for cadmium
# plt.scatter(distance,cadmium)
# plt.title('cadmium concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('cadmium concentration in 10^-2 g/L')
# plt.savefig('initial_cadmium.png')
# plt.show()

# after plotting the data, we decided to eliminate the outliers in the cadmium data (it is a datapoint that is significantly different from other observations)
cadmiumv2 = np.array([i for i in cadmium if i<120])
distancev2 = np.array([distance[i] for i in range(len(cadmium)) if cadmium[i]<120])
# plt.scatter(distancev2,cadmiumv2)
# plt.title('cadmium concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('cadmium concentration in 10^-2 g/L')
# plt.savefig('fixed_cadmium.png')
# plt.show()

# # with log scale on y axis
cadmium_log = np.log(cadmiumv2)
plt.scatter(distancev2,cadmium_log)
plt.title('log of cadmium concentration as a function of distance')
plt.xlabel('distance to emissary in m')
plt.ylabel('log of cadmium concentration in 10^-2 g/L')
plt.savefig('fixed_cadmium_log.png')
plt.show()


# for copper
# plt.scatter(distance,copper)
# plt.title('copper concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('copper concentration in 10^-2 g/L')
# plt.savefig('initial_copper.png')
# plt.show()
# after plotting the data, we decided not to consider this pollutant because the concentration and the distance did not seem to be correlated


# # for iron
# plt.scatter(distance,iron) #pas mal
# plt.title('iron concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('iron concentration in 10^-2 g/L')
# plt.savefig('initial_iron.png')
# plt.show()

# # after plotting the data, we decided to eliminate the outliers in the iron data (it is a datapoint that is significantly different from other observations)
ironv2 = np.array([i for i in iron if i<500 and i>100])
distancev3 = np.array([distance[i] for i in range(len(iron)) if iron[i]<500 and iron[i]>100])
# plt.scatter(distancev3,ironv2)
# plt.title('iron concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('iron concentration in 10^-2 g/L')
# plt.savefig('fixed_iron.png')
# plt.show()

# # with log scale on y axis
iron_log = np.log(ironv2)
plt.scatter(distancev3,iron_log)
plt.title('log of iron concentration as a function of distance')
plt.xlabel('distance to emissary in m')
plt.ylabel('log of iron concentration in 10^-2 g/L')
plt.savefig('fixed_iron_log.png')
plt.show()

# for zinc
# plt.scatter(distance,zinc) 
# plt.title('zinc concentration as a function of distance')
# plt.xlabel('distance to emissary in m')
# plt.ylabel('zinc concentration in 10^-2 g/L')
# plt.savefig('initial_zinc.png')
# plt.show()
# after plotting the data, we decided not to consider this pollutant because the concentration and the distance did not seem to be correlated


# after this initial plotting, we decided to only consider iron and cadmium, we noticed a linear relation for those pollutants

# we create new csv files for iron and cadmium concentrations
# for iron
combined = np.column_stack((distancev3,ironv2))
np.savetxt("fixed_data_iron.csv",combined,delimiter=';',fmt='%f')

# for log of iron
combined = np.column_stack((distancev3,iron_log))
np.savetxt("fixed_data_iron_log.csv",combined,delimiter=';',fmt='%f')

# for cadmium
combined = np.column_stack((distancev2,cadmiumv2))
np.savetxt("fixed_data_cadmium.csv",combined,delimiter=';',fmt='%f')

# for log of cadmium
combined = np.column_stack((distancev2,cadmium_log))
np.savetxt("fixed_data_cadmium_log.csv",combined,delimiter=';',fmt='%f')

# https://www.youtube.com/watch?v=vG6tDQc86Rs