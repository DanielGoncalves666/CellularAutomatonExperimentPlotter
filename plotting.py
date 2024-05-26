import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

import sys

COLORS = ["darkblue","blue","royalblue","cyan","limegreen","yellow","darkorange","red","darkred"]

def set_colormap():
    """
        Create and configure the colors of a heatmap.

        Returns:
            mcolors.LinearSegmentedColormap:
                The heatmap created.
    """

    hmap = mcolors.LinearSegmentedColormap.from_list("heatmap", COLORS)
    hmap.set_over("darkred") # values above MAX_VALUE receive red color
    hmap.set_under("black") # values below MIN_VALUE receive black color
    
    return hmap

def get_levels(min_max_values, data_type):
    """
        Determine the levels for the contour graphic.

        Args:
            min_max_values (tuple): A tuple containing two floats indicating the minimum and maximum values, respectively.
            data_type (str): Indicates whether the levels generated should be of type 'int' or 'float'.

        Returns:
            np.ndarray: An array containing the levels to be used in plt.contour and plt.contourf.
    """

    min_value, max_value = min_max_values

    if data_type == "int":
        levels = np.linspace(min_value,max_value, 9, endpoint=False, dtype=int)
    elif data_type == "float":
        levels = np.linspace(min_value, max_value, 9, endpoint=False, dtype=float)
    else:
        sys.stderr.write(f"Unknow data type on get_levels.\n")
        exit()

    return levels

def plot_heatmap_or_contours(data_matrix, min_max_values, output_file, labels, graphic_type, data_type):
    """
        Generate a heatmap or contours graphic based on the parameters' data.

        Args:
            data_matrix (np.ndarray): A 2D numpy array representing the data.
            min_max_values (tuple): indicates the minimum and maximum values, respectively.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                       - labels[0]: The title of the graph.
                       - labels[1]: The label for the x-axis.
                       - labels[2]: The label for the y-axis.
            graphic_type (str): Indicates if the graphic to be generated is a heatmap or a contours graphic.
            data_type (str): indicates if the heatmap or contours graphic is generated out of "int" or "float" data.

        Returns:
            None
    """

    fig = plt.figure()

    (min_value, max_value) = min_max_values
    if graphic_type == "contours":
        levels = get_levels(min_max_values, data_type)
        plt.contour(data_matrix, vmin=min_value, vmax=max_value, levels=levels, colors="black", origin="lower", extend="both", linewidths=0.5) # generate contour lines
        plt.contourf(data_matrix, vmin=min_value, vmax=max_value, levels=levels, cmap=set_colormap(), origin="lower", extend="both", antialiased=True) # generate filled contour
    else:
        plt.imshow(data_matrix, vmin=min_value, vmax=max_value, cmap=set_colormap(), origin="lower") # generate the heatmap
        
    plt.colorbar() # add the colorbar
        
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])
    
    plt.show() # show the graphic
    
    fig.savefig(f"out/{output_file}")
    
def plot_alizadeh_alpha_timesteps_relation(x_axis, y_axis, output_file, labels):
    """
        Generate a simple line graphic.

        Args:
            x_axis (list): The data to be plotted on the x-axis.
            y_axis (list): The data to be plotted on the y-axis.
            output_file (str): The name of the file where the generated image will be saved.
            labels (list): A list of labels to be included in the graphic. Should contain:
                       - labels[0]: The title of the graph.
                       - labels[1]: The label for the x-axis.
                       - labels[2]: The label for the y-axis.
        Returns:
            None
    """

    fig = plt.figure()
    plt.plot(x_axis, y_axis, "o-k")

    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])

    plt.show() # show the graphic

    fig.savefig(f"out/{output_file}")

