FROM verificarlo/verificarlo:latest
ARG instr
RUN apt update -y && apt install -y liblog4cpp5v5 liblog4cpp5-dev nano python3-tk
RUN apt install -y linux-tools-common linux-tools-generic linux-cloud-tools-generic build-essential


RUN pip3 install pandas seaborn

RUN cd /opt/ &&\
	git clone --depth=1 --single-branch --branch veripaille https://github.com/big-data-lab-team/benchmark-har-data-stream.git veripaille &&\
	cd veripaille &&\
	git submodule init &&\
	git submodule update &&\
	cp makefile_streamDM streamDM-Cpp/makefile &&\
	if [ $instr = "node" ] ; then cp mondrian_node.hpp OrpailleCC/src/mondrian.hpp ; else cp mondrian_whole.hpp OrpailleCC/src/mondrian.hpp ; fi &&\
	if [ $instr = "node" ] ; then cp Makefile_node Makefile ; else cp Makefile_whole Makefile ; fi &&\
	cd streamDM-Cpp &&\
	CXX=g++-7 CC=gcc-7 make -j 8 lib &&\
	cd .. &&\
	mkdir bin &&\
	tar xf datasets.tar.xz &&\
	mkdir tmp &&\
	cp *.log tmp
RUN cd /opt/veripaille/ &&\
	bash setup.sh CXX=g++-7 &&\
	mkdir verificarlo_results &&\
	bash mkdirs.sh

ENTRYPOINT ["/bin/bash"]
	
