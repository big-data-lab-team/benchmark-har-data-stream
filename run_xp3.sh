#!/usr/bin/bash

result_dir="f1_data"
rep_count=20
#rm -rf $result_dir
mkdir $result_dir

declare -A dataset_last_data_point=( [banos_6]=11050 [RandomRBF_stable]=17050 )

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
	local trim_size='0.03'
	local binary="bin/$dataset/mondrian_coarse_acc_"$memory"M"
	local f="mondrian_original_add_1_to_"$tree_count_target"_"$memory"M_ttf_"$trim_type"_th_"$threshold_overfit"_st_"$stats_type
	$binary $dataset.log $seed 3 $seed \
		lifetime:0.5 base_measure:0.0 discount_factor:1.0 \
		extend_type:original split_helper:none trim_type:$trim_type maximum_trim_size:$trim_size \
		enable_tree_change:yes \
		tree_count:$tree_count tree_count_target:$tree_count_target \
		threshold_overfit:$threshold_overfit \
		step_tree_change:$step_tree_change \
		last_data_point:${dataset_last_data_point[$dataset]} \
		stats_type:$stats_type \
		>> $result_dir/$dataset/$f.csv
}
for s in `seq $rep_count`; do
	for memory in 0.2 0.6 10; do
		#mkdir $result_dir/$dataset
		for dataset in RandomRBF_stable banos_6; do
			for threshold_overfit in 'z-test' 't-test' 'sum-std' 'sum-var' 'delta-sum-std'; do
				for stats_type in 'fading' 'sliding'; do
					for trim_type in random count; do
						runny $s 1 best $dataset $memory $threshold_overfit $trim_type $stats_type &
					done
				done
			done
			wait
		done
	done

	#for memory in 0.2 0.6 10; do
		#for dataset in RandomRBF_stable banos_6; do
			#for tct in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 20 25; do
				#for trim_type in random count; do
					#runny $s 1 $tct $dataset $memory -1 $trim_type &
				#done
				#wait
			#done
		#done
	#done
	echo "Iteration $s"
done

#for s in `seq $rep_count`; do
	#for dataset in RandomRBF_stable banos_6; do
		#mkdir $result_dir/$dataset
		#for memory in 0.2 0.6 10; do
			#for threshold_overfit in 0.02 0.05 0.1 0.15 0.2; do
				#for trim_type in random count; do
					#runny $s 1 best $dataset $memory $threshold_overfit $trim_type 0.03 &
				#done
			#done
			#wait
		#done
	#done

	#for dataset in RandomRBF_stable banos_6; do
		#mkdir $result_dir/$dataset
		#for memory in 0.2 0.6 10; do
			#for tct in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 20 25; do
				#for trim_type in random count; do
					#runny $s 1 $tct $dataset $memory -1 $trim_type 0.03 &
				#done
				#wait
			#done
		#done
	#done
#done
