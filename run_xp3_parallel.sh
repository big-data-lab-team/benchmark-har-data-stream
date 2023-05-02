#!/usr/bin/bash

result_dir="results_xp3_0_90"
backup_dir="results_xp3_backup"
rep_count=20
comp_test="$@"
#rm -rf $result_dir
mkdir $result_dir

declare -A dataset_last_data_point=( [banos_6]=11050 [RandomRBF_stable]=17050 [RandomRBF_drift]=17050 [drift_6]=11050 [recofit_6]=80000 [covtype]=570000)

runny()
{
	local seed=$1
	local tree_count=$2
	local tree_count_target=$3
	local dataset=$4
	local memory=$5
	local threshold_overfit=$6
	local trim_type=$7
	local step_tree_change=500
	local stats_type=$8
	local iteration_dir=$9
	local trim_size='0.03'
	local binary="bin_0_90/$dataset/mondrian_coarse_acc_"$memory"M"
	local f="mondrian_original_add_"$tree_count"_to_"$tree_count_target"_"$memory"M_ttf_"$trim_type"_th_"$threshold_overfit"_st_"$stats_type

	$binary $dataset.log $seed 3 $seed \
		lifetime:0.5 base_measure:0.0 discount_factor:1.0 \
		extend_type:original split_helper:none trim_type:$trim_type maximum_trim_size:$trim_size \
		enable_tree_change:yes \
		tree_count:$tree_count tree_count_target:$tree_count_target \
		threshold_overfit:$threshold_overfit \
		step_tree_change:$step_tree_change \
		last_data_point:${dataset_last_data_point[$dataset]} \
		stats_type:$stats_type \
		>> $result_dir/$dataset/$iteration_dir/$f.csv
}
name_namy=''
ID=$RANDOM
namy()
{
	local seed=$1
	local tree_count=$2
	local tree_count_target=$3
	local dataset=$4
	local memory=$5
	local threshold_overfit=$6
	local trim_type=$7
	local step_tree_change=500
	local stats_type=$8
	local iteration_dir=$9
	local trim_size='0.03'
	local binary="bin/$dataset/mondrian_coarse_acc_"$memory"M"
	local f="mondrian_original_add_"$tree_count"_to_"$tree_count_target"_"$memory"M_ttf_"$trim_type"_th_"$threshold_overfit"_st_"$stats_type


	name_namy="$result_dir/$dataset/$iteration_dir/$f.csv"
	echo $name_namy > /tmp/namy$ID
}

#Run Adaptive Threshold
for s in `seq $rep_count`; do
	for dataset in RandomRBF_stable RandomRBF_drift banos_6 drift_6 covtype recofit_6; do
		for memory in 0.2 0.6 10; do
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			#for threshold_overfit in 'z-test' 't-test' 'sum-std' 'sum-var' 'delta-sum-std'; do
			for threshold_overfit in $comp_test; do
				for stats_type in 'fading' 'sliding'; do
					for trim_type in 'random' 'count' 'chop'; do
						runny $s 1 best $dataset $memory $threshold_overfit $trim_type $stats_type $s &
					done
				done
			done
		done
	done
	echo "Adaptive Threshold Iteration $s/$rep_count"
done
echo "Waiting"
wait
echo "Merging"
for s in `seq $rep_count`; do
	for dataset in RandomRBF_stable RandomRBF_drift banos_6 drift_6 covtype recofit_6; do
		for memory in 0.2 0.6 10; do
			for threshold_overfit in $comp_test; do
				for stats_type in 'fading' 'sliding'; do
					for trim_type in 'random' 'count' 'chop'; do
						namy $s 1 best $dataset $memory $threshold_overfit $trim_type $stats_type $s
						name_namy=`cat /tmp/namy"$ID"`
						f=`basename $name_namy`
						cat $name_namy >> $result_dir/$dataset/$f
					done
				done
			done
		done
	done
done
