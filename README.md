# job-tracker
A scraper that retrieves graduate opportunities from BrightNetwork, Gradcracker, and Trackr, sending daily notifications when new positions open.

## Why I built this
As a final year student, I found myself obsessively checking these three sites every day, manually filtering through opportunities. Most days? Nothing new. It felt like a waste of time, but I couldn't afford to miss that one posting that might be perfect for me.
So I decided to automate it. This scraper compares newly found listings against what's already in `seen.json` and emails me only the fresh opportunities. No more mindless browsing, just the information I actually need.

## Current Progress (08/12/2025)
### Setup Complete
- ✅ URL selectors configured for each site (stored in config.json)
- ✅ Google app password set up for email notifications via SMTP
- ✅ Playwright integrated for browser automation
- ✅ Pre-filtered URLs to show only graduate schemes in my area of interest (keeps the data lean and personalised)
- ✅ Core scraping logic implemented with site-specific extractors
- ✅ Email notification system built and ready to test

### Scraping Status:
- ✅ **Trackr scraper**: Working! Successfully retrieving and parsing job data.
- 🚧 **BrightNetwork & Gradcracker**: Hit a wall with Cloudflare protection. Currently exploring Apify integration to get around this.

## How It Works
- Scrapes each site using Playwright with site-specific CSS selectors
- Compares found listings against seen.json to identify new postings
- Emails you a clean summary with titles and links for anything new
- Updates seen.json so you don't get duplicate notifications

## What's Next
- Overcome Cloudflare protection on BrightNetwork and Gradcracker
- Testing of the email workflow
- Set up as a cron job for daily automated runs
- Write setup instructions (config template, installation steps, customization guide)

## The Goal
Once complete, you'll get an email like:
```
New job postings found - 08-12-2025

trackr:
Software Engineering Graduate Scheme
https://trackr.co.uk/jobs/12345

brightnetwork:
Technology Graduate Programme - London
https://www.brightnetwork.co.uk/graduate-jobs/67890"
```

No more tab juggling. No more "did I check this already?" Just the new stuff, delivered to your inbox.
