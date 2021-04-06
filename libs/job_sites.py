from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from datetime import datetime
import re

from common.errors import RequestFailureError, HTMLElementNotFoundError


@dataclass(eq=False)
class JobSite:
    name: str
    url: str
    tag_name: str
    query: Dict
    job_profile_elements: Dict
    headers: str = field(default=None)

    def load_data(self, payload: Dict, file_path: str = None) -> None:
        # response = requests.get(self.url, params=payload, headers=self.headers)
        occupation_url = "https://www.indeed.com/jobs?q=data+ENgineer&l="
        response = requests.get(occupation_url)
        if response.status_code != 200:
            raise RequestFailureError(f"Request failure for job site {self.name}, {response.content}")

        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.findAll(self.tag_name, self.query)

        if elements is None:
            raise HTMLElementNotFoundError("")

        if file_path is None:
            file_path = f"../data/{self.name}_{payload['p']}_{datetime.today().strftime('%Y%m%d%H')}.txt"

        file = open(file_path, 'w')
        file.write("job_url," + ",".join(self.job_profile_elements.keys()) + "\n")

        try:
            for element in elements:
                job_url = "https://www.indeed.com" + element['href']
                job_profile = self.extract_job_profile(job_url)
                file.write(f"{job_url}," + ",".join(job_profile) + "\n")

        finally:
            file.close()

    def extract_job_profile(self, job_url: str) -> List[str]:
        response = requests.get(job_url)
        if response.status_code != 200:
            raise RequestFailureError(f"Request failure for job url {job_url}, {response.content}")

        soup = BeautifulSoup(response.content, 'html.parser')
        job_profile = []
        for attr, profile in self.job_profile_elements.items():
            element = soup.find(*profile)
            text = element.text

            # most of requirements are under <li>
            # if <li> exists, then only use text in <li>
            # else, use whole text
            if attr == 'job_description':
                items = element.find_all('li')
                if len(items) >= 5:
                    text = ','.join([item.text for item in items])

            job_profile.append(re.sub(r'[,\s]+', ' ', text))

        return job_profile


indeed = JobSite(
    name="indeed",
    url="https://www.indeed.com/jobs",
    tag_name="a",
    query={"class": "jobtitle turnstileLink"},
    job_profile_elements={
        "job_title": ["h1", {"class": "jobsearch-JobInfoHeader-title"}],
        "job_description": ["div", {"id": "jobDescriptionText"}],

    }
)
indeed.load_data({"p": "data engineer"})


