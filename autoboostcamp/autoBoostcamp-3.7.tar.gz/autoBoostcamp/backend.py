import os
from selenium import webdriver
from queue import Queue
import threading
import chromedriver_autoinstaller
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple
import time
from pathlib import Path
import shutil

################################# region backend ###############################################################

class get_authNum(threading.Thread):
    '''
    example)
    1. download google sms app on android phone and set that to the default message app.
    2. pair "GOOGLE SMS APP" and "GOOGLE SMS WEB", on the android and desktop, respectively.
    3. use below example. queue will be filled after the thread successfully gets an authNum.

    queue = Queue()
    get_authNum_thread = get_authNum(queue)
    get_authNum_thread.start()
    '''

    def __init__(self, queue:Queue, static_chromedriver_path = "C:/chromedriverAuth/chromedriver.exe"):
        threading.Thread.__init__(self)
        self.static_chromedriver_path = static_chromedriver_path # chromedriver should not be used from other thread.
        self.queue = queue
    def init_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r'user-data-dir=C:\chromewebdriverAuth_profile')
        options.add_experimental_option("detach", True)
        scpath = self.static_chromedriver_path
        try:
            driver = webdriver.Chrome(scpath, options=options)
        except:
            scpath = chromedriver_autoinstaller.install()  # returns static_path
            Path(os.path.dirname(self.static_chromedriver_path)).mkdir(parents=True, exist_ok=True) # make another path
            shutil.copy(scpath, self.static_chromedriver_path) # make copy for independent use of chromedriver

            driver = webdriver.Chrome(self.static_chromedriver_path, options=options)
        return driver
    def find_authNum(self, driver, timeout = 60):
        driver.get("https://messages.google.com/web/conversations")
        start = time.time()
        while time.time() - start < 60:
            try:
                WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class = "text-content"]')))
            except TimeoutException:
                raise Exception("휴대전화가 온라인 상태가 아니거나, 컴퓨터와 페어링 되어있지 않습니다. 연결상태를 확인해주세요.")
            # explicit wait 이 최초의 appear까지라면..? time.sleep(1) 정도가 더 필요해짐.
            unreads = driver.find_elements_by_css_selector('div[class = "text-content unread"]')
            unread_msgs = [unread.find_element_by_css_selector('span[class="ng-star-inserted"]') for unread in unreads]
            unread_texts = [webEl.text for webEl in unread_msgs]
            nums = []
            for msg in unread_texts:
                sear = re.search("(\d+)?\D+인증\D+(\d+)?", msg)
                if sear:
                    n = list(filter(lambda x: x != None, sear.groups())).pop()
                    nums.append(n)
            authNum = None
            for num in nums:
                if len(num) > 3:
                    authNum = num
                    return authNum
            time.sleep(1)
        authNum = "Failed to get authNum ! check your message storage"
        return authNum
    def run(self):
        driver = self.init_webdriver()
        try:
            authNum = self.find_authNum(driver, timeout = 60)
            self.queue.put(authNum)
        except:
            pass
        driver.quit()

def init_chrome_driver(static_path = ""):
    options = webdriver.ChromeOptions()
    options.add_argument(r'user-data-dir=C:\chromewebdriver_profile')
    options.add_experimental_option("detach", True)
    try:
        driver = webdriver.Chrome(static_path, options = options)
    except:
        static_path = chromedriver_autoinstaller.install() # returns static_path
        driver = webdriver.Chrome(static_path, options=options)
    return driver
def init_slack(driver):
    driver.get("https://bcaitech1.slack.com")
    driver.get("https://bcaitech1.slack.com") # 평가판 어쩌구.. 하면서 오류나는거 한번 건너뛰기 위해 두번 리디렉션

def collect_webElements(driver, web_elements: dict, what: str):
    if what == "channels":
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#C01HZAT6R0X")))
        except:
            raise Exception("슬랙에 정상적으로 로그인되어 있는지 확인해주세요.")
        web_elements["channels"]["attendance"] = driver.find_element_by_css_selector("#C01HZAT6R0X")
    elif what == "articles":
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[role="listitem"]')))
        web_elements["current_view_articles"] = driver.find_elements_by_css_selector('div[role="listitem"]')
    return web_elements

def get_emojis(web_elements):
    return web_elements["current_view_articles"][-1].find_element_by_css_selector('div[class="c-message_kit__reaction_bar c-reaction_bar c-reaction_bar--light"')

def init_edwith(driver):
    driver.get("https://www.edwith.org/neoid/snsLoginBegin?snsCode=naver&sd=www.edwith.org")
    driver.get("https://www.edwith.org/bcaitech1/joinLectures/76032")

def get_learn_btn(driver) -> Tuple[WebElement, WebElement]:
    try:
        learn = driver.find_element_by_css_selector('button[class="btn_learning"]')
        learn_end = None
    except NoSuchElementException:
        learn = None
        learn_end = driver.find_element_by_css_selector('button[class="btn_learning end"]')
    return learn, learn_end
def delete_auth(driver):
    WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[data-btn="authDelete"]')))
    delet = driver.find_element_by_css_selector('button[data-btn="authDelete"]')
    delet.click()
    delet_confirm = driver.find_element_by_css_selector('a[data-btn="delete"]')
    delet_confirm.click()
    WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[data-btn="refresh"]')))
    confirm = driver.find_element_by_css_selector('a[data-btn="refresh"]')
    confirm.click()

def init_auth(driver):
    driver.get("https://www.edwith.org/userInfo/base-info")
    try:
        delete_auth(driver) # 인증이 이미 삭제되어있는 경우
    except:
        pass # 그대로 진행
    WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="btn_reg"][data-btn="auth"]')))
    regist = driver.find_element_by_css_selector('button[class="btn_reg"][data-btn="auth"]')
    regist.click()
    WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[data-btn="authenticate"')))
    do_mobile_auth = driver.find_element_by_css_selector('a[data-btn="authenticate"')
    do_mobile_auth.click()

def collect_inputs(driver):
    inputs = defaultdict(dict)

    textInputs = driver.find_elements_by_css_selector('input[type="text"]')
    for ti in textInputs:
        inputs['text'][ti.get_attribute("placeholder")] = ti
    selectInputs = driver.find_elements_by_css_selector('select')
    for si in selectInputs:
        inputs['select'][si.get_attribute("id")] = dict()
        inputs['select'][si.get_attribute("id")]["self"] = si
        options = si.find_elements_by_css_selector("option")
        for opt in options:
            inputs['select'][si.get_attribute("id")][opt.get_attribute("value")] = opt
    inputs["button"]["man"] = driver.find_element_by_css_selector('label[for="man"]')
    inputs["button"]["woman"] = driver.find_element_by_css_selector('label[for="woman"]')
    inputs["button"]["mvno_sk"] = driver.find_element_by_css_selector('label[for="mvno_sk"]')
    inputs["button"]["mvno_kt"] = driver.find_element_by_css_selector('label[for="mvno_kt"]')
    inputs["button"]["mvno_lg"] = driver.find_element_by_css_selector('label[for="mvno_lg"]')
    return inputs

def make_default_auth_table():
    table = defaultdict()
    table["이름"] = "my_name"
    table["성별"] = "man/woman"
    table["년(4자)"] = "1993"
    table["birth_month"] = "7"
    table["일"] = "4"
    table["mobile_cd"] = "SKT/KTF/LGT/MVNO"
    table["통신사"] = "mvno_sk/mvno_kt/mvno_lg"
    table["휴대전화번호"] = "01012341234"
    return table

def get_table(path="auth_key.txt"):
    if not os.path.exists(path):
        default_table = make_default_auth_table()
        with open(path, mode="w") as file:
            file.write("\n".join([f"{k}:{v}" for k,v in default_table.items()]))
    with open(path, mode='r') as file:
        text = file.read()
    table = dict()
    for t in text.split('\n'):
        ts = t.split(':')
        table[ts[0]] = ts[1]
    return table

def doInput(inputs, table: dict):
    def send_keys(inputs, keys: list, table: dict):
        for k, v in table.items():
            if k in keys:
                inputs[k].send_keys(v)
    try:
        keys = ["이름", "년(4자)", "일", "휴대전화번호"]
        send_keys(inputs["text"], keys, table)

        inputs["button"][table["성별"]].click()
        inputs["select"]["birth_month"][table["birth_month"]].click()
        inputs["select"]["mobile_cd"][table["mobile_cd"]].click()
        if "통신사" in table.keys() and table["통신사"]:
            inputs["button"][table["통신사"]].click()
    except KeyError:
        print("auth_key.txt 가 올바르지 않습니다. 수정해주세요.")

def is_reacted(emoji_element):
    attr_class = emoji_element.get_attribute('class').split()
    if 'c-reaction--reacted' in attr_class:
        return True
    else:
        return False

### endregion
################################# region process ###############################################################
def quick_start():
    qs = '''# copy & paste below codes. check it each works properly
abc.backend.isready_slack_driver()
abc.backend.isready_naver_driver()
abc.backend.isready_auth_driver()
table_path = abc.backend.isready_table()
print(table_path)

abc.doHi()
abc.doBye()
abc.do()'''
    print(qs)

def isready_auth_driver():
    temp = get_authNum(None)
    driver = temp.init_webdriver()
    temp.find_authNum(driver)
    print("구글SMS 페어링 확인")
    driver.quit()

def isready_slack_driver(driver = None):
    if driver is None:
        driver = init_chrome_driver()
    init_slack(driver)
    collect_webElements(driver, web_elements=defaultdict(dict), what = "channels")
    print("슬랙 로그인 확인")
    driver.quit()

def isready_naver_driver(driver = None):
    if driver is None:
        driver = init_chrome_driver()
    init_edwith(driver)
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="btn_learning"], button[class="btn_learning end"]')))
    except:
        raise Exception("네이버에 로그인 되어 있는지 확인해주세요.")
    print("네이버 로그인 확인")
    driver.quit()

