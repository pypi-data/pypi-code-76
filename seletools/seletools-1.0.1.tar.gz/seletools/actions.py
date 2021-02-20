def drag_and_drop(driver, source, target):
    f = open("drag_and_drop.js", "r")
    javascript = f.read()
    f.close()
    driver.execute_script(javascript, source, target)
