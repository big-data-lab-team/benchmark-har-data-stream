#!/bin/bash
rm -rf bin
mkdir bin
mkdir bin/banos_3 bin/banos_6 bin/recofit_3 bin/recofit_6 bin/RandomRBF_drift bin/RandomRBF_stable bin/covtype bin/drift_3 bin/drift_6

make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #Banos 6 axis
cp bin/empty_classifier bin/mondrian_* bin/banos_6
cp bin/empty_classifier bin/mondrian_* bin/drift_6

make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #RandomRBF_stable and RandomRBF_drift
cp bin/empty_classifier bin/mondrian_* bin/RandomRBF_drift
cp bin/empty_classifier bin/mondrian_* bin/RandomRBF_stable

make LABEL_COUNT=7 FEATURES_COUNT=54 BANOS=1 -j 8 xp1 #covtype
cp bin/empty_classifier bin/mondrian_* bin/covtype

make BANOS=1 -j 8 xp1 #Banos
cp bin/empty_classifier bin/mondrian_* bin/banos_3
cp bin/empty_classifier bin/mondrian_* bin/drift_3

make LABEL_COUNT=41 FEATURES_COUNT=6 BANOS=1 -j 8 xp1 #recofit
cp bin/empty_classifier bin/mondrian_* bin/recofit_3

make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 xp1 #recofit 6
cp bin/empty_classifier bin/mondrian_* bin/recofit_6

UNBOUND_MEMORY=2000000000

make MEMORY_SIZE=$UNBOUND_MEMORY LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 mondrian_coarse_empty #Banos 6 axis
cp bin/mondrian_coarse_empty bin/banos_6/mondrian_coarse_empty_unbound
cp bin/mondrian_coarse_empty bin/drift_6/mondrian_coarse_empty_unbound

make MEMORY_SIZE=$UNBOUND_MEMORY LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 mondrian_coarse_empty #RandomRBF_stable and RandomRBF_drift
cp bin/mondrian_coarse_empty bin/RandomRBF_drift/mondrian_coarse_empty_unbound
cp bin/mondrian_coarse_empty bin/RandomRBF_stable/mondrian_coarse_empty_unbound

make MEMORY_SIZE=$UNBOUND_MEMORY LABEL_COUNT=7 FEATURES_COUNT=54 BANOS=1 -j 8 mondrian_coarse_empty #covtype
cp bin/mondrian_coarse_empty bin/covtype/mondrian_coarse_empty_unbound

make MEMORY_SIZE=$UNBOUND_MEMORY BANOS=1 -j 8 mondrian_coarse_empty #Banos
cp bin/mondrian_coarse_empty bin/banos_3/mondrian_coarse_empty_unbound
cp bin/mondrian_coarse_empty bin/drift_3/mondrian_coarse_empty_unbound

make MEMORY_SIZE=$UNBOUND_MEMORY LABEL_COUNT=41 FEATURES_COUNT=6 BANOS=1 -j 8 mondrian_coarse_empty #recofit
cp bin/mondrian_coarse_empty bin/recofit_3/mondrian_coarse_empty_unbound

make MEMORY_SIZE=$UNBOUND_MEMORY LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 mondrian_coarse_empty #recofit 6
cp bin/mondrian_coarse_empty bin/recofit_6/mondrian_coarse_empty_unbound
