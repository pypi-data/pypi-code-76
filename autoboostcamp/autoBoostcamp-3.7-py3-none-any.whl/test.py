from .backend import *

# start monitoring sms
driver = init_chrome_driver()

q = Queue()
GetauthNum = get_authNum(q)
GetauthNum.start()

# hi_edwith
init_edwith(driver)

learn, _ = get_learn_btn(driver)
learn.click()
driver.switch_to.alert.accept()

init_auth(driver)
driver.switch_to.window(driver.window_handles[1])
agree = driver.find_element_by_css_selector('label[for="chk_agree3"]')
agree.click()

inputs = collect_inputs(driver)

table = get_table()
doInput(inputs, table)

send_auth = driver.find_element_by_css_selector('a[class="btn_c btn_mobile_submit"')
send_auth.click()

authNum = q.get(timeout=5)
inputs["text"]["인증번호"].send_keys(authNum)

confirm_btn = driver.find_element_by_css_selector('a[class="btn"]')
confirm_btn.click()

driver.switch_to.default_content()