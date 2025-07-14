import time
import argparse
import sys
from matplotlib import pyplot as plt

import plotting
import processing

def creating_arg_parser():

    description = 'A simple graphic generator for cellular automaton experiments.'
    epilog = """The options --ignore-marked-data and --force-over-values only works for heatmap and contours graphics. The --wall-threshold option only works for environment_heatmap graphics.\n
    Options not needed to some graphics are ignored."""

    # ArgumentParser will contain all information about the command line interface
    parser = argparse.ArgumentParser(description=description, epilog=epilog)

    # add_argument adds new arguments or options that can be inserted by command line.
    parser.add_argument('-i', required=True, nargs=1, help="Filename that contains the data from which the graphic will be generated.")
    possible_graphics = ["environment_heatmap", "3d_environment_heatmap", "heatmap", "int_contours", "float_contours", "line_graphic",
                         "scatter_graphic", "varas_door_width_7", "varas_door_width_9"]
    parser.add_argument('-g','--graphic', choices=possible_graphics, required=True, nargs=1, help="Specifies which graphic should be generated.")
    parser.add_argument('-o','--out', nargs="?", default="", help="Filename on which the graphic should be saved.")
    parser.add_argument('-t','--title', nargs=1, help="The title of the generated graphic.")
    parser.add_argument('-x', '--xlabel', nargs=1, help="X-axis label")
    parser.add_argument('-y', '--ylabel', nargs=1, help="Y-axis label")
    parser.add_argument('--ignore-marked-data', action='store_true', help="Ignore marked data in lines beginning with #1 during the calculation of the min/max values.")
    parser.add_argument('--suppress-heatmap-exits', action='store_true', help="Suppress the exit cells located on the edges of a environment heatmap.")
    parser.add_argument('--force-over-values', action='store_true', help="Force values exceeding the maximum determined value to be colored dark red. Without this, some graphics may display a mix of colors where only dark red should appear.")
    parser.add_argument('--only-save-fig', action='store_true', help="Doesn't show the generated graphic.")
    parser.add_argument('--wall-threshold', nargs=1, default=[1000.0], help="Threshold value above (or bellow, if negative) which a cell is considered a wall or obstacle. The threshold value itself is also treated as a wall.")

    return parser

def generate_graphic():
    if choice == "environment_heatmap":
        x_axis_ticks, y_axis_ticks, _, data_matrix, maximum_value = processing.process_env_heatmap_data(input_file, wall_threshold, "2d", suppress_heatmap_exits)
        plotting.plot_heatmap(x_axis_ticks, y_axis_ticks, data_matrix, (0, maximum_value), output_file, labels, over_value_color="white", origin="upper")
    elif choice == "3d_environment_heatmap":
        x_axis_ticks, y_axis_ticks, z_axis_ticks, data_matrix, maximum_value = processing.process_env_heatmap_data(input_file, wall_threshold, "3d", suppress_heatmap_exits)
        plotting.plot_3d_heatmap(x_axis_ticks, y_axis_ticks, z_axis_ticks, data_matrix, (0, maximum_value), output_file, labels, over_value_color="none")
    elif choice == "heatmap":
        (data_matrix, min_max_values) = processing.process_heatmap_data(input_file, ignore_marked_data, "int", force_over_values)
        plotting.plot_heatmap(([],[]), ([],[]), data_matrix, min_max_values, output_file, labels)
    elif choice == "int_contours":
        (data_matrix, min_max_values) = processing.process_heatmap_data(input_file, ignore_marked_data, "int", force_over_values)
        plotting.plot_contours_graphic(data_matrix, min_max_values, output_file, labels, "int")
    elif choice == "float_contours":
        (data_matrix, min_max_values) = processing.process_heatmap_data(input_file, ignore_marked_data, "float", force_over_values)
        plotting.plot_contours_graphic(data_matrix, min_max_values, output_file, labels, "float")
    elif choice == "line_graphic":
        x_axis_ticks, y_axis_ticks, legends, data_vector = processing.process_configuration_file(input_file)
        plotting.plot_line_graphic(x_axis_ticks, y_axis_ticks, legends, data_vector, output_file, labels, False)
    elif choice == "scatter_graphic":
        x_axis_ticks, y_axis_ticks, legends, data_vector = processing.process_configuration_file(input_file)
        plotting.plot_scatter_graphic(x_axis_ticks, y_axis_ticks, legends, data_vector, output_file, labels)
    elif choice == "varas_door_width_7":
        x_axis_ticks, y_axis_ticks, legends, data_vector = processing.process_configuration_file(input_file)
        processed_legends, difference_data_vector = processing.varas_door_width_fig_7(legends, data_vector)
        plotting.plot_line_graphic(x_axis_ticks, y_axis_ticks, processed_legends, difference_data_vector, output_file, labels, False)
    elif choice == "varas_door_width_9":
        x_axis_ticks, y_axis_ticks, legends, data_vector = processing.process_configuration_file(input_file)
        quotient_data_vector = processing.varas_door_width_fig_9(legends, data_vector)
        plotting.plot_line_graphic(x_axis_ticks, y_axis_ticks, legends, quotient_data_vector, output_file, labels, True)
    else:
        sys.stderr.write("Invalid graphic.\n")
        exit()

if __name__ == "__main__":
    command_line = creating_arg_parser().parse_args()
    
    input_file = command_line.i[0]
    choice = command_line.graphic[0]
    output_file = command_line.out if command_line.out != "" else f"{choice}_{time.strftime('%Y-%m-%d_%H:%M:%S')}.png"
    
    labels = [command_line.title[0] if command_line.title is not None else "",
              command_line.xlabel[0] if command_line.xlabel is not None else "",
              command_line.ylabel[0] if command_line.ylabel is not None else ""]
    
    ignore_marked_data = command_line.ignore_marked_data
    force_over_values = command_line.force_over_values
    suppress_heatmap_exits = command_line.suppress_heatmap_exits

    wall_threshold = float(command_line.wall_threshold[0])
    
    generate_graphic()

    if not command_line.only_save_fig:
        plt.show()  # show the graphic