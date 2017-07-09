OUTPUT=mandelbrotOpenMPI

IMAGE=.ppm

CC=mpicc
CC_OPT=-std=c11

CC_OMP=-fopenmp

.PHONY: all
all: $(OUTPUT)_omp $(OUTPUT)_seq

$(OUTPUT)_omp: $(OUTPUT)_omp.c
	$(CC) $(CC_OPT) $(CC_OMP) $(OUTPUT)_omp.c -o $(OUTPUT)_omp

$(OUTPUT)_seq: $(OUTPUT)_seq.c
	$(CC) $(CC_OPT) $(OUTPUT)_seq.c -o $(OUTPUT)_seq

.PHONY: clean
clean:
	rm $(OUTPUT)_omp $(OUTPUT)_seq *$(IMAGE)
