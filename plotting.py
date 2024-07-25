import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

import sys

COLORS = ["darkblue","blue","royalblue","cyan","limegreen","yellow","darkorange","red","darkred"]

def set_colormap(under_color="black", over_color="darkred"):
    """
        Create and configure the colors of a heatmap.

        Args:
            under_color (str): The name of the color to be set for undervalues. Defaults to black.
            over_color (str): The name of the color to be set for over values. Defaults to darkred.

        Returns:
            mcolors.LinearSegmentedColormap:
                The heatmap created.
    """

    hmap = mcolors.LinearSegmentedColormap.from_list("heatmap", COLORS)
    hmap.set_over(over_color) # values above MAX_VALUE
    hmap.set_under(under_color) # values below MIN_VALUE
    
    return hmap

def set_labels(labels):
    """
        Set the x-axis, y-axis and title labels of the graphic.

        Args:
            labels (list): A list of labels to be included in the graphic. Should contain:
                           - labels[0]: The title of the graphic.
                           - labels[1]: The label for the x-axis.
                           - labels[2]: The label for the y-axis.
        Returns:
            None
    """

    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])

def get_levels(min_max_values, data_type):
    """
        Determine the levels for the contour graphic.

        Args:
            min_max_values (tuple): A tuple containing two floats indicating the minimum and maximum values, respectively.
            data_type (str): Indicates whether the levels generated should be of type 'int' or 'float'.

        Returns:
            np.ndarray: An array containing the levels to be used in contour and contourf functions.
    """

    min_value, max_value = min_max_values

    levels = None
    if data_type == "int":
        levels = np.linspace(min_value,max_value, 9, endpoint=False, dtype=int)
    elif data_type == "float":
        levels = np.linspace(min_value, max_value, 9, endpoint=False, dtype=float)
    else:
        sys.stderr.write(f"Unknow data type on get_levels.\n")
        exit()

    return levels

def get_scaling_law():
    """
        Determines the x and y values of the scaling law from VARAS (2007).

        Returns:
            tuple: A tuple containing two lists:
                - The first list contains the x values.
                - The second list contains the y values of the scaling law from Eq(1) in the VARAS (2007) article.
    """

    exit_width = np.linspace(1, 14, 100)
    scaling_law = [2 / ew for ew in exit_width]
    exit_width = exit_width - 1 # the axis plot begins at point zero

    return  exit_width, scaling_law

def plot_heatmap(data_matrix, min_max_values, output_file, labels, over_value_color="darkred", origin="lower"):
    """
        Generate a heatmap based on the parameters' data.

        Args:
            data_matrix (np.ndarray): A 2D numpy array representing the data.
            min_max_values (tuple): indicates the minimum and maximum values, respectively.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                       - labels[0]: The title of the graph.
                       - labels[1]: The label for the x-axis.
                       - labels[2]: The label for the y-axis.
            over_value_color (str): The color to be used for coloring over values. Defaults to darkred.
            origin (str): Indicates where the [0,0] coordinates should be placed (lower, upper). Defaults to "lower".
        Returns:
            None
    """

    fig = plt.figure()

    (min_value, max_value) = min_max_values
    plt.imshow(data_matrix, vmin=min_value, vmax=max_value, cmap=set_colormap(over_color=over_value_color), origin=origin)
    plt.colorbar()

    set_labels(labels)

    fig.savefig(f"out/{output_file}")

def plot_contours_graphic(data_matrix, min_max_values, output_file, labels, data_type):
    """
        Generate a contour graphic based on the parameters' data.

        Args:
            data_matrix (np.ndarray): A 2D numpy array representing the data.
            min_max_values (tuple): indicates the minimum and maximum values, respectively.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                       - labels[0]: The title of the graph.
                       - labels[1]: The label for the x-axis.
                       - labels[2]: The label for the y-axis.
            data_type (str): indicates if the contour graphic is generated out of "int" or "float" data.

        Returns:
            None
    """

    fig = plt.figure()

    (min_value, max_value) = min_max_values
    levels = get_levels(min_max_values, data_type)

    plt.contour(data_matrix, vmin=min_value, vmax=max_value, levels=levels, colors="black", origin="lower", extend="both", linewidths=0.5)  # generate contour lines
    plt.contourf(data_matrix, vmin=min_value, vmax=max_value, levels=levels, cmap=set_colormap(), origin="lower", extend="both", antialiased=True)  # generate filled contour

    plt.colorbar()  # add the colorbar

    set_labels(labels)

    fig.savefig(f"out/{output_file}")

