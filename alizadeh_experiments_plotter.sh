#!/bin/bash

# Prints the provided text in the given color.
# $1 Sequence code of the chosen color.
# $2 The string to be printed.
print_in_color()
{
    echo -e "$1$2\033[0m"
}

clear
print_in_color "\033[0;32m" "Alizadeh Experiments Plotter Script!"

mkdir -p out/alizadeh

print_in_color "\033[0;34m" "Generating Graphics: 1/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_9a_onlyValid.png -iin/alizadeh/alizadeh_fig_9a_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 2/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_9b_onlyValid.png -iin/alizadeh/alizadeh_fig_9b_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 3/9"
python3 run.py -gfloat_contours -oalizadeh/alizadeh_fig_10a_onlyValid.png -iin/alizadeh/alizadeh_fig_10a_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 4/9"
python3 run.py -gfloat_contours -oalizadeh/alizadeh_fig_10b_onlyValid.png -iin/alizadeh/alizadeh_fig_10b_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 5/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_12a_onlyValid.png -iin/alizadeh/alizadeh_fig_12a_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 6/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_12b_onlyValid.png -iin/alizadeh/alizadeh_fig_12b_onlyValid.txt --xlabel="Position of Door A" --ylabel="Position of Door B" --ignore-marked-data --force-over-values --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 7/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_13a.png -iin/alizadeh/alizadeh_fig_13a.txt --xlabel="Width of A" --ylabel="Width of B" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 8/9"
python3 run.py -gint_contours -oalizadeh/alizadeh_fig_13b.png -iin/alizadeh/alizadeh_fig_13b.txt --xlabel="Width of A" --ylabel="Width of B" --only-save-fig

print_in_color "\033[0;34m" "Generating Graphics: 9/9"
python3 run.py -gline_graphic -oalizadeh/alizadeh_fig_15.png -iin/alizadeh/alizadeh_fig_15_config.txt --xlabel="Alpha" --ylabel="Timesteps" --only-save-fig
