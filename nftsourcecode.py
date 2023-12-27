import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
import json
import requests
from cryptography.fernet import Fernet
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
import datetime

root = Tk()
root.geometry('310x420')
root.title("OpenSea NFT Uploader V2")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)
is_properties = BooleanVar()
is_properties.set(False)
is_unlockable_content = BooleanVar()
is_unlockable_content.set(False)
is_freeze_metadata = BooleanVar()
is_freeze_metadata.set(False)
data_sitekey = '6LecZkIeAAAAALsWBCdLMQSR4GLE18xt86ZB9XDO'
page_url ='https://opensea.io/collection/unicapital-collection/assets/create'
api_key = '72b09d1e9fcbeafc370e0b8c212a7066'

captcha_response_1 = ""
captcha_response_2 = ""
captcha_response_3 = ""

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )


def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud")


def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    name_change_img_folder_button(upload_path)


def open_json_file():
    global json_file_path
    json_file_path = filedialog.askdirectory()
    name_change_json_folder_button(json_file_path)


def name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input


def name_change_json_folder_button(json_file_path):
    upload_property_input_button["text"] = json_file_path


class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)


collection_link_input = InputField("Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT Image Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)
unlockable_content = InputField("Unlockable Content:", 10, 0, 9)


def captcha_service(thread_name, self):
    global captcha_response_1
    global captcha_response_2
    global captcha_response_3

    if thread_name == "thread1":
        while True:
            try:
                u1 = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
                r1 = requests.get(u1)
                print(str(datetime.datetime.now()) + " : thread 1 : " + str(r1.json()))
                if r1.json().get("status") == 1:
                    rid = r1.json().get("request")
                    break
                time.sleep(2)
            except:
                time.sleep(2)
                continue

        while True:
            try:
                rid = r1.json().get("request")
                u12 = f"https://2captcha.com/res.php?key={api_key}&action=get&id={int(rid)}&json=1"
                r12 = requests.get(u12)
                print(str(datetime.datetime.now()) + " : thread 1 : " + str(r12.json()))
                if r12.json().get("status") == 1:
                    captcha_response_1 = r12.json().get("request")
                    break
                time.sleep(5)
            except:
                time.sleep(5)
                continue

    if thread_name == "thread2":
        while True:
            try:
                u1 = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
                r1 = requests.get(u1)
                print(str(datetime.datetime.now()) + " : thread 2 : " + str(r1.json()))
                if r1.json().get("status") == 1:
                    rid = r1.json().get("request")
                    break
                time.sleep(2)
            except:
                time.sleep(2)
                continue

        while True:
            try:
                rid = r1.json().get("request")
                u12 = f"https://2captcha.com/res.php?key={api_key}&action=get&id={int(rid)}&json=1"
                r12 = requests.get(u12)
                print(str(datetime.datetime.now()) + " : thread 2 : " + str(r12.json()))
                if r12.json().get("status") == 1:
                    captcha_response_2 = r12.json().get("request")
                    break
                time.sleep(5)
            except:
                time.sleep(5)
                continue

    if thread_name == "thread3":
        while True:
            try:
                u1 = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
                r1 = requests.get(u1)
                print(str(datetime.datetime.now()) + " : thread 3 : " + str(r1.json()))
                if r1.json().get("status") == 1:
                    rid = r1.json().get("request")
                    break
                time.sleep(2)
            except:
                time.sleep(2)
                continue

        while True:
            try:
                rid = r1.json().get("request")
                u12 = f"https://2captcha.com/res.php?key={api_key}&action=get&id={int(rid)}&json=1"
                r12 = requests.get(u12)
                print(str(datetime.datetime.now()) + " : thread 3 : " + str(r12.json()))
                if r12.json().get("status") == 1:
                    captcha_response_3 = r12.json().get("request")
                    break
                time.sleep(5)
            except:
                time.sleep(5)
                continue


def save():
    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)
    unlockable_content.save_inputs(9)


