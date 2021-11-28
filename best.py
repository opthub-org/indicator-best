#!/bin/env python
# coding: utf-8
"""
Best fitness value.
"""
import json
import logging
from os import path
from sys import float_info
from traceback import format_exc

import click
from jsonschema import validate
import numpy as np
import yaml


_logger = logging.getLogger(__name__)


solution_to_score_jsonschema = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Solution to score",
  "type": "object",
  "properties": {
    "objective": {
      "type": ["number", "null"]
    },
    "constraint": {
      "OneOf": [
        {"type": ["number", "null"]},
        {"type": "array", "minItems": 1, "items": {"type": "number"}}
      ]
    }
  }
}"""

solutions_scored_jsonschema = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Solutions scored",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "objective": {
        "type": ["number", "null"]
      },
      "score": {
        "type": "number"
      },
      "constraint": {
        "OneOf": [
          {"type": ["number", "null"]},
          {"type": "array", "minItems": 1, "items": {"type": "number"}}
        ]
      }
    },
    "required": ["score"]
  }
}"""


def load_config(ctx, self, value):
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param self: Self object
    :param value: File name
    :return dict: Loaded config
    """
    if not path.exists(value):
        return {}
    with open(value) as f:
        ctx.default_map = yaml.safe_load(f)
    return ctx.default_map


def feasible(s):
    o = s.get('objective')
    c = s.get('constraint')
    return (isinstance(o, float) or isinstance(o, int)) and (c is None or np.all(np.array(c) <= 0.0))


@click.command(help='Best fitness value.')
@click.option('-m', '--float-max', type=float, default=float_info.max, help='Worst value.')
@click.option('-q', '--quiet', count=True, help='Be quieter.')
@click.option('-v', '--verbose', count=True, help='Be more verbose.')
@click.option('-c', '--config',
              type=click.Path(dir_okay=False), default='config.yml',
              is_eager=True, callback=load_config, help='Configuration file.')
@click.version_option('1.0.0')
@click.pass_context
def main(ctx, float_max, quiet, verbose, config):
    verbosity = 10 * (quiet - verbose)
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    _logger.info('Log level is set to %d.', log_level)

    x = input()
    _logger.debug('input_x = %s', x)
    solution_to_score = json.loads(x)
    _logger.debug('x = %s', x)
    validate(solution_to_score, json.loads(solution_to_score_jsonschema))

    xs = input()
    _logger.debug('input_xs = %s', xs)
    solutions_scored = json.loads(xs)
    _logger.debug('xs = %s', xs)
    validate(solutions_scored, json.loads(solutions_scored_jsonschema))

    if feasible(solution_to_score):
        y = solution_to_score['objective']
    else:
        y = float_max
    if not solutions_scored:
        score = y
    else:
        best = solutions_scored[-1]['score']
        score = min(y, best)

    print(json.dumps({'score': score}))
    _logger.debug('End')


if __name__ == '__main__':
    try:
        _logger.info('Start')
        main(auto_envvar_prefix='BEST')  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
        _logger.info('Successfully finished')
    except Exception as e:
        _logger.error(format_exc())
        print(json.dumps({'score': None, 'error': str(e)}))
