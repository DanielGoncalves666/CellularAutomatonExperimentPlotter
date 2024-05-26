import time
import argparse
import sys

import processing
import plotting

def creating_arg_parser():
    # ArgumentParser will contain all information about the command line interface
    parser = argparse.ArgumentParser(description='Graphic Generator')

    # add_argument adds new arguments or options that can be inserted by command line
    parser.add_argument('-i', required=True, nargs=1, help="Filename that contains the data from which the graphic will be generated.")
    possible_graphics = ["alizadeh_evac_time", "alizadeh_ped_distribution", "alizadeh_relation_alpha_timesteps"]
    parser.add_argument('-g','--graphic', choices=possible_graphics, required=True, nargs=1, help="Specifies which graphic should be generated.")
    parser.add_argument('-o','--out', nargs="?", default="", help="Filename on which the graphic should be saved.")
    parser.add_argument('-t','--title', nargs=1, help="The title of the generated graphic.")
    parser.add_argument('-x', '--xlabel', nargs=1, help="X-axis label")
    parser.add_argument('-y', '--ylabel', nargs=1, help="Y-axis label")
    parser.add_argument('--type', choices=["heatmap", "contours"], nargs=1, help="Indicates which type of graphic should be generated (contours by default). Works for 'alizadeh_evac_time' and 'alizadeh_ped_distribution'.")
    parser.add_argument('--ignore-marked-data', action='store_true', help="Ignore marked data in lines beggining with #1 during the calculation of the min/max values.")
    parser.add_argument('--force-over-values', action='store_true', help="Force values exceeding the maximum determined value to be colored dark red. Without this, some graphics may display a mix of colors where only dark red should appear.")

    return parser

def generate_graphic():
    if choice == "alizadeh_evac_time":
        (data_matrix, min_max_values) = processing.alizadeh_heatmap(input_file, ignore_marked_data, "int", force_over_values)
        plotting.plot_heatmap_or_contours(data_matrix, min_max_values, output_file, labels, graphic_type, "int")
    elif choice == "alizadeh_ped_distribution":
        (data_matrix, min_max_values) = processing.alizadeh_heatmap(input_file, ignore_marked_data, "float", force_over_values)
        plotting.plot_heatmap_or_contours(data_matrix, min_max_values, output_file, labels, graphic_type, "float")
    elif choice == "alizadeh_relation_alpha_timesteps":
        (x_axis, y_axis) = processing.alizadeh_alpha_timesteps_relation(input_file)
        plotting.plot_alizadeh_alpha_timesteps_relation(x_axis, y_axis, output_file, labels)
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
    
    graphic_type = command_line.type[0] if command_line.type is not None else "contours"
    ignore_marked_data = command_line.ignore_marked_data
    force_over_values = command_line.force_over_values
    
    generate_graphic()