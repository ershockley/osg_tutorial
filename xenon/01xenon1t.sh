#!/usr/bin/env bash

# activate environment
# some envs you can try are:
#      1. pax_v6.10.1 (or another pax version)
#      2. lower (used for LowER analysis)
#      3. stats (old env I made for doing blueice stuff. Not sure it still works)

source /cvmfs/xenon.opensciencegrid.org/releases/anaconda/2.4/bin/activate lower


echo "Which python version are we using?"
which python

echo
echo "Can we import xenon software?"
echo

# function that takes a python package to import, checks if it is in the path, and prints the __init__ file
function xe1timport {
    echo "Trying to import $1...."
    export ARG=$1
    if $(python -c "import $1"); then
        path=`python -c "import $ARG; print($ARG.__file__)"`
        echo "Found $ARG at $path"
    else
        echo "$1 not installed in this environment"
    fi
    echo "------------------------------------"
}

# loop over a few XENON software packages. Feel free to play with these.
for pkg in LowER pax multihist blueice hax; do
    xe1timport $pkg
done

