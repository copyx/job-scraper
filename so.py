import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "s-pagination"})
    anchors = pagination.find_all("a")
    anchors = anchors[0:-1]

    pages = []
    for anchor in anchors:
        pages.append(int(anchor.span.string))

    return max(pages)


def extract_job(html):
    title = html.h2.a["title"].strip()
    company, location = html.h3.find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.string.strip()

    job_id = html["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page + 1):
        print(f"Scraping Stackoverflow page {page}")
        result = requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_cards = soup.find_all("div", {"class": "-job"})
        for job_card in job_cards:
            jobs.append(extract_job(job_card))

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs