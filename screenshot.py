from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = r"D:\Python\RedditVideoGenerator\Screenshots"
screenWidth = 400
screenHeight = 800


def getPostScreenshots(filePrefix, script, id):
    print("Taking screenshots...")
    # driver, wait = __setupDriver(script.url)
    options = webdriver.ChromeOptions()
    options.headless = True
    options.enable_mobile = False
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(script.url)

    id = script.url.split("comments/")[1].split("/")[0]
    print(id)

    handle = f"t3_{id}"
    # script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, "Post")
    method = By.ID
    search = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((method, handle))
    )
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    script.titleSCFile = fileName
    for commentFrame in script.frames:
        print(f"Finding {commentFrame.commentId}..")
        # commentFrame.screenShotFile = __takeScreenshot(
        #    filePrefix, driver, wait, f"t1_{commentFrame.commentId}"
        # )
        # handle = f"t1_{commentFrame.commentId}"
        handle = f'[thingid="t1_{commentFrame.commentId}"]'
        method = By.CSS_SELECTOR
        search = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((method, handle))
        )
        driver.execute_script("window.focus();")
        handle = commentFrame.commentId
        fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
        fp = open(fileName, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()
        commentFrame.screenShotFile = fileName
    driver.quit()


# def __takeScreenshot(filePrefix, driver, wait, handle="Post"):

#    return fileName


# Example usage:
# filePrefix = "example"
# script = YourScriptObject
# getPostScreenshots(filePrefix, script)
