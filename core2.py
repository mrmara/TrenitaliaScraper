import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from mytelegram import bot
from selenium.webdriver.common.by import By
import warnings
from datetime import datetime
from param2 import *
warnings.filterwarnings("ignore", category=DeprecationWarning)
hless = True
restTime=5 #seconds
cycleTime=60 #seconds
notification=60 #minutes
cnt=0

def init():
    print("Initializing...")
    options = webdriver.FirefoxOptions()
    #options = webdriver.ChromeOptions()
    if hless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    #options.add_argument('window-size=1200x600')
    return driver
def calculateMonthDif():
    if datetime.now().year==year:
        return month-datetime.now().month
    if datetime.now().year<year:
        return 12-datetime.now().month+month
def searchTrain(driver):
    driver.get("https://www.trenitalia.com/")
    assert "Trenitalia" in driver.title
    depStat = driver.find_element_by_name("departureStation")
    print("Departure Station found")
    depStat.clear()
    depStat.send_keys(DepartureStation)
    depStat.send_keys(Keys.RETURN)
    arrStat = driver.find_element_by_name("arrivalStation")
    print("Arrival Station found")
    arrStat.clear()
    arrStat.send_keys(ArrivalStation)
    arrStat.send_keys(Keys.RETURN)
    calendar = driver.find_element_by_name("departureDateVISIBLE")
    print("Date found")
    calendar.click()
    dif=calculateMonthDif()
    for i in range(0,dif-1):
        nxtMonthButt = driver.find_element(By.ID,"ui-datepicker-div").find_element(By.CLASS_NAME,"ui-datepicker-group-last").find_element(By.CLASS_NAME,"ui-datepicker-header").find_element(By.CLASS_NAME,"ui-datepicker-next")
        print("Next month found")
        nxtMonthButt.click()
    date = driver.find_element(By.ID,"ui-datepicker-div").find_element(By.CLASS_NAME,"ui-datepicker-group-last").find_element(By.CLASS_NAME,"ui-datepicker-calendar").find_elements(By.TAG_NAME,"td")
    for dat in date:
        if int(dat.text)==day:
            print("Date found")
            dat.click()
            break
    depTime = driver.find_element_by_id("biglietti_ora_p")
    print("Time found")
    Select(depTime).select_by_value(hr)
    passenger = driver.find_element_by_id("biglietti_adulti")
    print("Passengers found")
    passenger.click()
    plus = driver.find_element_by_id('addAdult')
    print("Number of passengers found")
    plus.click()
    go = driver.find_element_by_xpath("/html/body/div[5]/form/div/div[3]/div[2]/div[6]/button")
    print("Search found")
    go.click()
    return 0

def getTrainList(driver):
    l =[]
    i=0
    while True:
        try:
            l.append(driver.find_element(By.ID, 'travelSolution'+str(i)))
            i+=1
        except NoSuchElementException:
            print("Solutions extracted: "+str(i-1))
            break
    if i!=0:
        return l
    else:
        return -1

def getTimes(solutions):
    d=[]
    for train in solutions:
        index = str(solutions.index(train))
        try:
            print("Searching times for solution "+index)
            hr=train.find_element(By.ID,"deptTime_"+index).get_attribute("value")
            ch=train.find_element(By.CLASS_NAME,"table-solution-hover").find_element(By.CLASS_NAME,"solutionRow").find_element(By.CLASS_NAME,"trainOffer").find_element(By.CLASS_NAME,"descr").text
            d.append(str(hr)+"_"+str(ch))
        except NoSuchElementException:
            print("Error in getting times or changes")
            return -1
    for dd in d:
        if "*" in dd:
            d.remove(dd)
    return d

def inform(mybot,message):
    mybot.send(message)

if __name__ == "__main__":
    mybot = bot("AntonioMarangi"+id)
    lastTimes=0
    while True:
        try:  
            t = time.time()     
            driver = init()
            print("Inizialized")
            res = searchTrain(driver)
            if res!=0:
                raise Exception
            Trains = getTrainList(driver)
            if Trains==-1:
                raise Exception
            Times = getTimes(Trains)
            if Times==-1:
                raise Exception
            if len(Times)!=lastTimes:
                lastTimes=len(Times)
                inform(mybot,str(Times))
                print("Informing")
            if cnt==notification:
                inform(mybot,str(Times))
                cnt=0
                print("Informing")
            driver.close()
            elapsed = time.time()-t
            print("Elapsed: "+str(elapsed))
            cnt+=1
            print("Iteration: "+str(cnt))
            time.sleep(cycleTime-elapsed)
        except Exception:
            print("error: END")
            time.sleep(restTime)


