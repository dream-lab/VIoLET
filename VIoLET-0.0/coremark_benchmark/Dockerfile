FROM centos

RUN yum install unzip -y
COPY dhrystone.zip /
#COPY c_dhrystone.py /
COPY c_coremark_1.py /
COPY c_coremark_2.py /
COPY c_coremark_4.py /
COPY Raspberry_Pi_Benchmarks.tar.tgz /
COPY coremark_1.exe /
COPY coremark_2.exe /
COPY coremark_4.exe /
COPY coremark_16.exe /
RUN unzip dhrystone.zip
RUN tar -zxvf Raspberry_Pi_Benchmarks.tar.tgz
RUN yum install java-1.8.0-openjdk -y 
RUN yum install java-1.8.0-openjdk-devel -y


