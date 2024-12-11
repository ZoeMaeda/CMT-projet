#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int ReadFile(char * name,double mat[25][7]){
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
            mat[i][j] = temp;
            record = strtok(NULL,";");
            j++;
        }
        i++ ;
    }
    return 0;
}

int main(){
    double mat[25][7];
    ReadFile("data.csv",mat);
    for (int row = 0;row <25;row++){
        for (int col=0;col<7;col++){
            printf("%0.3f ",mat[row][col]);        
        }
        printf("\n");
    }
    printf("%f",mat[1][0]);
    return 0 ;
 }