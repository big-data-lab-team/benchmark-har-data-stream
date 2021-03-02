FROM verificarlo/verificarlo:latest

RUN apt update -y && apt install -y liblog4cpp5v5 liblog4cpp5-dev linux-tools-common linux-tools-5.8.0-43-generic linux-cloud-tools-5.8.0-43-generic

RUN pip3 install pandas seaborn

#TO DO: Get precision

RUN cd /opt/ && \
	git clone --depth=1 https://github.com/MarkCycVic/benchmark-har-data-stream.git &&\
	cd benchmark-har-data-stream &&\
	git submodule init &&\
	git submodule update &&\
	cp makefile_streamDM streamDM-Cpp/makefile &&\
	cp mondrian_get_set.hpp OrpailleCC/src/mondrian.hpp &&\
	cd streamDM-Cpp &&\
	CXX=g++-7 CC=gcc-7 make -j 8 lib &&\
	cd .. &&\
	mkdir bin &&\
	CXX=g++-7 ./setup.sh &&\
	tar xf datasets.tar.xz &&\
	mkdir tmp &&\
	cp *.log tmp &&\
	export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=$(PRECISION)" &&\
	mkdir verificarlo_results &&\
	make rerun &&\
	cp tmp/output verificarlo_results/output_$i &&\
	cp tmp/output_runs verificarlo_results/output_runs_$i &&\
	cp models.csv verificarlo_results/models_$i.csv

ENTRYPOINT ["/bin/bash"]
	
