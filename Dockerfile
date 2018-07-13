FROM centos
ENV container docker

RUN mkdir -p /etc/selinux/targeted/contexts/
RUN echo '<busconfig><selinux></selinux></busconfig>' > /etc/selinux/targeted/contexts/dbus_contexts

COPY coremark.exe /
RUN yum install -y iproute
RUN yum install -y traceroute
RUN yum install -y iptables-services
RUN yum install -y iperf3
RUN yum install -y nmap
RUN yum install -y net-tools
RUN yum --enablerepo=extras install -y epel-release
RUN yum install -y python-pip
RUN pip install paho-mqtt
RUN pip install numpy
RUN pip install flask
RUN pip install gunicorn
RUN pip install requests
RUN yum install -y mosquitto
RUN yum install -y wget
RUN yum install -y java-1.8.0-openjdk
RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y epel-release
RUN yum install -y fping
RUN yum install htop -y

RUN yum install -y openssh-clients

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup", "/tmp", "/run", "/run/lock" ]
CMD ["/usr/sbin/init"]

