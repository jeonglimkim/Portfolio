# Question 1
#On the following Harris School website:
#https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp
#There is a list of Program Details after the introductory paragraphs, with 23 bullet points.
#Collect the text of each of these bullet points into a list, i.e. a list that will contain
#23 strings.  As we are scraping only one website, you can write your code without generalization,
#e.g. referencing index 21 in a list of things, rather than using code to determine that index 21
#is what you want.  However, there is up to 10% bonus points available on this assignment for
#efforts at generalizing your code.

import requests
from bs4 import BeautifulSoup

url = r'https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

response.text.find('Program Details',)
response.text[96600:100050]

soup.find_all('h2')[5]

pro_details = [tag.text for tag in soup.find_all('h2') if tag.text == 'Program Details']
pro_details[0]

unordered_list = soup.find_all('ul')[35]
unordered_list

unordered_list.find_all('li')

tag_list = [tag.text.replace('\n', '').replace('\xa0', '') for tag in unordered_list.find_all('li')]
tag_list

len(tag_list) #24

#Unlike the question provides, it counts 24 bullet points instead of 23 due to the double bullet point next 
#to "PPHA 32300 Principles of" in the website.

#Attempt at bonus points

def web_scrapping(url, detail, header, headnum, bp, bpnum, li):
    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    response.text.find(detail)
    
    soup.find_all(header)[headnum]
    
    unordered_list = soup.find_all(bp)[bpnum]
    unordered_list
    
    unordered_list.find_all(li)
    
    tag_list = [tag.text.replace('\n', '') for tag in unordered_list.find_all(li)]
    print(tag_list)
    
    return len(tag_list)

url = r'https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp'
detail = 'Program Details'
header = 'h2'
headnum = 5
bp = 'ul'
bpnum = 35
li = 'li'

print(web_scrapping(url, detail, header, bp, li))



