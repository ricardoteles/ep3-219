#! /bin/bash

set -o xtrace

NP=2
NTHREADS=4

MEASUREMENTS=10
SIZE=8192

NAMES=('mandelbrotOpenMPI_seq' 'mandelbrotOpenMPI_omp' 'mandelbrot_seq')
MODOS=('com' 'sem')


make
mkdir results
mkdir graphics

for NAME in ${NAMES[@]}; do
    mkdir results/$NAME
    mkdir graphics/$NAME


    for MODO in ${MODOS[@]}; do             
        for ((j = 1; j <= MEASUREMENTS; j++)); do
            if [ $NAME = 'mandelbrotOpenMPI_seq' ] 
            then    
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $MODO >> "full_mpi_$MODO.log" 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $MODO >> "seahorse_mpi_$MODO.log" 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $MODO >> "elephant_mpi_$MODO.log" 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $MODO >> "triple_spiral_mpi_$MODO.log" 2>&1
            elif [ $NAME = 'mandelbrotOpenMPI_omp' ] 
            then 
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $NTHREADS $MODO >> 'full_'$NTHREADS'_mpi_'$MODO'.log' 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $NTHREADS $MODO >> 'seahorse_'$NTHREADS'_mpi_'$MODO'.log' 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $NTHREADS $MODO >> 'elephant_'$NTHREADS'_mpi_'$MODO'.log' 2>&1
                perf stat -r 1 mpirun -np $NP -hostfile hostfile ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $NTHREADS $MODO >> 'triple_spiral_'$NTHREADS'_mpi_'$MODO'.log' 2>&1
            else
                perf stat -r 1 ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $MODO >> "full_$MODO.log" 2>&1
                perf stat -r 1 ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $MODO >> "seahorse_$MODO.log" 2>&1
                perf stat -r 1 ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $MODO >> "elephant_$MODO.log" 2>&1
                perf stat -r 1 ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $MODO >> "triple_spiral_$MODO.log" 2>&1
            fi
        done
                
        mv *.log results/$NAME
   done

done

#rm *.ppm




