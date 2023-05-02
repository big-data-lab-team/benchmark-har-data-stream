OrpailleCC_DIR=$(shell pwd)/OrpailleCC
OrpailleCC_INC=$(OrpailleCC_DIR)/src
StreamDM_DIR=$(shell pwd)/streamDM-Cpp
#MOA_DIR=$(shell pwd)/MOA
MOA_DIR=/home/magoa/phd/moa
MOA_COMMAND=java -Xmx512m -cp "$(MOA_DIR)/lib/moa-2019.05.0:$(MOA_DIR)/lib/*" -javaagent:$(MOA_DIR)/lib/sizeofag-1.0.4.jar moa.DoTask
PYTHON_COMMAND=python
ifndef LABEL_COUNT
LABEL_COUNT=33
endif
ifndef FEATURES_COUNT
FEATURES_COUNT=6
endif
ifdef BANOS
BANOS_FLAG=-DBANOS
endif
ifndef MEMORY_SIZE
MEMORY_SIZE=600000
endif
ifdef NN_TRAIN
NN_TRAINING=-DNN_TRAINING
endif
ifndef CXX
CXX=g++
endif
ifdef UNBOUND_OPTIMIZE
UNBOUND_OPTI=-DUNBOUND_OPTIMIZE
endif
SHELL := /bin/bash

ifeq ($(config), debug)
DEBUG_FLAGS= -g -O0 -DDEBUG #$(FLAG_GCOV)
else #release config by default
DEBUG_FLAGS=-O3
endif

COMMON_FLAGS=-std=c++11 -I$(OrpailleCC_INC) -DLABEL_COUNT=$(LABEL_COUNT) -DFEATURES_COUNT=$(FEATURES_COUNT) -DSIZE=$(MEMORY_SIZE) $(NN_TRAINING) $(UNBOUND_OPTI) $(DEBUG_FLAGS) 

ALL_TARGET = empty_classifier previous_classifier \
			 streamdm_ht streamdm_naive_bayes streamdm_perceptron\
			 mondrian_t1 mondrian_t2 mondrian_t3 mondrian_t4 mondrian_t5 \
			 mondrian_t6 mondrian_t7 mondrian_t8 mondrian_t9 mondrian_t10 \
			 mondrian_t11 mondrian_t12 mondrian_t13 mondrian_t14 mondrian_t15 \
			 mondrian_t16 mondrian_t17 mondrian_t18 mondrian_t19 mondrian_t20 \
			 mondrian_t21 mondrian_t22 mondrian_t23 mondrian_t24 mondrian_t25 \
			 mondrian_t26 mondrian_t27 mondrian_t28 mondrian_t29 mondrian_t30 \
			 mondrian_t31 mondrian_t32 mondrian_t33 mondrian_t34 mondrian_t35 \
			 mondrian_t36 mondrian_t37 mondrian_t38 mondrian_t39 mondrian_t40 \
			 mondrian_t41 mondrian_t42 mondrian_t43 mondrian_t44 mondrian_t45 \
			 mondrian_t46 mondrian_t47 mondrian_t48 mondrian_t49 mondrian_t50\
			 mondrian_coarse_rs\
			 mondrian_coarse_acc\
			 mondrian_coarse_kap\
			 mondrian_coarse_racc\
			 mondrian_coarse_rkap\
			 mondrian_coarse_empty\
			 mcnn_c10 mcnn_c20 mcnn_c32 mcnn_c33 mcnn_c34 mcnn_c40 mcnn_c50 \
			 naive_bayes \
			 mlp_3

compile:  $(ALL_TARGET)

mcnn_%: src/main.cpp src/mcnn.cpp
	$(eval clusters=$(shell sed -nr 's/^c([0-9]+)/\1/p' <<< $*))
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mcnn.cpp\"" \
		-DMAX_CLUSTERS=$(clusters) -o bin/$@

mondrian_coarse_empty: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=NoMetrics)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@
mondrian_coarse_rs: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=ReservoirSamplingMetrics)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@

mondrian_coarse_acc: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=ErrorMetrics<false>)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@

mondrian_coarse_kap: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=KappaMetrics<$(LABEL_COUNT), false>)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@

mondrian_coarse_racc: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=ErrorMetrics<true>)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@

