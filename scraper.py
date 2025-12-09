from playwright.sync_api import sync_playwright
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


with open("config.json") as f:
    config = json.load(f)

URLS = config["urls"]
EMAIL = config["email"]

SEEN_FILE = "seen.json"

SELECTORS = {
    "trackr": "a.text-trackr-link-blue",
    "brightnetwork": "a[href*='/graduate-jobs/']",
    "gradcracker": "a[href*='/graduate-job/']"
}

def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return json.load(f)
    except:
        return {}
    
def save_seen(data):
  with open(SEEN_FILE, "w") as f:
      json.dump(data, f, indent=2)

def send_email(new_jobs):
    today = datetime.now().strftime("%d-%m-%Y")
    subject = f"New job postings found - {today}"

    body = "\n\n".join(
        f"{site}:\n{title}\n{link}"
        for site, title, link in new_jobs
    )

    msg = MIMEText(body)
    msg["From"] = EMAIL["from"]
    msg["To"] = EMAIL["to"]

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(EMAIL["from"], EMAIL["password"])
        s.send_message(msg)

def extract_jobs(page, selector, site):
    """Extract job titles and links from a page using a CSS selector."""
    jobs = []
    if site == "gradcracker":
        for article in page.query_selector_all("article"):
            link_el = article.query_selector("header a")
            if link_el:
                title = (link_el.text_content() or "").strip()
                url = link_el.get_attribute("href")
                if title and url:
                    jobs.append((title, url))
    elif site == "brightnetwork":
        for job_el in page.query_selector_all("div.search-result-card"):
          link_el = job_el.query_selector("a.result-link")
          if link_el:
              title = (link_el.text_content() or "").strip()
              url = link_el.get_attribute("href") or job_el.get_attribute("data-href")
              if title and url:
                  # prepend domain if it's relative
                  if url.startswith("/"):
                      url = "https://www.brightnetwork.co.uk" + url
                  jobs.append((title, url))
    elif site == "trackr":
        for job_el in page.query_selector_all("a.text-trackr-link-blue"):
            title = (job_el.text_content() or "").strip()
            url = job_el.get_attribute("href")
            if title and url:
                jobs.append((title, url))
    return jobs

def main():
    seen = load_seen()
    new_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for site, url in URLS.items():
            page.goto(url)
            page.wait_for_timeout(3000)  # wait for JS to render

            print(f"--- {site} page content ---")
            print(page.content()[:2000])

            selector = SELECTORS[site]
            jobs = extract_jobs(page, selector, site)

            old_links = set(seen.get(site, []))
            current_links = [link for _, link in jobs]

            for title, link in jobs:
                if link not in old_links:
                    new_jobs.append((site, title, link))

            seen[site] = current_links

        browser.close()

    if new_jobs:
        send_email(new_jobs)

    if not seen:
        save_seen(seen)

if __name__ == "__main__":
    main()