def isready_table(path="auth_key.txt"):
    if not os.path.exists(path):
        default_table = make_default_auth_table()
        with open(path, mode="w") as file:
            file.write("\n".join([f"{k}:{v}" for k,v in default_table.items()]))
    with open(path, mode='r') as file:
        text = file.read()
    table = dict()
    for t in text.split('\n'):
        ts = t.split(':')
        table[ts[0]] = ts[1]

    # table validation 코드
    print("""예시
이름:홍길동
성별:man
년(4자):1993
birth_month:7
일:4
mobile_cd:SKT
통신사:
휴대전화번호:01012341234
    """)

    return os.path.abspath(path)

def hi_slack(driver):
    init_slack(driver)
    web_elements = defaultdict(dict)
    web_elements = collect_webElements(driver, web_elements, what="channels")
    web_elements["channels"]["attendance"].click()
    web_elements = collect_webElements(driver, web_elements, what="articles")
    emojis = get_emojis(web_elements)
    first_emoji = emojis.find_element_by_css_selector("*")
    if not is_reacted(first_emoji):
        first_emoji.click()

def hi_edwith(driver):
    # start monitoring sms
    q = Queue()
    GetauthNum = get_authNum(q)
    GetauthNum.start()

    # hi_edwith
    init_edwith(driver)

    learn, _ = get_learn_btn(driver)
    if learn is not None:
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

    authNum = q.get(timeout=60)
    inputs["text"]["인증번호"].send_keys(authNum)

    confirm_btn = driver.find_element_by_css_selector('a[class="btn"]')
    confirm_btn.click()

    driver.switch_to.default_content()

def bye_edwith(driver):
    init_edwith(driver)
    _, learn_end = get_learn_btn(driver)
    if learn_end is not None:
        learn_end.click()
    driver.switch_to.alert.accept()

def doHi():
    static_path = ''
    driver = init_chrome_driver(static_path)

    hi_slack(driver)
    hi_edwith(driver)

    time.sleep(1)

    driver.quit()

def doBye():
    static_path = ''
    driver = init_chrome_driver(static_path)

    bye_edwith(driver)

    driver.quit()

### endregion