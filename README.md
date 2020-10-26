paper-benchmark
===============

Setup the repository
--------------------------
First we clone the repository and we initialize the submodules.
```
git clone https://github.com/azazel7/paper-benchmark.git benchmark
cd benchmark
git submodule init
git submodule update
```

Then we compile streamDM-Cpp. To get a static library, we patch the Makefile.
```
patch streamDM-Cpp/makefile streamdm_patch
cd streamDM-Cpp
make static
cd ..
```

Then we compile all the binary to run the experiment.
```
mkdir bin
./setup.sh
```
The setup.sh script take care of compiling the binary files and placing these files into a directory related to the dataset name.

```
tar xf datasets.tar.xz
cp *.log /tmp
rm -rf results_9
mkdir results_9
make run
cp models.csv /tmp/output /tmp/output_runs .
```

```
make process
make process_calibration
```

Generating latex
----------------

The latex code to compile the skeleton for the benchmark.

```
python makefile.py latex
```

or

```
cd paper
make
```


Setup on rapl-tool
------------------
This procedure works for both Ubuntu and Archlinux.
Before using rapl-tool, you will need to load the msr module and adjust the permissions.

```
# Install and load the msr module
sudo apt-get install msr-tools
sudo modprobe msr

# Set permissions
sudo chmod o+rw /dev/cpu/0/msr
```

Recent versions of the linux kernel require special permission to access the msr.
```
sudo apt-get install libcap2-bin
sudo setcap cap_sys_rawio+ep ./AppPowerMeter
sudo setcap cap_sys_rawio+ep ./PowerMonitor
```

Notes
-----
Turn datafile into ARRF file.
sed 's/\(.*\)\..*/\1/' a.log | ag -v ',0$' > final_a.log


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

