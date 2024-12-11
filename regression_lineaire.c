#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int ReadFile(char * name,double mat[][2]){
    // reads file of name : name into 2D array with 2 colomns
    char buffer[1024] ;
    char *record,*line;
    int i=0,j=0;
    double temp;

    FILE *fstream = fopen(name,"r"); // opening file
    if(fstream == NULL){ // if file empty
        printf("\n file opening failed ");
        return -1 ;
    }
    while((line=fgets(buffer,sizeof(buffer),fstream))!=NULL){ // reading line by line
        record = strtok(line,";"); // takes string that is before first ";" in first line
        j = 0;
        while(record != NULL){
            temp = atof(record); // converting into a double
            mat[i][j++] = temp; 
            record = strtok(NULL,";"); // takes next element of line
        }
        i++;
    }
    return 0;
}

void print_mat(double mat[][2], int row){
    // printing 2D array is useful to visualise matrices when coding debugging
    for (int r = 0;r <row;r++){
        for (int c=0;c<2;c++){
            printf("%0.3f ",mat[r][c]);        
        }
        printf("\n");
    }
}

void extract_data(double data[][2],double distance[],double concentration[],int n){
    // extract data into 2 1D array
    for (int i = 0;i <n;i++){
        distance[i] = data[i][0];
        concentration[i] = data[i][1];
    }
}


// implementing linear model : y = x*a + b
// can be used as exponetnial model if y is replaced by log(y)
// as we want to return an array of the concentrations the function takes an additionnal array as a parameter and puts values in it
void linear_model(double distance[],double param[2],double model[],int n){ 
    for (int i = 0;i<n;i++){
        model[i] = 0;
        model[i] = param[0]*distance[i]+param[1];
    }
}

// mean square error to measure error between the model and observations
double mean_square_error(double distance[],double concentration[],double param[],int n){
    double total = 0;
    double model[n];
    linear_model(distance,param,model,n);
    for (int i = 0;i<n;i++){
        total += (model[i]-concentration[i])*(model[i]-concentration[i]);
    }
    return total/(2*n);
}

// gradient is the derivative of the mean square error function used in the gradient descent 
// returns values in array "gradient" passed as parameter
void gradient(double distance[],double concentration[],double param[2],double gradient[2],int n){
    double model[n];
    linear_model(distance,param,model,n);
    gradient[0] = 0;
    gradient[1] = 0;
    for (int i = 0;i<n;i++){
        gradient[0] += (distance[i])*(model[i]-concentration[i]);
        gradient[1] += (model[i]-concentration[i]);
    }
    gradient[0] /= n;
    gradient[1] /= n;
}

// returns new parameters in array "final_param" passed as parameter
void gradient_descent(double distance[],double concentration[],double param[2],double final_param[2],int n,double tol,double learning_rate){
    // calculates iteratively the best parameter for model by finding parameters that causes minimum mean square error
    // takes additonnal parameters :
    // tol : tolerence ie acceptable mean square error at which point the function can stop
    // learning rate : speed at which parameter change from an iteration to an other
    int blocked = 0; // after too many loops without change in parameters the function stops 
    // allocation space for gradient, temporary parameters and mean squared errors
    double grad[2];  
    double temp_param[2];
    temp_param[0] = param[0];
    temp_param[1] = param[1];
    final_param[0] = param[0];
    final_param[1] = param[1];
    double mse_temp = mean_square_error(distance,concentration,param,n);
    double mse_init = mean_square_error(distance,concentration,param,n);

    // gradient descent loop
    while (mse_temp > tol && blocked<20){
        mse_init = mean_square_error(distance,concentration,final_param,n);
        gradient(distance,concentration,final_param,grad,n);    // updating parameters
        temp_param[0] = final_param[0] - learning_rate*grad[0];
        temp_param[1] = final_param[1] - learning_rate*grad[1]; 
        mse_temp = mean_square_error(distance,concentration,temp_param,n);
        if (mse_temp<mse_init){ // update parameters only if it decreases mean square error
            blocked = 0;
            final_param[0] = temp_param[0];
            final_param[1] = temp_param[1];
            learning_rate *= 2;
        } else {
            blocked += 1;
            learning_rate *= 0.5; // decresing the learning rate for more precise change
        }
    }
}

int main(){
    // reading files 
    double iron_data[22][2];
    ReadFile("fixed_data_iron.csv",iron_data);
    double iron_log_data[22][2];
    ReadFile("fixed_data_iron_log.csv",iron_log_data);
    double cadmium_data[19][2];
    ReadFile("fixed_data_cadmium.csv",cadmium_data);
    double cadmium_log_data[19][2];
    ReadFile("fixed_data_cadmium_log.csv",cadmium_log_data);

    // seperating data into distance and concentration
    double distance_iron[22];
    double iron[22];
    double iron_log[22];
    double distance_cadmium[19];
    double cadmium[19];
    double cadmium_log[19];
    extract_data(iron_data,distance_iron,iron,22);
    extract_data(iron_log_data,distance_iron,iron_log,22);
    extract_data(cadmium_data,distance_cadmium,cadmium,19);
    extract_data(cadmium_log_data,distance_cadmium,cadmium_log,19);
    
    // estimating initial parameters
    double initial_param_iron[] = {-0.5,400};
    double final_param_iron[] = {-0.5,400};
    double inititial_param_iron_log[] = {-0.003,5.9};
    double final_param_iron_log[] = {-0.003,5.9};  
    double initial_param_cadmium[] = {-0.03,65};
    double final_param_cadmium[] = {-0.03,65};
    double initial_param_cadmium_log[] = {-0.001,4};
    double final_param_cadmium_log[] = {-0.001,4};

    // finding optimal parameters
    gradient_descent(distance_iron,iron,initial_param_iron,final_param_iron,22,745,0.01);
    gradient_descent(distance_iron,iron_log,inititial_param_iron_log,final_param_iron_log,22,0.02,0.01);
    gradient_descent(distance_cadmium,cadmium,initial_param_cadmium,final_param_cadmium,19,90,0.01);
    gradient_descent(distance_cadmium,cadmium_log,initial_param_cadmium_log,final_param_cadmium_log,19,0.2,0.001);

    // writing to parameters to file 
    FILE *file;
    file = fopen("param.csv", "w+");
    fprintf(file,"%f;%f\n",final_param_iron[0],final_param_iron[1]);
    fprintf(file,"%f;%f\n",final_param_iron_log[0],final_param_iron_log[1]);
    fprintf(file,"%f;%f\n",final_param_cadmium[0],final_param_cadmium[1]);
    fprintf(file,"%f;%f\n",final_param_cadmium_log[0],final_param_cadmium_log[1]);
    fclose(file);
    return 0;
}
