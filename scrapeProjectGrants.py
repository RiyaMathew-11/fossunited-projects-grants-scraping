import requests
from bs4 import BeautifulSoup

import csv

siteURL = "https://archive.fossunited.org/grants"


def fetch_grants_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    grants = soup.find_all('section',{'data-section-template':'Grant Recipient'})
    data = []
    for grant in grants:
        about_project = grant.find('p').text.strip()
        grant_status = 'Accepted'
        project_name = grant.find('h4',{'class':'mt-0'}).text.strip()
        project_website = grant.find('a', {'class':'mt-3'})['href']
        project_stats = grant.find_all('div',{'class':'col-6 col-md-6'})
        co_sponsor = ''
        
        date_of_provision = project_stats[0].text.strip()
        grant_amount = project_stats[1].text.strip()
        if len(project_stats) > 2:
            co_sponsor = project_stats[2].text.strip()
        data.append([about_project,grant_status,project_name,project_website,co_sponsor,date_of_provision,grant_amount])
        
    return data
        
        
def write_to_csv(data):
    with open('data/foss_project_grants.csv', 'a',) as file:
        writer = csv.writer(file)
        writer.writerows(data)
        

grants_data = fetch_grants_data(siteURL)
write_to_csv(grants_data)
    