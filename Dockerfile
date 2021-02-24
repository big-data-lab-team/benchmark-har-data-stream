FROM verificarlo/verificarlo:latest

RUN apt update -y && apt install -y liblog4cpp5v5 liblog4cpp5-dev linux-tools-common linux-tools-5.8.0-43-generic linux-cloud-tools-5.8.0-43-generic

RUN pip3 install pandas seaborn



RUN cd /opt/ && \
	git clone --depth=1 https://github.com/MarkCycVic/benchmark-har-data-stream.git &&\
	cd benchmark-har-data-stream &&\
	git submodule init &&\
	git submodule update &&\
	cp makefile_streamDM streamDM-Cpp/makefile &&\
	cd streamDM-Cpp &&\
	CXX=g++-7 CC=gcc-7 make -j 8 lib &&\
	cd .. &&\
	mkdir bin &&\
	CXX=g++-7 ./setup.sh

ENTRYPOINT ["/bin/bash"]
	
