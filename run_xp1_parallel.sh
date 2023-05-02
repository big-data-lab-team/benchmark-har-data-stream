#!/usr/bin/bash

result_dir="results_xp1"
rep_test="$@"
[ -d $result_dir ] || mkdir $result_dir

ID=$RANDOM

runny()
{
	local seed=$1
	local tree_count=$2
	local extend_type=$3
	local dataset=$4
	local memory=$5
	local iteration_dir=$6
	local binary="bin/$dataset/mondrian_coarse_empty_"$memory
	local f="mondrian_t$tree_count"_"$extend_type"_"$memory"
	if [ "$iteration_dir" -le "11" ]; then
		echo "$binary $dataset.log $seed 3 $seed lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$tree_count extend_type:$extend_type >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
	else
		echo "$binary $dataset.log $seed 3 $seed lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$tree_count extend_type:$extend_type | tail -n 1 >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
	fi
}
runny_generated()
{
	local seed=$1
	local tree_count=$2
	local extend_type=$3
	local dataset=$4
	local memory=$5
	local iteration_dir=$6
	local binary="bin/$dataset/mondrian_coarse_empty_"$memory
	local f="mondrian_t$tree_count"_"$extend_type"_"$memory"
	if [ "$iteration_dir" -le "11" ]; then
		echo "$binary datasets/$dataset.log $seed 3 $seed lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$tree_count extend_type:$extend_type  >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
	else
		echo "$binary datasets/$dataset.log $seed 3 $seed lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$tree_count extend_type:$extend_type | tail -n 1  >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
	fi
}
#Run all out-of-memory strategy for validation generated datasets
for s in $rep_test; do
	for memory in '0.6M'; do
		#for d in datasets/*.log; do
		for d in datasets/hyperplane_0_4_001_01.*; do
			dataset=`basename $d .log`
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			for t in 1 5 10 20 30 50; do
				for et in none original count_only partial ghost; do
					runny_generated $s $t $et $dataset $memory $s
				done
			done
		done
	done
done

#Run all out-of-memory strategy
for s in $rep_test; do
	for memory in '0.6M'; do
		for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6 pamap_chest harth har70; do
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			for t in 1 5 10 20 30 50; do
				for et in none original count_only partial ghost; do
					runny $s $t $et $dataset $memory $s
				done
			done
		done
	done
done

#Run all out-of-memory strategy with more memory
#Only run 10 repetitions 
for s in ${rep_test[@]:0:10}; do
	for memory in '1M' '10M' '50M' '100M' '200M'; do
		for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6 pamap_chest harth har70; do
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			for t in 1 5 10 20 30 50; do
				for et in none original count_only partial ghost; do
					runny $s $t $et $dataset $memory $s
				done
			done
		done
	done
done

#Run with unbound
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6 pamap_chest harth har70; do
	binary="bin/$dataset/mondrian_coarse_empty_2G"
	[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
	[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
	for s in $rep_test; do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				f="mondrian_unbound_t$t"_"$et"
				if [ "$s" -le "11" ]; then
					echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$s/$f.csv" >> commands_$ID.txt
				else
					echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et | tail -n 1 >> $result_dir/$dataset/$s/$f.csv" >> commands_$ID.txt
				fi
			done
		done
	done
done

echo "Done Listing; Start Running"
parallel --memfree 4G --retries 10 --progress < commands_$ID.txt
rm -f commands_$ID.txt
