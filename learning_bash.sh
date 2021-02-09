#!/bin/bash
	echo Beginning evaluation.
	#precisions=( "32" "64" )
	precisions=( "32" "40" "48" "56" "64" )
	# precisions=( "32" "36" "40" "44" "48" "52" "56" "60" "64" )
	mkdir verificarlo_results
	for i in "${precisions[@]}"
	do
		echo Running Mondrians with precision of $i bits...
		export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=$i"
		make run
		echo Copying result files...
		cp /tmp/output verificarlo_results/output_$i
		cp /tmp/output_runs verificarlo_results/output_runs_$i
		cp models.csv verificarlo_results/models_$i.csv
	done


