Numerical precision, classification accuracy, and memory footprint in the Mondrian Forest
=============================================================================================

This repository contains the script, the datasets, and the source code to
conduct a benchmark of the OrpailleCC Mondrian Tree implementation for numerical 
precision. The original paper was proposed in [here](https://www.overleaf.com/read/rtvpkqksbqxj). The results are available 
in the results branch.


Requirements
------------
This benchmark requires the following software:
- git: to download the source codes, the modules, and the datasets.
- gcc: to compile.
- pandas, seaborn, matplotlib: to plot the figures.
- log4cpp: log4cpp is a requirement for streamDM-Cpp.

Setup the repository
--------------------
We do not recommend this, as runs tend to be long and containerizing make more sense, especially in a SLURM context.

First, install Verificarlo, to allow numerical precision reduction.
All instructions are available in [here](https://github.com/verificarlo/verificarlo).

Then, install all the software needed.
```
apt update -y && apt install -y liblog4cpp5v5 liblog4cpp5-dev nano python3-tk git
apt install -y linux-tools-common linux-tools-generic linux-cloud-tools-generic build-essential
```
Then, we clone the repository and we initialize the submodules.

```
git clone --depth=1 https://github.com/MarkCycVic/mondrian-veripaille.git veripaille
cd veripaille
git submodule init
git submodule update
```

Then, we compile streamDM-Cpp. To get a static library, we patch the Makefile.
```
patch streamDM-Cpp/makefile streamdm_patch
cd streamDM-Cpp
make -j 8 static
cd ..
```
Then, to setup the node version, we copy the necessary files.
```
cp mondrian_node.hpp OrpailleCC/src/mondrian.hpp
cp Makefile_node Makefile
```
If, however, you wish to test the whole instrumentation, copy the following.
```
cp mondrian_whole.hpp OrpailleCC/src/mondrian.hpp
cp Makefile_whole Makefile
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

Setup the Docker image
----------------------
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
---------------------------
```
singularity build IMAGENAME docker://vicuna/verificarloorpaille
```

From the experiment results, refer to the ins
```
python3 plot_verificarlo.py
```
Testing
-------

Training is made through a single file: run_1_verificarlo.sh.
To verify your installation, run this file in the veripaille directory at a given precision (1-52) and a given exponent (2-11)
```
./run_1_verificarlo.sh PRECISION EXPONENT
```
To run many precisions using SLURM and containers, download the files task.sh and main.sh.

Then, adapt the task.sh file to your specific directories and container. 

Finally, adapt the for-loop in the main.sh file to run all the precisions and exponents you want. You can now run the main.sh file from outside your container.
```
./main.sh
```
By default, all datasets will be run. This can take up to 10 hours for node, 20 hours for whole (Compute Canada, Beluga, Scratch).
To run change the datasets run, modify line 156 of the makefile.py file to the intented datasets. For a simple and quick dataset, use banos_3.

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

Plotting, data analysis
-----------------------
Plots and results are available from two zip files available [here]. 
To plot, follow the instructions of the plot_veripaille.ipynb file.

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



