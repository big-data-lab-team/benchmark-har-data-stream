#!/usr/bin/bash

result_dir="results_xp2"
rep_test="$@"
[ -d $result_dir ] || mkdir $result_dir

declare -A dataset_last_data_point=( [banos_6]=11050 [RandomRBF_stable]=17050 [RandomRBF_drift]=17050 [drift_6]=11050 [recofit_6]=80000 [covtype]=570000)

#Add other datasets if necessary
for dataset in datasets/*.log; do
	d_name=`basename $dataset .log`
	dataset_last_data_point[$d_name]=17050
done

ID=$RANDOM

runny()
{
	local s=$1
	local t=$2
	local et=$3
	local sh=$4
	local tt=$5
	local dataset=$6
	local memory=$7
	local iteration_dir=$8
	local binary="bin/$dataset/mondrian_coarse_empty_"$memory
	local f="mondrian_t"$t"_"$et"_"$sh"_"$tt"_"$memory
	echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et split_helper:$sh trim_type:$tt maximum_trim_size:0.03 >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
}
runny_2G()
{
	local s=$1
	local t=$2
	local et=$3
	local dataset=$4
	local iteration_dir=$1 #the iteration_dir is the seed name
	local binary="bin/$dataset/mondrian_coarse_empty_2G"
	local f="mondrian_undound_t$t"_"$et"
	echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$iteration_dir/$f.csv" >> commands_$ID.txt
}

echo "Listing Commands"
for s in $rep_test; do
	for memory in '0.6M' '1M' '10M' '100M' '200M'; do
		for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
			#Create the directories if they don't exist
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			for t in 1 5 10 20 30 50; do
				for extend_type in original,none barycenter,weighted barycenter,avg; do
					for tt in none random fading_score count; do
						IFS="," read -r -a array <<< $extend_type
						et=${array[0]}
						sh=${array[1]}
						runny $s $t $et $sh $tt $dataset $memory $s 
					done
				done
			done
		done
	done
done

#rm -f commands_$ID.txt

#Run with unbound
for dataset in recofit_6 banos_6 RandomRBF_stable RandomRBF_drift covtype drift_6; do
	[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
	[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
	for s in $rep_test; do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				runny_2G $s $t $et $dataset 
			done
		done
	done
done

for s in $rep_test; do
	for memory in '0.6M' '1M' '10M' '100M' '200M'; do
		for d in datasets/*.log; do
			datasets=`basename $d .log`
			#Create the directories if they don't exist
			[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
			[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
			for t in 1 5 10 20 30 50; do
				for extend_type in original,none barycenter,weighted barycenter,avg; do
					for tt in none random fading_score count; do
						IFS="," read -r -a array <<< $extend_type
						et=${array[0]}
						sh=${array[1]}
						runny $s $t $et $sh $tt $dataset $memory $s 
					done
				done
			done
		done
	done
done

#rm -f commands_$ID.txt

#Run with unbound
for d in datasets/*.log; do
	datasets=`basename $d .log`
	[ -d $result_dir/$dataset ] || mkdir $result_dir/$dataset
	[ -d $result_dir/$dataset/$s ] || mkdir $result_dir/$dataset/$s
	for s in $rep_test; do
		for t in 1 5 10 20 30 50; do
			for et in original; do
				runny_2G $s $t $et $dataset 
			done
		done
	done
done

echo "Done Listing; Start Running"
parallel --memsupend 4G < commands_$ID.txt
