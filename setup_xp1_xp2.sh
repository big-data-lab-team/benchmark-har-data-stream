#!/bin/bash
rm -rf bin
mkdir bin
mkdir bin/banos_6 bin/recofit_6 bin/RandomRBF_drift bin/RandomRBF_stable bin/covtype bin/drift_6 bin/pamap_chest bin/har70 bin/harth

compile () {
	memory=$1
	memory_name=$2
	make MEMORY_SIZE=$memory LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #Banos 6 axis
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/banos_6
	cp bin/empty_classifier* bin/mondrian_* bin/drift_6
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #RandomRBF_stable and RandomRBF_drift, other RBF and hyperplane
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/RandomRBF_drift
	cp bin/empty_classifier* bin/mondrian_* bin/RandomRBF_stable
	for dataset in datasets/rbf*.log datasets/hyperplane*.log; do
		d_name=`basename $dataset .log`
		[ -d bin/$d_name ] || mkdir bin/$d_name
		cp bin/empty_classifier* bin/mondrian_* bin/$d_name
	done
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=7 FEATURES_COUNT=54 BANOS=1 -j 8 xp1 #covtype
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/covtype
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #recofit 6
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/recofit_6
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=12 FEATURES_COUNT=12 -j 8 xp1 #PAMAP2
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/pamap_chest
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=8 FEATURES_COUNT=6 BANOS=1 -j 8 xp1 #HAR70
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/har70
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=12 FEATURES_COUNT=6 BANOS=1 -j 8 xp1 #HARTH
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/harth
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=2 FEATURES_COUNT=3 -j 8 xp1 #SEA
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	for dataset in datasets/sea*.log; do
		d_name=`basename $dataset .log`
		[ -d bin/$d_name ] || mkdir bin/$d_name
		cp bin/empty_classifier* bin/mondrian_* bin/$d_name
	done
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory LABEL_COUNT=2 FEATURES_COUNT=4 -j 8 xp1 #SINE
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	for dataset in datasets/sine*.log; do
		d_name=`basename $dataset .log`
		[ -d bin/$d_name ] || mkdir bin/$d_name
		cp bin/empty_classifier* bin/mondrian_* bin/$d_name
	done
	rm -f bin/empty_classifier* bin/mondrian_*
}
compile_opti_unbound () {
	memory=$1
	memory_name=$2
	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #Banos 6 axis
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/banos_6
	cp bin/empty_classifier* bin/mondrian_* bin/drift_6
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #RandomRBF_stable and RandomRBF_drift
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/RandomRBF_drift
	cp bin/empty_classifier* bin/mondrian_* bin/RandomRBF_stable
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=7 FEATURES_COUNT=54 BANOS=1 -j 8 xp1 #covtype
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/covtype
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #recofit 6
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/recofit_6
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=12 FEATURES_COUNT=12 -j 8 xp1 #PAMAP
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/pamap_chest
	rm -f bin/empty_classifier* bin/mondrian_*

	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=8 FEATURES_COUNT=6 BANOS=1 -j 8 xp1 #HAR70
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/har70
	rm -f bin/empty_classifier* bin/mondrian_*
	make MEMORY_SIZE=$memory UNBOUND_OPTIMIZE=1 LABEL_COUNT=12 FEATURES_COUNT=6 BANOS=1 -j 8 xp1 #HARTH
	for f in bin/mondrian_*; do mv $f "${f}_${memory_name}"; done
	mv bin/empty_classifier "bin/empty_classifier_${memory_name}"
	cp bin/empty_classifier* bin/mondrian_* bin/harth
	rm -f bin/empty_classifier* bin/mondrian_*
}

compile '600000' '0.6M'
compile '1000000' '1M'
compile '2000000' '2M'
compile '10000000' '10M'
compile '50000000' '50M'
compile '100000000' '100M'
compile '200000000' '200M'
compile_opti_unbound '2000000000' '2G'
