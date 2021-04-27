#!/bin/bash
# Expecting the first argument to be the precision
OUTDIR=tmp_$1_$2
	echo Beginning evaluation.
	mkdir verificarlo_results
	echo Running Mondrians with precision of $1 bits and exponent $2...
	export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=$1 --range-binary64=$2"
	make rerun PRECISION=$1 EXPONENT=$2
	echo Copying result files...
	cp ${OUTDIR}/output verificarlo_results/$2_output_$1
	cp ${OUTDIR}/output_runs verificarlo_results/$2_output_runs_$1
	cp ${OUTDIR}/models.csv verificarlo_results/$2_models_$1.csv
