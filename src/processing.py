import math
import numpy as np
import sys

class NoticeError(Exception):
    """Exception raised to indicate that an error occurred elsewhere and has already been handled, but the program must be terminated. It is used to ensure that files opened within functions in the call tree are properly closed.

    Attributes:
        message (str): explanation of the error
    """

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[Error]: {self.message}"

def extract_tick_information(line):
    """
        Extract individual axis tick information from the given string.

        Args:
            line (str): a string containing axis tick information.
        Returns
            list: A list of strings representing the axis tick information.
              If the input string contains no tick information, an empty list is returned.
    """

    line = line.strip(" \n")

    if line == "":
        return []

    return line.split(" ")

def process_env_heatmap_data(filename: str, wall_threshold: float, dimension: str):
    """
        Process data that will be plotted into an environment heatmap.

        Args:
            filename (str): The name of the file containing the axis tick configurations and the data.
            wall_threshold (float): The threshold from which a value is considered to be an over value. For a negative threshold the values below it are considered.
            dimension (str): Indicates the dimension to which the extracted data will be plotted. Used to ignore z-axis tick information for 2d graphics.

        Returns:
            A tuple containing:
                - A 2-tuple with the locations and values of the x-axis ticks.
                - A 2-tuple with the location and values of the y-axis ticks.
                - A 2-tuple with the location and values of the z-axis ticks.
                - A 2 dimension numpy array.
                - A float, indicating the maximum value of the data (ignoring over values).
    """

    data_matrix = []
    maximum_value = -1

    very_high_value = 2 ** 30 # For a negative threshold, all values equal or below it are converted to the very_high_value in order to not require further alterations in the code.
    verification_threshold = wall_threshold if wall_threshold > 0 else very_high_value

    z_ticks = ([], [])
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

            x_tick_locations = extract_tick_information(lines[0])
            x_tick_values = extract_tick_information(lines[1])
            y_tick_locations = extract_tick_information(lines[2])
            y_tick_values = extract_tick_information(lines[3])

            line_index = 4
            if dimension == "3d":
                z_tick_locations = extract_tick_information(lines[line_index])
                z_tick_values = extract_tick_information(lines[line_index + 1])
                z_ticks = (z_tick_locations, z_tick_values)

            line_index += 2

            first_data_line = lines[line_index].strip("\n ").split()
            line_index += 1
            if wall_threshold < 0:
                first_data_line = [very_high_value if float(x) <= wall_threshold else x for x in first_data_line]

            data_matrix.append(list(map(float, first_data_line)))

            len_of_lines = len(first_data_line)
            for line_number, line in enumerate(lines[line_index:], start=1):
                if line == "\n":
                    continue

                line = line.strip("\n ").split()

                if len(line) != len_of_lines:
                    sys.stderr.write(f"Line {line_number} contains a different number of elements ({len(line)}) compared to the first line ({len_of_lines}).\n")
                    exit()

                if wall_threshold < 0:
                    line = [very_high_value if float(x) <= wall_threshold else x for x in line]

                line_data = list(map(float, line))
                for v in line_data:
                    if maximum_value < v < verification_threshold:
                        maximum_value = v

                data_matrix.append(line_data)
    except FileNotFoundError:
        sys.stderr.write(f"File {filename} not found.\n")
        exit()
    except ValueError:
        sys.stderr.write(f"Non-numeric value found in the data.\n")
        exit()

    return (x_tick_locations, x_tick_values), (y_tick_locations, y_tick_values), z_ticks, np.array(data_matrix), maximum_value

