#!/bin/bash
# increase the number of open files on each server

# From the executeTestbed/
#./increase_open_files

# ssh mkunal@128.104.222.246 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.247 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.248 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.249 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.250 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.251 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.252 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.253 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.254 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.222.255 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.0 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.1 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.2 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.3 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.4 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.5 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.6 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.7 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.8 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.9 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.10 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.11 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.12 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.13 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.14 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.15 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.16 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.17 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.18 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.19 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.20 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"
# ssh mkunal@128.104.223.21 sudo bash -c "echo fs.file-max=100000 >> /etc/sysctl.conf"

Login into each machine using ssh

Run the following:
sudo bash -c "echo fs.file-max=200000 >> /etc/sysctl.conf"; sudo sysctl -p; sudo bash -c "echo mkunal soft nofile 200000 >> /etc/security/limits.conf"; sudo bash -c "echo mkunal hard nofile 200000 >> /etc/security/limits.conf"; sudo bash -c "echo session required pam_limits.so >> /etc/pam.d/common-session"; exit

Logout

Login again and the limits will be changed