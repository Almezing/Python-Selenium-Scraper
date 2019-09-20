"""
    Use update_chromedriver(download_path, current_exe_path="") to update the
    chromedriver to the current version of chrome installed.

    *NOTE* As long as the directory containing the Version Number continues
    to exist within C:\\ProgramFiles (x86)\\Google\\Chrome\\Application\\

    2019 Quest Global Digital Solutions
"""
# Standard Library Imports
import os
import re
import urllib
import hashlib
import datetime as dt
import zipfile as zf
import xml.etree.ElementTree as et

# External Imports
import requests
import logging


def get_proxy_dict():
    """
        Get the Proxy dictionary of the `http` and `https` protocols.

        :return: dict<str -> str>: Return a dictionary that returns the map of `http`
            and `https` string to the proxy string which is the url of the proxy.
    """
    http_proxy = "http://zs-servproxy.utc.com:80"
    https_proxy = "https://zs-servproxy.utc.com:80"
    proxy_dict = {"http": http_proxy, "https": https_proxy}
    return proxy_dict


def prepare_urllib_proxy():
    """
        Prepare the urllib request proxy by calling the appropriate methods.

        :return: A string containing success or an error message
            - Currently only 2 different return values `CDUProxyInstalled` or `CDUFailed`
    """
    # Try to setup proxy for urllib as well
    try:
        proxies = urllib.request.ProxyHandler(get_proxy_dict())
    except Exception as error:
        thing_to_print = "CDU: Error {} | Failed to create urllib.request.ProxyHandler".format(
            error
        )
        logging.warning(thing_to_print)
        return "CDUFailed"

    try:
        opener = urllib.request.build_opener(proxies)
    except Exception as error:
        thing_to_print = "CDU: Error {} | Failed to create urllib.request.build_opener for proxies".format(
            error
        )
        logging.warning(thing_to_print)
        return "CDUFailed"

    try:
        urllib.request.install_opener(opener)
    except Exception as error:
        thing_to_print = "CDU: Error {} | Failed to urllib.request.install_opener for opener".format(
            error
        )
        logging.warning(thing_to_print)
        return "CDUFailed"

    # Return success if everything has passed.
    return "CDUProxyInstalled"


