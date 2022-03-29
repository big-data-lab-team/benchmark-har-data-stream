#!/usr/bin/fish

set result_dir results_xp1
#rm -rf $result_dir
mkdir $result_dir
set rep_count 1

#for dataset in RandomRBF_stable RandomRBF_drift;
	#set binary bin/$dataset/mondrian_coarse_empty
	#mkdir $result_dir/$dataset
	#for s in (seq $rep_count);
		#for t in 1 5 10 20 30 50;
			#for et in none original ghost count_only partial;
				#set f mondrian_t"$t"_"$et"
				#echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				#$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			#end
		#end
	#end
#end
for dataset in recofit_6 covtype;
	set binary bin/$dataset/mondrian_coarse_empty_unbound
	mkdir $result_dir/$dataset
	for s in (seq $rep_count);
		for t in 1 5 10 20 30 50;
			for et in original;
				set f mondrian_undound_t"$t"_"$et"
				echo "$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et"
				#$binary $dataset.log $s 3 $s lifetime:0.5 base_measure:0.0 discount_factor:1.0 tree_management:phoenix tree_count:$t extend_type:$et >> $result_dir/$dataset/$f.csv
			end
		end
	end
end

for dataset in recofit_6 covtype;
	set binary bin/$dataset/mondrian_coarse_empty_unbound
	mkdir $result_dir/$dataset
	for s in (seq $rep_count);
		for t in 1 5 10 20 30 50;
			for et in original;
				set f mondrian_undound_t"$t"_"$et"
				echo "$dataset.log tree_count:$t"
				grep "memory" $result_dir/$dataset/$f.csv
			end
		end
	end
end
