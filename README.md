# Py-AVHzY-CT-2

> A python program to interact with the AVHzY CT-2 power meter https://store.avhzy.com/index.php?route=product/product&product_id=50

This python utilities allows to interact with the AVHzy CT-2 power meter as the Kotomi App

## Installation
Prerequisites: Python 3.x

Make it executable:
```
chmod +x ./py_AVHzY_CT2
```

## Usage example

Continously read data:
```
./py_AVHzY_CT2 read
```

Read 4 samples every 5 seconds and stop
```
./py_AVHzY_CT2 read -r 4 -t 5
```

Continously read and save to a file:
```
./py_AVHzY_CT2 read -o file.csv
```

## Release History
* v0.1 
    * Added action to read live meter data

## Meta

Benedetto Girgenti - benedetto.girgenti@protonmail.com

TODO: Distributed under the GPL v3.0 license. See ``LICENSE.md`` for more information
