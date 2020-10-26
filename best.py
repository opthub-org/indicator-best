# coding: utf-8
"""
Best fitness value.
"""
import json
import sys

def main():
    with open(sys.argv[1]) as f, open(sys.argv[2]) as g:
        solution_to_score = json.load(f)
        solutions_scored = json.load(g)
    y = solution_to_score['objective']
    if not solutions_scored:
        score = y
    else:
        best = solutions_scored[-1]['score']
        score = min(y, best)
    print(json.dumps({'score': score}))


if __name__ == '__main__':
    main()
