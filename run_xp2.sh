#!/usr/bin/bash

result_dir="results_xp2"
rep_count=10
rm -rf $result_dir
mkdir $result_dir

runny()
{
	local s=$1
	local t=$2
	local et=$3
	local sh=$4
	local tt=$5
	local dataset=$6
	local binary="bin/$dataset/mondrian_coarse_empty"
	local f="mondrian_t"$t"_"$et"_"$sh"_"$tt
	$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et split_helper:$sh trim_type:$tt maximum_trim_size:0.03 >> $result_dir/$dataset/$f.csv
}

for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	mkdir $result_dir/$dataset
	for s in `seq $rep_count`; do
		for t in 1 5 10 20 30 50; do
			for extend_type in original,none barycenter,weighted barycenter,avg; do
				for tt in none random fading_score count; do
					IFS="," read -r -a array <<< $extend_type
					et=${array[0]}
					sh=${array[1]}
					runny $s $t $et $sh $tt $dataset &
				done
			done
		done
		wait
	done
done

#Run with unbound
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	binary="bin/$dataset/mondrian_coarse_empty_unbound"
	mkdir $result_dir/$dataset
	for s in (seq $rep_count); do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				f="mondrian_undound_t$t"_"$et"
				echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			done
		done
	done
done