def update_chromedriver(download_path, current_exe_path=""):
    """
        Get the version of chromedriver that matches the current version of chrome.
        Must be after version 73.#.# because of the way that names used to called (ie. 2.46).

        Checks the MD5 of the current exe and the newly downloaded exe, if they are different
        then the download was a success.

        :param download_path: str: the path that you want the new exe to download to.
        NOTE: The file is actually downloaded to `C:\\Users\\<Username>\\Downloads` and then
        removed after it is extracted to the `download_path` provided.

        :param current_exe_path: str: the full path to the location of the current chromedriver
        exe.  By default the value is ''
        NOTE When left with the default value, the exe will just be copied to the `download_path`
        provided.

        :return: return `CDUSuccess` or `CDUFailed` depending on run.
    """
    # ################################################################################################
    # CONSTANTS
    # ################################################################################################
    URL = "https://chromedriver.storage.googleapis.com"
    DL_PATH = f"C:\\Users\\{os.environ['USERNAME']}\\Downloads\\"

    # ################################################################################################
    # UTILITY FUNCTIONS
    # ################################################################################################
    def get_chrome_version():
        """
            Get the chrome version from a file contianed in the same directory.
            This is the currently installed version of chrome.

            If the function can not find the version file, it will return None.

            :return chrome_version: str: the string of the chrome version.
        """
        chrome_exe_path = (
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        )

        app_dir = None
        if os.path.isfile(chrome_exe_path):
            # Get the list of the files in the Folder that contains `chrome.exe`
            app_dir = os.listdir(chrome_exe_path.replace("\\chrome.exe", ""))
        else:
            thing_to_print = "CDU: Couldn't find chrome executable at this path -> {}".format(
                chrome_exe_path
            )
            logging.warning(thing_to_print)
            return None

        # If the Application Directory is not None
        if app_dir:
            version_file_list = [
                file
                for file in app_dir
                if re.search(r"[0-9]{1,}.[0-9]{1,}.[0-9]{1,}", file)
            ]
            if version_file_list:
                version_file = ".".join(version_file_list[0].split(".")[:-1])
                return version_file
        return None

    def get_chromedriver_api_versions(version):
        """
            Get the `chromedriver` version that matches the version file of chrome.

            :param chrome_version: the version that is found from the get_chrome_version
            function.
        """
        url_request = requests.get(URL, proxies=get_proxy_dict())

        response_text = None

        if url_request.status_code is 200:
            response_text = url_request.text

        chromedriver_dl_versions = []
        if response_text:
            elem_tree = et.fromstring(response_text)
            for child in elem_tree:
                for elem in child:
                    if version in elem.text and "win32" in elem.text:
                        chromedriver_dl_versions.append(elem.text)
        if chromedriver_dl_versions:
            return chromedriver_dl_versions[-1]
        else:
            return None

    def md5(fname):
        """
            Perform an MD5 Checksum on the filepath provided.
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def exit_if_downloaded_in_past_day(dl_path, ce_path):
        """
            Exit the program with a success if a chromedriver can be found that
            has been downloaded in the past day.

            :param dl_path: str: path to download the chromedriver to go to.

            :param ce_path: str: default '': the full path to the chromedriver that
            is being replaced. If left blank the file is simply downloaded to the dl_path.

            :return: return `CDUSuccess` or `None` depending if the file has been
            downloaded already in the past day.
        """
        past_one_day = dt.datetime.now() - dt.timedelta(days=1)

        if ce_path != "" and os.path.isfile(ce_path):
            cur_mod_time = dt.datetime.fromtimestamp(os.path.getmtime(ce_path))
            # If the current modify time is older than past one day
            if cur_mod_time < past_one_day:
                return None

        # If there is no given chromedriver then check the download path for a
        # previously downloaded file.
        if not dl_path.endswith("\\"):
            dl_path += "\\"
        downloaded_file_path = dl_path + "chromedriver.exe"
        if os.path.isfile(downloaded_file_path):
            cur_mod_time = dt.datetime.fromtimestamp(
                os.path.getmtime(downloaded_file_path)
            )
            # If the current modify time is older than past one day
            if cur_mod_time < past_one_day:
                return None
        else:
            return None 
        return "Success"

    # ################################################################################################

    # Before running any other code, see when the last time the driver was downloaded
    # and exit with success if it is on the same day
    if current_exe_path != "":
        result_of_exit = exit_if_downloaded_in_past_day(download_path, current_exe_path)
        if result_of_exit:
            return "CDUSuccess"

    # Get the md5 checksum of the executable before
    OLD_EXE_PATH_MD5 = None
    new_path_name_current_exe = ""
    if os.path.isfile(current_exe_path):
        OLD_EXE_PATH_MD5 = md5(current_exe_path)
        try:
            # Rename old exe to .old to make sure this works before copying it
            new_path_name_current_exe = current_exe_path + ".old"
            os.rename(current_exe_path, new_path_name_current_exe)
        except Exception as error:
            thing_to_print = "CDU: Error {} | Failed to rename current exe at {} to {}".format(
                error, current_exe_path, new_path_name_current_exe
            )
            logging.warning(thing_to_print)
        thing_to_print = "CDU: Old EXE MD5 -> {}".format(OLD_EXE_PATH_MD5)
        logging.info(thing_to_print)

    # Get the Currently installed chrome version
    version = get_chrome_version()

    # If the version is not none then get the chromedriver api version
    # that matches from the chromedriver api website.
    if version:
        chromedriver_dl_path = get_chromedriver_api_versions(version)
    else:
        logging.warning("CDU: Failed to get currenly installed chrome version")
        return "CDUFailed"

    dl_url = None

    if chromedriver_dl_path:
        dl_url = f"{URL}/{chromedriver_dl_path}"
    else:
        logging.warning("CDU: Could not get download path for the chromedriver")
        return "CDUFailed"

    file_to_dl = f"chromedriver_win32_{version}.zip"

    file_dl_path = DL_PATH + file_to_dl

    proxy_result = prepare_urllib_proxy()
    # If an error occurred return it
    if proxy_result != "CDUProxyInstalled":
        return proxy_result

    if dl_url:
        urllib.request.urlretrieve(dl_url, filename=file_dl_path)

    if not zf.is_zipfile(file_dl_path):
        thing_to_print = "Zip File does not exist at {}".format(file_dl_path)
        logging.warning(thing_to_print)
        return "CDUFailed"

    return_val = None
    with zf.ZipFile(file_dl_path, "r") as zipped:
        if "chromedriver.exe" not in zipped.namelist():
            logging.warning("CDU: Could not find `chromedriver.exe` in zip file.")
            return_val = "CDUFailed"

        if not download_path.endswith("\\"):
            download_path += "\\"
        # This will extract and overwrite any thing with the same name in the path
        # provided below
        current_exe = download_path + "chromedriver.exe"
        try:
            zipped.extract("chromedriver.exe", path=download_path)
        except Exception as error:
            thing_to_print = "CDU: Error -> {} | Failed to extract chromedriver.exe to {}".format(
                error, download_path
            )
            logging.warning(thing_to_print)
            return_val = "CDUFailed"

        if return_val:
            return return_val

    NEW_EXE_PATH = download_path + "\\chromedriver.exe"
    NEW_EXE_PATH_MD5 = None
    if os.path.isfile(NEW_EXE_PATH):
        NEW_EXE_PATH_MD5 = md5(NEW_EXE_PATH)
        thing_to_print = "CDU: New EXE MD5 -> {}".format(NEW_EXE_PATH_MD5)
        logging.info(thing_to_print)

    # Check if they are not None and that they also equal eachother
    if NEW_EXE_PATH_MD5 == OLD_EXE_PATH_MD5 and NEW_EXE_PATH_MD5 and OLD_EXE_PATH_MD5:
        logging.info("CDU: Chromedriver already up to date")
    else:
        logging.info("CDU: Chromedriver successfully updated")

    if os.path.isfile(NEW_EXE_PATH):
        logging.info("CDU: Succesfully Downloaded and extracted chromedriver")
        logging.info("CDU: Removing Temporary Folders and files...")
        if os.path.isfile(file_dl_path):
            try:
                os.remove(file_dl_path)
            except PermissionError:
                thing_to_print = "Could not remove {} | Perhaps it is being used".format(
                    file_dl_path
                )
                logging.warning(thing_to_print)
        if os.path.isfile(new_path_name_current_exe):
            try:
                os.remove(new_path_name_current_exe)
            except PermissionError:
                thing_to_print = "Could not remove {} | Perhaps it is being used".format(
                    file_dl_path
                )
                logging.warning(thing_to_print)
        thing_to_print = "CDU: Succesfully Updated. New chromedriver can be found here: {}".format(
            NEW_EXE_PATH
        )
        logging.info(thing_to_print)

    else:
        thing_to_print = "CDU: New chromedriver is not being found here: {}".format(
            NEW_EXE_PATH
        )
        logging.warning(thing_to_print)
    return "CDUSuccess"
