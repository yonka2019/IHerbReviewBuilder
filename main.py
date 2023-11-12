from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

import time
from random import randint
import strings
import elements


def main():
    # ! || RU VERSION || RU VERSION || RU VERSION || RU VERSION || RU VERSION || RU VERSION || RU VERSION || RU VERSION || !
    # go to firefox.exe folder, run in cmd: >> 'firefox.exe -marionette'  in order to enable remote connection
    # go to https://il.iherb.com/ugc/myaccount/review (my account -> my reviews)
    # put X number of stars on any item (in order to open review menu)
    # run the script & enjoy
    firefox_services = Service(executable_path=r"files", service_args=['--marionette-port', '2828', '--connect-existing'])
    driver = webdriver.Firefox(service=firefox_services)

    print("[STATUS] Checking current webpage URL..")
    url_status = check_url(driver)

    if url_status:  # check if the correct web page
        print("[STATUS] Success")
    else:
        print("[ERROR] Bad webpage opened (your are not in 'ugc/myaccount/review')")
        return

    print("\n[STATUS] filling up the title review..")
    title_status = fill_title(driver)  # fill title with randomized string

    if title_status is None:
        print("[STATUS] Success")
    else:
        print("[ERROR] Cant find title\n>> " + title_status.__str__())
        return

    print("\n[STATUS] Getting the required themes..")
    required_themes = get_required_themes(driver)  # get required themes from page

    if required_themes is not None:
        print("[STATUS] Success")
    else:
        return

    print("\n[STATUS] Building review text and filling it..")
    review_text = build_review_text(required_themes)  # build an appropriate review according the required themes

    filled_review = fill_review(driver, review_text)
    if filled_review:  # fill the built review text
        print("[STATUS] Success")
    else:
        return

    time.sleep(1)  # wait until review text will be fully filled in
    print("\n[STATUS] Submitting the review form..")
    submit_status = click_submit(driver)

    if submit_status:  # click on the submit button and close the 'review' form
        print("[STATUS] Success")
    else:
        return

    print("\n[SUCCESS] Finished")


def check_url(driver):
    current_url = driver.current_url

    if "ugc/myaccount/review" not in current_url:
        return False

    return True


def fill_title(driver):
    try:
        title = driver.find_element(By.ID, elements.TITLE)
    except Exception as e:
        return e

    title.clear()  # clear before filling
    title.send_keys(strings.DEFAULT_TITLE[randint(0, len(strings.DEFAULT_TITLE) - 1)])
    return None


def get_required_themes(driver):
    try:
        ul_element = driver.find_element(By.CLASS_NAME, elements.THEMES)
    except Exception as e:
        print(f"[ERROR] Can't find required themes list:\n{e}")
        return None

    try:
        list_items = ul_element.find_elements(By.TAG_NAME, "li")  # list item
    except Exception as e:
        print(f"[ERROR] Can't find required theme:\n{e}")
        return None

    return [li.text for li in list_items]


def build_review_text(required_themes):
    review_text = ""

    for theme in required_themes:
        if theme in strings.THEME_STRINGS:
            review_text += (strings.THEME_STRINGS[theme] + strings.THEME_STRING_SEPARATOR)

    review_text += f"\n{strings.FINAL_STRING[randint(0, len(strings.FINAL_STRING) - 1)]}"
    return review_text


def fill_review(driver, review_text):
    try:
        review = driver.find_element(By.ID, elements.REVIEW)
    except Exception as e:
        print(f"[ERROR] Can't find review text box:\n{e}")
        return False

    review.clear()  # clear before filling
    review.send_keys(review_text)  # fill the review box
    return True


def click_submit(driver):
    try:
        send_button = driver.find_element(By.CLASS_NAME, elements.SEND_BUTTON)
    except Exception as e:
        print(f"[ERROR] Can't find 'submit' button:\n{e}")
        return False

    send_button.click()
    return True


if __name__ == '__main__':
    main()
