from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

import time
from random import randint
import strings
import elements


def main():
    # go to firefox.exe folder, run in cmd: >> 'firefox.exe -marionette'  in order to enable remote connection
    firefox_services = Service(executable_path=r"files", service_args=['--marionette-port', '2828', '--connect-existing'])
    driver = webdriver.Firefox(service=firefox_services)

    if not check_url(driver):  # check if the correct web page
        return

    if not fill_title(driver):  # fill title with randomized string
        return

    required_themes = get_required_themes(driver)  # get required themes from page
    if required_themes is None:
        return

    review_text = build_review_text(required_themes)  # build an appropriate review according the required themes
    if not fill_review(driver, review_text):  # fill the built review text
        return

    time.sleep(1)  # wait until review text will be fully filled in

    if not click_submit(driver):  # click on the submit button and close the 'review' form
        return

    print("[SUCCESS] Done.")


def check_url(driver):
    current_url = driver.current_url

    if "ugc/myaccount/review" not in current_url:
        print("[ERROR] Wrong webpage! (your are not in 'ugc/myaccount/review')")
        return False

    return True


def fill_title(driver):
    try:
        title = driver.find_element(By.ID, elements.TITLE)
    except Exception as e:
        print(f"[ERROR] Can't find title:\n{e}")
        return False

    title.clear()  # clear before filling
    title.send_keys(strings.DEFAULT_TITLE[randint(0, len(strings.DEFAULT_TITLE) - 1)])
    return True


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
        print(f"[ERROR] Can't find send button:\n{e}")
        return False

    send_button.click()
    return True


if __name__ == '__main__':
    main()
