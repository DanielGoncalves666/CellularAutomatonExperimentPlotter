# Cellular Automaton Experiment Plotter

A simple program designed to process and plot data generated from various Cellular Automaton models applied to pedestrian evacuation scenarios.

## Required Dependencies

To run the program, you need to install the `numpy` and `matplotlib` libraries, preferably in a Python virtual environment. You can create and activate the virtual environment and install the necessary packages by executing the `env_setup.sh` script.

```shell
./env_setup.sh
```

## How to Run

To execute the program, run the `run.sh` script followed by the required options. For a list of all available options, run:

```shell
./run.sh --help
```

The scripts `varas_experiments_plotter.sh` and `alizadeh_experiments_plotter.sh` provide examples of how to run the program to generate various graphics. 

## Available Options

### Input

The `-i` option specifies the name of the file containing the data to be used for plotting the graphic. 
This file can either be an actual data file, or a configuration file. Refer to the [Selecting the Graphic to be generated](#selecting-the-graphic-to-be-generated) section to determine the required file type for each graphic.

#### Data file

This file is the direct output obtained from an experiment using any implementation of a Cellular Automaton for pedestrian evacuation (with exception to files for environment_heatmap graphics). Its content follows this structure:

* The first line contains the command used to generate the data.
* The second line is a separator formed by hyphens (`-`).
* The third line is empty.
* The remaining lines contain the simulation results, typically the number of timesteps. Each line refers to a combination of doors.  

#### Environment Heatmap Data File

This kind of file is used to generate environment heatmaps. Optionally, the beginning of the file may include the locations and corresponding values of the axis ticks for each axis in the following structure:

* The first line contains the locations of the x-axis ticks.
* The second line contains the values of the x-axis ticks.
* The third line contains the locations of the y-axis ticks.
* The fourth line contains the values of the y-axis ticks.
* The fifth line contains the locations of the z-axis ticks (for 3D heatmaps).
* The sixth line contains the values of the z-axis ticks (for 3D heatmaps).

If some tick information is not defined, the line must remain blank. 
Following these may come any number of lines, where each value in each line corresponds to a single cell.

For 2d environment heatmaps the z-axis tick information is ignored.

#### Configuration File

This file contains information about the graphic tick locations and values for each axis, as well as the name of at least one data file. Its content follows this structure:

* The first line contains the locations of the x-axis ticks.
* The second line contains the values of the x-axis ticks.
* The third line contains the locations of the y-axis ticks.
* The fourth line contains the values of the y-axis ticks.
* The remaining lines each contain the name of a data file, optionally followed by the legend to be used for it, if necessary.

The axes tick information is optional. Refer to the code to understand how the program behaves when some or all tick information is not provided.

### Output

The output will always be stored in the `out/` directory. You can specify the name of the output file using the `-o` option. If the `-o` option is not provided, a default name will be assigned to the file.

### Title and axis labels

You can specify the title and labels for the x and y axes using the `-t`, `-x`, and `-y` options, respectively.

### Selecting the Graphic to be generated

The graphic to be generated must be selected using the `-g` or `--graphic` option. The following graphics are available:

1. environment_heatmap: \
Generates a heatmap of an environment. 
Each value in the input file (after the ticks configuration lines) corresponds to a single cell in the environment.
2. 3d_environment_heatmap: \
Generates a 3d heatmap of an environment.
The input data is the same as the environment_heatmap. The final graphic will have one less cell in both axis, since the values are used to plot a surface instead of a grid. 
3. heatmap: \
Generates a heatmap. 
Each line of the input file corresponds to a single value in the heatmap. If necessary, a mean of the values in each line is calculated.
4. int_contours: \
Generates a contour graphic from integer data. 
5. float_contours: \
Generates a contour graphic from floating point data.
6. line_graphic: \
Generates a line graphic with at least one line. 
7. scatter_graphic: \
Generates a point graphic. Multiple data sets can be plotted into the same graphic.
8. varas_door_width_7: \
Generates a line graph. The provided data undergo the necessary operations to recreate Figure 7 from Varas (2007).
9. varas_door_width_9: \
Generates a line graph. The provided data undergo the necessary operations to recreate Figure 9 from Varas (2007).

### Dealing with specific data

#### Single door rooms (on simulations that should be double)

The **heatmap** and **contours** graphics can receive data from simulations where a single door was used. In those cases, the `--ignore-marked-data` option will make the program ignore that data when calculating the minimum and maximum values. The minimum and maximum values affect the colorbar and the levels of the contour graphic.

#### Forcing over values

In some instances of **contours** graphics, certain values may not be colored correctly. In these cases, the `--force-over-values` option can be used to ensure they are properly colored.

#### Wall and obstacle value

In the **environment_heatmap** graphic, values equal and above (or below) a certain threshold are considered as a wall or obstacle and colored outside the colorbar range. 
For positive threshold, values equal and above are the ones considered, while for a negative threshold values equal and below are the ones considered.
The default value for this feature is 1000, but can be altered using the `--wall-threshold` option. 

#### Suppressing exits in 3D environment heatmap

For 3d environment heatmaps the exits in the reticulate will appear outside the main part body of the graphic and single walls will not be plotted altogether. The latter occurs because the 3D heatmap is plotted using 
a surface function. In order to avoid the former, the `-suppress-heatmap-exits` option can be used to remove the exits.

## Program Architecture

The program is divided into three Python files. The `run.py` file contains the main code, where all necessary functions are called to generate the desired graphic.

### Processing module

The `processing.py` file contains functions responsible for reading the input file and calculating the necessary data to generate the graphics.

### Plotting module.py

The `plotting.py` file contains functions responsible for preparing and plotting the graphics.