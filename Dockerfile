FROM verificarlo/verificarlo:latest
ARG instr
RUN apt update -y && apt install -y liblog4cpp5v5 liblog4cpp5-dev nano python3-tk
RUN apt install -y linux-tools-common linux-tools-generic linux-cloud-tools-generic build-essential
#RUN linux-tools-3.10.0-3.12-generic linux-cloud-tools-3.10.0-3.12-generic

RUN pip3 install pandas seaborn

RUN cd /opt/ &&\
	git clone --depth=1 https://github.com/MarkCycVic/mondrian-veripaille.git veripaille &&\
	cd veripaille &&\
	git submodule init &&\
	git submodule update &&\
	cp makefile_streamDM streamDM-Cpp/makefile &&\
	if [ $instr = "node" ] ; then cp mondrian_node.hpp OrpailleCC/src/mondrian.hpp ; else cp mondrian_whole.hpp OrpailleCC/src/mondrian.hpp ; fi &&\
	cd streamDM-Cpp &&\
	CXX=g++-7 CC=gcc-7 make -j 8 lib &&\
	cd .. &&\
	mkdir bin
#RUN tar xf datasets.tar.xz &&\
#	mkdir /tmp &&\
#	cp *.log /tmp
#RUN CXX=g++-7 ./setup.sh
#RUN bash setup.sh
#	export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=52" &&\
#	mkdir verificarlo_results &&\

ENTRYPOINT ["/bin/bash"]
	
