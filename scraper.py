####################################################################
""" Importing Libraries """
####################################################################

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from logger import LogRecord
from webdriver_manager.chrome import ChromeDriverManager

######################################################################################################################
"""
In below section it shows that Scraper class has been created that contain information of login page of LinkedIn
and then allow the instance to load the website page where person might find a cookies to store and reject option 
that also taken care of, by using accept_cookies function and the it allow us to enter username and password of website 
to login.

"""
class Scraper():
    def __init__(self, username, password):
        self.driver = webdriver.Chrome('/Users/pratiksha/Documents/scratch/Datacollectionpipeline/Data-Collection-Pipeline/chromedriver')    
        self.username = username
        self.password = password

    def __accept_cookies(self):
        """
            In this Method we accept the cookies of Linkedin.com website.
        """
        try:
            accept_cookies_by_clicking = self.__get_each_element("//*[@class='artdeco-global-alert-action artdeco-button artdeco-button--inverse artdeco-button--2 artdeco-button--primary']") 
            accept_cookies_by_clicking.click()
        except AttributeError:
            pass
        except Exception as e:
            LogRecord.log_record(str(e))
            pass  

    def get_iterate_items(self,item_iterate,item_name,item_cutomize=0):
        if item_cutomize == 1:
            gathred_urls = [{'url': li.get_attribute('href')} for li in item_iterate[0:5]]# this loop will collect only required URL with given range [0:5]
            gathred_name = [{'name': name} for name in item_name]
            item_list = list(zip(gathred_name,gathred_urls)) 
        else:
            gathred_urls = [{'url': li.get_attribute('href')} for li in item_iterate]
            gathred_name = [{'name': name} for name in item_name]
            item_list = list(zip(gathred_name,gathred_urls)) 
        return item_list

    name_topbar_menu = []
    def select_options_url(self)-> list:
        """
            In this Method we gathered all the URLs of Menus available for different purpose.
        """
        all_li = self.__get_elements_list("//li/a")
        name_topbar_menu = ["Home","My Network","Jobs","Messageing","Notifications"]
        gathered_name_urls = self.get_iterate_items(all_li,name_topbar_menu,1)
        return gathered_name_urls


    """
        Below section collect the jobs that are recomended and remote
    """

    def get_linkedin_remote_jobs(self):
        job_list = []
        jobs = self.__get_elements_list("//*[@class='job-card-list__entity-lockup  artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view']")
        for job in jobs:
            job_title = job.find_element(by=By.XPATH, value=".//*[@class='disabled ember-view job-card-container__link job-card-list__title']").text
            company_name = job.find_element(by=By.XPATH, value=".//*[@class='job-card-container__link job-card-container__company-name ember-view']").text
            job_location = job.find_element(by=By.XPATH, value=".//*[@class='job-card-container__metadata-wrapper']").text 
            comapny_logo = job.find_element(by=By.XPATH, value=".//*[@class='ember-view']").get_attribute('src') 
            job_container = {
                'job_title':job_title,
                'company_name':company_name,
                'job_location':job_location,
                'comapny_logo':comapny_logo
            }
            job_list.append(job_container)
            
        return job_list

    def get_link_jobs(self):
        categories_jobs = ['Recommended','Remote']
        get_link_recomended = self.__get_elements_list("//*[@class='app-aware-link artdeco-button artdeco-button--2 artdeco-button--tertiary']")
        job_link_urls = self.get_iterate_items(get_link_recomended,categories_jobs,0)

        return job_link_urls
    
    def get_remote_recomended_jobs(self):
        url_remote = "https://www.linkedin.com/jobs/search?geoId=101165590&f_WT=2&origin=JOBS_HOME_REMOTE_JOBS"
        url_recomended ="https://www.linkedin.com/jobs/collections/recommended"
        self.driver.get(url_remote)
        sleep(2)
        self.driver.execute_script("window.open('');")
        get_remote_jobs = self.get_linkedin_remote_jobs()
        sleep(4)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url_recomended)
        get_recomended_jobs = self.get_linkedin_remote_jobs()
        sleep(4)
        self.driver.execute_script("window.close('');")
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(2)
        self.driver.switch_to.default_content()
        return  get_remote_jobs,get_recomended_jobs     
      
    #below are the methods of selenium commands to save repeatation of code
    def __get_each_element(self, places_locate) -> object:
        elements = self.driver.find_element(by=By.XPATH, value=places_locate) 
        return elements

    def __get_elements_list(self, places_locate) -> list:
        elements = self.driver.find_elements(by=By.XPATH, value=places_locate)
        return elements 

    def __login_page(self):
        """
            Login Page to send username and password using selenium command
        """
        try:
            u_name = self.__get_each_element("//input[@name='session_key']")
            u_password = self.__get_each_element("//input[@name='session_password']")
            u_name.send_keys(self.username)
            u_password.send_keys(self.password)
            submit = self.__get_each_element("//button[@type='submit']")
            submit.click()
        except AttributeError:
            pass
        except Exception as e:
            LogRecord.log_record(str(e))
            pass  

    def load_page(self, url):
        self.driver.get(url)
        sleep(2)
        self.__accept_cookies()
        self.__login_page()
        sleep(2)
        return None

if __name__ == "__main__":
    scraper = Scraper("pratikshavyas93@gmail.com","**********")
    scraper.load_page('https://www.linkedin.com')
    get_all_topbar_url_name = scraper.select_options_url()
    for url_name, url in get_all_topbar_url_name:
        if url_name['name'] == "Jobs":
            scraper.load_page(url['url'])
            remotejobs, recomendedjob = scraper.get_remote_recomended_jobs()  
            