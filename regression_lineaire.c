#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int ReadFile(char * name,double mat[][2]){
    char buffer[1024] ;
    char *record,*line;
    int i=0,j=0;
    double temp;

    FILE *fstream = fopen(name,"r");
    if(fstream == NULL){
        printf("\n file opening failed ");
        return -1 ;
    }
    while((line=fgets(buffer,sizeof(buffer),fstream))!=NULL){
        record = strtok(line,";");
        j = 0;
        while(record != NULL){
            // printf("%s ",record) ;    //here you can put the record into the array as per your requirement.
            temp = atof(record);
            mat[i][j++] = temp;
            record = strtok(NULL,";");
        }
        i++;
    }
    return 0;
}

void print_mat(double mat[][2], int row){
    for (int r = 0;r <row;r++){
        for (int c=0;c<2;c++){
            printf("%0.3f ",mat[r][c]);        
        }
        printf("\n");
    }
}

void extract_data(double data[][2],double distance[],double concentration[],int n){
    for (int i = 0;i <n;i++){
        distance[i] = data[i][0];
        concentration[i] = data[i][1];
    }
}


// implementing linear model
void linear_model(double distance[],double param[2],double model[],int n){ 
    for (int i = 0;i<n;i++){
        model[i] = param[0]*distance[i]+param[1];
    }
}

double mean_square_error(double distance[],double concentration[],double param[],int n){
    double total;
    double model[n];
    linear_model(distance,param,model,n);
    for (int i = 0;i<n;i++){
        total += (model[i]-concentration[i])*(model[i]-concentration[i]);
    }
    return total/(2*n);
}

void gradient(double distance[],double concentration[],double param[2],double gradient[2],int n){
    double model[n];
    linear_model(distance,param,model,n);
    for (int i = 0;i<n;i++){
        gradient[0] += (distance[i])*(model[i]-concentration[i]);
        gradient[1] += (model[i]-concentration[i]);
    }
    gradient[0] /= n;
    gradient[1] /= n;
}

void gradient_descent(double distance[],double concentration[],double param[2],double final_param[2],int n,double tol,double learning_rate){
    // blocked = 0
    // while mean_squared_error(X,Y,param) > tol and blocked < 20:
    //     mse_init = mean_squared_error(X_distance_iron,iron,param)
    //     param_temp = param - learning_rate*(gradient(X,Y,param))
    //     # print(f"mae = {mean_squared_error(X,Y,param_temp)}")
    //     if mean_squared_error(X,Y,param_temp)<mse_init:
    //         blocked = 0
    //         param = param_temp
    //         learning_rate *= 1.5
    //     else:
    //         blocked += 1
    //         learning_rate *= 0.5
    // return param
    int blocked = 0;
    double mse;
    double grad[2];
    double temp_param[2];
    temp_param[0] = param[0];
    temp_param[1] = param[1];
    final_param[0] = param[0];
    final_param[1] = param[1];
    while (mean_square_error(distance,concentration,final_param,n) > tol && blocked<20){
        mse = mean_square_error(distance,concentration,final_param,n);
        gradient(distance,concentration,final_param,grad,n);
        temp_param[0] = final_param[0] - learning_rate*grad[0];
        temp_param[1] = final_param[1] - learning_rate*grad[1];
        printf("mse = %f\n",mean_square_error(distance,concentration,final_param,n));
        if (mean_square_error(distance,concentration,temp_param,n)<mse){
            blocked = 0;
            final_param[0] = temp_param[0];
            final_param[1] = temp_param[1];
            learning_rate *= 2;
        } else {
            blocked += 1;
            learning_rate *= 0.5;
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
    // for (int i = 0;i<22;i++){
    //     printf("%f %f %f\n",distance_iron[i],iron[i],iron_log[i]);
    // }
    // printf("\n");
    // for (int i = 0;i<19;i++){
    //     printf("%f %f %f\n",distance_cadmium[i],cadmium[i],cadmium_log[i]);
    // }
    
    double initial_param_iron[] = {-0.5,400};
    double final_param_iron[] = {-0.5,400};
    gradient_descent(distance_iron,iron,initial_param_iron,final_param_iron,22,745,0.01);
    printf("%f %f\n",final_param_iron[0],final_param_iron[1]);
    return 0;

    
}
