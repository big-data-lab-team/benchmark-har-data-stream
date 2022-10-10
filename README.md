Mondrian Forest Under Memory Constraints
========================================

This repository contains the script, the datasets, and the source code to
conduct a benchmark of Mondrian Forest under Memory Constraints. The original study was proposed
in [todo](). The results were obtained with the
version 1.1 of this repository.

Requirements
------------
This benchmark requires the following software:
- git: to download the source codes, the modules, and the datasets.
- gcc: to compile.
- pandas, seaborn, matplotlib: to plot the figures.

Setup the repository for Mondrian Forest under Memory Constraints
-----------------------------------------------------------------
First we clone the repository and we initialize the submodules.
```
git clone https://github.com/big-data-lab-team/benchmark-har-data-stream.git benchmark
cd benchmark
git submodule init
git submodule update
```

Then we compile all the binary to run the experiment.
```
./setup_xp1_xp2.sh
```
This script take care of compiling the binary files and placing these files into a directory related to the dataset name.

Then we extract the datasets and we place the dataset in memory.
```
tar xf datasets_xp1_xp2.tar.xz
cp *.log /tmp
```

To run the experiment, we rely on two more scripts.
```
./run_xp1.sh
./run_xp2.sh
```
Two directories are generated, results_xp1 and results_xp2.

From these results directories, we generate the plots with the following command:
```
./plot_xp1.py
./plot_xp2.py
```

Regenerating MOA datasets
-------------------------

The MOA dataset can be regenerated with the command `make moa_xp1_xp2` even
though they are also stored in datasets.tar.xz.  MOA archive is available
[here](https://sourceforge.net/projects/moa-datastream/). You can download it
and place it in the repository under the name *moa* or you can modify the
variable *MOA_DIR* in the Makefile. Then you'll need to modify the arff files
to remove the header and change the tabulation into commas and rename the class
name to actual numbers starting at zero.


Result Structure
----------------
The results are split in six directories containing the results for each datasets.
For a given dataset, there is one result file per method. For instance, the
file mondrian_t30_partial.csv contains the results for the Mondrian Forest with
30 trees with the Partial Update out-of-memory strategy.

An output file is a CSV file split in these columns:
- model_id: not used here.
- run_id: the id of the repetition, which is a number between 0 and the number of repetitions.
- element_count: the number of data point seen so far.
- seed: the seed used for that repetition.
- accuracy: the accuracy updated with the last data point.
- f1: the F1 score updated with the last data point.
- memory: The amount of memory used.

A benchmark of data stream classification for human activity recognition on connected objects
=============================================================================================

This repository contains the script, the datasets, and the source code to
conduct a benchmark of data stream classifiers. The original study was proposed
in [here](https://arxiv.org/abs/2008.11880). The results were obtained with the
version 1.0 of this repository.

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
```
git clone https://github.com/big-data-lab-team/benchmark-har-data-stream.git benchmark
cd benchmark
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

Then we compile all the binary to run the experiment.
```
mkdir bin
./setup_xp0.sh
```
This script take care of compiling the binary files and placing these files into a directory related to the dataset name.

Then we extract the datasets and we place the dataset in memory.
```
tar xf datasets_xp0.tar.xz
cp *.log /tmp
```

To run the experiment, we rely on the make command, then we collect the result
on the current directory. Note that `make run` can be replaced by `make
calibration` to run an extensive search on the parameter.
```
make run
cp models.csv /tmp/output /tmp/output_runs .
```

From the experiment results, we generate the plots (Figure 1-3) with the following command:
```
make plot_results
```

From the calibration results, we generate the plots (Figure 4,5) with this command:
```
make plot_hyperparameters
```

Regenerating MOA datasets
-------------------------

The MOA dataset can be regenerated with the command `make moa_xp0` even
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

Adding a classifier
-------------------
To add a new classifier, you need to code a C++ file that defines the function
*get_classifier* and that returns a classifier object. This object must implement
two functions: train and predict. The file *empty.cpp* is an example.

Once you have written the classifier code, you need to modify the Makefile so
it compiles it depending on the parameter provided to *make* such as
the number of features or the number of classes.

Finally, you will need to modify the function *final_list* in *makefile.py* to
add the classifier to each dataset.

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

Impact of the base count with 10 trees, a budget of 1.0, and a discount factor of 0.2.
![](paper/figures/calibration_mondrian_base.png)

Impact of the budget with 10 trees, a base count of 0.1, and discount factor of 0.2.
![](paper/figures/calibration_mondrian_discount.png)

Impact of the discount factor with 10 trees, a budget of 1.0, and a base count of 0.1.
![](paper/figures/calibration_mondrian_lifetime.png)

*** MCNN

Hyperparameters used for MCNN:
| Number of clusters | Error threshold | Participation threshold |
|--------------------|-----------------|-------------------------|
| 10                 | 2               | 10                      |
| 20                 | 10              | 10                      |
| 33                 | 16              | 10                      |
| 40                 | 8               | 10                      |
| 50                 | 2               | 10                      |

Error threshold tuning of \mcnn with the first subject of Banos et al dataset. Error threshold in parenthesis.
![](paper/calibration_mcnn.png)

References
----------
This repository is related to the following papers:
- M. Khannouz and T. Glatard, “Mondrian Forest for Data Stream Classification Under Memory Constraints,” 2022.
- Martin Khannouz and Tristan Glatard. A benchmark of data stream classification for human activity recognition on connected objects. Sensors (Basel, Switzerland), 20, 2020.
- M. Khannouz, B. Li, and T. Glatard, “OrpailleCC: a Library for Data Stream Analysis on Embedded Systems,” The Journal of Open Source Software, vol. 4, p. 1485, 07 2019.
