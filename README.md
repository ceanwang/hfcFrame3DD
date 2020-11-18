## hfcFrame3DD
Accessing Frame3DD within FreeCAD

![Frame3dd-screenshot](https://user-images.githubusercontent.com/4140247/78903287-e7001e00-7a48-11ea-939d-0ac8b7da99cd.png)

## Background
[Frame3DD](http://frame3dd.sourceforge.net/) is free open-source software for static and dynamic structural analysis of 2D and 3D frames and trusses with elastic and geometric stiffness. It computes the static deflections, reactions, internal element forces, natural frequencies, mode shapes and modal participation factors of two- and three- dimensional elastic structures using direct stiffness and mass assembly. Frame3DD has its own text-file input format (.3dd), but additionally supports matlab (.m) and spreadsheet (.csv) file formats, and offers graphical output including mode shape animation via Gnuplot

[FreeCAD](https://freecadweb.org) is an open source CAD/CAM solution.


## Features 
Currently this workbench contains the following tools:

###  Reading 3DD files 
The ability to read in an 3DD case file. It also copies said 3DD file into FreeCad's `bin/` folder and renames it as `hfcFrame3DD.3DD`.

### Outputting 3DD file
Not implemented yet.  
Output a new 3DD file when user makes some change to the model or load.

### Run Frame3DD
Execute the `Frame3DD` binary which reads in the `hfcFrame3DD.3DD` file and writes the result into the `hfcFrame3DD.txt` file (within FreeCad's `bin/` folder).

### Show Results
Read in the `hfcFrame3DD.txt` file and draw the mesh and displacement.

## Prerequisites

* Frame3DD v
* FreeCAD v0.19.x

## Installation
This workbench is developed on Windows 10.  

Note: Frame3DD excutable file must be located at FreeCad's `bin/` folder. Under Window 10, it is named `Frame3DD.exe` . Under Linux. it is named 'Frame3DD' . 

Download as hFrame3DD.zip and unzip it under FreeCad's `Mod/` folder. The result is a new 'Mod/hFrame3DD' folder with all the codes.

## Discussion
Feedback, discussion, and any participation can be done through the [dedicated FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=18&t=45026) 

## License
GPL v3.0 (see [LICENSE](LICENCE) file)
