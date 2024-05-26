import math
import numpy as np
import sys

def alizadeh_heatmap(filename, ignore_marked_data, data_type, force_over_values):
    """
        Process data related to the experiments of (Alizadeh, 2011) that are plotted as heatmaps or contours.
        This function can process the data originated from the pedestrian distribution (between two doors) experiment and the evacuation timestep experiments.

        Args:
            filename (str): The name of the file containing the data.
            ignore_marked_data (bool): Indicates if data on lines beginning with '#1' must be ignored when calculating min/max.
            data_type (str): Indicates whether the data contained on FILENAME is of type 'int' or 'float'.
            force_over_values (bool): Indicates if over values (on lines beggining with #1) must be forced to be higher (in order for them to be colored darkred).

        Returns:
            tuple (np.ndarray, tuple(float, float)):
                A tuple containing:
                - An array reshaped into a square matrix.
                - Another tuple containing two float numbers representing the min and max values of the data processed.

        Notes:
            - It is expected that the input file contains 3 lines without simulation data at the beginning of the file.
            - The remaining lines of the file must each contain at least one data value.
            - Lines beginning with '#1' indicate a set of simulations done in a room with only one door and are ignored when calculating min/max values.
            - Data values equal to -1 refer to simulations where one of the doors was not accessible and should be ignored.
    """

    data_vector = []
    min_value = math.inf
    max_value = -math.inf

    try:
        with open(filename) as file:
            for _ in range(3):
                file.readline()  # ignore the lines that doesn't contain simulation data on the beggining of the file

            while True:
                line = file.readline()

                if line == "":
                    break  # EOF reached

                current_line_data = line.strip("\n ").split(" ")
                if current_line_data[0] == "#1":
                    marked_data = True
                    current_line_data = current_line_data[1:]
                else:
                    marked_data = False

                if data_type == "int":
                    data_value = list(map(int, current_line_data))
                elif data_type == "float":
                    data_value = list(map(float,current_line_data))
                else:
                    sys.stderr.write(f"Unknow data type on alizadeh_heatmap.\n")
                    exit()

                if not marked_data or not ignore_marked_data:
                    min_corrent = min(data_value)
                    max_corrent = max(data_value)
                    if min_corrent != -1 and min_corrent < min_value:
                        min_value = min_corrent

                    if max_corrent != -1 and max_corrent > max_value:
                        max_value = max_corrent

                if marked_data and force_over_values:
                    data_value = [x * 2 for x in data_value] # by making the values higher the generated contours will be correct.

                data_vector.append(np.mean(data_value))
    except FileNotFoundError:
        sys.stderr.write(f"File {filename} not found.\n")
        exit()
    except ValueError:
        sys.stderr.write(f"Non-numeric value found in the data.\n")
        exit()

    # the square root of the number of values in data_vector must be an integer, indicating that is possible to build a square matrix out of it.
    data_vector_len = math.sqrt(len(data_vector))
    data_vector_len_truncated = int(data_vector_len)
    if abs(data_vector_len - data_vector_len_truncated) > 1e-8:
        sys.stderr.write(f"Not enough data lines in {filename}\n")
        exit()

    return np.array(data_vector).reshape(data_vector_len_truncated, data_vector_len_truncated), (min_value, max_value)

def alizadeh_alpha_timesteps_relation(filename):
    """
        Process data related to the alpha/timesteps relation experiment of (Alizadeh, 2011).

        Args:
            filename (str) - name of the file containing the data

        Returns
            tuple: a tuple containing the data of the x-axis and the y-axis to be plotted, respectively.

        Note:
            It is expected that the input file contains only lines with data. The first line must contain the x-axis data, while the remaining lines must contain at least one value each. The mean value of all data in the same line will be used as the data for the y-axis, corresponding to the i-th value of the x-axis.
    """
    
    y_axis = [] # store data to be plotted on the y-axis
    
    try:
        with open(filename) as file:
            lines = file.readlines()
            
            x_axis = lines[0].strip("\n ").split(" ")  # store data to be plotted on the x-axis

            for line in lines[1:]:
                y_axis.append(np.mean( np.array([float(x) for x in line.strip("\n ").split(" ")])))
    except FileNotFoundError:
        sys.stderr.write(f"File {filename} not found.\n")
        exit()
    except ValueError:
        sys.stderr.write(f"Non-numeric value found in the y-axis data.\n")
        exit()
        
    if len(x_axis) != len(y_axis):
        sys.stderr.write(f"The number of elements in the x-axis ({len(x_axis)}) is different from the number os elements in the y-axis ({len(y_axis)}).\n")
        exit()
        
    return x_axis, y_axis
