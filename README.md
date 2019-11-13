paper-benchmark
===============

Downloading the repository
--------------------------

```
git clone --recursive git@github.com:azazel7/paper-benchmark.git
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
