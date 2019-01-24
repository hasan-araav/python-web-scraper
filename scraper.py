import requests
from bs4 import BeautifulSoup
import lxml

def getPageContent(url):
	result = requests.get(url)
	src = result.content
	return BeautifulSoup(src, "lxml")
	
page = getPageContent('http://www.bdjobs.com/')
category = page.find_all('div', { 'class': 'category-list' })

functional_category = category[0].find_all('a')
industrial_category	= category[1].find_all('a')
special_category	= category[2].find_all('a')

functional_category_links = []
industrial_category_links = []
special_category_links	  = []

def get_pages(url):
	page = getPageContent(url)
	pages = page.select("#topPagging > ul > li:last-child > a:last-child")
	if not pages:
		total_pages = '0'
	else:
		total_pages = pages[0].text
	final_pages = int(total_pages.lstrip('.'))
	return final_pages
	# print(final_pages)

for link in functional_category:
	if link.has_attr('title') and link.has_attr('href'):
		functional_category_links.append({'title': link.attrs['title'], 'url': link.attrs['href'], 'pages': get_pages(link.attrs['href'])})

for link in industrial_category:
	if link.has_attr('title') and link.has_attr('href'):
		industrial_category_links.append({'title': link.attrs['title'], 'url': link.attrs['href'], 'pages': get_pages(link.attrs['href'])})

for link in special_category:
	if link.has_attr('title') and link.has_attr('href'):
		special_category_links.append({'title': link.attrs['title'], 'url': link.attrs['href'], 'pages': get_pages(link.attrs['href'])})

def get_job_url(url,page):
	result = requests.post(url,
		data = {
			'txtsearch': '',
			'fcat': '19',
			'qOT': '0',
			'iCat': '0',
			'Country': '0',
			'qPosted': '0',
			'qDeadline': '0',
			'Newspaper': '0',
			'qJobSpecialSkill': '-1',
			'qJobNature': '0',
			'qJobLevel': '0',
			'qExp': '0',
			'qAge': '0',
			'hidOrder': '',
			'pg': page,
			'hidJobSearch': 'JobSearch',
			'MPostings': '',
			'ver': '',
			'strFlid_fvalue': '',
			'strFilterName': '',
			'hClickLog': '1',
			'hPopUpVal': '1',
			'rc1': '1',
			'userfiltername1': '',
			'userfiltername': '',
			'hUserfiltername': '0'
		})
	src = result.content
	page = BeautifulSoup(src, "lxml")
	links = page.select('.job-title-text a')
	urls = []
	for link in links:
		urls.append('http://jobs.bdjobs.com/'+link.attrs['href'])
	return urls

def get_job(url,page):
	job_urls = get_job_url(url,page)
	print(job_urls)


def get_jobs(links):
	jobs = []
	for link in links:
		for page in range(link['pages']):
			job = get_job(link['url'], page+1)

functional_category_jobs = get_jobs(functional_category_links)
# industrial_category_jobs = get_jobs(industrial_category_links)
# special_category_jobs	 = get_jobs(special_category_links)
# print(functional_category_jobs)
