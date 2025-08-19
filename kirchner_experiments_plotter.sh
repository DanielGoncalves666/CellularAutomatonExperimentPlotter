#!/bin/bash

# Prints the provided text in the given color.
# $1 Sequence code of the chosen color.
# $2 The string to be printed.
print_in_color()
{
    echo -e "$1$2\033[0m"
}

clear
print_in_color "\033[0;32m" "Kirchner Experiments Plotter Script!"

mkdir -p out/kirchner

print_in_color "\033[0;34m" "Generating Graphics: 1/-"
./run.sh -gline_graphic -okirchner/kirchner_fig5a.png -iin/kirchner/config/kirchner_fig5a_config.txt --xlabel="ks" --ylabel="Timesteps" --only-save-fig --no-marker

print_in_color "\033[0;34m" "Generating Graphics: 2/-"
./run.sh -gline_graphic -okirchner/kirchner_fig5b.png -iin/kirchner/config/kirchner_fig5b_config.txt --xlabel="kd" --ylabel="Timesteps" --only-save-fig --no-marker

print_in_color "\033[0;34m" "Generating Graphics: 3/-"
./run.sh -gline_graphic -okirchner/kirchner_fig7a.png -iin/kirchner/config/kirchner_fig7a_config.txt --xlabel="kd" --ylabel="Timesteps" --only-save-fig --no-marker

print_in_color "\033[0;34m" "Generating Graphics: 4/-"
./run.sh -gline_graphic -okirchner/kirchner_fig7b.png -iin/kirchner/config/kirchner_fig7b_config.txt --xlabel="kd" --ylabel="Timesteps" --only-save-fig --no-marker

print_in_color "\033[0;34m" "Generating Graphics: 5/-"
./run.sh -gline_graphic -okirchner/kirchner_fig8a.png -iin/kirchner/config/kirchner_fig8a_config.txt --xlabel="alpha" --ylabel="Timesteps" --only-save-fig --no-marker

print_in_color "\033[0;34m" "Generating Graphics: 6/-"
./run.sh -gline_graphic -okirchner/kirchner_fig8b.png -iin/kirchner/config/kirchner_fig8b_config.txt --xlabel="alpha" --ylabel="Timesteps" --only-save-fig --no-marker
