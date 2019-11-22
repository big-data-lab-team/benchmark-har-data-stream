OrpailleCC_DIR=/home/magoa/phd/OrpailleCC
OrpailleCC_INC=$(OrpailleCC_DIR)/src
LABEL_COUNT=33
FEATURES_COUNT=6

ifeq ($(config), debug)
DEBUG_FLAGS=-DDEBUG -g -O0 $(FLAG_GCOV)
else #release config by default
DEBUG_FLAGS=-Os -O3
endif

COMMON_FLAGS=-std=c++11 -I$(OrpailleCC_INC) -DLABEL_COUNT=$(LABEL_COUNT) -DFEATURES_COUNT=$(FEATURES_COUNT) $(DEBUG_FLAGS)

compile: AppPowerMeter mondrian_t10 mondrian_t50 mondrian_t100 empty_classifier

mondrian_t%: mond.cpp main.cpp
#	$* contains everything within "%" of the target
	g++ main.cpp  $(COMMON_FLAGS)\
		-DCLASSIFIER_INITIALIZATION_FILE="\"mond.cpp\"" -DTREE_COUNT=$* -o $@

empty_classifier: empty.cpp main.cpp
	g++ main.cpp $(COMMON_FLAGS) \
		-DCLASSIFIER_INITIALIZATION_FILE="\"empty.cpp\"" -DTREE_COUNT=10 -o $@

AppPowerMeter:
	$(MAKE) -C rapl-tools
	cp rapl-tools/AppPowerMeter rapl-tools/PowerMonitor .

latex:
	python makefile.py latex
dataset:
	python makefile.py dataset
run:
	python makefile.py run
rerun:
	rm -f /tmp/output
	python makefile.py run
process:
	python makefile.py process
clean:
	rm -rf mondrian_t* empty_classifier
fullclean: clean
	$(MAKE) -C rapl-tools clean
	rm -f AppPowerMeter PowerMonitor
