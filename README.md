# pybis2spice
A python tool that converts IBIS models to SPICE models. The ibis model types currently supported are: 
* Input
* Output
* 3-State
* Open_Drain
* I/O

This tool was originally developed and maintained by Kishan Amratia (https://github.com/kamratia1) but has since moved to a new repo (https://github.com/Jamanaman/pybis2spice) and the project will be continued there for the foreseeable future.

## Docs
To read the docs go to https://pybis2spice.readthedocs.io/en/latest/. These are maintained alongside the project and include some simple code examples for programmatic use of the internal functions that may be helpful for integration into automation projects. 

## Usage
The bin folder holds a zipped file for each released version containing a windows executable program that can be run standalone.

![](/img/gui-window.png)

### The executable program allows the user to:
* Browse for an ibis model file
* Select the component and the model
* Create the SPICE subcircuit files
* View the ibis model characteristics (I-V and Voltage-Time graphs)

![](/img/gui-check-model.png)


### Spice Subcircuit option: 
* LTSpice: LTSpice option produces a subcircuit file and corresponding LTSpice symbol file. 
This option creates a subcircuit that is specifically intended to be used with LTSpice. 
This is the recommended option as it provides the most flexibility for output model stimulus sources. 
* Generic: generic option produces a subcircuit file that most Spice simulators should be able to parse.
* ngSPICE: ngSPICE option produces a subcircuit file that is compatible with ngSPICE and can therefore be used for KiCAD and QUCS-S simulation as well as PySPICE/InSPICE simulations. This works with the same output model stimulus sources as provided by the LTSpice option. 

### Corner Select: 
* Weak-Slow: Combines the minimum (weak) I-V curves and minimum (slow) Voltage-Time waveforms   
* Typical: Combines the typical I-V curves and typical Voltage-Time waveforms
* Fast-Strong: Combines the maximum (strong) I-V curves and maximum (fast) Voltage-Time waveforms
* All: Creates the subcircuit files for all corners simultaneously

## Examples
LTSpice examples are given to highlight the different options available. 
These are available in the examples folder provided with the executables.

## Contribution
Developers can contribute to the tool by forking the repository and submitting pull requests.

## Issues and Feature Requests
* Please record any bugs, issues and feature requests here: https://github.com/Jamanaman/pybis2spice/issues
* Detailed information on how any issue can be reproduced should be provided including any IBIS files used and version number of the program. Screenshots would also help.

## References
The tool would not be possible without the ecdtools library. This parses the ibis file into python data structures.
https://ecdtools.readthedocs.io/en/latest/#