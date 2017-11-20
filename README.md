# G-code-repositories
Python scripts for generating G-code in LinuxCNC.

In fact, the scripts will run even if LinuxCNC is not detected. In that event, a `print` button will appear. This will then generate the G-code and print it to the Python interpreter window. Cut and paste into a text file and you can then run the G-code with any G-code interpreter.


## Hole Borer wizard
This is the equivalent to a drill press, with an infinite number of bits.

User steps:
- Step 1: center the router bit over the center of the hole that you wish to drill.
- Step 2: run the wizard.

Machine steps:
- Step 3: the machine will move the bit to Safe Z height (see below for this definition).
- Step 4: the machine will move the bit down to the workpiece with a fast move, then plunge at the specified feed rate.
- Step 5: the machine will cut a series of circles, plunging only as much as is defined by user input.
- Step 6: the machine will withdraw the bit and move back up to Safe Z height and return to the center.

![Hole Borer screenshot](/images/hole_borer.png)

The options offered in the wizard are:
- 'Safe Z travel height': the height at which it is safe for the router and bit to move in the XY-plane; default value is 100mm.
- 'Stock thickness': the thickness of the workpiece; the wizard will cut all the way through the workpiece.
- 'Maximum depth of cut': the wizard will cut the bore in passes of X thickness to be defined here.
- 'Cutter diameter': the wizard presents a list of pre-defined options. Add additional sizes to the top of the `MC_defaults.py` file, to the tuple assigned to `bits`.
- 'Hole diameter': the diameter of the hole to be cut; the wizard adjusts the cutting arc radius according to the bit selected to achieve this diameter. 
- 'Feed rate': the wizard will use this to set the feed rate when making cuts; fast moves are made according to the machine's default configuration.

NOTE: the G-code generated uses G2 for the arcs, so it makes clockwise moves to cut the circles.


## Doughnut Cutter wizard
This cuts a pair of concentric holes. The inner hole is defined as an inner diameter (ID) and the outer hole is defined as an outer diameter (OD). Given that multiple separate pieces will be created, in order to prevent them flying around as they are cut free, three tabs are left to connect each piece to each other.

User steps:
- Step 1: center the router bit over the center of the doughnut that you wish to cut.
- Step 2: run the wizard.

Machine steps:
- Step 3: the machine will move the bit to Safe Z height (see below for this definition).
- Step 4: the machine will move the bit across to a starting point on the radius of the ID, then down to the workpiece with a fast move, then plunge at the specified feed rate.
- Step 5: the machine will cut a series of circles, plunging only as much as is defined for the tab thickness.
- Step 6: the machine will withdraw the bit, move back up to Safe Z height and return to center.
- Step 7...: the machine will repeat the above procedure to produce the OD cut.

![Doughnut Cutter screenshot](/images/doughnut_cutter.png)

The options offered in the wizard are:
- 'Feed rate': the wizard will use this to set the feed rate when making cuts; fast moves are made according to the machine's default configuration.
- 'Safe Z travel height': the height at which it is safe for the router and bit to move in the XY-plane; default value is 100mm.
- 'Maximum cut per pass': the wizard will cut the circles in passes of X thickness to be defined here.
- 'Cutter diameter': the wizard presents a list of pre-defined options. Add additional sizes to the top of the `MC_defaults.py` file, to the tuple assigned to `bits`.
- 'Stock thickness': the thickness of the workpiece; the wizard will cut all the way through the workpiece.
- 'Tab thickness': the thickness of the tabs to be left behind.
- 'Tab width': the width of the tabs to be left behind; a default is set at 6.35mm.
- 'Doughnut OD': the outer diameter of the doughnut; the wizard adjusts the cutting arc radius according to the bit selected to achieve this diameter.
- 'Doughnut ID': the inner diameter of the doughnut; again, the wizard adjusts the cutting arc radius according to the bit selected to achieve this diameter.

## Polar Holes wizard
This cuts a circular pattern of regularly spaced, and identically sized, holes.

User steps:
- Step 1: center the router bit over the center of the hole pattern that you wish to cut.
- Step 2: run the wizard.

Machine steps:
- Step 3: the machine will move the bit to Safe Z height.
- Step 4: the machine will then move to the first hole location and perform a hole boring operation identical to the Hole Borer procedure, except for returning to center.
- Step 5...: the machine will move to the next hole repeat the hole boring procedure.
- Step 6: the machine will move back up to Safe Z height and return to center.

![Polar Hole Pattern Cutter screenshot](/images/polar_holes.png)

The options offered in the wizard are:
- 'Feed rate': the wizard will use this to set the feed rate when making cuts; fast moves are made according to the machine's default configuration.
- 'Safe Z travel height': the height at which it is safe for the router and bit to move in the XY-plane; default value is 100mm.
- 'Maximum cut per pass': the wizard will cut the circles in passes of X thickness to be defined here.
- 'Cutter diameter': the wizard presents a list of pre-defined options. Add additional sizes to the top of the `MC_defaults.py` file, to the tuple assigned to `bits`.
- 'Stock thickness': the thickness of the workpiece; the wizard will cut all the way through the workpiece.
- 'Hole diameter': the diameter of each the holes to be cut; the wizard adjusts the cutting arc radius according to the bit selected to achieve this diameter. 
- 'Number of holes': the minimum number of holes is 2. Given _x_ holes, they will be spaced 360°/_x_ apart.
- 'Hole circle diameter': this is the diameter of a circle that crosses the center-point of all of the cut holes.

## MC_defaults.py
This file provides a common location for defining the defaults to all of the wizard options.

Define:
- standard bit diameters
- default safe Z height
- default feed rate
- default tab width