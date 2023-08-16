'''
    @brief utils module component containing functions to be injected
    @author oldgod
    @note For each of the functions mentioned here, there is a specific prefix which will be
    used in order to load them appropriately
'''

from selenium import webdriver

def idriver_chrome(driver_path: str):
    '''
        @brief function to create a webdriver instance for Chrome browser
        @param driver_path: String containing the path to the web driver
        @return returns the driver instance created for chrome web driver
        @author oldgod
    '''
    if not isinstance(driver_path, str):
        return None
    elif len(driver_path) == 0:
        return None

    return webdriver.Chrome(executable_path=driver_path)
