import cfscrape
import requests
import os, sys
from recaptcha import *
from bs4 import BeautifulSoup
import re

# Requests wrapper
#url = 'https://www.acgnx.se/'
url = 'https://www.acgnx.se/show-8A7C71BCBEB854DDF0880AF26FB4504A47F50B2D.html'
session = requests.session()
session.headers = 'content-type'
session.mount("http://", cfscrape.CloudflareScraper())
scraper = cfscrape.create_scraper(sess=session)
req = scraper.get(url).content
#print req

### Save request as HTML named as 'Result.html'

f_name = "Page.html"
f = open(f_name, 'w')
f.write(req.encode('UTF-8'))
f.close()

### Excute JavaScript file
start = time()

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.getcwd()}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = os.getcwd()+"\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
driver.get(os.path.realpath(f_name))


### Get download link
soup = BeautifulSoup(driver.page_source, "lxml")
link = str(soup.find(id="download"))
name = str(soup.find('div', {"class":"location"}))
#print link

### Parse link and name
regex1 = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
link = regex1.findall(link)
regex2 = re.compile('<div[^>]+class="location">[ \t\n\r\f\v]+(.*?)[ \t\n\r\f\v]+</div>', re.IGNORECASE)
name = regex2.findall(name)

#print link
link = 'https://www.acgnx.se/'+str(link[0])
#response = requests.request('GET', link)
print "The download link: " + link + '\n'
print "The name of the file: " + name[0] + '\n'

### Download
driver.find_element_by_id("download").click()
sleep(5)
driver.close()

#output = open(str(name[0])+".torrent", 'w')
#output.write(response)
#output.close()

#mainWin = driver.current_window_handle
#driver = recaptcha_process(driver)
#print(driver.page_source)
#driver.close()
#elapsed = time() - start
#print(elapsed)



