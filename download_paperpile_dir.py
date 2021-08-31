import os
import zipfile
import argparse
import pickle

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
    try:
        if os.path.exists(args.cookies_path):
            driver.get("https://paperpile.com")
            try:
                with zipfile.ZipFile(args.cookies_path, 'r') as zip_cookies:
                    zip_cookies.extractall(path='./', pwd=bytes(args.cookies_pwd, encoding="utf-8"))
                cookies = pickle.load(open(args.cookies_path[:-4], "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.get("https://paperpile.com/app")
                print("Cookies loaded succesfully, no Google login needed!")
                sleep(3)
            except RuntimeError:
                print("Bad password for the zipped pickle. Have you set the right COOKIES_PWD environment variable?")
        else:
            print(f"No cookies or unzip password found. The file should be located at {args.cookies_path} and the --cookies_pwd arg must be specified.")
            raise AttributeError()
    except (AttributeError, RuntimeError):
        print("Problem with loading cookies. I'll try to login on Google manually, but if this fail you'll have to relogin locally on a Google-recognized PC.")
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
        print("Google login succesful!")
        sleep(2)
        pickle.dump( driver.get_cookies() , open(args.cookies_path[:-4],"wb"))
        with zipfile.ZipFile(args.cookies_path, 'w') as zip:
            zip.write(args.cookies_path[:-4])
            if args.cookies_pwd is not None:
                zip.setpassword(bytes(args.cookies_pwd, encoding="utf-8"))
        print(f'Saving pickled cookies to {args.cookies_path}...')
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
    sleep(3)
    print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download a folder from Paperpile in CSV format'
    )
    parser.add_argument("--username", type=str, help="Google email associated to Paperpile account")
    parser.add_argument("--password", type=str, help="Password associated to Paperpile account")
    parser.add_argument("--folder_id", type=str, help="Paperpile folder id (Found by inspecting the page and getting the id of the corresponding div)")
    parser.add_argument("--cookies_path", type=str, default="cookies.pkl.zip", help="Path to the password-protected .zip file containing the cookies in pkl format")
    parser.add_argument("--cookies_pwd", type=str, default=None, help="Password to unzip the cookies zipped file")
    args = parser.parse_args()
    main(args)