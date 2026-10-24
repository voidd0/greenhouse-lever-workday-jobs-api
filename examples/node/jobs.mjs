// Every open job from a few careers pages, printed as JSON lines.
//   npm install apify-client
//   APIFY_TOKEN=... node jobs.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('v0iddo/mint-ats-jobs-scraper').call({
    companies: [
        'https://job-boards.greenhouse.io/discord',
        'https://jobs.lever.co/spotify',
        'https://jobs.ashbyhq.com/notion',
        'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite',
    ],
    titleKeywords: ['engineer'],
    maxJobsPerCompany: 25,
    maxItems: 100,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) console.log(JSON.stringify({ company: job.company, title: job.title, location: job.location, url: job.url }));
console.error(`${items.length} jobs, run ${run.status}`);
