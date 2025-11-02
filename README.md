# NFA_RegEx_converter
A python script that converts a RegEx string to a NFA machine and one that converts a NFA to a RegEx

## RegEx -> NFA | RegEx_to_NFA.py

### Usage: 
Put the Regex you want to convert in the v_REGEX variable inside the python file then run it.

## NFA -> Regex | NFA_to_Regex.py

### Usage: 

Put the file you want inside the file variable(default "ex.txt") and run the program.

### Format:

- all the edges | 0 being the lambda edge
- all the nodes
- pairs of (in_node out_node edge_used)