def main_program_loop():
    # START #
    project_path = main_directory
    file_path = upload_path
    json_path =  json_file_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()
    loop_unlockable_content = unlockable_content.input_field.get()

    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_css_selector_test(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    nft_counter = 1

    driver.get(collection_link)

    main_page = driver.current_window_handle

    n = 3
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * n)
    actions.perform()

    diff = end_num - start_num

    if diff == 0 or diff > 0:
        driver.execute_script("window.open('');")

    if diff == 1 or diff > 1:
        driver.switch_to.window(main_page)
        driver.execute_script("window.open('');")

    if diff > 1:
        driver.switch_to.window(main_page)
        driver.execute_script("window.open('');")

    start = 1
    while end_num >= start_num:
        diff = end_num - start_num
        no_of_tabs = len(driver.window_handles)

        uploaded_numbers = []
        upload_list = []
        for i in range(no_of_tabs - 1):
            print(str(datetime.datetime.now()) + " : Start creating NFT " + loop_title + str(start_num))

            driver.switch_to.window(driver.window_handles[i + 1])
            time.sleep(0.5)

            driver.get(collection_link + "/assets/create")
            time.sleep(0.5)

            while True:
                try:
                    wait_xpath('//*[@id="media"]')
                    break
                except:
                    print(str(datetime.datetime.now()) + " : Page loading failed. Attempting to load again...")
                    driver.get(collection_link + "/assets/create")
                    continue

            image_upload = driver.find_element_by_xpath('//*[@id="media"]')
            image_path = os.path.abspath(
                file_path + "/images/" + str(start_num) + "." + loop_file_format)  # change folder here
            image_upload.send_keys(image_path)

            name = driver.find_element_by_xpath('//*[@id="name"]')
            name.send_keys(loop_title + str(start_num))
            time.sleep(0.5)

            ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
            ext_link.send_keys(loop_external_link)
            time.sleep(0.5)

            desc = WebDriverWait(driver, 20).until(ExpectedConditions.element_to_be_clickable((By.XPATH, '//*[@id="description"]')))
            desc._parent.execute_script("""
                var elm = arguments[0], text = arguments[1];
                if (!('value' in elm))
                    throw new Error('Expected an <input> or <textarea>');
                elm.focus();
                elm.value = text;
                elm.dispatchEvent(new Event('change'));
                """, desc, loop_description)
            desc.send_keys(Keys.RETURN)
            time.sleep(0.5)

            if is_properties.get():
                jsonFile = json_path + "/json/"+ str(start_num) + ".json"
           
            

                if os.path.isfile(jsonFile) and os.access(jsonFile, os.R_OK):
            
                    print('true')
                    wait_css_selector("button[aria-label='Add properties']")
                    properties = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Add properties']")
                    driver.execute_script("arguments[0].click();", properties)
                    time.sleep(0.5)

                    # checks if file exists
                    jsonData = json.loads(open(json_path + "\\json\\"+ str(start_num) + ".json").read())
                
                    if "attributes" in jsonData:
                        jsonMetaData = jsonData['attributes']

                        for key in jsonMetaData:
                            input1 = driver.find_element(By.XPATH, '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
                            input2 = driver.find_element(By.XPATH, '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')
                            print(str(key['trait_type']))
                            print(str(key['value']))
                            input1.send_keys(str(key['trait_type']))
                            input2.send_keys(str(key['value']))
                            addmore_button = driver.find_element(By.XPATH, '//button[text()="Add more"]')
                            driver.execute_script("arguments[0].click();", addmore_button)
                        time.sleep(0.5)

                        try:
                            save_button = driver.find_element(By.XPATH, '//button[text()="Save"]')
                            driver.execute_script("arguments[0].click();", save_button)
                            time.sleep(0.5)
                        except:
                            driver.find_element(By.XPATH, '//button[text()="Save"]').click()
                            time.sleep(0.5)

                    elif "properties" in jsonData:
                        jsonMetaData = jsonData['properties']
                    
                        wait_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')#HKN
                        for key in jsonMetaData:
                            input1 = driver.find_element(By.XPATH, '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
                            input2 = driver.find_element(By.XPATH, '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')
                            #print(str(key['type']))
                            #print(str(key['name']))
                            input1.send_keys(str(key['type']))
                            input2.send_keys(str(key['name']))
                            addmore_button = driver.find_element(By.XPATH, '//button[text()="Add more"]')
                            driver.execute_script("arguments[0].click();", addmore_button)
                        time.sleep(0.5)

                        try:
                            save_button = driver.find_element(By.XPATH, '//button[text()="Save"]')
                            driver.execute_script("arguments[0].click();", save_button)
                            time.sleep(0.5)
                        except:
                            driver.find_element(By.XPATH, '//button[text()="Save"]').click()
                            time.sleep(0.5)

                    else:
                        print("keys not found!") 

                else:
                    print('json file not found')        
                
                    

            if is_unlockable_content.get():
                wait_css_selector("input[id='unlockable-content-toggle']")
                driver.find_element_by_css_selector("input[id='unlockable-content-toggle']").click()

                meta = driver.find_element_by_xpath(
                    '//*[@id="main"]/div/div/section/div[2]/form/section/div[4]/div[2]/textarea')
                meta.send_keys(loop_unlockable_content)
                time.sleep(0.5)

            if is_polygon.get():
                blockchain_button = driver.find_element(By.XPATH,
                                                        '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div[7]/div/div[2]')
                blockchain_button.click()
                polygon_button_location = '//span[normalize-space() = "Polygon"]'
                wait.until(ExpectedConditions.presence_of_element_located(
                    (By.XPATH, polygon_button_location)))
                polygon_button = driver.find_element(
                    By.XPATH, polygon_button_location)
                polygon_button.click()

            create = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
            driver.execute_script("arguments[0].click();", create)
            time.sleep(1)

            if start == 1 or start % 30 == 0:
                if i == 0:
                    thread1 = threading.Thread(target=captcha_service, args=("thread1", []))
                    thread1.start()
                    print(str(datetime.datetime.now()) + " : Captcha thread 1 started")

                if i == 1:
                    thread2 = threading.Thread(target=captcha_service, args=("thread2", []))
                    thread2.start()
                    print(str(datetime.datetime.now()) + " : Captcha thread 2 started")

                if i == 2:
                    thread3 = threading.Thread(target=captcha_service, args=("thread3", []))
                    thread3.start()
                    print(str(datetime.datetime.now()) + " : Captcha thread 3 started")

            upload_list.append(str(start_num))
            start_num = start_num + 1
            nft_counter = nft_counter + 1

            if diff == 0:
                break

            if diff == 1 and i == 1:
                break

        while True:
            if diff == 0 or diff > 0:
                if captcha_response_1 != "" and str(1) not in uploaded_numbers:
                    driver.switch_to.window(driver.window_handles[1])

                    driver.execute_script("""
                        const reduceObjectToArray = (obj) => Object.keys(obj).reduce(function (r, k) {
                                return r.concat(k, obj[k]);
                        }, []);

                        const client = ___grecaptcha_cfg.clients[0]
                        let result = [];
                        result = reduceObjectToArray(client).filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        result = result.flatMap(r => {
                            return reduceObjectToArray(r)
                        })

                        result = result.filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        const reqObj = result.find( r => r.callback)
                        reqObj.callback("${captcha_response_1}")
                        """)

                    try:
                        wait_css_selector("i[aria-label='Close']")
                        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
                        cross.click()
                        time.sleep(2)

                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!')
                    except:
                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!. But will not list for sale due to OpenSea error.')

                    uploaded_numbers.append(str(1))

                    driver.switch_to.window(driver.window_handles[0])

            if diff == 1 or diff > 1:
                if captcha_response_2 != "" and str(2) not in uploaded_numbers:
                    driver.switch_to.window(driver.window_handles[2])

                    driver.execute_script("""
                        const reduceObjectToArray = (obj) => Object.keys(obj).reduce(function (r, k) {
                                return r.concat(k, obj[k]);
                        }, []);

                        const client = ___grecaptcha_cfg.clients[0]
                        let result = [];
                        result = reduceObjectToArray(client).filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        result = result.flatMap(r => {
                            return reduceObjectToArray(r)
                        })

                        result = result.filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        const reqObj = result.find( r => r.callback)
                        reqObj.callback("${captcha_response_2}")
                        """)

                    try:
                        wait_css_selector("i[aria-label='Close']")
                        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
                        cross.click()
                        time.sleep(2)

                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!')
                    except:
                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!. But will not list for sale due to OpenSea error.')

                    uploaded_numbers.append(str(2))

                    driver.switch_to.window(driver.window_handles[0])

            if diff > 1:
                if captcha_response_3 != "" and str(3) not in uploaded_numbers:
                    driver.switch_to.window(driver.window_handles[3])

                    driver.execute_script("""
                        const reduceObjectToArray = (obj) => Object.keys(obj).reduce(function (r, k) {
                                return r.concat(k, obj[k]);
                        }, []);

                        const client = ___grecaptcha_cfg.clients[0]
                        let result = [];
                        result = reduceObjectToArray(client).filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        result = result.flatMap(r => {
                            return reduceObjectToArray(r)
                        })

                        result = result.filter(c => Object.prototype.toString.call(c) === "[object Object]")

                        const reqObj = result.find( r => r.callback)
                        reqObj.callback("${captcha_response_3}")
                        """)

                    try:
                        wait_css_selector("i[aria-label='Close']")
                        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
                        cross.click()
                        time.sleep(2)

                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!')
                    except:
                        print(str(datetime.datetime.now()) + " : #" + upload_list[0] +  ' NFT upload completed!. But will not list for sale due to OpenSea error.')

                    uploaded_numbers.append(str(3))

                    driver.switch_to.window(driver.window_handles[0])

            if diff == 0:
                if len(uploaded_numbers) == 1:
                    break

            if diff == 1:
                if len(uploaded_numbers) == 2:
                    break

            if diff == 2 or diff > 2:
                if len(uploaded_numbers) == 3:
                    break

            time.sleep(5)

        if is_freeze_metadata.get():
            for y in range(no_of_tabs - 1):
                driver.switch_to.window(driver.window_handles[y + 1])

                current_url = driver.current_url
                driver.get(current_url)

                wait_xpath('//*[@id="main"]/div/div/div[1]/div/span/a')
                driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div/span/a').click()
                time.sleep(5)

                while True:
                    try:
                        edit_page = driver.current_url

                        wait_css_selector("input[id='freezeMetadata']")
                        driver.find_element_by_css_selector("input[id='freezeMetadata']").click()
                        time.sleep(2)

                        wait_xpath('//*[@id="main"]/div/div/section/div[2]/form/div[8]/button')
                        driver.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/form/div[8]/button').click()
                        time.sleep(5)

                        wait_css_selector("input[id='freezeMetadataConsent']")
                        driver.find_element_by_css_selector("input[id='freezeMetadataConsent']").click()
                        time.sleep(3)

                        wait_xpath('//*[text()="Confirm"]')
                        driver.find_element_by_xpath('//*[text()="Confirm"]').click()
                        time.sleep(2)

                        for handle in driver.window_handles:
                            if handle != main_page:
                                login_page = handle

                        driver.switch_to.window(login_page)

                        wait_xpath('//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]')
                        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]').click()
                        time.sleep(1)

                        wait_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]')
                        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]').click()
                        time.sleep(1)

                        driver.switch_to.window(main_page)

                        wait_xpath('/html/body/div[8]/div/div/div/div[1]/section/section/div/div/div[2]/div[1]/div[2]')
                        freeze_success = driver.find_element_by_xpath(
                            '/html/body/div[8]/div/div/div/div[1]/section/section/div/div/div[2]/div[1]/div[2]').text

                        if freeze_success == 'Complete':
                            break
                    except:
                        driver.get(edit_page)
                        continue

                time.sleep(2)

                driver.get(current_url)

                if diff == 0:
                    break

                if diff == 1 and i == 1:
                    break

        start = start + 1


button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=29, column=1)
button_save = tkinter.Button(root, width=20, text="Save Form", command=save)
button_save.grid(row=28, column=1)
open_browser = tkinter.Button(root, width=20, text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=27, column=1)
upload_property_input_button = tkinter.Button(root, width=20, text="JSON Folder", command=open_json_file)
upload_property_input_button.grid(row=26, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Image Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=25, column=1)
isFreezeMetadata = tkinter.Checkbutton(root, text='Freeze Metadata        ', var=is_freeze_metadata)
isFreezeMetadata.grid(row=24, column=0)
isProperties = tkinter.Checkbutton(root, text='Upload Properties      ', var=is_properties)
isProperties.grid(row=23, column=0)
isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain  ', var=is_polygon)
isPolygon.grid(row=21, column=0)
isUnlockableContent = tkinter.Checkbutton(root, text='Unlockable Content  ', var=is_unlockable_content)
isUnlockableContent.grid(row=20, column=0)

try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass

root.mainloop()
