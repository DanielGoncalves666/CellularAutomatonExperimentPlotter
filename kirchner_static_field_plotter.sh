#!/bin/bash

# Prints the provided text in the given color.
# $1 Sequence code of the chosen color.
# $2 The string to be printed.
print_in_color()
{
    echo -e "$1$2\033[0m"
}

clear
print_in_color "\033[0;32m" "Kirchner Static Field Plotter Script!"

dir_name=kirchner_static_field
mkdir -p out/$dir_name

for auxiliary_file in "2a" "2b"; do
  for static_field in 1 2 3; do
    print_in_color "\033[0;34m" "Generating 3d graphic ${auxiliary_file} - Static field $static_field"
    ./run.sh -g3d_environment_heatmap --wall-threshold=-1000 -iin/${dir_name}/aux_kirchner_fig${auxiliary_file}.txt_static_field_${static_field}.txt \
              -o${dir_name}/kirchner_fig${auxiliary_file}_static-field${static_field}.png --only-save-fig --suppress-heatmap-exits
  done
done