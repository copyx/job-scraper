import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
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

    companyElement = html.find("span", {"class": "company"})

    if companyElement.a is not None:
        company = companyElement.a.string
    else:
        company = companyElement.string

    company = company.strip()

    locationElement = html.find("span", {"class": "location"})
    if locationElement is None:
        locationElement = html.find("div", {"class": "location"})
    location = locationElement.string

    # location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(url, last_page):
    jobs = []
    for page in range(0, last_page):
        print(f"Scraping Indeed page {page + 1} / {last_page}")
        result = requests.get(f"{url}&start={page * 50}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_cards = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for job_card in job_cards:
            jobs.append(extract_job(job_card))

    return jobs


def get_jobs(keyword):
    limit = 50
    url = f"https://kr.indeed.com/jobs?q={keyword}&limit={limit}&filter=0"
    last_page = get_last_page(url)
    jobs = extract_jobs(url, last_page)

    return jobs
