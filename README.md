# Best Fitness
This scorer assigns the best fitness value found so far.

## Usage
```
$ python best.py <(echo '{"objective": 1}') <(echo '[{"objective": 2}, {"objective": 3}]')
{"score": 1}
```

```
$ python best.py <(echo '{"objective": 3}') <(echo '[{"objective": 1}, {"objective": 2}]')
{"score": 1}
```

## Environmental Variables
No variable.
