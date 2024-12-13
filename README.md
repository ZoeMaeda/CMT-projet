# Computational Methods and Tools - Project : River pollution regression

## Project description

This program find a linear and an exponential realtion between pollution concentration in fish and distance to emitter. Then given a concentration will find an estimation of the distance to the pollution emmiter.

The program will:
1. Read in initial data of concentration and distance provided by Professor Jean-Christophe Loubier (HES-SO Valais-Wallis) and print graphs ("premiersgraphs.py").
2. Find the parameters of the relation between pollution concentration and distance to emitter using two model : exponetial and linear ("regression_lineaire.c").
3. Graph data and model obtained, and predict distance to emitter given pollution concentration with the uncertanty.

## Project structure

- "initial" contains input data for the regression and for the prediction
- "internal_data" contains files used for passing information between C and Python. They are automatically edited by the program and should not be manually modified.
- "code" contains program code.
- "results" contains saved .jpg files of graphs and final parameters.

### Inputs and Outputs

Inputs:
- "data.csv" is a semicolon-delimited file.
- "ennui_sur_blase.csv" is a semicolon-delimited file.

Internal files:
- "fixed_data_cadmium.csv" is a semicolon-delimited file.
- "fixed_data_cadmium_log.csv" is a semicolon-delimited file.
- "fixed_data_iron.csv" is a semicolon-delimited file.
- "fixed_data_iron_log.csv" is a semicolon-delimited file.

Outputs:
- "results" contains several image files, each has a custom name of format: "fixed_iron.png". You can save them or delete them as required.
- "param.csv" contains parameters that were found by regression.
- "results.txt" is a text file containing summarized information of the simulation, such as final distance to pollution emitter uncertanty of this result using thw two models. Do **not** delete this file.

## Implementation details

**Overview:**
- Python sends input values to C through a text file, which contains parameters selected by the user.
- The simulation is handled by C. It directly outputs the results of computation into a CSV file.
- Python also handles the output and visualisation.

**Structure**: In the directory "*Code/*" are located:
- "*RhineData.py*"
    - Reads in the CSVs located in "*Data*".
    - Computes average monthly values of river parameters : flowrate / temperature / dissolved oxygen...
- "*Parameterchoice.py*"
    - Imports "*RhineData.py*" as a module.
    - Writes all selected parameters ("*RhineData.py*" + pollution values) into a text file "*Internal/PythonParameters.txt*".
- "*Computations.c*"
    - Reads in "*Internal/PythonParameters.txt*".
    - Performs computations.
    - Exports results into the CSV "*Internal/CalculatedData.csv*".
- "*Visualisation.py*"
    - Executes the compiled C file.
    - Reads in the CSV "*Internal/CalculatedData.csv*".
    - Plots results in a separate window.
    - Saves key plots to directory "*Results*".
    - Writes a summary file to "*Results*".

## Instructions

To reproduce results in the report, four steps should be followed:
1. Navigate to the "*Parameterchoice.py*" function located in the "*Code*" directory. The function contains commented instructions for the user to modify input parameters. Modify as desired, and save the file.
2. Navigate to the makefile to ensure the Python interpreter selected is yours.
3. Open the terminal from the project root directory (location of this README.md file). You can check this is the case by typing:
    ```
    ls
    ```
    The terminal should return:
    ```
    Code    Data    Internal    README.md   Results    makefile
    ```
4. Run the following line in the terminal:
    ```
    make
    ```
The program will run automatically, and will open two plotting windows in full screen. Once you close them , the program cleans up compiled filed files and terminates automatically.

## Requirements

Versions of Python and C used are as follows.
```
$ python --version
Python 3.11.5

$ gcc --version
Apple clang version 14.0.0
```
The Python libraries utilized were the following:
```
pandas 2.1.4 py311hdb55bb0_0

numpy 1.26.0 py311h728a8a3_0  
numpy-base 1.26.0 py311h53bf9ac_0

subprocess 2.4

matplotlib 3.8.0 py311hecd8cb5_0  
matplotlib-base 3.8.0 py311h41a4f6b_0  
matplotlib-inline 0.1.6 py311hecd8cb5_0 

csv 1.0
```

## Credits

### Data

The data files "*Rhine_DO_Palmrainbrücke.csv*", "*Rhine_Flowrate_Rheinhalle.csv*"  and "*Rhine_Watertemperature_Palmrainbrucke.csv*" come from the [Swiss Federal Bureau for the Environment](https://www.bafu.admin.ch/bafu/en/home/topics/water/state/data/obtaining-monitoring-data-on-the-topic-of-water/hydrological-data-service-for-watercourses-and-lakes.html).

The data file "*Rhine_depth.csv*" comes from the [French eauFrance](hydro.eaufrance.fr).

The data file "*Rhine_windspeeds.txt*" comes from the [Swiss Federal Office of Meteorology](https://www.meteoswiss.admin.ch/services-and-publications/service/weather-and-climate-products/data-portal-for-teaching-and-research.html).

### Formulae

The function tracking dissolved oxygen relies on the [Streeter-Phelps](https://en.wikipedia.org/wiki/Streeter%E2%80%93Phelps_equation) equation, taken from Pearson's *[Introduction to Environmental Engineering and Science](https://www.pearson.com/en-gb/subject-catalog/p/introduction-to-environmental-engineering-and-science-pearson-new-international-edition/P200000004949/9781292025759)*.

The function tracking pollutant concentrations is based on the Van Genuchten equation, solved by Jin & al in *[Mitigation of impact of a major benzene spill into a river](https://www.sciencedirect.com/science/article/pii/S0043135420300257)*.
