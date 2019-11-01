# black formattor
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html#adding-files-to-the-bundle
# os.path.dirname(os.path.abspath(__file__))
# https://pyinstaller.readthedocs.io/en/stable/usage.html
# https://brice-v.github.io/docs/BriceVadnaisResume.pdf
# https://www.reddit.com/r/raspberry_pi/comments/dmmdb0/raspberry_pi_nas_setup_build_inside_old_lenovo/
# https://www.reddit.com/r/raspberry_pi/comments/do9h7z/setup_my_home_network_pihole_i_know_the_picture/
# https://blog.cryptoaustralia.org.au/instructions-for-setting-up-pi-hole/
# https://github.com/RIOT-OS/RIOT/releases/tag/2019.10

import time
import os, sys, re
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

start_time = time.time()
# TODO chrome set up
def setup_chrome():
    cwd = str(os.getcwd())
    chromedriver_path = cwd + r"\x\chromedriver.exe"
    options = Options()
    options.add_experimental_option(
        "prefs", {"download.prompt_for_download": False, "safebrowsing.enabled": True}
    )
    options.add_argument("--disable-gpu")
    options.add_extension(f"{cwd}\\x\\ublock.crx")
    options.binary_location = cwd + r"\x\Chromium-77\chrome.exe"
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    return driver


# TODO sign on safely
def signon(wd):
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
    # quit()


def csv_download(wd=None):
    wd.get(
        "https://mint.intuit.com/transactionDownload.event?accountId=0&queryNew=&offset=0&comparableType=8"
    )
    print("Downloading")
    file_handler()


# TODO download file
def file_handler(data=None, account_name=None):
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
        # print(f"File downloaded {download_file} ")
        if "transaction" not in download_file:
            # print("Downloaded file not found or moved")
            pass
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
                # print(f"Unable to move {download_file}")
                pass

    except:
        print("Fail to download")
    if data != None:
        pattern = re.compile(r"""[^A-z\s\d][\\\^]?""")
        new_name = (pattern.sub("", account_name)).replace(" ", "-")
        dump_file = f"{cwd}\\x\\dumpfolder\\{new_name}.dump"
        try:
            pickle.dump(data, open(dump_file, "wb"))
            print(f"Object saved: \t '{new_name}'")
        except:
            print(f"Failed to save object: \t '{new_name}''")
    else:
        print("Data file skipped")


# TODO scraper
def gather_accounts(wd):
    wd.get("https://mint.intuit.com/transaction.event")
    account_text = []
    account_link = []
    account_text_link = {}
    time.sleep(4)
    count = 0
    try:
        for listitem in wd.find_elements_by_xpath(
            r"""/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[1]/div/div/ul/li[position()<3]"""
        ):
            temp_type = []
            temp_account = []
            temp_account_info = []

            temp_account = [
                item.text for item in listitem.find_elements_by_xpath(".//ul/li/a")
            ]
            temp_account_info = [
                item.text for item in listitem.find_elements_by_xpath(".//ul/li/small")
            ]

            if len(temp_account_info) != 0:
                temp_type = list(zip(temp_account, temp_account_info))
                for item in temp_type:
                    a, b = item
                    # account_text.append(str(count) + "-" + a + " " + b)
                    account_text.append(f"{str(count)} {a} {b}")
                    count = count + 1
                    # print(account_text[-1:])
            else:
                for item in temp_account:
                    account_text.append(f"{str(count)} {item}")
                    count = count + 1

            account_link.extend(
                [
                    item.get_attribute("href")
                    for item in listitem.find_elements_by_xpath(".//ul/li/a")
                ]
            )
            account_text_link = {
                key: value for key, value in zip(account_text, account_link)
            }
    except:
        print("Fail to get accounts and links")
        return {}

    print("Have accounts and links")
    # ic(account_text_link)
    return account_text_link


# TODO aggergate data
def aggergate_data(wd=None):
    all_header = {}
    all_data = {}
    # wd.get("https://mint.intuit.com/transaction.event")
    # time.sleep(3)
    accounts_info = gather_accounts(wd)
    try:
        if len(accounts_info) != 0:
            for account_name, account_url in accounts_info.items():
                temp = {}
                wd.get(account_url)
                time.sleep(1)
                all_header[account_name] = get_header(wd)
                temp[account_name] = scrap_info(wd, account_url)
                all_data.update(temp)

                file_handler(temp, account_name)
    except:
        print("Fail to run for loop")
        signoff(wd)
        return None

    print("Done aggergate")
    return all_data


# TODO
def get_header(wd=None):
    header = []
    time.sleep(2)
    try:
        table = wd.find_elements_by_xpath(
            "/html/body/div[3]/div[5]/div/div[1]/div[7]/div[2]/div[7]/div[2]/div/table/tbody/tr/td[2]/div[3]/div[5]/div[2]/table/tbody/tr/*[position()<3]"
        )
        for item in table:
            if len(item.text) != 0:
                header.append(item.text)
        # print(header)
        return header
    except:
        print("Fail to get header")
        return None