def process_heatmap_data(filename, ignore_marked_data, data_type, force_over_values):
    """
        Process data that can be plotted into a heatmap or into a contour graphic.
        The data is read from a single file, processed and then returned as a square matrix.

        Args:
            filename (str): the name of the file containing the data.
            ignore_marked_data (bool): indicates if data on lines beginning with '#1' must be ignored when calculating min/max.
            data_type (str): indicates whether the data contained on the FILENAME is of type 'int' or 'float'.
            force_over_values (bool): indicates if over values (on lines beginning with #1) must be forced to be higher (in order for them to be colored darkred).

        Returns:
            tuple (np.ndarray, tuple(float, float)):
                A tuple containing:
                - An array reshaped into a square matrix.
                - Another tuple containing two float numbers representing the min and max values of the data processed.

        Notes:
            - It is expected that the input file contains 3 lines without simulation data at the beginning.
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
                file.readline()  # ignore the lines that don't contain simulation data on the beggining of the file.

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
                    sys.stderr.write(f"Unknow data type on process_heatmap_data.\n")
                    exit()

                if not marked_data or not ignore_marked_data:
                    min_current = min(data_value)
                    max_current = max(data_value)
                    if min_current != -1 and min_current < min_value:
                        min_value = min_current

                    if max_current != -1 and max_current > max_value:
                        max_value = max_current

                if marked_data and force_over_values:
                    data_value = [x * 2 for x in data_value] # by making the values higher, the generated contours will be correct.

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

def process_configuration_file(filename):
    """
        Process information from a configuration file, which can contain the location and value of the x and y-axis ticks and must contain the name of at least one data file. Optionally, each data file can be accompanied by a legend.

        Args:
            filename (str): The name of the file that contains information about the x-axis and y-axis ticks, the names of the files with the data, and their respective legends.
        Returns:
            tuple: a 4-tuple of two 2-tuples and two lists:
                This first element contains a tuple with the locations and values of the x-axis ticks.
                The second element contains a tuple with the locations and values of the y-axis ticks.
                The third element contains a list with the legends of each data set.
                The fourth element contains a list with the data sets (a list of lists).

        Note:
            It's expected that the input file follows this structure:
                - The first line must contain the locations of the x-axis ticks.
                - The second line must contain the values of the x-axis ticks.
                - The third line must contain the locations of the y-axis ticks.
                - The fourth line must contain the values of the y-axis ticks.
                - The remaining lines must contain pairs of filenames, with a set of data, and the respective legend to be included in the graphic.

            It's assumed that the configuration file and all the files with their names inside it are located in the same directory.
    """

    legends = []
    data_vector = []

    directory = "/".join(filename.split("/")[:-1]) # extract the directory of the configuration file

    try:
        with open(filename) as file:
            lines = file.readlines()

            x_tick_locations = extract_tick_information(lines[0])
            x_tick_values = extract_tick_information(lines[1])
            y_tick_locations = extract_tick_information(lines[2])
            y_tick_values = extract_tick_information(lines[3])

            for line in lines[4:]:
                try:
                    data_file, legend = line.strip("\n ").split(" ")
                except ValueError:
                    legend = None
                    data_file = line.strip("\n ")

                legends.append(legend)
                data_vector.append(process_experimental_data_file(f"{directory}/{data_file}"))
    except FileNotFoundError:
        sys.stderr.write(f"File {filename} not found.\n")
        exit()
    except NoticeError:
        exit()

    return (x_tick_locations, x_tick_values), (y_tick_locations, y_tick_values), legends, data_vector

def process_experimental_data_file(filename):
    """
        Process data outputed from the implementation of a cellular automaton model.

        Args:
            filename (str): name of the file containing the data

        Returns:
            list: containing the data obtained from the file.

        Raises:
            NoticeError: If the file is not found or if there are non-numeric values in its data, NoticeError is raised to indicate that the necessary actions to deal with the error were performed and that any function that calls 'process_varas_data_file' needs to terminate the program. This is done to ensure that any open file is closed.
    """

    data_vector = []

    try:
        with open(filename) as file:
            for _ in range(3):
                file.readline()  # ignore the lines that don't contain simulation data on the beggining of the file.

            while True:
                line = file.readline()

                if line == "":
                    break  # EOF reached

                current_line_data = list(map(int,line.strip("\n ").split(" ")))

                data_vector.append(np.mean(current_line_data))
    except FileNotFoundError:
        sys.stderr.write(f"File {filename} not found.\n")
        raise NoticeError
    except ValueError:
        sys.stderr.write(f"Non-numeric value found in the {filename} data.\n")
        raise NoticeError

    return data_vector

def varas_door_width_fig_7(legends, data_vector):
    """
        Calculates the Tu - Te difference, where Tu stands for a simulation of the Fig. 6 (VARAS, 2007) experiment and Te stands for the same simulation but with the two columns to the left of the room without any pedestrians.
        This difference is used to plot the Fig. 7 experiment from (VARAS, 2007).

        Both legends and data_vector contain values related to Tu and Te, in alternating order.
        The first value is a Tu, the second Te, the third Tu and so on.

        Args:
            legends (list): the legends of each data set.
            data_vector (list[lists]): a list with the data sets
        Returns:
            tuple: a 2-tuple containg two lists:
                - the final legends
                - the calculated Tu - Te difference for every pair of normal configuration and empty configuration vectors of data_vector.
    """

    if len(data_vector) % 2 != 0:
        sys.stderr.write(f"The number of data sets must be even.\n")
        exit()

    normal_configuration = [u for u in data_vector[::2]]
    empty_configuration = [e for e in data_vector[1::2]] # data sets where the two first columns at the lef of the room were empty.

    difference_data_vector = []
    for tu, te in zip(normal_configuration, empty_configuration):
        if len(tu) != len(te):
            sys.stderr.write(f"O número de elementos dos vetores Tu deve ser o mesmo dos vetores Te.\n")

        difference_data_vector.append([u - e for u, e in zip(tu, te)])

    legends = [i for i in legends[::2]]

    return legends, difference_data_vector

def varas_door_width_fig_9(legends, data_vector):
    """
        Calculates the T/N quotient, where T is the timesteps mean and N is the number of pedestrians.

        Args:
            legends (list): the legends of each data set. They will be used to extract the N values.
            data_vector (list[lists]): a list with the data sets
        Returns:
            list: containing the T/N quotient for each data set.
    """

    number_pedestrians = []
    for l in legends:
        _, n = l.split("=")
        number_pedestrians.append(int(n))

    quotient_data_vector = []
    for data_set, n in zip(data_vector, number_pedestrians):
        quotient_data_vector.append([t / n for t in data_set])

    return quotient_data_vector