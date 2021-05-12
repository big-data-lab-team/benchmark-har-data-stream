Numerical precision, classification accuracy, and memory footprint in the Mondrian Forest
=============================================================================================

This repository contains the script, the datasets, and the source code to
conduct a benchmark of the OrpailleCC Mondrian Tree implementation for numerical 
precision. The original paper was proposed in [here]. The results are available 
in the results branch.

Requirements
------------
This benchmark requires the following software:
- git: to download the source codes, the modules, and the datasets.
- gcc: to compile.
- perf: to evaluate the resource usage, in particular, the runtime and the energy.
- pandas, seaborn, matplotlib: to plot the figures.
- log4cpp: log4cpp is a requirement for streamDM-Cpp.

Setup the repository
--------------------
First we clone the repository and we initialize the submodules.

mkdir verificarlo_results &&\
bash mkdirs.sh
```
git clone --depth=1 https://github.com/MarkCycVic/mondrian-veripaille.git veripaille
cd veripaille
git submodule init
git submodule update
```

Then we compile streamDM-Cpp. To get a static library, we patch the Makefile.
```
patch streamDM-Cpp/makefile streamdm_patch
cd streamDM-Cpp
make -j 8 static
cd ..
```
Then, to setup the node version, we copy the necessary files.
```
cp mondrian_node.hpp OrpailleCC/src/mondrian.hpp
echo DO_two_Makefile_s
```
If, however, you wish to test the whole instrumentation, copy the following.
```
cp mondrian_whole.hpp OrpailleCC/src/mondrian.hpp
echo DO_two_Makefile_s
```
Then we extract the datasets and we place the dataset in memory.
```
tar xf datasets.tar.xz &&\
mkdir tmp &&\
cp *.log tmp
```
Then we compile all the binary to run the experiment.
```
mkdir bin
./setup.sh CXX=g++-7
```
The setup.sh script take care of compiling the binary files and placing these files into a directory related to the dataset name.
Then we create all the directories necessary for result output.
```
mkdir verificarlo_results
./mkdirs.sh
```


To run the experiment on a single precision, simply run verificarlo at a single precision and exponent length:
```
./run_1_verificarlo.sh PRECISION EXPONENT
```
Setup the Docker image
--------------------
Simply run the Dockerfile as follows:

```
docker build --build-arg="node" -t IMAGENAME .
```
We rely of two overarching bash file: main.sh and task.sh. task.sh are the slurm adapted .sh file to run a single model on your image.
main.sh is a loop on task.sh, to attempt all precisions and exponent combinations wanted.
Simply change those two files to your environment and purposes, and run:
```
./main.sh
```
Setup the Singularity image
--------------------
```
singularity build IMAGENAME docker://vicuna/verificarloorpaille
```

From the experiment results, we generate the plots (Figure 1-3) with the following command:
```
python3 plot_verificarlo.py
```



Regenerating MOA datasets
-------------------------

The MOA dataset can be regenerated with the command `make moa` even
though they are also stored in datasets.tar.xz.  MOA archive is available
[here](https://sourceforge.net/projects/moa-datastream/). You can download it
and place it in the repository under the name *moa* or you can modify the
variable *MOA_DIR* in the Makefile. Then you'll need to modify the arff files
to remove the header and change the tabulation into commas and rename the class
name to actual numbers starting at zero.


Result Structure
----------------
The results are split in three files:
- models.csv
- output 
- output_runs

The models.csv file contains information about the runs.
- model_id: a primary key that identify each models (algorithm+parameter+dataset).
- name: the algorithm's name.
- file: the dataset used.
- parameters: the other field are the parameter of the algorithm.

The file output_runs contains information about each repetition:
- model_id: the id of the model.
- run_id: the id of the repetition.
- time: the runtime in seconds.
- energy: the energy used in joules.
- power: the power consumption in watts.

The file output is a CSV file split in these columns:
- model_id: the id of the model seen in models.csv.
- run_id: the id of the repetition, which is often a number between 0 and the number of repetitions.
- element_count: the number of data point seen so far.
- seed: the seed used for that repetition.
- accuracy: the accuracy updated with the last data point.
- f1: the F1 score updated with the last data point.
- memory: The amount of memory used.

Adding a dataset
----------------
To add a new dataset, you need a CSV file where each line is a data point and
the last field of that line is an integer that represents the class of the data
point.  Then you need to add a make command in the script *setup.sh* to have
the binary files place in the proper directory. The name of that directory
should be the name of the dataset file.

Then, you'll need to modify the function *final_list* in *makefile.py* to
append the name of the new dataset to the list.


Hyperparameters
---------------

*** Mondrian Forest

Hyperparameters used for Mondrian:

| Number of trees | Base count | Discount | Budget |
|-----------------|------------|----------|--------|
| 1               | 0.0        | 1.0      | 1.0    |
| 5               | 0.0        | 1.0      | 0.4    |
| 10              | 0.0        | 1.0      | 0.4    |
| 50              | 0.0        | 1.0      | 0.2    |



