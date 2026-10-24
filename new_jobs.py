"""Print only the jobs that are new since the last run: a daily job alert for a list of companies.

    python new_jobs.py companies.txt            # one careers link per line
    python new_jobs.py companies.txt --keyword engineer --location Remote

The ids already seen are kept in seen_jobs.json next to this script; delete it to start over.  Schedule it with cron,
or schedule the Actor itself on Apify (Console > Schedules) and read the newest dataset.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from apify_client import ApifyClient

ACTOR = "v0iddo/mint-ats-jobs-scraper"
SEEN = Path(__file__).with_name("seen_jobs.json")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("companies_file")
    p.add_argument("--keyword", action="append", default=[])
    p.add_argument("--location")
    p.add_argument("--max-items", type=int, default=2000)
    a = p.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")
    companies = [l.strip() for l in open(a.companies_file, encoding="utf-8") if l.strip() and not l.startswith("#")]
    run_input = {"companies": companies, "maxItems": a.max_items, "includeDescription": False}
    if a.keyword:
        run_input["titleKeywords"] = a.keyword
    if a.location:
        run_input["locationContains"] = a.location

    client = ApifyClient(token)
    run = client.actor(ACTOR).call(run_input=run_input, logger=None)
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    new = []
    for job in client.dataset(run["defaultDatasetId"]).iterate_items():
        key = job.get("url") or f"{job.get('company')}|{job.get('jobId')}"
        if key not in seen:
            seen.add(key)
            new.append(job)
    SEEN.write_text(json.dumps(sorted(seen)))
    for j in new:
        print(f"{j.get('company')}: {j.get('title')} ({j.get('location') or 'location not stated'}) {j.get('url')}")
    print(f"{len(new)} new of {len(seen)} known jobs", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
