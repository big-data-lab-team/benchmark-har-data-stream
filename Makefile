OrpailleCC_DIR=/home/magoa/phd/OrpailleCC
OrpailleCC_INC=$(OrpailleCC_DIR)/src
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

SHELL := /bin/bash

ifeq ($(config), debug)
DEBUG_FLAGS= -g -O0 $(FLAG_GCOV)
else #release config by default
DEBUG_FLAGS=-Os -O3
endif

COMMON_FLAGS=-std=c++11 -I$(OrpailleCC_INC) -DLABEL_COUNT=$(LABEL_COUNT) -DFEATURES_COUNT=$(FEATURES_COUNT) $(DEBUG_FLAGS)

ALL_TARGET = AppPowerMeter empty_classifier previous_classifier \
			 streamdm_ht streamdm_naive_bayes streamdm_perceptron\
			 mondrian_t1 mondrian_t5 mondrian_t10 mondrian_t20 mondrian_t50 mondrian_t100 \
			 mcnn_c10 mcnn_c20 mcnn_c32 mcnn_c33 mcnn_c34 mcnn_c40 mcnn_c50

compile:  $(ALL_TARGET)

mcnn_%: main.cpp mcnn.cpp
	$(eval clusters=$(shell sed -nr 's/^c([0-9]+)/\1/p' <<< $*))
	g++ main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mcnn.cpp\"" \
		-DMAX_CLUSTERS=$(clusters) -o $@

mondrian_t%: mond.cpp main.cpp
#	$* contains everything within "%" of the target
	g++ main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond.cpp\"" -DTREE_COUNT=$* -o $@

empty_classifier: empty.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"empty.cpp\"" -o $@

previous_classifier: previous.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"previous.cpp\"" -o $@

streamdm_ht: streamdm_ht.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I/home/magoa/phd/streamDM-Cpp/code \
		-llog4cpp \
		-L/home/magoa/phd/streamDM-Cpp \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_ht.cpp\"" -o $@ 
streamdm_naive_bayes: streamdm_naive_bayes.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I/home/magoa/phd/streamDM-Cpp/code \
		-llog4cpp \
		-L/home/magoa/phd/streamDM-Cpp \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_naive_bayes.cpp\"" -o $@ 
streamdm_perceptron: streamdm_ht.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I/home/magoa/phd/streamDM-Cpp/code \
		-llog4cpp \
		-L/home/magoa/phd/streamDM-Cpp \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_perceptron.cpp\"" -o $@ 

mlp_%: neural_network.cpp main.cpp
	g++ main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"neural_network.cpp\"" -DLAYER_COUNT=$* -o $@
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
rerun: compile
	rm -f /tmp/output /tmp/output_runs models.csv
	python makefile.py run
moa:
	cd $(MOA_DIR)
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.HyperplaneGenerator -a 3 -k 0) -f dataset_1.arff -m 20000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomRBFGenerator -r 777 -i 888 -a 3 -n 20) -f dataset\_2.arff -m 20000"
	$(MOA_COMMAND) "WriteStreamToARFFFile -s (generators.RandomTreeGenerator -r 777 -i 888 -c 10 -o 0 -u 6 -d 10 -l 5) -f dataset\_3.arff -m 20000"
process:
	PYTHONHASHSEED=0 python makefile.py process
clean:
	rm -rf mondrian_t* empty_classifier previous_classifier mcnn_* streamdm_ht streamdm_perceptron streamdm_naive_bayes
fullclean: clean
	$(MAKE) -C rapl-tools clean
	rm -f AppPowerMeter PowerMonitor