def plot_line_graphic(x_axis_ticks, y_axis_ticks, legends, data_vector, output_file, labels, scaling_law):
    """
        Generates a line graph with at least one line. Each line is plotted using each list of data_vector.

        Args:
            x_axis_ticks (tuple): A tuple containing two elements:
                                  - The location of the x-axis ticks.
                                  - The values of the x-axis ticks.
            y_axis_ticks (tuple): A tuple containing two elements:
                                  - The location of the y-axis ticks.
                                  - The values of the y-axis ticks.
            legends (list): The legends of each data set (list) in data_vector.
            data_vector (list[list]): A list of lists containing the data to be plotted.
                                      Each list represents one of the lines of the graphic.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                           - labels[0]: The title of the graphic.
                           - labels[1]: The label for the x-axis.
                           - labels[2]: The label for the y-axis.
            scaling_law (bool): Indicates if the scaling law of (VARAS, 2007) should be plotted.
        Returns:
            None

        Note:
            If no axis information is provided, the locations and values of both the x-axis and y-axis are automatically determined.
            If axis locations are specified but values are not, the values are automatically determined.
            If x-axis values are provided without locations, these values are used directly as the x argument in the plot function.
            If y-axis values are provided without locations, they are ignored.
    """

    x_tick_locations, x_tick_values = x_axis_ticks
    y_tick_locations, y_tick_values = y_axis_ticks

    fig, ax = plt.subplots()

    if x_tick_locations:
        x_tick_locations = list(map(float, x_tick_locations))

        if x_tick_values:
            ax.set_xticks(x_tick_locations,x_tick_values)
        else:
            ax.set_xticks(x_tick_locations)

    if y_tick_locations:
        y_tick_locations = list(map(float, y_tick_locations))

        if y_tick_values:
            ax.set_yticks(y_tick_locations, y_tick_values)
        else:
            ax.set_yticks(y_tick_locations)

    for data_line in data_vector:
        if not x_tick_locations and x_tick_values:
            if len(x_tick_values) != len(data_line):
                sys.stderr.write(f"The number of elements in the x-axis ({len(x_tick_values)}) is different from the number os elements in the y-axis ({len(data_line)}).\n")
                exit()

            plt.plot(x_tick_values, data_line, 'o-')
        else:
            plt.plot(data_line, "o-")

    if scaling_law:
        legends.append("T/N=2/a")
        x, y = get_scaling_law()
        plt.plot(x,y)

    set_labels(labels)

    if len(legends) > 1:
        plt.legend(legends)

    fig.savefig(f"out/{output_file}")

def plot_scatter_graphic(x_axis_ticks, y_axis_ticks, legends, data_vector, output_file, labels):
    """
        Generates a point graphic. Multiple data sets can be plotted into the same graphic.

        Args:
            x_axis_ticks (tuple): A tuple containing two elements:
                                  - The location of the x-axis ticks.
                                  - The values of the x-axis ticks.
            y_axis_ticks (tuple): A tuple containing two elements:
                                  - The location of the y-axis ticks.
                                  - The values of the y-axis ticks.
            legends (list): The legends of each data set (list) in data_vector.
            data_vector (list[list]): A list of lists containing the data to be plotted.
                                      Each list represents one of the lines of the graphic.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                           - labels[0]: The title of the graphic.
                           - labels[1]: The label for the x-axis.
                           - labels[2]: The label for the y-axis.
        Returns:
            None

        Note:
            If axis locations are provided without corresponding values, the values will be automatically determined.
            The x-axis locations are required.
            If y-axis values are provided without locations, they are ignored.
    """

    x_tick_locations, x_tick_values = x_axis_ticks
    y_tick_locations, y_tick_values = y_axis_ticks

    fig, ax = plt.subplots()

    if not x_tick_locations:
        sys.stderr.write(f"x-axis tick locations are required.\n")
        exit()

    if y_tick_locations:
        y_tick_locations = list(map(float, y_tick_locations))

        if y_tick_values:
            ax.set_yticks(y_tick_locations, y_tick_values)
        else:
            ax.set_yticks(y_tick_locations)

    x_tick_locations = list(map(float, x_tick_locations))

    if not x_tick_values:
        ax.set_xticks(x_tick_locations)
    else:
        ax.set_xticks(x_tick_locations, x_tick_values)

    plt.scatter(x_tick_locations, data_vector[0])

    set_labels(labels)

    if len(legends) > 1:
        plt.legend(legends)

    fig.savefig(f"out/{output_file}")