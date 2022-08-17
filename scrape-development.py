from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import time

# save current time to watch how much time it took to complete task
start_time = time.time()

print('Traversing throughout the internet. Keep patience...')

options = Options()

# true if you don't went to pop up the GUI (Chrome window in this case)
options.headless = True
# don't close GUI upon completing the code
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.get('https://www.myhome.ge/ka/s/iyideba-bina-Tbilisi?Keyword=%E1%83%97%E1%83%91%E1%83%98%E1%83%9A%E1%83%98%E1%83%A1%E1%83%98&AdTypeID=1&PrTypeID=1&mapC=41.73188365%2C44.8368762993663&regions=687611312.687586034.688137211.687602533.687618311.-1&districts=26445359.2022621279.58873656.1651252654.737816010.2172993612.28045012.737261604.152296216&cities=1996871&GID=1996871')
last_page = driver.find_elements(By.XPATH, '//li[@class="page-item number space-item-last"]/a[@class="page-link"]')[0].text
forward_button = ''
search_keywords = [
    'saswrafod',
    'saswrafot',
    'sastsrafod',
    'sastsrafot',
    'mechqareba',
    'mechkareba',
    'sachqarod',
    'sachkarod',
    'sachqarot',
    'sachkarot',
    'სასწრაფოთ',
    'სასწრაფოდ',
    'მეჩქარება',
    'საჩქაროთ',
    'საჩქაროდ'
]

# workaround for .click() method. Since that method didn't work. My guess is the website tries to block crawlers
# so this solution is also viable
def click(element):
    driver.execute_script("arguments[0].click();", element)

# you can use any condition here
def condition_check(price, sqm, floor=4):
    cond1 = price < 1700
    cond2 = sqm > 90
    cond3 = floor > 3
    return (cond1 & cond2 & cond3)

# you can use any condition here
def keyword_check(text):
    for key in search_keywords:
        if key in text:
            return True
    return False

# here I check all cards on provided website and if all my conditions are met
# each card I open in new tab and check on my condition functions above
# in case of success I write the tab link in a file and close the tab
# playsound is library for music player
# if you use playsound part here make sure to install 'PyObjC' package as well
def check_perform():
    cards = driver.find_elements(By.XPATH, '//div[@class="statement-card"]/a[@class="card-container"]')

    for card in cards:
        click(card)
        driver.switch_to.window(driver.window_handles[1])

        price_elem = driver.find_elements(By.XPATH, '//div[@class="price_icons_wrap d-flex align-items-end justify-content-between"]/span[@class="d-block price-per-square"]/span[@class="convertable"]')
        sqm_elem = driver.find_elements(By.XPATH, '//div[@class="main-features row no-gutters"]/div[@class="col-6 col-lg-4 mb-0 mb-md-4 mb-lg-0 d-flex align-items-center mb-lg-0 mb-4 pr-2 pr-lg-0"]//span[@class="d-block"]')
        desc_elem = driver.find_elements(By.XPATH, '//p[@class="pr-comment translated"]')

        if (price_elem and price_elem[0]):
            price = int(price_elem[0].text)
        else:
            price = 99999999
        if (sqm_elem and sqm_elem[0]):
            sqm = int(sqm_elem[0].text[:-6])
        else:
            sqm = 0
        if (desc_elem and desc_elem[0]):
            desc = desc_elem[0].text
        else:
            desc = ''

        if (keyword_check(desc)):
            # it's always good to provide absolute paths
            # which I didn't do XD
            with open('appartment-info.txt', 'a') as f:
                f.write('\n'+driver.current_url)
                playsound('/Users/nika/Documents/Music/Sounds/notification_sound.mp3')
        # closing tab
        driver.close()
        # by the rules of this program there can only be two tabs
        # but when we close the second tab driver doesn't automatically switch target
        # to previous tab. Need to set it manually
        driver.switch_to.window(driver.window_handles[0])

# since there is a pagination we want to run through all the pages
# and wait for 20s to make sure ajax loaded the content
for page in range(int(last_page)):
    forward_button = driver.find_elements(By.XPATH, '//li[@class="page-item step-forward-item"]/a[@class="page-link step-forward active-step"]')[0]
    check_perform()
    click(forward_button)
    time.sleep(20)


print('Process ended. Check the output file!')

# upon ending the code running show how much time it took to complete all the work
print("--- %s seconds ---" % (time.time() - start_time))