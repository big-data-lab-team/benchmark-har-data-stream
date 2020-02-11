OrpailleCC_DIR=/home/magoa/phd/OrpailleCC
OrpailleCC_INC=$(OrpailleCC_DIR)/src
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


compile: AppPowerMeter mondrian_t10 mondrian_t1 mondrian_t5 mondrian_t50 mondrian_t100 empty_classifier mcnn_c20e10p10 previous_classifier mcnn_c10e10p10 mcnn_c40e10p10 mcnn_c100e10p10 mcnn_c31e10p10 mcnn_c33e10p10 mcnn_c34e10p10 mcnn_c50e10p10 mcnn_c50e10p10

mcnn_%: main.cpp mcnn.cpp
	$(eval clusters=$(shell sed -nr 's/^c([0-9]+)e([0-9]+)p([0-9]+)/\1/p' <<< $*))
	$(eval error_th=$(shell sed -nr 's/^c([0-9]+)e([0-9]+)p([0-9]+)/\2/p' <<< $*))
	$(eval performa=$(shell sed -nr 's/^c([0-9]+)e([0-9]+)p([0-9]+)/\3/p' <<< $*))
	g++ main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mcnn.cpp\"" -DMAX_CLUSTERS=$(clusters)\
		-DERROR_THRESHOLD=$(error_th)\
		-DPERFORMANCE_THRESHOLD=$(performa) -o $@

mondrian_t%: mond.cpp main.cpp
#	$* contains everything within "%" of the target
	g++ main.cpp  $(COMMON_FLAGS) $(BANOS_FLAG)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond.cpp\"" -DTREE_COUNT=$* -o $@

empty_classifier: empty.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"empty.cpp\"" -DTREE_COUNT=10 -o $@

previous_classifier: previous.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"previous.cpp\"" -DTREE_COUNT=10 -o $@

streamdm_ht: streamdm_ht.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) $(BANOS_FLAG)\
		-I/home/magoa/phd/streamDM-Cpp/code \
		-llog4cpp \
		-L/home/magoa/phd/streamDM-Cpp \
		-lstreamdm \
		-DCLASSIFIER_INITIALIZATION_FILE="\"streamdm_ht.cpp\"" -DTREE_COUNT=10 -o $@ 
AppPowerMeter:
	$(MAKE) -C rapl-tools
	cp rapl-tools/AppPowerMeter rapl-tools/PowerMonitor .

latex:
	python makefile.py latex
dataset:
	python makefile.py dataset
run:
	python makefile.py run
rerun: compile
	rm -f /tmp/output /tmp/output_runs models.csv
	python makefile.py run
process:
	PYTHONHASHSEED=0 python makefile.py process
clean:
	rm -rf mondrian_t* empty_classifier previous_classifier mcnn_* streamdm_*
fullclean: clean
	$(MAKE) -C rapl-tools clean
	rm -f AppPowerMeter PowerMonitor
