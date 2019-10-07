import time
import os
import pickle
import xlwings as xw
import pandas as pd
import itertools
import fileinput as fs
from icecream import ic
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# https://www.statworx.com/de/blog/web-scraping-101-in-python-with-requests-beautifulsoup/
# https://kanoki.org/2019/09/25/building-a-web-app-using-python-and-mongodb/
# https://docs.xlwings.org/en/stable/quickstart.html


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
        r"""https://accounts.intuit.com/index.html?offering_id=Intuit.ifs.mint&namespace_id=50000026&redirect_url=https%3A%2F%2Fmint.intuit.com%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown%26ivid%3D93b930db-f416-43a1-933f-fba8db6942ff""",
    ]
    wd.get(xpath_list[3])
    try:
        assert "Sign In" in wd.title
        with fs.input(file_path) as f:
            for line, path in zip(f, xpath_list):
                form_textfield = wd.find_element_by_xpath(path)
                form_textfield.send_keys(line)
        action = wd.find_element_by_xpath(xpath_list[2])
        form_textfield = ""
        file_path = ""
        fs.close()
        action.click()
        start = time.time()
        while "Sign In" in wd.title:
            time.sleep(1)
            elapse = time.time() - start
            print(f"Waiting for {elapse}")
        print("Sign in OK")

    except:
        print("Already signed in or not on correct page")
        file_path = ""
        form_textfield = ""
        fs.close()
        signoff(wd)

    time.sleep(4)


# TODO sign off safely
def signoff(wd):
    time.sleep(3)
    try:
        xpath = '//*[@id="link-logout"]'
        action = wd.find_element_by_xpath(xpath)
        action.click()
        print("Signing Off")
    except:
        print("Not logged in")
    wd.quit()


def csv_download(wd=None, url_path=None):
    wd.get(url_path["download_path"])
    print("Downloading")
    download_handler()


# TODO download file
def download_handler(data=None):
    time.sleep(2)
    cwd = str(os.getcwd())
    local_download_path = os.path.expanduser("~") + "\\Downloads"
    download_file = ""
    try:
        # time.sleep()
        download_file = max(
            [file for file in os.listdir(local_download_path)],
            key=lambda x: os.path.getctime(os.path.join(local_download_path, x)),
        )
        print(download_file)
        if "transaction" not in download_file:
            print("Downloaded file not found or moved")
        else:
            print(f"File {download_file} has been downloaded")
            # TODO Move file
            try:
                os.replace(
                    f"{local_download_path}\\{download_file}",
                    cwd + "\\x\\transaction.csv",
                )
                print("File moved")
            except:
                print(f"Unable to move {download_file}")

    except:
        print("Fail to download")
    if data != None:
        try:
            dump_file = f"{cwd}\\x\\dump"
            with open(dump_file, "wb") as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            print("Object saved")
        except:
            print("Failed to save object")
    else:
        print("Data file skipped")


# TODO scraper
def scape_info(wd, url_path):
    time.sleep(7)
    xpath_list = [
        '//*[@id="account-table-all"]/tr[2]/*',
        '//*[@id="transaction-list-body"]',
        "/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/ul/li[last()]",
        "/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/ul/li[@class='next wide']",
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
        time.sleep(2)
        last_page = wd.find_element_by_xpath(xpath_list[2]).text
        print(last_page)
    except:
        print("Fail to get last page")
        signoff(wd)
        return None
    try:
        wd.get(url_path["first_page_path"])
        start = time.time()
        date = []
        title = []
        cat = []
        money = []
        for page in range(1, int(last_page)):
            table = wd.find_elements_by_xpath(xpath_list[1])
            for row in table:
                date = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='date'][1]")
                ]
                title = [
                    span.text for span in row.find_elements_by_xpath(".//td[@title]")
                ]
                cat = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='cat'][1]")
                ]
                money = [
                    td.text
                    for td in row.find_elements_by_xpath(".//td[@class='money'][1]")
                ]
            temp = itertools.zip_longest(date, title, cat, money)
            data_dump.append(temp)
            elapse = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
            print(
                f"Current page {page} returned {len(date), len(title), len(cat), len(money)}. Elapse Time {elapse}s"
            )
            next_page = wd.find_element_by_xpath(xpath_list[3])
            next_page.click()
            time.sleep(3)
        download_handler(data_dump)
        print(f"Total Time {elapse}")
        return data_dump

    except:
        print("Fail to run for loop")
        signoff(wd)
        return None


# TODO data consolidate
def data_to_xl(data=None):
    wb = xw.Book(str(os.getcwd()) + r"\x\template.xlsx")
    sht = wb.sheets["Sheet1"]
    labels = ["Index", "Date", "Description", "Category", "Amount"]

    for page in range(0, len(data)):
        df = pd.DataFrame(data[page])
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        df.columns.name = None
        df.index.name = None
        row = page * 100 + 2
        sht.range(f"A{row}").value = df

    sht.range("A1").value = labels


def main():
    url_path = {
        "first_page_path": "https://mint.intuit.com/transaction.event#location:%7B%22accountId%22%3A0%2C%22offset%22%3A0%2C%22typeSort%22%3A8%7D",
        "download_path": "https://mint.intuit.com/transactionDownload.event?accountId=0&queryNew=&offset=0&comparableType=8",
    }

    with setup_chrome() as wd:
        signon(wd, url_path)
        csv_download(wd, url_path)
        data = scape_info(wd, url_path)
        signoff(wd)

        data_to_xl(data)


if __name__ == "__main__":
    print(__name__)
    main()
    # data_to_xl()
