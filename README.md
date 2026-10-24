# Greenhouse, Lever, Ashby & Workday jobs API: every open job to CSV or JSON

Get every open job posting from company careers pages, in one format, without writing a scraper for each job
system. Give it careers page links. It returns the title, location, remote flag, department, posting date, salary
(where the company publishes it) and the link to the posting.

Supported job systems: **Greenhouse, Lever, Ashby, Workday, Workable, Recruitee, Personio and BambooHR**. The
system is detected from the link. Postings are read from each system's public job board feed, so the data is the
same as what job seekers see.

This repository has ready scripts for the
[ATS Jobs Scraper](https://apify.com/v0iddo/mint-ats-jobs-scraper) Actor on Apify. The Actor does the fetching,
paging and normalising, and the scripts here turn its output into a CSV file or a daily alert.

```text
$ python jobs_to_csv.py https://job-boards.greenhouse.io/discord https://jobs.lever.co/spotify \
    https://jobs.ashbyhq.com/notion https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite --per-company 10
40 jobs written to jobs.csv (run status SUCCEEDED: 40 results)
```

## Quick start

1. Create an Apify account and copy your API token from
   [Console > Settings > Integrations](https://console.apify.com/settings/integrations).
2. Install the client and run the script:

```bash
pip install apify-client
export APIFY_TOKEN=your_token
python jobs_to_csv.py https://job-boards.greenhouse.io/discord https://jobs.lever.co/spotify -o jobs.csv
```

Filters:

```bash
python jobs_to_csv.py https://job-boards.greenhouse.io/discord --keyword engineer --location Remote --days 14
```

## Daily alert: only the jobs that are new

`new_jobs.py` reads the companies in `companies.txt`, remembers the jobs it has seen in `seen_jobs.json`, and prints
only the new ones. Run it from cron once a day:

```bash
python new_jobs.py companies.txt --keyword "data engineer"
# discord: Senior Data Engineer, Ads (Remote (U.S.)) https://job-boards.greenhouse.io/discord/jobs/8299493002
# 1 new of 15 known jobs
```

You can also schedule the Actor itself on Apify (Console > Schedules) and connect its output to Google Sheets,
Slack, Zapier or Make.

## Node.js

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('v0iddo/mint-ats-jobs-scraper').call({
    companies: ['https://job-boards.greenhouse.io/discord', 'https://jobs.lever.co/spotify'],
    titleKeywords: ['engineer'],
    maxItems: 100,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

Full example: [`examples/node/jobs.mjs`](examples/node/jobs.mjs).

## Any language: one HTTP request

```bash
curl -X POST "https://api.apify.com/v2/acts/v0iddo~mint-ats-jobs-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"companies": ["https://jobs.lever.co/spotify"], "maxItems": 50}'
```

The response is the JSON array of jobs.

## Input

| Field | What it does |
| --- | --- |
| `companies` | Careers page links, one per company (up to 200 per run) |
| `titleKeywords` | Only titles containing at least one of these words |
| `locationContains` | For example `Remote`, `Berlin`, `US` |
| `remoteOnly` | Only postings marked remote |
| `postedWithinDays` | Only postings published in the last N days |
| `includeDescription` | Adds the description as plain text (slower, bigger rows) |
| `maxJobsPerCompany` | Stops one big employer from filling the whole run |
| `maxItems` | Caps the rows, and so the cost, of one run |

Links that work, for example:

| System | Link |
| --- | --- |
| Greenhouse | `https://job-boards.greenhouse.io/discord` |
| Lever | `https://jobs.lever.co/spotify` |
| Ashby | `https://jobs.ashbyhq.com/notion` |
| Workday | `https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite` |
| Workable | `https://apply.workable.com/huggingface` |

## Output

One row per job. A real row from each system is in [`examples/sample-output.json`](examples/sample-output.json):

```json
{
  "ats": "greenhouse",
  "company": "discord",
  "title": "Commercial Policy Lead",
  "department": "Policy",
  "location": "San Francisco Bay Area",
  "remote": true,
  "postedAt": "2026-09-15T16:52:11Z",
  "url": "https://job-boards.greenhouse.io/discord/jobs/8806482002",
  "salaryMin": 192000,
  "salaryMax": 216000,
  "salaryCurrency": "USD",
  "salaryInterval": "year"
}
```

Fields: `ats`, `company`, `jobId`, `title`, `department`, `team`, `location`, `country`, `remote`, `workplaceType`,
`employmentType`, `postedAt`, `updatedAt`, `url`, `applyUrl`, `salaryMin`, `salaryMax`, `salaryCurrency`,
`salaryInterval`, `scrapedAt`, and `description` when asked for.

## Cost

The Actor is paid per result: **$1.20 per 1,000 jobs**, nothing per run. `maxItems` caps what a run can cost. A new
Apify account gets $5 of platform credit every month, which covers about 4,000 jobs.

## Related Actors

- [Workday Jobs Scraper](https://apify.com/v0iddo/mint-workday-jobs-scraper): Workday career sites only, with the
  exact posting date, country, workplace type and pay range. $0.90 per 1,000 jobs.
- [Greenhouse Jobs API](https://apify.com/v0iddo/greenhouse-public-jobs),
  [Lever Jobs API](https://apify.com/v0iddo/lever-public-jobs) and
  [Ashby Jobs API](https://apify.com/v0iddo/ashby-public-jobs): one job system each, by company slug.

## License

MIT for the code in this repository. Made by [vøiddo](https://voiddo.com).
