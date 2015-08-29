# G-code-repositories
Python scripts for generating G-code in LinuxCNC.

In fact, the scripts will run even if LinuxCNC is not detected. In that event, a `print` button will appear. This will then generate the G-code and print it to the Python interpreter window. Cut and paste into a text file and you can then run the G-code with any G-code interpreter.


## Hole Borer wizard
This is the equivalent to a drill press, with an infinite number of bits.

User steps:
- Step 1: center the router bit over the center of the hole you wish to drill.
- Step 2: run the wizard.

Machine steps:
- Step 3: the machine will move the bit to Safe Z height (see below for this definition).
- Step 4: the machine will move the bit down to the workpiece with afast move, then plunge at the specified feed rate.
- Step 5: the machine will cut a series of circles, plunging only as much as is defined by user input.
- Step 6: the machine will withdraw the bit and move back up to Safe Z height.

![Hole Borer screenshot](/images/hole_borer.png)

The options offered in the wizard are:
- 'Safe Z travel height': the height at which it is safe for the router and bit to move in the XY-plane; default value is 100mm.
- 'Stock thickness': the thickness of the workpiece; the wizard will cut all the way through the workpiece.
- 'Maximum depth of cut': the wizard will cut the bore in passes of X thickness to be defined here.
- 'Cutter diameter': the wizard presents a list of pre-defined options. Add additional sizes to the top of the `Hole_Borer.py` file, to the tuple assigned to `bits`.
- 'Hole diameter': the diameter of the hole to be cut; the wizard adjusts the cutting arc radius according to the bit selected to achieve this diameter. 
- 'Feed rate': the wizard will use this to set the feed rate when making cuts; fast moves are made according to the machine's default configuration.

NOTE: the G-code generated uses G2 for the arcs, so it makes clockwise moves to cut the circles.
