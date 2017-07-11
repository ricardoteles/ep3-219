#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

int size, rank, msg, tag;
double c_x_min;
double c_x_max;
double c_y_min;
double c_y_max;

double pixel_width;
double pixel_height;

int iteration_max = 200;

int image_size;
int*iteration_buffer;
int *iteration_buffer_MASTER;
unsigned char **image_buffer_MASTER;
char modo[5];

int i_x_max;
int i_y_max;
int image_buffer_size;
int image_buffer_size_MASTER;

int gradient_size = 16;
int colors[17][3] = {
                        {66, 30, 15},
                        {25, 7, 26},
                        {9, 1, 47},
                        {4, 4, 73},
                        {0, 7, 100},
                        {12, 44, 138},
                        {24, 82, 177},
                        {57, 125, 209},
                        {134, 181, 229},
                        {211, 236, 248},
                        {241, 233, 191},
                        {248, 201, 95},
                        {255, 170, 0},
                        {204, 128, 0},
                        {153, 87, 0},
                        {106, 52, 3},
                        {0, 0, 0},
                    };
void allocate_image_buffer_MASTER(){
    int rgb_size = 3;
    image_buffer_MASTER = (unsigned char **) malloc(sizeof(unsigned char *) * image_buffer_size_MASTER);

    for(int i = 0; i < image_buffer_size_MASTER; i++){
        image_buffer_MASTER[i] = (unsigned char *) malloc(sizeof(unsigned char) * rgb_size);
    };
}

void desallocate_image_buffer_MASTER(){  
    for(int i = 0; i < image_buffer_size_MASTER; i++)
        free(image_buffer_MASTER[i]);
    free(image_buffer_MASTER);    
}

void allocate_iteration_buffer_MASTER(){
    //alocar vetor completo de iteracoes
    iteration_buffer_MASTER = (int *) malloc(sizeof(int ) * image_buffer_size_MASTER);
};

void desallocate_iteration_buffer_MASTER(){
    free(iteration_buffer_MASTER);
};

void allocate_iteration_buffer_maquina(){
    //alocar pedaco do vetor a ser computado pelo maquina
    
    if (rank == size - 1)
        image_buffer_size += (image_buffer_size_MASTER % size);
    iteration_buffer = (int *) malloc(sizeof(int ) * image_buffer_size);
};

void desallocate_iteration_buffer_maquina(){
    free(iteration_buffer);
};

void init(int argc, char *argv[]){
    if(argc < 7) {
        printf("usage: mpirun -np #numMaquinas mandelbrot_seq c_x_min c_x_max c_y_min c_y_max image_size modo_operacao\n");
        printf("image_size = {2^4 = 16, 32, 64, ... , 2^13 = 8192}\n");
        printf("modo_operacao = {com, sem}\n");
        printf("examples with image_size = 11500:\n\n");
        printf("    Full Picture:         mpirun -np 4 mandelbrotOpenMPI_seq -2.5 1.5 -2.0 2.0 11500 com\n");
        printf("    Seahorse Valley:      mpirun -np 4 mandelbrotOpenMPI_seq -0.8 -0.7 0.05 0.15 11500 sem\n");
        printf("    Elephant Valley:      mpirun -np 4 mandelbrotOpenMPI_seq 0.175 0.375 -0.1 0.1 11500 com\n");
        printf("    Triple Spiral Valley: mpirun -np 4 mandelbrotOpenMPI_seq -0.188 -0.012 0.554 0.754 11500 sem\n");
        exit(0);
    }
    else {
        sscanf(argv[1], "%lf", &c_x_min);
        sscanf(argv[2], "%lf", &c_x_max);
        sscanf(argv[3], "%lf", &c_y_min);
        sscanf(argv[4], "%lf", &c_y_max);
        sscanf(argv[5], "%d", &image_size);
        sscanf(argv[6], "%s", &modo[0]);
        printf("MODO = %s I/O e alloc. memoria\n", &modo[0]);

        i_x_max           = image_size;
        i_y_max           = image_size;

        pixel_width       = (c_x_max - c_x_min) / i_x_max;
        pixel_height      = (c_y_max - c_y_min) / i_y_max;
    };
};

