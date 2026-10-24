# Greenhouse, Lever, Workday & Ashby Jobs Scraper: export to CSV or JSON with Python, Node.js or curl

Collect public job postings from Greenhouse, Lever, Workday, Workable, Ashby, Recruitee, Personio and BambooHR with one consistent schema. Paste careers page links and the system is detected for you. Filter by title, location, remote and date. Pay and plain text descriptions included.

This repository has ready scripts for the [Greenhouse, Lever, Workday & Ashby Jobs Scraper: Careers API](https://apify.com/v0iddo/ats-jobs-scraper) Actor on Apify. The Actor does the
fetching, paging and cleaning; the scripts here run it with your input and save the results as a CSV or JSON file.

## Quick start

1. Create an Apify account and copy your API token from
   [Console > Settings > Integrations](https://console.apify.com/settings/integrations).
2. Install the client and run the script with the example input:

```bash
pip install "apify-client>=2"
export APIFY_TOKEN=your_token
python run.py input.json -o results.csv --max-items 50
```

Edit `input.json` for your own run. You can also run the Actor in the browser on its
[Apify page](https://apify.com/v0iddo/ats-jobs-scraper), schedule it there, and connect its output to Google Sheets, Slack, Zapier or Make.

## Input

The example input (`input.json`):

```json
{
  "companies": [
    "https://job-boards.greenhouse.io/discord",
    "https://jobs.lever.co/spotify",
    "https://apply.workable.com/huggingface"
  ],
  "includeDescription": true,
  "maxItems": 50,
  "maxJobsPerCompany": 20
}
```

| Field | Type | What it does |
| --- | --- | --- |
| `companies` | array | One company per line, at most 200. |
| `titleKeywords` | array | Optional. Only postings whose title contains at least one of these words or phrases are returned. |
| `locationContains` | string | Optional text such as Berlin, Remote, Canada or US. |
| `remoteOnly` | boolean | Return only postings that are marked remote or say remote in their location. |
| `postedWithinDays` | integer | Optional. Skip postings that were published longer ago than this. |
| `includeDescription` | boolean | Add the job description as plain text. |
| `maxJobsPerCompany` | integer | Optional. Stop reading a company after this many matching postings and go on to the next one, so a large employer first in the list does not fill the whole run. |
| `maxItems` | integer | The run stops after this many result rows. |

## Output

One row per result. A real row from a run of the example input (more in
[`examples/sample-output.json`](examples/sample-output.json)):

```json
{
  "ats": "greenhouse",
  "company": "discord",
  "jobId": "8806482002",
  "title": "Commercial Policy Lead",
  "department": "Policy",
  "team": null,
  "location": "San Francisco Bay Area",
  "country": null,
  "remote": true,
  "workplaceType": null,
  "employmentType": null,
  "postedAt": "2026-09-15T16:52:11Z",
  "updatedAt": "2026-10-21T00:27:20Z",
  "url": "https://job-boards.greenhouse.io/discord/jobs/8806482002",
  "applyUrl": "https://job-boards.greenhouse.io/discord/jobs/8806482002",
  "salaryMin": 192000,
  "salaryMax": 216000,
  "salaryCurrency": "USD",
  "salaryInterval": "year",
  "descriptionText": "Discord has a highly engaged community of millions of daily active users who use the platform for many different reasons, but there’s one thing that nearly everyone does: play video games. Discord plays a uniquely important role in the future of gaming, and we are focused on m...",
  "scrapedAt": "2026-10-24T18:34:02Z"
}
```

Fields: `ats`, `company`, `jobId`, `title`, `department`, `team`, `location`, `country`, `remote`, `workplaceType`, `employmentType`, `postedAt`, `updatedAt`, `url`, `applyUrl`, `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryInterval`, `descriptionText`, `scrapedAt`.

## Node.js

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('v0iddo/ats-jobs-scraper').call({"companies": ["https://job-boards.greenhouse.io/discord", "https://jobs.lever.co/spotify", "https://apply.workable.com/huggingface"], "includeDescription": true, "maxItems": 50, "maxJobsPerCompany": 20});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

Full example: [`examples/node/run.mjs`](examples/node/run.mjs).

## Any language: one HTTP request

```bash
curl -X POST "https://api.apify.com/v2/acts/v0iddo~ats-jobs-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"companies": ["https://job-boards.greenhouse.io/discord", "https://jobs.lever.co/spotify", "https://apply.workable.com/huggingface"], "includeDescription": true, "maxItems": 50, "maxJobsPerCompany": 20}'
```

The response is the JSON array of results.

## Cost

The Actor is paid per result: **$1.20 per 1,000 results**, nothing per run. `maxItems` caps the rows, and so the cost, of one run. A new Apify account gets $5 of platform credit every month.

## License

MIT for the code in this repository. Made by [vøiddo](https://voiddo.com).
