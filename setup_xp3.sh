#!/bin/bash
rm -rf bin
mkdir bin
mkdir bin/banos_6 bin/recofit_6 bin/RandomRBF_drift bin/RandomRBF_stable bin/covtype bin/drift_3 bin/drift_6

compile () {
	memory=$1
	memory_name=$2
	make MEMORY_SIZE=$memory LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp3 #Banos 6 axis
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	cp bin/empty_classifier bin/mondrian_* bin/banos_6
	cp bin/empty_classifier bin/mondrian_* bin/drift_6
	rm -f bin/empty_classifier bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp3 #RandomRBF_stable and RandomRBF_drift
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	cp bin/empty_classifier bin/mondrian_* bin/RandomRBF_drift
	cp bin/empty_classifier bin/mondrian_* bin/RandomRBF_stable
	rm -f bin/empty_classifier bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=7 FEATURES_COUNT=54 BANOS=1 -j 8 xp3 #covtype
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	cp bin/empty_classifier bin/mondrian_* bin/covtype
	rm -f bin/empty_classifier bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 xp3 #recofit 6
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	cp bin/empty_classifier bin/mondrian_* bin/recofit_6
	rm -f bin/empty_classifier bin/mondrian_*
}

compile '200000' '0.2M'
compile '600000' '0.6M'
compile '10000000' '10M'

