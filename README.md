# Best Fitness
This scorer assigns the best fitness value found so far.

## Usage
```
$ python best.py < population.txt
{"score": 1}
```

## Environmental Variables
`BEST_FLOAT_MAX` defines the max value of score, which is used if all solutions are infeasible. Default to `sys.float_info.max`.
