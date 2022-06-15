####################################################################
""" Importing Libraries """
####################################################################
from re import sub
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from logger import LogRecord
######################################################################################################################
"""
In below section it shows that Scraper class has been created that contain information of login page of LinkedIn
and then allow the instance to load the website page where person might find a cookies to store and reject option 
that also taken care of, by using accept_cookies function and the it allow us to enter username and password of website 
to login.

"""
class Scraper():
    def __init__(self, username, password):
        self.driver = webdriver.Chrome('./chromedriver')    
        self.username = username
        self.password = password 
    def __accept_cookies(self):
        try:
            accept_cookies_by_clicking = self.__get_each_element("//*[@class='artdeco-global-alert-action artdeco-button artdeco-button--inverse artdeco-button--2 artdeco-button--primary']") 
            accept_cookies_by_clicking.click()
        except AttributeError:
            pass
        except Exception as e:
            LogRecord.log_record(str(e))
            pass   

    def select_options_url(self)-> list:
        options_locator = "//*[@class='global-nav__primary-items']"
        gather_all_url_list = self.__get_elements_list(options_locator)
        print("gather the link", gather_all_url_list)
        return gather_all_url_list

    def __get_each_element(self, places_locate) -> object:
        elements = self.driver.find_element(by=By.XPATH, value=places_locate) 
        return elements

    def __get_elements_list(self, places_locate) -> list:
        elements = self.driver.find_elements(by=By.XPATH, value=places_locate)
        return elements  

    def __login_page(self):
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
        return None

if __name__ == "__main__":
    scraper = Scraper("pratikshavyas93@gmail.com","**********")
    scraper.load_page('https://www.linkedin.com')
    get_all_topbar_url = scraper.select_options_url()
