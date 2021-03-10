#!/bin/bash
# Expecting the first argument to be the precision
OUTDIR=/tmp
	echo Beginning evaluation.
	mkdir verificarlo_results
	echo Running Mondrians with precision of $1 bits...
	export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=$1"
	make rerun
	echo Copying result files...
	cp ${OUTDIR}/output verificarlo_results/output_$1
	cp ${OUTDIR}/output_runs verificarlo_results/output_runs_$1
	cp models.csv verificarlo_results/models_$1.csv
