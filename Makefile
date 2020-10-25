OrpailleCC_DIR=$(shell pwd)/OrpailleCC
OrpailleCC_INC=$(OrpailleCC_DIR)/src
StreamDM_DIR=$(shell pwd)/streamDM-Cpp
MOA_DIR=/home/magoa/phd/moa
MOA_COMMAND=java -Xmx512m -cp "$(MOA_DIR)/lib/moa-2019.05.0:$(MOA_DIR)/lib/*" -javaagent:$(MOA_DIR)/lib/sizeofag-1.0.4.jar moa.DoTask
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

SHELL := /bin/bash

ifeq ($(config), debug)
DEBUG_FLAGS= -g -O0 $(FLAG_GCOV)
else #release config by default
DEBUG_FLAGS=-Os -O3
endif

COMMON_FLAGS=-std=c++11 -I$(OrpailleCC_INC) -DLABEL_COUNT=$(LABEL_COUNT) -DFEATURES_COUNT=$(FEATURES_COUNT) -DSIZE=$(MEMORY_SIZE) $(NN_TRAINING) $(DEBUG_FLAGS) 

ALL_TARGET = AppPowerMeter empty_classifier previous_classifier \
			 streamdm_ht streamdm_naive_bayes streamdm_perceptron\
			 mondrian_t1 mondrian_t5 mondrian_t10 mondrian_t20 mondrian_t50 mondrian_t100 \
			 mcnn_c10 mcnn_c20 mcnn_c32 mcnn_c33 mcnn_c34 mcnn_c40 mcnn_c50 \
			 naive_bayes \
			 mlp_3

compile:  $(ALL_TARGET)

mcnn_%: src/main.cpp src/mcnn.cpp
	$(eval clusters=$(shell sed -nr 's/^c([0-9]+)/\1/p' <<< $*))
	g++ src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mcnn.cpp\"" \
		-DMAX_CLUSTERS=$(clusters) -o bin/$@

mondrian_t%: src/mond.cpp src/main.cpp
#	$* contains everything within "%" of the target
	g++ src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond.cpp\"" -DTREE_COUNT=$* -o bin/$@

empty_classifier: src/empty.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"empty.cpp\"" -o bin/$@

previous_classifier: src/previous.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"previous.cpp\"" -o bin/$@

naive_bayes: src/naive_bayes.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"naive_bayes.cpp\"" -o bin/$@

streamdm_ht: src/streamdm_ht.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-L$(StreamDM_DIR) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_ht.cpp\"" -o bin/$@ 
streamdm_naive_bayes: src/streamdm_naive_bayes.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-L$(StreamDM_DIR) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_naive_bayes.cpp\"" -o bin/$@ 
streamdm_perceptron: src/streamdm_ht.cpp src/main.cpp
	g++ src/main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I$(StreamDM_DIR)/code \
		-llog4cpp \
		-L$(StreamDM_DIR) \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_perceptron.cpp\"" -o bin/$@ 

mlp_%: src/neural_network.cpp src/main.cpp
	g++ src/main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"neural_network.cpp\"" -DLAYER_COUNT=$* -o bin/$@
AppPowerMeter:
	$(MAKE) -C rapl-tools
	cp rapl-tools/AppPowerMeter rapl-tools/PowerMonitor .

latex:
	python makefile.py latex
dataset:
	python makefile.py dataset
	shuf /tmp/processed_subject1_ideal.log > /tmp/processed_subject1_ideal_shuf.log
run:
	python makefile.py run
rerun: 
	rm -f /tmp/output /tmp/output_runs models.csv
	python makefile.py run
moa:
	cd $(MOA_DIR)
	#We set the random seed to 888
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -a 3 -k 0 -i 888) -f dataset_1.arff -m 200000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 777 -i 888 -a 3 -n 20) -f dataset_2.arff -m 200000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomTreeGenerator -r 777 -i 888 -c 10 -o 0 -u 6 -d 10 -l 5) -f dataset_3.arff -m 200000"
	 sed 's/,class1,/,0/g' dataset_1.arff | sed 's/,class2,/,1/g' | sed 's/,/	/g' > dataset_1.log
	 sed 's/,class1,/,0/g' dataset_2.arff | sed 's/,class2,/,1/g' | sed 's/,/	/g' > dataset_2.log
	 sed 's/,class10,/,9/g' dataset_3.arff | sed 's/,class1,/,0/g' | sed 's/,class2,/,1/g' | sed 's/,class3,/,2/g' | sed 's/,class4,/,3/g' | sed 's/,class5,/,4/g' | sed 's/,class6,/,5/g' | sed 's/,class7,/,6/g' | sed 's/,class8,/,7/g' | sed 's/,class9,/,8/g' | sed 's/,/	/g' > dataset_3.log
	 cp dataset_*.log /tmp
process:
	PYTHONHASHSEED=0 python makefile.py process
clean:
	rm -rf bin/mondrian_t* bin/empty_classifier bin/previous_classifier bin/mcnn_* bin/streamdm_ht bin/streamdm_perceptron bin/streamdm_naive_bayes bin/naive_bayes
fullclean: clean
	$(MAKE) -C rapl-tools clean
	rm -f AppPowerMeter PowerMonitor
