#!/bin/bash

# Prints the provided text in the given color.
# $1 Sequence code of the chosen color.
# $2 The string to be printed.
print_in_color()
{
    echo -e "$1$2\033[0m"
}

clear
print_in_color "\033[0;32m" "Varas Experiments Plotter Script!"

mkdir -p out/varas


print_in_color "\033[0;34m" "Generating Graphics: 1/9"
./run.sh -gline_graphic -ovaras/varas_fig_6.png -iin/varas/config_files/varas_fig_6_config.txt --xlabel="Exit Width" --ylabel="T" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 2/9"
./run.sh -gvaras_door_width_7 -ovaras/varas_fig_7.png -iin/varas/config_files/varas_fig_7_config.txt --xlabel="Exit Width" --ylabel="Tu - Te" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 3/9"
./run.sh -gvaras_door_width_9 -ovaras/varas_fig_9.png -iin/varas/config_files/varas_fig_9_config.txt --xlabel="Exit Width" --ylabel="T/N" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 4/9"
./run.sh -gline_graphic -ovaras/varas_fig_12.png -iin/varas/config_files/varas_fig_12_config.txt --xlabel="Exit Position" --ylabel="T" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 5/9"
./run.sh -gline_graphic -ovaras/varas_fig_13.png -iin/varas/config_files/varas_fig_13_config.txt --xlabel="Exit Width" --ylabel="T" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 6/9"
./run.sh -gscatter_graphic -ovaras/varas_fig_14.png -iin/varas/config_files/varas_fig_14_config.txt --xlabel="Exit Position" --ylabel="T" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 7/9"
./run.sh -gheatmap -ovaras/varas_fig_15.png -iin/varas/varas_fig_15/varas_fig_15.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 8/9"
./run.sh -gline_graphic -ovaras/varas_fig_17a.png -iin/varas/config_files/varas_fig_17a_config.txt --xlabel="Exit Position" --ylabel="T" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 9/9"
./run.sh -gscatter_graphic -ovaras/varas_fig_17b.png -iin/varas/config_files/varas_fig_17b_config.txt --xlabel="Exit Position" --ylabel="T" --only-save-fig
