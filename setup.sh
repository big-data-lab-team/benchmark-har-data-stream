#!/bin/bash
rm -rf bin
mkdir bin
mkdir bin/banos_3 bin/banos_6 bin/banos_6_v2 bin/banos_6_v3 bin/banos_6_v4 bin/banos_6_v5 bin/banos_6_v6 bin/banos_6_v1 bin/recofit_3 bin/recofit_6 bin/dataset_1 bin/dataset_2 bin/dataset_3 bin/banos_3_histogram bin/banos_6_histogram bin/drift_3 bin/drift_6
make LABEL_COUNT=2 FEATURES_COUNT=3 #dataset 1 and 2
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_1
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_2
make LABEL_COUNT=10 FEATURES_COUNT=6 #dataset 3
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/dataset_3
make LABEL_COUNT=41 FEATURES_COUNT=6 BANOS=1 #recofit
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/recofit_3
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 #recofit 6
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/recofit_6
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1200000 #recofit 6
cp bin/mondrian_t1 bin/recofit_6/mondrian_t1_double
cp bin/mondrian_t10 bin/recofit_6/mondrian_t10_double
cp bin/mondrian_t100 bin/recofit_6/mondrian_t100_double
cp bin/mondrian_t20 bin/recofit_6/mondrian_t20_double
cp bin/mondrian_t5 bin/recofit_6/mondrian_t5_double
cp bin/mondrian_t50 bin/recofit_6/mondrian_t50_double
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1800000 #recofit 6
cp bin/mondrian_t1 bin/recofit_6/mondrian_t1_triple
cp bin/mondrian_t10 bin/recofit_6/mondrian_t10_triple
cp bin/mondrian_t100 bin/recofit_6/mondrian_t100_triple
cp bin/mondrian_t20 bin/recofit_6/mondrian_t20_triple
cp bin/mondrian_t5 bin/recofit_6/mondrian_t5_triple
cp bin/mondrian_t50 bin/recofit_6/mondrian_t50_triple
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=2400000 #recofit 6
cp bin/mondrian_t1 bin/recofit_6/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/recofit_6/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/recofit_6/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/recofit_6/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/recofit_6/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/recofit_6/mondrian_t50_quadruple
make LABEL_COUNT=41 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=3000000 #recofit 6
cp bin/mondrian_t1 bin/recofit_6/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/recofit_6/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/recofit_6/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/recofit_6/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/recofit_6/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/recofit_6/mondrian_t50_quintuple

