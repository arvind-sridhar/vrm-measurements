# CARRICOOL PYTHON


## Introduction

## Requirements

* Python 3.6
* Eclipse Neon.3 Release (4.6.3) (Debug only)
* PyDev for Eclipse	5.7.0.201704111357 (Debug only)

## Install Packages
The required packages can be installed through the python 3.6 native package manager pip using the following command:

	# python -m pip install -r requirements.txt

## Run main application

	# python GF1408.py
	
## Main packages

1. GF1408_tools
	* main package for the GF1408 RIT GUI
1. measurement
	* package for new style instrument classes	 
1. measurement_old
	* package for old style instruments classes from pre-2014
	* to run old code, python 2.7 and PyVISA 1.8  might be necessary
1. lkuluu
	* example implementation of a measurement setup using the new objects
	

## Bits of the GF1410 CarrICool Chip 


| Register name     | Register address|  Bits |
|-------------------|:---------------:|:-----:|
| EN_DPWM           |        0        |   0   |
| RESET_COUNT       |        0        |   1   |
| DUTY              |        0        |  2:5  |
| Deadtime NMOS     |        0        |  6:8  |
| Deadtime PMOS     |        0        |  9:11 |
| SEL_0             |        1        |  0:1  |
| SEL_1             |        1        |  2:3  |
| SEL_2             |        1        |  4:5  |
| SEL_3             |        1        |  6:7  |
| EN_PH             |        1        |  8:11 |
| LOAD_EN           |        2        |  0:11 |
| LOAD_EN           |        3        |  0:11 |
| LOAD_EN           |        4        |  0:7  |
| LOAD_CTRL_EN      |        4        |   8   |
| LOAD_CTRL_PROG    |        4        |   9   |
| LOAD_CTRL_SEL_CLK |        4        | 10:11 |


### Bit to duty cycle map

| Duty Cycle  | 		Bits<0:3>		|
|-------------|:------------------:|
| 0 %         |        0000 	   	|
| 6.25 %      |        0001 	   	|
| ...         |        ... 	   		|
| 93.75 %     |        1111 	   	|


### P- and N-MOS switches deadtime map 

| Deadtime in units <0:2>     | Deadtime bit value|
|-----------------------------|:-----------------:|
| TODO           		     	  |        TODO       |

### Phase Selection

| SEL_X  | 		Bits		|
|-----------------------------|:----------------:|
| 0°          		     	  |        00 	   |
| 90°           		     	  |        01 	   |
| 180°           		     	  |        10 	   |
| 270°           		     	  |        11 	   |




	