void update_rgb_buffer(int iteration, int x, int y){
    int color;

    if(iteration == iteration_max){
        color = 16;
    }
    else {
        color = iteration % gradient_size;
    };

    image_buffer_MASTER[(i_x_max * y) + x][0] = colors[color][0];
    image_buffer_MASTER[(i_x_max * y) + x][1] = colors[color][1];
    image_buffer_MASTER[(i_x_max * y) + x][2] = colors[color][2];
};

void write_to_file(){
    FILE * file;
    char * filename               = "outputOpenMPI_seq.ppm";
    char * comment                = "# ";

    int max_color_component_value = 255;

    file = fopen(filename,"wb");

    fprintf(file, "P6\n %s\n %d\n %d\n %d\n", comment,
            i_x_max, i_y_max, max_color_component_value);

    for(int i = 0; i < image_buffer_size_MASTER; i++){
        fwrite(image_buffer_MASTER[i], 1 , 3, file);
    };

    fclose(file);
};

void compute_mandelbrot(){
    double z_x;
    double z_y;
    double z_x_squared;
    double z_y_squared;
    double escape_radius_squared = 4;

    int iteration;
    int i_x;
    int i_y;
    int pos;
    int pos_min_maquina;
    int pos_max_maquina;

    double c_x;
    double c_y;

    if (rank != size- 1) {
        pos_min_maquina = image_buffer_size * rank;
        pos_max_maquina = image_buffer_size * (rank + 1);
    }

    else {        
        pos_max_maquina = image_buffer_size_MASTER;
        pos_min_maquina = image_buffer_size_MASTER - image_buffer_size;
    }  

    for(pos = pos_min_maquina; pos < pos_max_maquina; pos++) {

        i_y = pos / image_size;
        i_x = pos % image_size;

        c_y = c_y_min + i_y * pixel_height;

        if (fabs(c_y) < pixel_height / 2){
            c_y = 0.0;
        };

        c_x         = c_x_min + i_x * pixel_width;

        z_x         = 0.0;
        z_y         = 0.0;

        z_x_squared = 0.0;
        z_y_squared = 0.0;

        for(iteration = 0;
            iteration < iteration_max && \
            ((z_x_squared + z_y_squared) < escape_radius_squared);
            iteration++){
            z_y         = 2 * z_x * z_y + c_y;
            z_x         = z_x_squared - z_y_squared + c_x;

            z_x_squared = z_x * z_x;
            z_y_squared = z_y * z_y;
        };

        // as duas versões devem executar a condição do if
        if (modo[0] == 'c') {
            iteration_buffer[pos % image_buffer_size] = iteration;
        }

    }
};


int main(int argc, char *argv[]){
    int *displs = NULL, *rcounts = NULL, pos;
    init(argc, argv);
    image_buffer_size_MASTER = image_size * image_size;    

    MPI_Status stat;        
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    // as duas versões devem executar a condição dos ifs 
    // de qualquer forma
    image_buffer_size = image_buffer_size_MASTER / size;
    if (modo[0] == 'c')
        allocate_iteration_buffer_maquina();

    compute_mandelbrot();

    if (modo[0] == 'c') {
        if (rank == 0)
            rcounts = (int *)malloc(size * sizeof(int));
        MPI_Gather(&image_buffer_size, 1, MPI_INT, rcounts, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        if (rank == 0) {
            allocate_iteration_buffer_MASTER();
            displs = (int *)malloc(size * sizeof(int));
            for (int i = 0; i < size; i++) {
                displs[i] = i * image_buffer_size;
            }
        }
        MPI_Gatherv(iteration_buffer, image_buffer_size, MPI_INT, iteration_buffer_MASTER, rcounts, displs, MPI_INT, 0, MPI_COMM_WORLD);
        desallocate_iteration_buffer_maquina();

        free(displs);
        free(rcounts);
        if (rank == 0) {            
            allocate_image_buffer_MASTER();
            for(pos = 0; pos < image_buffer_size_MASTER; pos++)
                update_rgb_buffer(iteration_buffer_MASTER[pos], (pos % image_size), (pos / image_size));
            desallocate_iteration_buffer_MASTER();          
            write_to_file();
            desallocate_image_buffer_MASTER();          
        }    
    }    

    MPI_Finalize(); 
    return 0;
};