mondrian_coarse_rkap: src/mond_coarse.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(eval sampling_object=KappaMetrics<$(LABEL_COUNT), true>)
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_coarse.cpp\"" \
		-DSAMPLING_OBJECT="$(sampling_object)" -o bin/$@

mondrian_t%: src/mond.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond.cpp\"" -DTREE_COUNT=$* -o bin/$@

mondrian_unbound: src/mond_unbound.cpp src/main.cpp
#	$* contains everything within "%" of the target
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond_unbound.cpp\"" -o bin/$@


empty_classifier: src/empty.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"empty.cpp\"" -o bin/$@

previous_classifier: src/previous.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"previous.cpp\"" -o bin/$@

naive_bayes: src/naive_bayes.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"naive_bayes.cpp\"" -o bin/$@

streamdm_ht: src/streamdm_ht.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-pthread \
		-L$(StreamDM_DIR) \
		$(log4cpp) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_ht.cpp\"" -o bin/$@ 
streamdm_naive_bayes: src/streamdm_naive_bayes.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-pthread \
		-L$(StreamDM_DIR) \
		$(log4cpp) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_naive_bayes.cpp\"" -o bin/$@ 
streamdm_perceptron: src/streamdm_ht.cpp src/main.cpp
	$(CXX) src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-pthread \
		-L$(StreamDM_DIR) \
		$(log4cpp) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_perceptron.cpp\"" -o bin/$@ 

mlp_%: src/neural_network.cpp src/main.cpp
	$(CXX) src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"neural_network.cpp\"" -DLAYER_COUNT=$* -o bin/$@
latex:
	$(PYTHON_COMMAND) makefile.py latex
dataset:
	$(PYTHON_COMMAND) makefile.py dataset
	shuf /tmp/processed_subject1_ideal.log > /tmp/processed_subject1_ideal_shuf.log
run:
	$(PYTHON_COMMAND) makefile.py run
rerun: 
	rm -f /tmp/output /tmp/output_runs models.csv
	$(PYTHON_COMMAND) makefile.py run
calibration: 
	$(PYTHON_COMMAND) makefile.py calibration
xp0: empty_classifier previous_classifier \
			 streamdm_ht streamdm_naive_bayes streamdm_perceptron\
			 mondrian_t1 mondrian_t2 mondrian_t3 mondrian_t4 mondrian_t5 \
			 mondrian_t6 mondrian_t7 mondrian_t8 mondrian_t9 mondrian_t10 \
			 mondrian_t11 mondrian_t12 mondrian_t13 mondrian_t14 mondrian_t15 \
			 mondrian_t16 mondrian_t17 mondrian_t18 mondrian_t19 mondrian_t20 \
			 mondrian_t21 mondrian_t22 mondrian_t23 mondrian_t24 mondrian_t25 \
			 mondrian_t26 mondrian_t27 mondrian_t28 mondrian_t29 mondrian_t30 \
			 mondrian_t31 mondrian_t32 mondrian_t33 mondrian_t34 mondrian_t35 \
			 mondrian_t36 mondrian_t37 mondrian_t38 mondrian_t39 mondrian_t40 \
			 mondrian_t41 mondrian_t42 mondrian_t43 mondrian_t44 mondrian_t45 \
			 mondrian_t46 mondrian_t47 mondrian_t48 mondrian_t49 mondrian_t50\
			 mcnn_c10 mcnn_c20 mcnn_c32 mcnn_c33 mcnn_c34 mcnn_c40 mcnn_c50 \
			 naive_bayes \
			 mlp_3
xp1: empty_classifier mondrian_t1 mondrian_t5 mondrian_t10 mondrian_t50 mondrian_coarse_empty
xp2: empty_classifier mondrian_t1 mondrian_t5 mondrian_t10 mondrian_t50 mondrian_coarse_empty
moa_xp0:
	cd $(MOA_DIR)
	#We set the random seed to 888
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -a 3 -k 0 -i 888) -f dataset_1.arff -m 200000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 777 -i 888 -a 3 -n 20) -f dataset_2.arff -m 200000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomTreeGenerator -r 777 -i 888 -c 10 -o 0 -u 6 -d 10 -l 5) -f dataset_3.arff -m 200000"
	 sed 's/,class1,/,0/g' dataset_1.arff | sed 's/,class2,/,1/g' | sed 's/,/	/g' > dataset_1.log
	 sed 's/,class1,/,0/g' dataset_2.arff | sed 's/,class2,/,1/g' | sed 's/,/	/g' > dataset_2.log
	 sed 's/,class10,/,9/g' dataset_3.arff | sed 's/,class1,/,0/g' | sed 's/,class2,/,1/g' | sed 's/,class3,/,2/g' | sed 's/,class4,/,3/g' | sed 's/,class5,/,4/g' | sed 's/,class6,/,5/g' | sed 's/,class7,/,6/g' | sed 's/,class8,/,7/g' | sed 's/,class9,/,8/g' | sed 's/,/	/g' > dataset_3.log
	 cp dataset_*.log /tmp
