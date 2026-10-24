// Run the Greenhouse, Lever, Workday & Ashby Jobs Scraper: Careers API Actor on Apify from Node.js.
//   npm install apify-client
//   APIFY_TOKEN=your_token node run.mjs
import { readFileSync } from 'node:fs';
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const input = JSON.parse(readFileSync(new URL('../../input.json', import.meta.url), 'utf8'));
const run = await client.actor('v0iddo/ats-jobs-scraper').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(`${items.length} results`, items[0]);
