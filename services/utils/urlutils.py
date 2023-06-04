'''
    @brief utils submodule component containing the routines for URL specific operations
    @author oldgod
'''

from urllib import request
from logging import info, debug, warn
from platform import architecture, system

def get_url_details(url: str):
    '''
        @brief function to get the url of the page redirected to
        @param url : String containing the source URL which redirects to the final URL
        @return Returns the URL where the source URL provided in the params redirects to
        @author oldgod
    '''
    info("Getting the redirected URL details")
    if not url or len(url) == 0:
        warn("URL provided is not a valid url")
        return None

    redirected_url = request.urlopen(url).geturl()
    debug(f"Final redirected URL : {redirected_url}")
    return redirected_url

def get_latest_default_driver_url(driver_version: str, driver_download_base_url: str) -> str:
    '''
        @brief function to return the URL from which the geckodriver can be downloaded
        @param driver_version : String containing the version of the driver to be downloaded
            driver_download_base_url : String containing the base URL where the version and other 
            platform architecture details will be substituted
        @return Returns the final URL from which the file is to be downloaded
    '''
    # fixme: add the code for returning the right URL
    download_path = ""
    if not driver_version or len(driver_version) == 0:
        warn("Driver version provided is not valid")
        return download_path
    if not driver_download_base_url or len(driver_download_base_url) == 0:
        warn("Driver download base URL is not valid")
        return download_path

    info("Preparing the webdriver final download path")

    platform_arch = f"{system().lower()}{architecture()[0][0:2]}"
    debug(f"geckodriver for system : {platform_arch}")
    # fixme: for now it has been hardcoded as this since I am targetting the Linux platform only
    compression = "tar.gz"
    download_path = driver_download_base_url.format(driver_version, driver_version, platform_arch, compression)

    debug(f"Final download path : {download_path}")
    return download_path
