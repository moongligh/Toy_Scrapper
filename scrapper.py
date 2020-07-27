import requests as req
from bs4 import BeautifulSoup as bs

# ======== StackOverFlow 스크랩퍼 Start ===================== #

def so_get_last_page(URL):    # 페이지 추출 함수
    result = req.get(URL)
    soup = bs(result.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'})

    if pages is None:   # 페이지 네비게이션이 없을경우를 위한 조건문
        last_page = 0
    else:
        pages.find_all('a')
        last_page = pages[-2].get_text(strip=True)

    return int(last_page)

def so_extract_job(html):  # 채용정보를 추출하여 doc 형태로 리턴
    title = html.find('a', {'class': 's-link'})['title']
    company, location = html.find('h3').find_all('span', recursive=False) # unpack value를 이용하기 위해 첫단계 'span'만 수집
    company.get_text(strip=True)
    location.get_text(strip=True).strip('-').strip(' \r').strip('\n')

    # company_location = html.find('h3').get_text(strip=True) # h3태그 안의 모든 text를 가져온다.
    # company = company_location.split('•')[0]    # 가져온 text의 값 중 • 을 기준으로 앞은 회사 뒤는 지역을 할당한다.
    # location = company_location.split('•')[1]

    job_id = html['data-jobid']

    return {'title': title,
        'company': company,
        'location': location,
        'link': f'https://stackoverflow.com/jobs/{job_id}'
    }

def so_extract_jobs(last_page, URL):    # 추출한 최종페이지를 이용하여 모든 채용 정보를 수집
    jobs=[]
    for page in range(last_page):   # 추출한 마지막 페이지를 이용한 범위지정 for loop
        print(f'StackOverFlow Scarpping page {page+1}')
        result = req.get(f'{URL}&pg={page+1}')
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})

        for result in results:
            job = so_extract_job(result)
            jobs.append(job)

    return jobs


def so_get_jobs(word):
    URL = f'https://stackoverflow.com/jobs?q={word}' # 페이지 추출을 위한 기본 URL
    last_page = so_get_last_page(URL) # 최종 페이지 추출
    jobs = so_extract_jobs(last_page, URL)  # 최종 페이지를까지 데이터 추출 
    return jobs

# ======== StackOverFlow 스크랩퍼 End ===================== #

# ======== indeed 스크랩퍼 Start ===================== #
import requests as req
from bs4 import BeautifulSoup as bs

LIMIT = 20 # 페이지당 출력되는 게시물 수

def indeed_get_last_page(URL):    # 페이지 추출 함수
    result = req.get(URL)
    soup = bs(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})

    if pagination is None:  # 페이지 네비게이션이 없을경우를 위한 조건문
        last_page = 0
    else:
        links = pagination.find_all('a')
        pages = []

        for link in links[:-1]: # 마지막 a링크는 '다음'으로 페이지가 아니므로 삭제
            pages.append(int(link.find('span').string)) # link에 String요소가 하나라면 link.string으로 수정가능
        last_page = pages[-1] # 마지막 페이지 추출

    return last_page

def indeed_extract_job(html): # 채용정보를 추출하여 doc 형태로 리턴
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:  # 회사명에 링크가 있는경우 앵커에서 추출, 아닌경우 그대로 추출
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip() # 빈칸제거
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']

    return {'title': title,
        'company': company,
        'location': location,
        'link': f'https://kr.indeed.com/viewjob?jk={job_id}'
    }

def indeed_extract_jobs(last_page, URL): # 추출한 최종페이지를 이용하여 모든 채용 정보를 수집
    jobs = []

    for page in range(last_page):  # 추출한 마지막 페이지를 이용한 범위지정 for loop
        print(f'indeed Scarpping page {page+1}')
        result = req.get(f'{URL}&start={page*LIMIT}')
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

        for result in results:
            job = indeed_extract_job(result)
            jobs.append(job)

    return jobs

def indeed_get_jobs(word):
    URL = f'https://kr.indeed.com/jobs?q={word}' # 페이지 추출을 위한 기본 URL
    last_page = indeed_get_last_page(URL) # 최종 페이지 추출
    jobs = indeed_extract_jobs(last_page, URL)  # 최종 페이지까지 데이터 추출 

    return jobs

# ======== indeed 스크랩퍼 Start ===================== #

# ======== 모든 구직정보 통합 Start ===================== #

def total_get_jobs(word):
    indeed_jobs = indeed_get_jobs(word)
    so_jobs = so_get_jobs(word)
    jobs = indeed_jobs + so_jobs

    return jobs

# ======== 모든 구직정보 통합 End ===================== #