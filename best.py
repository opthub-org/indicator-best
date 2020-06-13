# coding: utf-8
"""
Best fitness value.
"""
import json
import sys

def main():
    solution_to_score = json.loads(sys.argv[1])
    solutions_scored = json.loads(sys.argv[2])
    y = solution_to_score['objective']
    best = solutions_scored[-1]['score']
    score = min(y, best)
    print(score)


if __name__ == '__main__':
    main()
