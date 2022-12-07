import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from . import scrapeModel
from user.models import UserAccount
from job_posting.models import JobPost
from job_posting.serializers import DefaultJobPostSerializer
import json
from django.core.serializers import serialize
import os
from decouple import config

def scraper(searchQuery,searchLocation,self):

    externalAccount=UserAccount.objects.get(pk=14)

    #https://stackoverflow.com/questions/37883759/errorssl-client-socket-openssl-cc1158-handshake-failed-with-chromedriver-chr
    options=webdriver.ChromeOptions()
    options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--window-size=1920x1480')
    #driver=webdriver.Chrome(executable_path=path,options=options)
    #driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)
    driver=webdriver.Chrome(executable_path=config("CHROMEDRIVER_PATH"),chrome_options=options)


    print("Inside Scraper", file=sys.stderr)
    driver.get('https://www.monster.ca/jobs')

    driver.maximize_window()
    #SEARCH INPUTS
    self.send(text_data=json.dumps({"message":"Beginning search"}))
    driver.find_element(By.ID,"search-job").send_keys(searchQuery)
    driver.find_element(By.ID,"search-location").send_keys(searchLocation)

    driver.find_element(By.XPATH, '//form[@class="form-inline"]/button[1]').click()
    #driver.implicitly_wait(105)
    time.sleep(7)

    jobCards=driver.find_elements(By.XPATH,'//article[@data-testid="svx_jobCard"]')
    print(len(jobCards))

    numOfResults=len(jobCards)
    currCard=0
    scraps=[]

    for jc in jobCards:
        
        jc.click()
        time.sleep(2)

        #finds DESCRIPTION
        descElement=driver.find_element(By.XPATH,'//div[@class="descriptionstyles__DescriptionBody-sc-13ve12b-4 djFvUg"]')
        descElementSource=driver.execute_script("return arguments[0].innerHTML;",descElement)
        descElementCleaned=scrapeModel.ScrapeModel.remove_html_tags(descElementSource)
        
        #finds POSTED DATE
        postDate=driver.find_element(By.XPATH,'//div[@data-test-id="svx-jobview-posted"]').text
        postDate=JobPost.calculatePostDate(postDate)

        #finds COMPANY NAME
        companyName=driver.find_element(By.XPATH,"//h2[@class='headerstyle__JobViewHeaderCompany-sc-1ijq9nh-6 dyxqrf']").text

        #finds JOB TITLE
        jobTitle=driver.find_element(By.XPATH,"//h1[@class='headerstyle__JobViewHeaderTitle-sc-1ijq9nh-5 eetoNA JobViewTitle']").text

        #finds LOCATION
        location=""
        try:
            location=driver.find_element(By.XPATH,"//div[@id='details-table']/div[@class='detailsstyles__DetailsTableRow-sc-1deoovj-2 fvvDpq'][3]/div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ']/div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ'][1]").text
            location+=" "+driver.find_element(By.XPATH,"//div[@id='details-table']/div[@class='detailsstyles__DetailsTableRow-sc-1deoovj-2 fvvDpq'][3]/div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ']/div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ'][2]").text
        except:
            try:
                location=driver.find_element(By.XPATH,"//div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ']/div[@class='detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 eyvZUJ']").text
            except:
                location="Location not specified"

        #finds LINK TO APPLICATION
        jobLink=driver.find_element(By.XPATH,'//a[@data-testid="svx_jobCard-title"]').get_attribute("href")

        #MAKES SURE JOB DOESN'T EXIST AS TO NOT RECREATE IT -- ASSUMES LINK IS UNCHANGING
        job=None

        try:
            job=JobPost.objects.get(link=jobLink)
        except:
            job=JobPost.objects.create(employer=externalAccount,title=jobTitle,location=location,description=descElementCleaned,company=companyName,date_created=postDate,link=jobLink)
        
        scraps.append(DefaultJobPostSerializer(job).data)
        currCard+=1.0
        percentage=f'{100*currCard/numOfResults:.2f}'
        self.send(text_data=json.dumps({"percent":percentage}))

        #makes sure card is focused, otherwise can't click
        driver.execute_script("arguments[0].scrollIntoView();",jc)

    #jobTitle=driver.find_elements(By.CLASS_NAME,'job-cardstyle__JobCardCompany-sc-1mbmxes-3')

    # titles=[jt.text for jt in jobTitle]
    # print(titles)

    def obj_dict(obj):
            return obj.__dict__

    self.send(text_data=json.dumps({"payload":json.dumps(scraps,default=obj_dict)}))

    for s in scraps:
        print(s.__str__(), file=sys.stderr)
        print(s.__str__())