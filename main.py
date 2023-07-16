import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config

LOGIN = config('LOGIN')
PSWRD = config('PASSWORD')
 
options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://read.amazon.com/notebook?ref_=kcr_notebook_lib&language=en-US')

def loginAmazon(email, password):
  login = driver.find_element(By.ID,'ap_email')
  login.send_keys(email)
  login = driver.find_element(By.ID,'ap_password')
  login.send_keys(password)
  login = driver.find_element(By.ID,'signInSubmit').click()

def collectBookQuotes():
  highlightsList = []
  books = driver.find_elements(By.TAG_NAME,'h2')
  # Create an dictionary for each book
  for book in books:
    quoteObject = {
      'book': book.text,
      'text': ""
    }
    book.click()
    WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.TAG_NAME,'h3')))
    quotesElements = driver.find_elements(By.ID,'highlight')
    # Create a list with all book's quotes
    for quote in quotesElements:
      divElement = quote.find_element(By.XPATH, '..')
      quoteObject = {
        'book': book.text,
        'text': quote.text,
        'quoteId': divElement.id
      }
      highlightsList.append(quoteObject)
  return highlightsList

def printQuotes(highlightsList):
  for quoteObj in highlightsList:
    print("\"" + quoteObj['text'] + "\" - " + quoteObj['book'] + " - (" + quoteObj['quoteId'] + ")")
    print("------------------------------\n")

def exportJSON(highlightsList):
  with open("highlights.json","w") as outfile:
    json.dump(highlightsList, outfile)

loginAmazon('danielbcuadros@gmail.com', PSWRD)

wait = WebDriverWait(driver,50)
element = wait.until(EC.visibility_of_element_located((By.TAG_NAME,'h1')))
highlightsList = collectBookQuotes()

# exportJSON(highlightsList)

printQuotes(highlightsList)
driver.implicitly_wait(10)
driver.close()