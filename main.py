import random
import time
import sys
from os import path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


url = "https://www.maxquant.org/download_asset/maxquant/latest"
download_dir = "W:\\Software\\MAXQUANT Version"

options = Options()
options.set_preference("browser.download.folderList", 2)  # Set default download location to Downloads folder.
options.set_preference("browser.download.manager.showWhenStarting", False);
options.set_preference("browser.download.dir", download_dir);
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip");
driver = webdriver.Firefox(options=options);


def random_keys():
    return "".join([random.choice('asdfjklreui') for _ in range(random.randrange(3, 10))])


driver.get(url)

# Get current version of MaxQuant from webpage header.
title = driver.find_element_by_tag_name('h2')
maxquant_version = title.text.split(' v')[1]
download_filename = f'MaxQuant_{maxquant_version}.zip'

if not path.exists(path.join(download_dir, download_filename)):

    # Fill out form
    form = driver.find_element_by_class_name('mq-form-download')
    form.find_element_by_name('name').send_keys(random_keys())
    form.find_element_by_name('email').send_keys(random_keys() + '@gmail.com')
    form.find_element_by_name('company').send_keys(random_keys())

    agree = form.find_element_by_class_name("form-check-input")
    if not agree.is_selected():
        agree.click()
    assert agree.is_selected()

    # Download MaxQuant
    form.submit()
    
    # click "license" link to get license text, and download it.
    driver.find_element_by_class_name('form-check-label').find_element_by_tag_name('a').click()
    license = driver.find_element_by_id('licenseModalDialog').find_element_by_class_name('modal-body').find_element_by_tag_name('form').text
    with open(path.join(download_dir, 'license.txt'), 'w') as f:
        f.write(license)


    # Wait until file is completely downloaded before exiting
    for el in range(120):
        time.sleep(1)
        if path.exists(path.join(download_dir, download_filename)) and not path.exists(path.join(download_dir, download_filename) + '.part'):
            driver.quit()
            break
    else:
        raise FileNotFoundError("After 120 seconds, download has not completed. Is this script still working?")



sys.exit()