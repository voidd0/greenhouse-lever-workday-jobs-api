"""Export every open job from company careers pages (Greenhouse, Lever, Ashby, Workday, Workable, Recruitee,
Personio, BambooHR) to a CSV file.

    pip install apify-client
    export APIFY_TOKEN=...            # https://console.apify.com/settings/integrations
    python jobs_to_csv.py https://job-boards.greenhouse.io/discord https://jobs.lever.co/spotify -o jobs.csv

Runs the "ATS Jobs Scraper" Actor on Apify: https://apify.com/v0iddo/mint-ats-jobs-scraper
"""
import argparse
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "v0iddo/mint-ats-jobs-scraper"
COLUMNS = ["company", "ats", "title", "location", "remote", "department", "employmentType", "postedAt", "url"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("companies", nargs="+", help="careers page links, one per company")
    p.add_argument("-o", "--out", default="jobs.csv")
    p.add_argument("--keyword", action="append", default=[], help="only titles containing this word (repeatable)")
    p.add_argument("--location", help="for example Remote, Berlin, US")
    p.add_argument("--days", type=int, help="only postings published in the last N days")
    p.add_argument("--per-company", type=int, default=200, help="at most this many jobs from one company")
    p.add_argument("--max-items", type=int, default=1000, help="caps the rows (and the cost) of one run")
    a = p.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")
    run_input = {"companies": a.companies, "maxItems": a.max_items, "maxJobsPerCompany": a.per_company,
                 "includeDescription": False}
    if a.keyword:
        run_input["titleKeywords"] = a.keyword
    if a.location:
        run_input["locationContains"] = a.location
    if a.days:
        run_input["postedWithinDays"] = a.days

    client = ApifyClient(token)
    run = client.actor(ACTOR).call(run_input=run_input, logger=None)
    if run is None:
        sys.exit("The run did not start.")
    rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in COLUMNS})
    print(f"{len(rows)} jobs written to {a.out} (run status {run.get('status')}: {run.get('statusMessage') or ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
