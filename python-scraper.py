import time
import os
import pickle
import xlwings as xw
import fileinput as fs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# TODO data consolidate

# TODO chrome set up
def setup_chrome():
    options = Options()
    options.add_experimental_option(
        "prefs", {"download.prompt_for_download": False, "safebrowsing.enabled": True}
    )
    driver = webdriver.Chrome(options=options)
    return driver


# TODO sign on safely
def signon(wd, url_path):
    time.sleep(3)
    form_textfield = ""
    action = ""
    file_path = f"{str(os.getcwd())}\\X\\X.txt"
    xpath_list = [
        '//*[@id="ius-userid"]',
        '//*[@id="ius-password"]',
        '//*[@id="ius-sign-in-submit-btn"]',
    ]
    wd.get(url_path["signon_path"])
    try:
        assert "Sign In" in wd.title
        with fs.input(file_path) as f:
            for line, path in zip(f, xpath_list):
                form_textfield = wd.find_element_by_xpath(path)
                form_textfield.send_keys(line)
        action = wd.find_element_by_xpath(xpath_list[2])
        action.click()
        fs.close()
        form_textfield = ""
        file_path = ""
    except:
        print("Already signed in")
        file_path = ""
        form_textfield = ""
        fs.close()


# TODO sign off safely
def sigoff(wd):
    time.sleep(10)
    try:
        xpath = '//*[@id="link-logout"]'
        action = wd.find_element_by_xpath(xpath)
        action.click()
        print("Signing Off")
    except:
        print("Not logged in")

    time.sleep(2)
    wd.quit()


# TODO download file
def download_handler(wd, url_path):
    time.sleep(5)
    cwd = str(os.getcwd())
    local_download_path = os.path.expanduser("~") + "\\Downloads"
    download_file = ""
    try:
        wd.get(url_path["download_path"])
        print("Downloading")
        time.sleep(5)
        download_file = max(
            [file for file in os.listdir(local_download_path)],
            key=lambda x: os.path.getctime(os.path.join(local_download_path, x)))
        print(f"File {download_file} has been downloaded")
    except:
        print("Fail to download")
    try:
        with open(cwd + "dump", "wb") as f:
            pickle.dump(this, f, pickle.HIGHEST_PROTOCOL)
        print("Object saved")
    except:
        print("Failed to save object")


# TODO scraper
def scape_info(wd, url_path):
    time.sleep(7)
    xpath_list = [
        '//*[@id="account-table-all"]/tr[2]/*',
        '//*[@id="transaction-list-body"]',
        "/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/ul/li[13]",
        "/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/ul/li[12]",
    ]
    header = []
    data_dump = []
    wd.get(url_path["first_page_path"])
    time.sleep(5)
    try:
        for item in wd.find_elements_by_xpath(xpath_list[0]):
            header.append(item.text)
        print(header)
    except:
        print("Fail to get header")
    try:
        xpath = '//*[@id="product-view-root"]/div[7]/div[3]/a'
        time.sleep(3)
        wd.find_element_by_xpath(xpath).click()
        xpath = '//*[@id="body-mint"]/div[8]/div[2]/div'
        time.sleep(3)
        wd.find_element_by_xpath(xpath).click()
    except:
        print("Button missing")
    try:
        last_page = wd.find_element_by_xpath(xpath_list[2])
        print(last_page.text)
        last_page.click()
        time.sleep(5)
        last_page = wd.find_element_by_xpath(xpath_list[3]).text
        print(last_page)
    except:
        print("Fail to get last page")
    try:
        wd.get(url_path["first_page_path"])
        for page in range(1, int(last_page)):
            table = wd.find_elements_by_xpath(xpath_list[1])
            for row in table:
                date = []
                description = []
                cat = []
                amount = []

                date = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='date'][1]")
                ]
                description = [
                    span.text for span in row.find_elements_by_xpath(".//td[@title]")
                ]
                cat = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='cat'][1]")
                ]
                amount = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='money'][1]")
                ]
                temp = list(zip(date, description, cat, amount))

            data_dump.append(temp)
            time.sleep(3)
            next_page = wd.find_element_by_xpath(xpath_list[3])
            print(
                f"Current page {page} returned {len(date), len(description), len(cat), len(amount)} Next page {next_page.text}"
            )
            next_page.click()

            time.sleep(2)

    except:
        print("Fail to run for loop")
        print(data_dump)


def main():
    url_path = {
        "signon_path": "https://accounts.intuit.com/index.html?offering_id=Intuit.ifs.mint&namespace_id=50000026&redirect_url=https%3A%2F%2Fmint.intuit.com%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown",
        "first_page_path": "https://mint.intuit.com/transaction.event#location:%7B%22accountId%22%3A0%2C%22offset%22%3A0%2C%22typeSort%22%3A8%7D",
        "download_path": "https://mint.intuit.com/transactionDownload.event?accountId=0&queryNew=&offset=0&comparableType=8",
    }

    wd = setup_chrome()

    signon(wd, url_path)
    # download_handler(wd, url_path)
    scape_info(wd, url_path)

    time.sleep(10)
    sigoff(wd)


if __name__ == "__main__":
    print(__name__)
    main()
