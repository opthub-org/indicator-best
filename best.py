#!/bin/env python
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


LOGGER = logging.getLogger(__name__)

SOLUTION_TO_SCORE_JSONSCHEMA = """{
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

SOLUTIONS_SCORED_JSONSCHEMA = """{
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


def load_config(ctx, _, value):
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param value: File name
    :return dict: Loaded config
    """
    if not path.exists(value):
        return {}
    with open(value, encoding="utf-8") as file:
        ctx.default_map = yaml.safe_load(file)
        if not isinstance(ctx.default_map, dict):
            raise TypeError(f"The content of `{value}` must be dict, but {type(ctx.default_map)}.")
    return ctx.default_map


def feasible(solution):
    """Test a solution is feasible or not."""
    objective = solution.get("objective")
    constraint = solution.get("constraint")
    return isinstance(objective, (float, int)) and (
        constraint is None or np.all(np.array(constraint) <= 0.0)
    )


@click.command(help="Best fitness value.")
@click.option(
    "-m", "--float-max", type=float, default=float_info.max, help="Worst value."
)
@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    default="config.yml",
    is_eager=True,
    callback=load_config,
    help="Configuration file.",
)
@click.version_option("1.0.0")
def main(float_max, quiet, verbose, config):  # pylint: disable=unused-argument
    """Calculate best fitness so far."""
    verbosity = 10 * (quiet - verbose)
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    LOGGER.info("Log level is set to %d.", log_level)

    json_solution_to_score = input()
    LOGGER.debug("json_solution_to_score = %s", json_solution_to_score)
    solution_to_score = json.loads(json_solution_to_score)
    LOGGER.debug("solution_to_score = %s", solution_to_score)
    validate(solution_to_score, json.loads(SOLUTION_TO_SCORE_JSONSCHEMA))

    json_solutions_scored = input()
    LOGGER.debug("json_solutions_scored = %s", json_solutions_scored)
    solutions_scored = json.loads(json_solutions_scored)
    LOGGER.debug("solutions_scored = %s", solutions_scored)
    validate(solutions_scored, json.loads(SOLUTIONS_SCORED_JSONSCHEMA))

    if feasible(solution_to_score):
        objective = solution_to_score["objective"]
    else:
        objective = float_max
    if not solutions_scored:
        score = objective
    else:
        best = solutions_scored[-1]["score"]
        score = min(objective, best)

    print(json.dumps({"score": score}))
    LOGGER.debug("End")


if __name__ == "__main__":
    try:
        LOGGER.info("Start")
        main(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
            auto_envvar_prefix="BEST"
        )
        LOGGER.info("Successfully finished")
    except Exception as e:  # pylint: disable=broad-exception-caught
        LOGGER.error(format_exc())
        print(json.dumps({"score": None, "error": str(e)}))
