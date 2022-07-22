import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.support.ui import Select

from config import *
from constants import *
from utils import *


def findElement(driver, elementXpath, elementName):
    pageTimer = 0
    while 1:
        try:
            element = driver.find_element_by_xpath(elementXpath)
            myLogger.info(f"Succeded to find the element {elementName}")
            return element
        except (NoSuchElementException, ElementNotInteractableException):
            myLogger.info(f"Looking for the element: {elementName}")
        except (WebDriverException):
            myLogger.info(f"Failed to reach webDriver")
        if pageTimer > PAGE_TIMEOUT:
            myLogger.info("Failed to load the page withim limit")
            return False

        pageTimer += 1
        time.sleep(1)


def clickElement(element, elementName):
    pageTimer = 0
    while 1:
        if element.is_enabled():
            try:
                element.click()
                myLogger.info(f"Succeded to click {elementName}")
                return True
            except (ElementNotInteractableException):
                myLogger.info(f"Element:{elementName} is not Interactable yet")
                pass
            except (WebDriverException):
                myLogger.info(f"Failed to reach webDriver")

            except (WebDriverException):
                myLogger.info(f"Failed to reach webDriver")
        if not element.is_enabled():
            myLogger.info(f"waiting for the element:{elementName} to be enabled")
        if pageTimer > PAGE_TIMEOUT:
            myLogger.info(f"Failed to enable the element:{elementName} within the limit")
            return False

        pageTimer += 1
        time.sleep(1)


def selectValue(element, elementName, elementValue):
    pageTimer = 0
    while 1:
        try:
            Select(element).select_by_value(elementValue)
            myLogger.info(f"Succeded to select value: {elementValue}")
            return True
        except (NoSuchElementException, ElementNotInteractableException):
            myLogger.info(f"Looking for the element: {elementName}")
        except (WebDriverException):
            myLogger.info(f"Failed to reach webDriver")
        if pageTimer > PAGE_TIMEOUT:
            myLogger.info(f"Failed to enable the element:{elementName} within the limit")
            return False
        pageTimer += 1
        time.sleep(1)


def findAndSelectElement(driver, elementXpath, elementName, elementValue):
    element = findElement(driver, elementXpath, elementName)
    time.sleep(2)
    if element:
        return selectValue(element, elementName, elementValue)
    else:
        return False


def findAndClickElement(driver, elementXpath, elementName):
    element = findElement(driver, elementXpath, elementName)
    time.sleep(2)
    if element:
        return clickElement(element, elementName)
    else:
        return False


def getHomePage(driver):
    try:
        driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en")
        myLogger.info("Main page is succeed to request")
        time.sleep(1)
        return True
    except:
        myLogger.info("Main page is failed  to request")
        return False


def clickBookAppointmentButton(driver):
    # Click to Book appointment
    elementXpath = '//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a'
    elementName = "book appointment button"
    return findAndClickElement(driver, elementXpath, elementName)


def clickAcceptTermsCheckbox(driver):
    elementXpath = '//*[@id="xi-cb-1"]'
    elementName = "accept terms checkbox"
    return findAndClickElement(driver, elementXpath, elementName)


def clickAcceptTermsButton(driver):
    elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
    elementName = "accept terms button"
    return findAndClickElement(driver, elementXpath, elementName)


def setCitizenship(driver):
    """ "
    set the country from the dropdown menu
    """
    elementXpath = '//*[@id="xi-sel-400"]'
    elementName = "Citizenship"
    return findAndSelectElement(driver, elementXpath, elementName, "163")


def setApplicantsNumber(driver):
    """ "
    set the Number of applicants who need a residence title (inluding foreign spouse and children)
    """
    elementXpath = '//*[@id="xi-sel-422"]'
    elementName = "Applications Count"
    return findAndSelectElement(driver, elementXpath, elementName, "1")


def setFamily(driver):
    elementXpath = '//*[@id="xi-sel-427"]'
    elementName = "Family member"
    return findAndSelectElement(driver, elementXpath, elementName, "2")


