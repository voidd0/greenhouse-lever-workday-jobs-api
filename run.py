#!/usr/bin/env python3
"""Run the Greenhouse, Lever, Workday & Ashby Jobs Scraper: Careers API Actor on Apify and save its results as CSV or JSON.

    pip install "apify-client>=2"
    export APIFY_TOKEN=your_token
    python run.py input.json -o results.csv
"""
import argparse
import csv
import json
import os
import sys

from apify_client import ApifyClient

ACTOR = "v0iddo/ats-jobs-scraper"
MAX_KEY = 'maxItems'


def flat(value):
    return json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value


def write(items, path):
    if path.endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        return
    columns = []
    for item in items:
        columns += [k for k in item if k not in columns]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for item in items:
            w.writerow({k: flat(v) for k, v in item.items()})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", nargs="?", default="input.json", help="the Actor input as a JSON file")
    ap.add_argument("-o", "--output", default="results.csv", help="results.csv or results.json")
    if MAX_KEY:
        ap.add_argument("--max-items", type=int, help="stop after this many results (caps the cost)")
    a = ap.parse_args(argv)
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN: Apify Console > Settings > Integrations")
    with open(a.input, encoding="utf-8") as f:
        run_input = json.load(f)
    if MAX_KEY and a.max_items:
        run_input[MAX_KEY] = a.max_items
    client = ApifyClient(token)
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    write(items, a.output)
    print(f"{len(items)} results written to {a.output} (run status {run['status']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
