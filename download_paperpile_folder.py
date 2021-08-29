import zipfile
import argparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


def change_window(driver):
    p = driver.current_window_handle
    chwd = driver.window_handles
    for w in chwd:
        if(w!=p):
            driver.switch_to.window(w)
            break

def main(args):
    # Extract the Paperpile extension (needed to proceed inside the website)
    with zipfile.ZipFile('paperpile.zip', 'r') as zip_ref:
        zip_ref.extractall('./')

    # Setup Chrome Driver
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument('--disable-dev-shm-using')
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--load-extension=paperpile')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    )
    driver = uc.Chrome(options=chrome_options)

    # Google Login
    driver.get('https://paperpile.com/app')
    driver.find_element_by_name("identifier").send_keys(args.username)
    WebDriverWait(driver, 10).until(element_to_be_clickable(
        (By.XPATH, "//*[@id='identifierNext']/div/button/span"))).click()
    driver.implicitly_wait(4)

    driver.find_element_by_name("password").send_keys(args.password)
    WebDriverWait(driver, 10).until(element_to_be_clickable(
        (By.XPATH, "//*[@id='passwordNext']/div/button/span"))).click()
    driver.implicitly_wait(4)
    sleep(4)

    # Navigate to link and download CSV
    action = ActionChains(driver)
    element = driver.find_element(by=By.ID, value=args.folder_id)
    action.move_to_element(element).perform()
    toggle = driver.find_element(by=By.ID, value="treeHoverMenu-1099")
    action.move_to_element(toggle).click().perform()
    export_list = driver.find_element(by=By.ID, value="exportCollectionMenuItem-1173-itemEl")
    action.move_to_element(export_list).click().perform()
    export_csv = driver.find_element(by=By.ID, value="menuitem-1177")
    action.move_to_element(export_csv).click().perform()
    sleep(10)
    print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download a folder from Paperpile in CSV format'
    )
    parser.add_argument("--username", type=str, help="Google email associated to Paperpile account")
    parser.add_argument("--password", type=str, help="Password associated to Paperpile account")
    parser.add_argument("--folder_id", type=str, help="Paperpile folder id (Found by inspecting the page and getting the id of the corresponding div)")
    args = parser.parse_args()
    main(args)