# Best Fitness
This scorer assigns the best fitness value found so far.

## Usage
```
$ echo -e '{"objective": 1}'\n[{"objective": 2}, {"objective": 3}]' | python best.py
{"score": 1}
```

```
$ echo -e '{"objective": 3}'\n[{"objective": 1}, {"objective": 2}]' | python best.py
{"score": 1}
```

## Environmental Variables
No variable.