def close_crap(wd=None):
    xpath_path = [
        '//*[@id="product-view-root"]/div[7]/div[3]/a',
        '//*[@id="body-mint"]/div[7]/div[2]/div/img',
    ]
    count = 0
    for item in xpath_path:
        try:
            wd.find_element_by_xpath(item).click()
            count = count + 1
            # print(f"Closed {count} element(s)")
        except:
            pass


def get_last_page(wd=None, xpath_list=None):
    try:
        last_page = wd.find_element_by_xpath(xpath_list[1])
        last_page_text = last_page.text
        if last_page_text.lower() == "last":
            time.sleep(3)
            try:
                last_page.click()
                time.sleep(2)
                last_page = wd.find_element_by_xpath(xpath_list[1])
                last_page_text = last_page.text
            except:
                pass
        else:
            last_page = wd.find_element_by_xpath(xpath_list[2])
            last_page_text = last_page.text

        print(f"{last_page_text} Pages")
        return last_page_text
    except:
        # print("Fail to get last page")
        return None


# TODO separate scrape
def scrap_info(wd=None, url=None):
    data_dump = []
    xpath_list = [
        '//*[@id="transaction-list-body"]',
        '//*[@id="transaction-paging"]/li[last()]',
        '//*[@id="transaction-paging"]/li[@class="next wide"]',
    ]
    close_crap(wd)
    check_table = None
    last_page_text = None
    try:
        check_table = wd.find_element_by_xpath(xpath_list[0])
    except:
        pass

    if check_table != None:
        try:
            last_page_text = get_last_page(wd, xpath_list)
            try:
                pages = int(last_page_text)
            except:
                pages = int(
                    wd.find_element_by_xpath(
                        '//*[@id="transaction-paging"]/li[last()-1]'
                    ).text
                )
        except:
            pages = 1
            pass

        wd.get(url)
        time.sleep(3)
        close_crap(wd)
        start = time.time()
        date = []
        title = []
        cat = []
        money = []
        pages = pages + 1
        try:
            for page in range(1, pages):
                table = wd.find_elements_by_xpath(xpath_list[0])
                for row in table:
                    date = [
                        td.text
                        for td in row.find_elements_by_xpath(".//td[@class='date'][1]")
                    ]
                    title = [
                        td.text for td in row.find_elements_by_xpath(".//td[@title]")
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
                data_dump.extend(temp)
                elapse = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
                print(
                    f"Current page {page} returned {len(date), len(title), len(cat), len(money)}. Elapse Time {elapse}s"
                )
                try:
                    next_page = wd.find_element_by_xpath(xpath_list[2])
                    next_page.click()
                except:
                    pass
            # data_dump = clean_data(data_dump)
            # print(data_dump[0])
            print(f"Total Time {elapse}")
            return data_dump
        except:
            return None
    else:
        return None


# TODO data consolidate to xl
def data_to_xl(data=None):
    try:
        wb2 = xw.Book(str(os.getcwd()) + r"\x\transaction.csv")
        sht2 = wb2.sheets[0]
        wb1 = xw.Book(str(os.getcwd()) + r"\x\template.xlsx")
        sht1 = wb1.sheets[0]
        # labels = ["Index", "Date", "Description", "Category", "Amount"]
        # for page in range(0, len(data)):
        #     df = pd.DataFrame(data[page])
        #     df.columns = df.iloc[0]
        #     df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        #     df.columns.name = None
        #     df.index.name = None
        #     row = page * 100 + 2
        #     sht1.range(f"A{row}").value = df
        # sht1.range("A1").value = labels

        # get data from csv
        table_total_range = sht2.range("A1").expand()
        table_sht2 = sht2.range(table_total_range).value
        table_section_range1 = sht2[:, 0:4]
        table_section_range2 = sht2[:, 5:9]

        table_section_1 = sht2.range(table_section_range1).value
        table_section_2 = sht2.range(table_section_range2).value

        # write data
        new_locaiton_range = sht1[:, 5:10]
        insert_range = sht1[1:, 4]
        sht1.range("A1").value = table_section_1
        sht1.range(insert_range).options(transpose=True).value = data
        sht1.range(new_locaiton_range).value = table_section_2
        sht1.range("e1").value = "Signed Amount"

    except:
        print("Data is None")
        pass

    try:
        wb1 = xw.Book(str(os.getcwd()) + r"\x\template.xlsx")
        sht1 = wb1.sheets[0]
    except:
        pass


def clean_data(data=None):
    clean_data = []
    try:
        for page in data:
            for row in page:
                # clean_data.append(row)
                clean_data.append(row[3])
        return clean_data
    except:
        print("Data not cleaned")
        return None

def main():
    with setup_chrome() as wd:
        signon(wd)
        # csv_download(wd, url_path)
        data = aggergate_data(wd)

        try:
            pickle.dump(data, open(dump_file, "wb"))
            print(f"Object saved: \t data")
        except:
            print(f"Failed to save object: \t data")

        signoff(wd)

        # data_to_xl(data)


if __name__ == "__main__":
    print(__name__)
    main()
print(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