def setVisaGroup(driver):
    elementXpath = '//*[@id="xi-div-30"]/div[1]/label/p'
    elementName = "set visa group"
    return findAndClickElement(driver, elementXpath, elementName)


def setVisaType(driver):
    elementXpath = '//*[@id="inner-163-0-1"]/div/div[3]/label'
    elementName = "set visa type"
    return findAndClickElement(driver, elementXpath, elementName)


def setBlueCard(driver):
    elementXpath = '//*[@id="SERVICEWAHL_EN163-0-1-1-324659"]'
    elementName = "click blue card"
    return findAndClickElement(driver, elementXpath, elementName)


def setWorkingPermit(driver):
    elementXpath = '//*[@id="SERVICEWAHL_EN163-0-1-1-324659"]'
    elementName = "click blue card"
    return findAndClickElement(driver, elementXpath, elementName)


def setQualifiedSkilledWithAE(driver):
    # Click to Book appointment
    elementXpath = '//*[@id="SERVICEWAHL_EN163-0-1-1-329328"]'
    elementName = "qualifiedSkilled"
    return findAndClickElement(driver, elementXpath, elementName)


def clickNext(driver):
    elementXpath = '//*[@id="applicationForm:managedForm:proceed"]'
    elementName = "next button"
    return findAndClickElement(driver, elementXpath, elementName)


def handleError(driver: Chrome):
    # Check Error Message
    pageTimer = 0
    elementXpath = (
        "/html/body/div[2]/div[2]/div[4]/div[2]/form/div[2]/div/div[2]/div/div[1]/div[3]/div[1]/fieldset/legend"
    )
    while 1:
        try:
            loader = driver.find_element_by_id("j_idt440")
            hidden = loader.get_attribute("aria-hidden")
            # Loader animation is there
            if hidden == "false":
                raise NoSuchElementException("Loader not completed yet")

            element = driver.find_element_by_class_name("antcl_wizardSteps")
            date_selection = element.find_element_by_xpath(".//ul/li[3]")
            elem_class = date_selection.get_attribute("class")

            # If the 3rd element in the top navigation bar is active
            if pageTimer > PAGE_TIMEOUT:
                myLogger.info("Failed to load the page withim limit")
                return False
            elif elem_class != "antcl_active":
                myLogger.info(f"No appointment, starting to process again in {TIMEOUT} seconds ...")
                time.sleep(TIMEOUT)
                return False
            else:
                sourceHtml = driver.page_source
                url = driver.current_url
                import webbrowser

                webbrowser.open(url)
                f = open("source-" + str(randint(1, 100)) + ".html", "w")
                f.write(sourceHtml)
                f.close
                makeCall()
                myLogger.info("FOUND IT")
                return True
        except (NoSuchElementException, ElementNotInteractableException) as e:
            print(e)
            myLogger.info("Page is loading")
        except (UnexpectedAlertPresentException):
            myLogger.warn("Someproblem happend ")
            return True
        except (WebDriverException):
            myLogger.error("Error on finding the driver")
            pass

        time.sleep(1)
        pageTimer += 1


def setDriver():
    op = webdriver.ChromeOptions()
    # op.add_argument("--headless")
    driver = webdriver.Chrome(options=op)

    return driver


if __name__ == "__main__":

    driver = setDriver()
    while 1:
        driver.quit()
        driver = setDriver()

        if not getHomePage(driver):
            continue
        if not clickBookAppointmentButton(driver):
            continue
        if not clickAcceptTermsCheckbox(driver):
            continue
        if not clickAcceptTermsButton(driver):
            continue

        if not setCitizenship(driver):
            continue
        if not setApplicantsNumber(driver):
            continue
        if not setFamily(driver):
            continue

        if not setVisaGroup(driver):
            continue
        if not setVisaType(driver):
            continue

        if not setBlueCard(driver):
            continue

        if not clickNext(driver):
            continue

        if not handleError(driver):
            continue

        time.sleep(TIMEOUT)

# To do
# After selecting make sure it is done by reading back again the value citizenship example sometimes doesn't select Turkey. Repeat it until is succeeds.
