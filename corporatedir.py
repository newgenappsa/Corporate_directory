from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import re
import time

def is_element_present(driver,by,what):
    try:
           driver.find_element(by = by,value = what)
    except NoSuchElementException:
            return False
    return True

def corporate_dir(account):
        link_,listy_,info = [],[],[]
        #driver = webdriver.Chrome(executable_path = '/Users/macbook/Desktop/BBB/chromedriver')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        driver = webdriver.Chrome(executable_path='/Users/macbook/Desktop/BBB/chromedriver', chrome_options=chrome_options)
        try:
            driver.get("https://corporatedir.com/")
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(text(), 'Welcome Guest')]")))
            element = driver.find_element_by_xpath("//a[contains(text(), 'Welcome Guest')]")
            element.click()
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'LOGIN')]")))
            element = driver.find_element_by_xpath("//*[contains(text(), 'LOGIN')]")
            element.click()
            WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID,"email")))
            driver.find_element_by_id("email").send_keys("pratha.saxena@newgenapps.com")
            driver.find_element_by_id("passsword").send_keys("Prihanna22")
            driver.find_element_by_xpath("//button[@name='login']").click()
        except TimeoutException:
            print("here")
            return info
        except WebDriverException:
            driver.quit()
            return info
        #driver.implicitly_wait(100)
        try:
            WebDriverWait(driver,20).until(EC.invisibility_of_element_located((By.ID,"email")))
            driver.find_element_by_id("search").send_keys(account)
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//button[@name='result']")))
            driver.find_element_by_xpath("//button[@name='result']").click()
        except (TimeoutException,WebDriverException) as e:
            return info
        if is_element_present(driver,By.ID,"myTable"):
            html = driver.page_source
            soup = BeautifulSoup(html,"lxml")
            table = soup.find("table",id ='myTable')
            trs = table.find_all("tr")
            for tr in trs[1:]:
                dict_= {}
                link  = tr.find("a")
                link = re.findall(r'"(.*?)"', str(link))[0].strip()
                #print(link)
                if link.find(account.split(" ")[0].lower()+"-")>-1:
                    link_.append(link)
            #print(listy_)
            for link in link_[0:5]:
                #print(set(link_))
                    details_dict,name,_dict = [],[],{}
                    try:
                        driver.get(link)
                    except Exception:
                        print("connection reset error")
                        continue
                    html = driver.page_source
                    soup = BeautifulSoup(html,"lxml")
                    table = soup.find("table",class_ = "table table-hover table-bordered table-striped")
                    keys = table.find_all("th")
                    values = table.find_all("td")
                    for i in range(0, len(keys)-1):
                        _dict[keys[i].get_text().replace(".","")]= values[i].get_text()
                    #details_dict.append(_dict)
                    details = soup.find("div",class_ = 'panel-body')
                    ps = details.find_all("p")
                    for p in ps:
                        a = p.find_all("a")
                        for a_ in a:
                            name.append(a_.get_text())
                        _dict["name"]=name
                    try:
                        driver.find_element_by_id("contact").click()
                        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'setemail')))
                        email = driver.find_element_by_xpath("//div[@id='setemail']").get_attribute('innerText')
                        _dict["email"] = email.replace("Email - ","")
                    except Exception:
                        continue
                    #print("email",email)
                    info.append(_dict)
        else:
            print("no records present")
        driver.quit()
        return info
