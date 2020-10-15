import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&filter=0"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    # search_count = indeed_soup.find("div", {"id": "searchCountPages"})
    # print(search_count)

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    links = links[0:-1]

    pages = []
    for link in links:
        pages.append(int(link.string))
        # pages.append(print(link["href"]))

    return max(pages)


def extract_job(html):
    title = html.find("h2", {"class": "title"}).a["title"]

    company = html.find("span", {"class": "company"})

    if company.a is not None:
        company = company.a.string
    else:
        company = company.string

    company = company.strip()

    location = html.find("span", {"class": "location"}).string
    # location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(0, last_page):
        print(f"Scraping Indeed page {page + 1}")
        result = requests.get(f"{URL}&start={page * 50}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_cards = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for job_card in job_cards:
            jobs.append(extract_job(job_card))

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs