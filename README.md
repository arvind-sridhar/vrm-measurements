# CarriCool Python


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
	

## Bits of the CarrICool Chips


### Open-Loop and Load Settings

<table style="text-align:center">
	<thead>
      <tr>
         <th></th>
         <th colspan="2">IBM32</th>
         <th colspan="2">GF1408</th>
         <th colspan="2">GF1409</th>
         <th colspan="2">GF1410</th>
      </tr>
      <tr>
         <th>Register name</th>
         <th>Reg #</th>
         <th>Bits</th>
         <th>Reg #</th>
         <th>Bits</th>
         <th>Reg #</th>
         <th>Bits</th>
         <th>Reg #</th>
         <th>Bits</th>
      </tr>
   </thead>
   <tbody>
    	<tr>
         <td style="text-align:center">EN_DPWM</td>
         <td>2</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>RESET_COUNT</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>1</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>DUTY</td>
         <td>1</td>
         <td>0:3</td>
         <td>0</td>
         <td>2:5</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>Deadtime NMOS</td>
         <td>2</td>
         <td>5:7</td>
         <td>0</td>
         <td>6:8</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>Deadtime PMOS</td>
         <td>2</td>
         <td>8:11</td>
         <td>0</td>
         <td>9:11</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>SEL_0</td>
         <td>1</td>
         <td>4:5</td>
         <td>1</td>
         <td>0:1</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>SEL_1</td>
         <td>1</td>
         <td>6:7</td>
         <td>1</td>
         <td>2:3</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>SEL_2</td>
         <td>1</td>
         <td>8:9</td>
         <td>1</td>
         <td>4:5</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>SEL_3</td>
         <td>1</td>
         <td>10:11</td>
         <td>1</td>
         <td>6:7</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>EN_PH</td>
         <td>2</td>
         <td>1:4</td>
         <td>1</td>
         <td>8:11</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_EN_1</td>
         <td>0</td>
         <td>3:7</td>
         <td>2</td>
         <td>0:11</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_EN_2</td>
         <td>-</td>
         <td>-</td>
         <td>3</td>
         <td>0:11</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_EN_3</td>
         <td>-</td>
         <td>-</td>
         <td>4</td>
         <td>0:7</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_CTRL_EN</td>
         <td>0</td>
         <td>1</td>
         <td>4</td>
         <td>8</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_CTRL_PROG</td>
         <td>0</td>
         <td>2</td>
         <td>4</td>
         <td>9</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
      <tr>
         <td>LOAD_CTRL_SEL_CLK</td>
         <td>-</td>
         <td>-</td>
         <td>4</td>
         <td>10:11</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
         <td>0</td>
      </tr>
   </tbody>
</table>




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


## List of equipment

- Input voltage node
	- Source: Keithley 2400 or 2602
	- Measurement:
		- Current: Keithley 2400 or 2602
		- Voltage: Agilent 34970 Data Acquisition/Switch
		- Voltage ripple: Oscilloscope Tektronix DSA72004
- Output voltage node
	- Measurement:
		- Output voltage ripple: Tektronix DSA72004
		- Voltage: Agilent 34970 Data Acquisition/Switch
- Vx node
	- Measurement: Oscilloscope Tektronix DSA72004
- High-frequency clock node:
	- Source: Signal generator Agilent 8648 D
- Vd node:
	- Source: DC power supply Agilent E3642A
- Communication board:
	- In-house customized interface board
- Inductor characterization:
	- 8360L Series Swept CW generator: 10MHz - 50 GHz (excitation)
	- HP8510C: Vector network analyzer
	- HP8517B: 45MHz - 50 GHz s-parameter test set
- Temperature measurement
	- Thermal camera
- Connections
	- DC and high-frequency cables


## TODO

- [x] Communication with hammerhead
- [x] Communication with instruments
- [ ] GUI-instruments binding
	