moa_xp1_xp2:
	cd $(MOA_DIR)
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGeneratorDrift -s 0.001 -c 33 -a 12 -r 1 -i 1) -f RandomRBF_drift.artf -m 20000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -c 33 -a 12 -r 1 -i 1) -f RandomRBF_stable.artf -m 20000"
	sed 's/class\([0-9]*\)/\1/' RandomRBF_drift.artf | sed 's/,/	/g' | tail -n +19 > RandomRBF_drift.log
	sed 's/class\([0-9]*\)/\1/' RandomRBF_stable.artf | sed 's/,/	/g' | tail -n +19 > RandomRBF_stable.log
	[ -d datasets ] || mkdir datasets
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 0 -c 33 -a 12 -k 6 -t 0.000 -n 04) -f hyperplane_0_6_000_04.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_0_6_000_04.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_0_6_000_04.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 0 -c 33 -a 12 -k 4 -t 0.001 -n 01) -f hyperplane_0_4_001_01.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_0_4_001_01.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_0_4_001_01.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 1 -c 33 -a 12 -k 7 -t 0.000 -n 08) -f hyperplane_1_7_000_08.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_1_7_000_08.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_1_7_000_08.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 1 -c 33 -a 12 -k 4 -t 0.001 -n 04) -f hyperplane_1_4_001_04.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_1_4_001_04.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_1_4_001_04.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 2 -c 33 -a 12 -k 5 -t 0.000 -n 04) -f hyperplane_2_5_000_04.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_2_5_000_04.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_2_5_000_04.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 2 -c 33 -a 12 -k 3 -t 0.001 -n 08) -f hyperplane_2_3_001_08.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_2_3_001_08.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_2_3_001_08.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 3 -c 33 -a 12 -k 2 -t 0.000 -n 08) -f hyperplane_3_2_000_08.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_3_2_000_08.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_3_2_000_08.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 3 -c 33 -a 12 -k 2 -t 0.001 -n 04) -f hyperplane_3_2_001_04.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_3_2_001_04.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_3_2_001_04.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 4 -c 33 -a 12 -k 4 -t 0.000 -n 00) -f hyperplane_4_4_000_00.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_4_4_000_00.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_4_4_000_00.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -i 4 -c 33 -a 12 -k 2 -t 0.001 -n 08) -f hyperplane_4_2_001_08.arff -m 20000 -h"
	sed 's/class\([0-9]*\)/\1/' hyperplane_4_2_001_08.arff | sed 's/,/	/g' | tail -n +19 > datasets/hyperplane_4_2_001_08.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 0 -f 3 -b) -f sine_0_3.arff -m 20000"
	sed 's/negative/0/' sine_0_3.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_0_3.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 1 -i 0 -b -n 10000 -p 8) -f sea_1_0_8.arff -m 20000"
	sed 's/groupA/0/' sea_1_0_8.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_1_0_8.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 0 -i 0 -c 33 -a 12 -n 52) -f rbf_0_52.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_0_52.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_0_52.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 1 -f 3 -b) -f sine_1_3.arff -m 20000"
	sed 's/negative/0/' sine_1_3.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_1_3.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 4 -i 1 -b -n 10000 -p 8) -f sea_4_1_8.arff -m 20000"
	sed 's/groupA/0/' sea_4_1_8.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_4_1_8.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 1 -i 1 -c 33 -a 12 -n 59) -f rbf_1_59.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_1_59.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_1_59.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 2 -f 3 -b) -f sine_2_3.arff -m 20000"
	sed 's/negative/0/' sine_2_3.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_2_3.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 4 -i 2 -b -n 10000 -p 4) -f sea_4_2_4.arff -m 20000"
	sed 's/groupA/0/' sea_4_2_4.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_4_2_4.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 2 -i 2 -c 33 -a 12 -n 190) -f rbf_2_190.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_2_190.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_2_190.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 3 -f 2 -b) -f sine_3_2.arff -m 20000"
	sed 's/negative/0/' sine_3_2.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_3_2.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 4 -i 3 -b -n 10000 -p 4) -f sea_4_3_4.arff -m 20000"
	sed 's/groupA/0/' sea_4_3_4.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_4_3_4.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 3 -i 3 -c 33 -a 12 -n 167) -f rbf_3_167.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_3_167.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_3_167.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 4 -f 3 -b) -f sine_4_3.arff -m 20000"
	sed 's/negative/0/' sine_4_3.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_4_3.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 1 -i 4 -b -n 10000 -p 8) -f sea_1_4_8.arff -m 20000"
	sed 's/groupA/0/' sea_1_4_8.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_1_4_8.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 4 -i 4 -c 33 -a 12 -n 37) -f rbf_4_37.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_4_37.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_4_37.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 5 -f 1 -b) -f sine_5_1.arff -m 20000"
	sed 's/negative/0/' sine_5_1.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_5_1.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 4 -i 5 -b -n 10000 -p 8) -f sea_4_5_8.arff -m 20000"
	sed 's/groupA/0/' sea_4_5_8.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_4_5_8.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 5 -i 5 -c 33 -a 12 -n 194) -f rbf_5_194.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_5_194.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_5_194.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 6 -f 1 -b) -f sine_6_1.arff -m 20000"
	sed 's/negative/0/' sine_6_1.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_6_1.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 4 -i 6 -b -n 10000 -p 4) -f sea_4_6_4.arff -m 20000"
	sed 's/groupA/0/' sea_4_6_4.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_4_6_4.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 6 -i 6 -c 33 -a 12 -n 96) -f rbf_6_96.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_6_96.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_6_96.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 7 -f 3 -b) -f sine_7_3.arff -m 20000"
	sed 's/negative/0/' sine_7_3.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_7_3.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 1 -i 7 -b -n 10000 -p 0) -f sea_1_7_0.arff -m 20000"
	sed 's/groupA/0/' sea_1_7_0.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_1_7_0.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 7 -i 7 -c 33 -a 12 -n 179) -f rbf_7_179.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_7_179.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_7_179.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 8 -f 2 -b) -f sine_8_2.arff -m 20000"
	sed 's/negative/0/' sine_8_2.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_8_2.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 2 -i 8 -b -n 10000 -p 0) -f sea_2_8_0.arff -m 20000"
	sed 's/groupA/0/' sea_2_8_0.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_2_8_0.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 8 -i 8 -c 33 -a 12 -n 173) -f rbf_8_173.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_8_173.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_8_173.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SineGenerator -i 9 -f 4 -b) -f sine_9_4.arff -m 20000"
	sed 's/negative/0/' sine_9_4.arff | sed 's/positive/1/' | sed 's/,/	/g' | tail -n +11 > datasets/sine_9_4.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.SEAGenerator -f 1 -i 9 -b -n 10000 -p 0) -f sea_1_9_0.arff -m 20000"
	sed 's/groupA/0/' sea_1_9_0.arff | sed 's/groupB/1/' | sed 's/,/	/g' | tail -n +10 > datasets/sea_1_9_0.log
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 9 -i 9 -c 33 -a 12 -n 115) -f rbf_9_115.arff -m 20000"
	sed 's/class\([0-9]*\)/\1/' rbf_9_115.arff | sed 's/,/	/g' | tail -n +19 > datasets/rbf_9_115.log
plot_results:
	PYTHONHASHSEED=0 $(PYTHON_COMMAND) makefile.py plot_results
plot_hyperparameters:
	PYTHONHASHSEED=0 $(PYTHON_COMMAND) makefile.py plot_hyperparameters
clean:
	rm -rf bin/mondrian_t* bin/empty_classifier bin/previous_classifier bin/mcnn_* bin/streamdm_ht bin/streamdm_perceptron bin/streamdm_naive_bayes bin/naive_bayes
