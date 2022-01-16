from bs4 import BeautifulSoup
import requests 
import csv
import http.client
import os.path

import re

filename = 'indeed_results.csv'
file = open(filename, 'w', encoding = 'utf8', newline = '')
writer = csv.writer(file)
writer.writerow(['Title','Company', 'Location', 'Url'])

def getjobs(page):
        try:
            html_text = requests.get(f'https://www.indeed.com/jobs?q=python%20internship&l=Hawthorne%2C%20NJ&start={page}')
            soup = BeautifulSoup(html_text.text, 'html.parser')

        # copys full text box
            jobs = soup.find_all('div', class_ ='slider_container')

            for job in jobs:
                titles = []
                companys = []
                locations = []
                newtag = [] 

                jobs = soup.find_all('h2', class_="jobTitle jobTitle-color-purple")
                title = job.find('h2').text

                jobs = soup.find_all('span', class_="companyName")
                company = job.find('span', class_ = 'companyName').text

                jobs = soup.find_all('div', class_= 'companyLocation')
                location = job.find('div', class_= 'companyLocation').text
                locations.append(location.replace(',', '.'))

                jobs = soup.find_all('div', id= 'mosaic-provider-jobcards')
                try:
                    atag = job.a['href']
                    #newtag.get('href')
                    atag = 'http://www.indeed.com' + atag
                except: AttributeError
              
            # Replace New York job locations with blank space
                NJ_locations = [s for s in locations if 'NJ' in s]  
                for element in NJ_locations:
                    if element == '':
                        NJ_locations.remove(element)

            # Append only New Jersey locatioins
                for element in NJ_locations:
                    if element != '':
                            titles.append(title)
                            companys.append(company)
                            newtag.append(atag)

                output = writer.writerow([','.join(titles), ','.join(companys), " ,".join(NJ_locations), ",".join(newtag)])

        except requests.exceptions.ConnectionError as e:
            html_text = "No Response"

if __name__=='__main__':
    page_number = 0
    for i in range(0,100,10):
        page_number+=1
        print("Collecting Data from page", page_number, "...")
        getjobs(i)