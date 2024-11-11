# Scripts
How to use:

`gen_tuning_plots.py`
Generates processed data for the tuning curves. `--combine-bins` tells you how many of the time bins to combine together (for instance, take each 3 time bins as one point)
Currently only supports:
- total velocity (speed)
- total acceleration
```
    gen_tuning_plots.py --combine-bins <num>
```

Generate matplotlib graphs for the tuning curve
- `--neuron` number of the neuron
- `--monkey` which monkey data to take from (MM_S1, for example)
- `-v` show velocity tuning plot
- `-a` show acceleration tuning plot
```
    gen_tuning_plots.py --neuron <neuron_num> --monkey <monkey> -(v or a)
```


