#!/bin/bash
# Transfer server trace files to each server

# From the Data_for_Testbed/Datamining/ServerFiles/
#./../../../transferTraces/transfer16nodes.sh
# ssh mkunal@128.104.222.117 "sudo python FlowSimCron.py 9:45 FlowSim.py sample_flows sample_flow_stats.csv 2 5"
ssh mkunal@128.104.222.246 "sudo screen -d -m python FlowSim.py server1.csv serv1_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.247 "sudo screen -d -m python FlowSim.py server2.csv serv2_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.248 "sudo screen -d -m python FlowSim.py server3.csv serv3_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.249 "sudo screen -d -m python FlowSim.py server4.csv serv4_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.250 "sudo screen -d -m python FlowSim.py server5.csv serv5_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.251 "sudo screen -d -m python FlowSim.py server6.csv serv6_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.252 "sudo screen -d -m python FlowSim.py server7.csv serv7_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.253 "sudo screen -d -m python FlowSim.py server8.csv serv8_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.254 "sudo screen -d -m python FlowSim.py server9.csv serv9_10dm_50_flow_stats.csv"
ssh mkunal@128.104.222.255 "sudo screen -d -m python FlowSim.py server10.csv serv10_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.0 "sudo screen -d -m python FlowSim.py server11.csv serv11_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.1 "sudo screen -d -m python FlowSim.py server12.csv serv12_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.2 "sudo screen -d -m python FlowSim.py server13.csv serv13_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.3 "sudo screen -d -m python FlowSim.py server14.csv serv14_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.4 "sudo screen -d -m python FlowSim.py server15.csv serv15_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.5 "sudo screen -d -m python FlowSim.py server16.csv serv16_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.6 "sudo screen -d -m python FlowSim.py server17.csv serv17_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.7 "sudo screen -d -m python FlowSim.py server18.csv serv18_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.8 "sudo screen -d -m python FlowSim.py server19.csv serv19_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.9 "sudo screen -d -m python FlowSim.py server20.csv serv20_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.10 "sudo screen -d -m python FlowSim.py server21.csv serv21_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.11 "sudo screen -d -m python FlowSim.py server22.csv serv22_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.12 "sudo screen -d -m python FlowSim.py server23.csv serv23_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.13 "sudo screen -d -m python FlowSim.py server24.csv serv24_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.14 "sudo screen -d -m python FlowSim.py server25.csv serv25_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.15 "sudo screen -d -m python FlowSim.py server26.csv serv26_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.16 "sudo screen -d -m python FlowSim.py server27.csv serv27_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.17 "sudo screen -d -m python FlowSim.py server28.csv serv28_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.18 "sudo screen -d -m python FlowSim.py server29.csv serv29_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.19 "sudo screen -d -m python FlowSim.py server30.csv serv30_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.20 "sudo screen -d -m python FlowSim.py server31.csv serv31_10dm_50_flow_stats.csv"
ssh mkunal@128.104.223.21 "sudo screen -d -m python FlowSim.py server32.csv serv32_10dm_50_flow_stats.csv"
