#!/bin/bash
# Transfer server trace files to each server

# From the Data_for_Testbed/Datamining/ServerFiles/
#./../../../transferTraces/transfer16nodes.sh
# ssh mkunal@128.104.222.117 "sudo python FlowSimCron.py 9:45 FlowSim.py sample_flows sample_flow_stats.csv 2 5"
ssh mkunal@128.104.222.117 "sudo time python FlowSim.py sample_flows sample_flow_stats.csv"
ssh mkunal@128.104.222.118 "sudo time python FlowSim.py sample_flows sample_flow_stats.csv"

