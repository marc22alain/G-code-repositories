# G-code-repositories

This repository holds a collection of scripts to generate g-code, each script specializing in a particular geometry and procedure.
The g-code generated is for a conventional 3-axis mill. The scripts have all been developed on a machine that is set up as a wood and soft-metal router.

These Python scripts can be triggered to run from LinuxCNC, posting code to the file tab. Alternatively, the Python scripts can be run independently to save the g-code as files that can then be run by any g-code interpreter


## How to install

If you aren't comfortable with **git**, just download the archive and extract in a location that is convenient to access from LinuxCNC or your other interpreter.

Otherwise, go ahead and clone the repo. This will of course be the easiest way to get updates and bug fixes. Please note that the master branch (the default branch) is the only script version to run your machine with.


## Learn more about the g-code generators

There is a [Wiki!](https://github.com/marc22alain/G-code-repositories/wiki) It details each of the g-code generators, with screenshots to explain the input parameters, their results, and points to watch out for.


## Disclaimer

You use the generators at your own risk. There is no guarantee that the generated code will run safely on your machine or cut the workpiece as you intend. **At the very least, always preview the programs!** You may not be getting what you expect. Read the g-code for more detail.
