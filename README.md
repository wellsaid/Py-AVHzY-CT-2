# Py-AVHzY-CT-2

> A python program to interact with the AVHzY CT-2 power meter https://store.avhzy.com/index.php?route=product/product&product_id=50

This python utilities allows to interact with the AVHzy CT-2 power meter as the Kotomi App

## Installation

1. Prerequisites:

 - Python 3.x

2. Make it executable

    chmod +x ./py_AVHzY_CT2

## Usage example

Continously read data:

    ./py_AVHzY_CT2 read

Read 4 samples every 5 seconds and stop
    ./py_AVHzY_CT2 read -r 4 -t 5

Continously read and save to a file:
    ./py_AVHzY_CT2 read -o file.csv

## Release History
TODO

## Meta

Benedetto Girgenti - benedetto.girgenti@protonmail.com

TODO: Distributed under the XYZ license. See ``LICENSE`` for more information