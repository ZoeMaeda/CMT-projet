# Computational Methods and Tools - Project : River pollution regression

## Project description

This program find a linear and an exponential realtion between pollution concentration in fish and distance to emitter. Then given a concentration will find an estimation of the distance to the pollution emmiter.

The program will:
1. Read in initial data of concentration and distance provided by Professor Jean-Christophe Loubier (HES-SO Valais-Wallis) and print graphs ("*premiersgraphs.py*").
2. Find the parameters of the relation between pollution concentration and distance to emitter using two model : exponetial and linear ("*regression_lineaire.c*").
3. Graph data and model obtained, and predict distance to emitter given pollution concentration with the uncertanty.

## Project structure

- "*initial*" contains input data for the regression and for the prediction
- "*internal_data*" contains files used for passing information between C and Python. They are automatically edited by the program and should not be manually modified.
- "*code*" contains program code.
- "*results*" contains saved .jpg files of graphs and final parameters.

### Inputs and Outputs

Inputs:
- "*data.csv*" is a semicolon-delimited file.
- "*ennui_sur_blase.csv*" is a semicolon-delimited file.

Internal files:
- "*fixed_data_cadmium.csv*" is a semicolon-delimited file.
- "*fixed_data_cadmium_log.csv*" is a semicolon-delimited file.
- "*fixed_data_iron.csv*" is a semicolon-delimited file.
- "*fixed_data_iron_log.csv*" is a semicolon-delimited file.

Outputs:
- "*results*" contains several image files, each has a custom name of format: "fixed_iron.png". You can save them or delete them as required.
- "*param.csv*" contains parameters that were found by regression.
- "*results.txt*" is a text file containing summarized information of the simulation, such as final distance to pollution emitter uncertanty of this result using thw two models. Do **not** delete this file.

## Implementation details

**Overview:**
- Python reads initial data, prints graphs, eliminates outliers and writes new data with selected data and without outliers modifies some of the data (applies log of certain data).
- C reads internal data values.
- The regression is handled by C. It directly outputs the found parameters into a CSV file.
- Python also handles the output, visualisation of the models, prediction of the distance with uncertainty given concentration of pollutant.

**Structure**: In the directory "*Code/*" are located:
- "*premiersgraphs.py*"
    - Imports csv, numpy and matplotlib.pyplot as a module
    - Reads in the CSVs located in "*data.csv*".
    - Selects wanted data : concentrations of pollutants
    - Plots concentration of different pollution concentrations as a function of distance to emitter, eliminating the outliers, and replotting data.
    - Returns new data and ln of data.
- "*regression_lineaire.c*"
    - Includes <stdio.h>, <stdlib.h> and <string.h> libraries.
    - Calculates mean square error, gradient of given data using functions.
    - Uses these functions find parameters of models using a gradients descent.
    - Writes found parameters into a csv file "*param.csv*".
- "*final_graph_prediction.py*"
    - Imports csv, numpy and matplotlib.pyplot as a module
    - Reads in "*param.csv*", "*fixed_data_iron.csv*", "*fixed_data_iron_log.csv*", "*fixed_data_cadmium.csv*", "*fixed_data_cadmium_log.csv*"
    - Plot data and each models individually using parameters in "*param.csv*" and comparision between models.
    - Exports graphs as "*comparision_cadmium.png*", "*prediction_cadmium.png*", ...

## Instructions

To reproduce results in the report, three steps should be followed:
1. Navigate to the "*premiersgraphs.py*" function located in the "code" directory. The program should be run, and will open eight plotting windows one after the other, save them and save internal data.
2. Navigate to the "*regression_lineaire.c*" function located in the "code" directory. This program should be run using terminal or run button. "*param.csv*" will be saved.
3. Navigate to the "*final_graph_prediction.py*" function located in the "code" directory. The program should be run, and will open 6 plotting windows one after the other, save them and return in the terminal :
   predicted distance using linear model :
   standard deviation using linear model :
   predicted distance using exponetial model :
   standard deviation using exponetial model :
## Requirements

Versions of Python and C used are as follows.
```
$ python --version
Python 3.9.12

$ gcc --version
Apple clang version 15.0.0
```
The Python libraries utilized were taken from anaconda :
```

numpy 1.26.4 py311h728a8a3_0  

matplotlib 3.8.4 py311hecd8cb5_0   

csv 1.0
```

## Credits

### Data

The data file "*data.csv*" was provided by Professor Jean-Christophe Loubier (HES-SO Valais-Wallis).

The data from "*ennui_sur_blase.csv*" was made up by ourselves.

### Formulae

The function gradient descent relies on the algoritm generally attributed to Augustin-Louis Cauchy. An overview of the method is available in this article : Gradient Descent in Machine Learning: A Basic Introduction (https://builtin.com/data-science/gradient-descent).

The statistical knowledge was taken from the statistics class we had.
