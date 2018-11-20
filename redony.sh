#!/bin/bash

# $1 - nappali le
# $2 - nappali fel
# $3 - konyha le
# $4 - konyha fel
SCRIPT_PATH='./python_scripts/Adafruit_PWM_Servo_Driver/redony.py'

if [[ $2 != stop ]]; then
    R_PORT=0
    if [[ $1 == nappali ]]; then 
        if [[ $2 == fel ]]; then
    	    R_PORT=5
        else 
            R_PORT=4
        fi
    fi
    
    if [[ $1 == konyha ]]; then
        if [[ $2 == fel ]]; then
    	    R_PORT=7
        else 
    	    R_PORT=6
        fi
    fi
    if (( ${R_PORT} > 0 )); then
	python ${SCRIPT_PATH} -p ${R_PORT} -v 1
    else
	if [[ $1 == stop ]]; then
	    python ${SCRIPT_PATH} -p 4 -v 0
	fi
    fi
else 
    python ${SCRIPT_PATH} -p 4 -v 0
fi