make BANOS=1 #Banos
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_3
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/drift_3
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 #Banos 6 axis
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v1
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v2
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v3
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v4
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v5
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_v6
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/drift_6
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1200000 #Banos 6 axis
cp bin/mondrian_t1 bin/banos_6/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v1/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v1/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v1/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v1/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v1/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v1/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v2/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v2/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v2/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v2/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v2/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v2/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v3/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v3/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v3/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v3/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v3/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v3/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v4/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v4/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v4/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v4/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v4/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v4/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v5/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v5/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v5/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v5/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v5/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v5/mondrian_t50_double
cp bin/mondrian_t1 bin/banos_6_v6/mondrian_t1_double
cp bin/mondrian_t10 bin/banos_6_v6/mondrian_t10_double
cp bin/mondrian_t100 bin/banos_6_v6/mondrian_t100_double
cp bin/mondrian_t20 bin/banos_6_v6/mondrian_t20_double
cp bin/mondrian_t5 bin/banos_6_v6/mondrian_t5_double
cp bin/mondrian_t50 bin/banos_6_v6/mondrian_t50_double
cp bin/mondrian_t1 bin/drift_6/mondrian_t1_double
cp bin/mondrian_t10 bin/drift_6/mondrian_t10_double
cp bin/mondrian_t100 bin/drift_6/mondrian_t100_double
cp bin/mondrian_t20 bin/drift_6/mondrian_t20_double
cp bin/mondrian_t5 bin/drift_6/mondrian_t5_double
cp bin/mondrian_t50 bin/drift_6/mondrian_t50_double
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=1800000 #Banos 6 axis
cp bin/mondrian_t1 bin/banos_6/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v1/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v1/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v1/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v1/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v1/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v1/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v2/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v2/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v2/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v2/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v2/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v2/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v3/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v3/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v3/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v3/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v3/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v3/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v4/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v4/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v4/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v4/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v4/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v4/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v5/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v5/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v5/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v5/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v5/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v5/mondrian_t50_triple
cp bin/mondrian_t1 bin/banos_6_v6/mondrian_t1_triple
cp bin/mondrian_t10 bin/banos_6_v6/mondrian_t10_triple
cp bin/mondrian_t100 bin/banos_6_v6/mondrian_t100_triple
cp bin/mondrian_t20 bin/banos_6_v6/mondrian_t20_triple
cp bin/mondrian_t5 bin/banos_6_v6/mondrian_t5_triple
cp bin/mondrian_t50 bin/banos_6_v6/mondrian_t50_triple
cp bin/mondrian_t1 bin/drift_6/mondrian_t1_triple
cp bin/mondrian_t10 bin/drift_6/mondrian_t10_triple
cp bin/mondrian_t100 bin/drift_6/mondrian_t100_triple
cp bin/mondrian_t20 bin/drift_6/mondrian_t20_triple
cp bin/mondrian_t5 bin/drift_6/mondrian_t5_triple
cp bin/mondrian_t50 bin/drift_6/mondrian_t50_triple
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=2400000 #Banos 6 axis
cp bin/mondrian_t1 bin/banos_6/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v1/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v1/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v1/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v1/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v1/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v1/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v2/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v2/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v2/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v2/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v2/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v2/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v3/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v3/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v3/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v3/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v3/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v3/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v4/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v4/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v4/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v4/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v4/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v4/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v5/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v5/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v5/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v5/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v5/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v5/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/banos_6_v6/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/banos_6_v6/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/banos_6_v6/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/banos_6_v6/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/banos_6_v6/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/banos_6_v6/mondrian_t50_quadruple
cp bin/mondrian_t1 bin/drift_6/mondrian_t1_quadruple
cp bin/mondrian_t10 bin/drift_6/mondrian_t10_quadruple
cp bin/mondrian_t100 bin/drift_6/mondrian_t100_quadruple
cp bin/mondrian_t20 bin/drift_6/mondrian_t20_quadruple
cp bin/mondrian_t5 bin/drift_6/mondrian_t5_quadruple
cp bin/mondrian_t50 bin/drift_6/mondrian_t50_quadruple
make LABEL_COUNT=33 FEATURES_COUNT=12 BANOS=1 MEMORY_SIZE=3000000 #Banos 6 axis
cp bin/mondrian_t1 bin/banos_6/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v1/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v1/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v1/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v1/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v1/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v1/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v2/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v2/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v2/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v2/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v2/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v2/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v3/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v3/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v3/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v3/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v3/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v3/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v4/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v4/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v4/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v4/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v4/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v4/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v5/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v5/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v5/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v5/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v5/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v5/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/banos_6_v6/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/banos_6_v6/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/banos_6_v6/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/banos_6_v6/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/banos_6_v6/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/banos_6_v6/mondrian_t50_quintuple
cp bin/mondrian_t1 bin/drift_6/mondrian_t1_quintuple
cp bin/mondrian_t10 bin/drift_6/mondrian_t10_quintuple
cp bin/mondrian_t100 bin/drift_6/mondrian_t100_quintuple
cp bin/mondrian_t20 bin/drift_6/mondrian_t20_quintuple
cp bin/mondrian_t5 bin/drift_6/mondrian_t5_quintuple
cp bin/mondrian_t50 bin/drift_6/mondrian_t50_quintuple


make LABEL_COUNT=33 FEATURES_COUNT=60 BANOS=1
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_3_histogram
make LABEL_COUNT=33 FEATURES_COUNT=120 BANOS=1 #Banos 6 axis
cp bin/empty_classifier bin/mcnn_* bin/mondrian_* bin/mlp_* bin/naive_bayes bin/streamdm_* bin/banos_6_histogram
