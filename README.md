## hFrame3DDfc
Accessing Frame3DD within FreeCAD

![Frame3dd-screenshot](https://user-images.githubusercontent.com/4140247/78903287-e7001e00-7a48-11ea-939d-0ac8b7da99cd.png)

## Background
[Frame3DD](http://frame3dd.sourceforge.net/) is free open-source software for static and dynamic structural analysis of 2D and 3D frames and trusses with elastic and geometric stiffness. It computes the static deflections, reactions, internal element forces, natural frequencies, mode shapes and modal participation factors of two- and three- dimensional elastic structures using direct stiffness and mass assembly. Frame3DD has its own text-file input format (.3dd), but additionally supports matlab (.m) and spreadsheet (.csv) file formats, and offers graphical output including mode shape animation via Gnuplot

[FreeCAD](https://freecadweb.org) is an open source CAD/CAM solution.


## Features 
Currently this workbench contains the following tools:

###  Reading 3DD files 
The ability to read in an 3DD case file. It also copies said 3DD file into FreeCad's `bin/` folder and renames it as `hFrame3DDfc.3DD`.

### Outputting 3DD file
Not implemented yet.  
Output a new 3DD file when user makes some change to the model or load.

### Run Frame3DD
Execture the `Frame3DD` binary which reads in the `hFrame3DDfc.3DD` file and writes the result into the `hFrame3DDfc.txt` file (within FreeCad's `bin/` folder).

### Show Results
Read in the `hFrame3DDfc.txt` file and draw the mesh and displacement.

## Prerequisites

* Frame3DD v
* FreeCAD v0.19.x

## Installation
Currently this workbench works on Windows.  
Note: Frame3DD excutable file must be located at FreeCad's `bin/` folder. It is named `Frame3DD.exe` under Window 10.

## Discussion
Feedback, discussion, and any participation can be done through the [dedicated FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=18&t=45026) 

## License
GPL v3.0 (see [LICENSE](LICENCE) file)
