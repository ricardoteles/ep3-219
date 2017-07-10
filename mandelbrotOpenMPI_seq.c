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
unsigned char **image_buffer;
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

    image_buffer_size_MASTER = image_size * image_size;
    image_buffer_MASTER = (unsigned char **) malloc(sizeof(unsigned char *) * image_buffer_size_MASTER);
    
    for(int i = 0; i < image_buffer_size_MASTER; i++){
        image_buffer_MASTER[i] = (unsigned char *) malloc(sizeof(unsigned char) * rgb_size);
    };
}

void allocate_image_buffer_maquina(){
    int rgb_size = 3;

    //alocar so a faixa a ser computada pelo maquina
    if (rank == size - 1)
        image_buffer_size = (image_size - (rank * ((image_size - 1) / size + 1))) * image_size;
    else
        image_buffer_size = ((image_size - 1) / size + 1) * image_size; //faixa final da imagem computada pela ultima maq
    

    image_buffer = (unsigned char **) malloc(sizeof(unsigned char *) * image_buffer_size);

    for(int i = 0; i < image_buffer_size; i++){
        image_buffer[i] = (unsigned char *) malloc(sizeof(unsigned char) * rgb_size);
    };
};

void init(int argc, char *argv[]){
    if(argc < 7){
        printf("usage: ./mandelbrot_seq c_x_min c_x_max c_y_min c_y_max image_size modo_operacao\n");
        printf("image_size = {2^4 = 16, 32, 64, ... , 2^13 = 8192}\n");
        printf("modo_operacao = {com, sem}\n");
        printf("examples with image_size = 11500:\n\n");
        printf("    Full Picture:         ./mandelbrot_seq -2.5 1.5 -2.0 2.0 11500 com\n");
        printf("    Seahorse Valley:      ./mandelbrot_seq -0.8 -0.7 0.05 0.15 11500 sem\n");
        printf("    Elephant Valley:      ./mandelbrot_seq 0.175 0.375 -0.1 0.1 11500 com\n");
        printf("    Triple Spiral Valley: ./mandelbrot_seq -0.188 -0.012 0.554 0.754 11500 sem\n");
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

    image_buffer[(i_x_max * y) + x][0] = colors[color][0];
    image_buffer[(i_x_max * y) + x][1] = colors[color][1];
    image_buffer[(i_x_max * y) + x][2] = colors[color][2];
};

void write_to_file(){
    FILE * file;
    char * filename               = "output_seq.ppm";
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

    double c_x;
    double c_y;
    int i_y_min_maquina = rank * ((i_y_max - 1) / size + 1);
    int i_y_max_maquina = (rank + 1) * ((i_y_max - 1) / size + 1);
    if (i_y_max_maquina > i_y_max)
        i_y_max_maquina = i_y_max;

    for(i_y = i_y_min_maquina; i_y < i_y_max_maquina; i_y++) {
        c_y = c_y_min + i_y * pixel_height;

        if (fabs(c_y) < pixel_height / 2){
            c_y = 0.0;
        };

        for(i_x = 0; i_x < i_x_max; i_x++){
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
                update_rgb_buffer(iteration, i_x, i_y - i_y_min_maquina);
            }
        };
    };
};


int main(int argc, char *argv[]){
    init(argc, argv);
    
    if (modo[0]=='c')
    	allocate_image_buffer_MASTER();

    MPI_Status stat;
        
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    // as duas versões devem executar a condição dos ifs 
    // de qualquer forma
    if (modo[0] == 'c') {
        allocate_image_buffer_maquina();
    }

    compute_mandelbrot();
printf ("++++++++%d %d\n", rank, size);
    
	MPI_Barrier(MPI_COMM_WORLD);
    // MPI_Gather(image_buffer, image_buffer_size, MPI_INT, image_buffer_MASTER, image_buffer_size, MPI_INT, 0, MPI_COMM_WORLD);
	int cont = 0;
    		

	printf ("size = %d\n", size);
    while(cont < size){
    	printf ("cont = %d\n", cont);
		MPI_Send(image_buffer, image_buffer_size, MPI_INT, 0, 0, MPI_COMM_WORLD);
        MPI_Recv(image_buffer_MASTER + (cont * ((i_y_max - 1) / size + 1)) * (i_x_max), image_buffer_size, MPI_INT, cont, 0, MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        // MPI_Recv(image_buffer, image_buffer_size, MPI_INT, rank, 0, MPI_COMM_WORLD,MPI_STATUS_IGNORE);
		cont++;
    }

printf ("========%d %d\n", rank, size);
    // MPI_Barrier(MPI_COMM_WORLD);
    

    if (modo[0] == 'c' && rank == 0) {
        write_to_file();
    }
    MPI_Finalize(); 
    return 0;
};