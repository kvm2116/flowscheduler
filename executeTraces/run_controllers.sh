#!/bin/bash

# From the executeTraces/
# ./run_controllers.sh

ssh mkunal@128.104.222.246 "cd floodlight; screen -d -m java -jar target/floodlight.jar"
ssh mkunal@128.104.222.247 "cd floodlight; screen -d -m java -jar target/floodlight.jar"
ssh mkunal@128.104.223.6 "cd floodlight; screen -d -m java -jar target/floodlight.jar"
ssh mkunal@128.104.223.7 "cd floodlight; screen -d -m java -jar target/floodlight.jar"