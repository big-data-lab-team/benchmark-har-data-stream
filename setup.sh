rm -rf bin
mkdir bin
mkdir bin/banos_3 bin/banos_6 bin/recofit_3 bin/recofit_6 bin/dataset_1 bin/dataset_2 bin/dataset_3 bin/banos_3_histogram bin/banos_6_histogram bin/drift_3
make LABEL_COUNT=2 FEATURES_COUNT=3 -j 8 #dataset 1 and 2
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_1
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_2
make LABEL_COUNT=10 FEATURES_COUNT=6 -j 8 #dataset 3
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_3
make LABEL_COUNT=41 FEATURES_COUNT=6 BANOS=1 -j 8 #recofit
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/recofit_3
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 -j 8 #recofit 6
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/recofit_6
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1200000 -j 8 #recofit 6
cp bin/mondrian_t1 bin/recofit_6/mondrian_t1_double
cp bin/mondrian_t10 bin/recofit_6/mondrian_t10_double
cp bin/mondrian_t100 bin/recofit_6/mondrian_t100_double
cp bin/mondrian_t20 bin/recofit_6/mondrian_t20_double
cp bin/mondrian_t5 bin/recofit_6/mondrian_t5_double
cp bin/mondrian_t50 bin/recofit_6/mondrian_t50_double

make BANOS=1 -j 8 #Banos
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_3
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/drift_3
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 -j 8 #Banos 6 axis
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1200000 -j 8 #Banos 6 axis
cp bin/mondrian_t1 bin/banos_6/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6/mondrian_t50_double


make LABEL_COUNT=33 FEATURES_COUNT=60 BANOS=1 -j 8
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_3_histogram
make LABEL_COUNT=33 FEATURES_COUNT=120 BANOS=1 -j 8 #Banos 6 axis
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_histogram

cp *.log /tmp