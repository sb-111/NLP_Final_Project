from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import json
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # 자동으로 chromedriver 설치

driver = webdriver.Chrome()
# driver = webdriver.Chrome(executable_path='../chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def scroll_down():
    pre_height = driver.execute_script("return document.body.scrollHeight")  # 현재 스크롤 위치 저장
    try_num = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 스크롤을 가장 아래로 내린다
        time.sleep(1)
        cur_height = driver.execute_script("return document.body.scrollHeight")  # 현재 스크롤을 저장한다.
        try_num += 1
        # print(try_num)
        if pre_height == cur_height:
            break
        else:
            pre_height = cur_height
    driver.implicitly_wait(30)


def go_page(region):
    # url입력
    url = "https://www.yogiyo.co.kr/mobile/#"  # 사이트 입력
    driver.get(url)  # 사이트 오픈
    driver.maximize_window()  # 전체장
    driver.implicitly_wait(1)  # 2초 지연

    # 검색창 선택
    xpath = '''//*[@id="search"]/div/form/input'''  # 검색창
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    driver.implicitly_wait(1)

    # 검색창 입력

    # value = input("지역을 입력하세요")
    value = region
    element.send_keys(value)
    driver.implicitly_wait(1)

    # 검색버튼 클릭
    search_xpath = '''//*[@id="button_search_address"]/button[2]'''
    search = driver.find_element_by_xpath(search_xpath)
    driver.execute_script("arguments[0].click();", search)

    # 검색 콤보상자 선택
    search_result_selector = '#search > div > form > ul > li:nth-child(3) > a'
    search_result = driver.find_element_by_css_selector(search_result_selector)
    driver.execute_script("arguments[0].click();", search_result)
    driver.implicitly_wait(3)

    errors = 0
    # 페이지 소스 출력
    html = driver.page_source
    html_source = BeautifulSoup(html, 'html.parser')
    # print(html_source)
    store_list = []
    stores = driver.find_elements_by_class_name('col-sm-6')
    stores_num = len(list(set(html_source.find_all('div', class_='restaurant-name ng-binding'))))
    for s in stores:
        store_list.append(s)
        # print(s.text)
    # print(len(store_list))
    stores_num = len(list(set(stores)))
    stores_num = list(range(stores_num))
    print('stores_num : ', stores_num)
    scroll_down()
    return stores_num


def goto_store(num):
    cnt_error = 0
    try:
        scroll_down()
        # 상점 이동
        in_store_xpath = f'''//*[@id="content"]/div/div[4]/div/div[2]/div[{num + 1}]/div/table/tbody/tr/td[2]'''
        in_store = driver.find_element_by_xpath(in_store_xpath)
        time.sleep(2)
        store_name = in_store.text
        store_name = store_name.split()[0]
        print('store_name :', store_name)
        # in_store.click()
        driver.execute_script("arguments[0].click();", in_store)
        # ActionChains(driver).double_click(in_store)
        driver.implicitly_wait(3)
        # 리뷰 탭 들어가기
        review_btn_xpath = '//*[@id="content"]/div[2]/div[1]/ul/li[2]/a'
        review_btn = driver.find_element_by_xpath(review_btn_xpath)
        driver.execute_script("arguments[0].click();", review_btn)
        driver.implicitly_wait(3)
        print(f'{store_name} get review btn')
        # 리뷰 더보기
        i = 0
        review_errors = 0
        while True:
            i += 1
            var = i * 10 + 2
            plus_btn_xpath = f'/html/body/div[6]/div[2]/div[1]/div[5]/ul/li[{var}]/a'
            # print(plus_btn_xpath)
            try:
                plus_btn = driver.find_element_by_xpath(plus_btn_xpath)
                # plus_btn.click()
                driver.execute_script("arguments[0].click();", plus_btn)
                print(i)
            except Exception as error:
                review_error_string = str(error)
                print(review_error_string)
                review_errors += 1
            if review_errors > 2:
                break
    except Exception as error:
        error_string = str(error)
        print(error_string)
    return store_name


def get_reviews(store_name):
    store_name = store_name
    html = driver.page_source
    html_source = BeautifulSoup(html, 'html.parser')
    reviews = html_source.find_all('p', attrs={'ng-show': 'review.comment',
                                               'ng-bind-html': 'review.comment|strip_html'})
    reviews = [r.text for r in reviews]
    taste_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                     'ng-show': "review.rating_taste > 0"})
    taste_star = [t.text for t in taste_star]
    quantity_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                        'ng-show': "review.rating_quantity > 0"})
    quantity_star = [q.text for q in quantity_star]
    delivery_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                        'ng-show': "review.rating_delivery > 0"})
    delivery_star = [d.text for d in delivery_star]
    stars = {'taste': taste_star, 'quantity': quantity_star, 'delivery': delivery_star}
    driver.implicitly_wait(2)

    return reviews, stars

# def go_page(region):
#     # url입력
#     url = "https://www.yogiyo.co.kr/mobile/#" # 사이트 입력
#     driver.get(url) # 사이트 오픈
#     driver.maximize_window() # 전체장
#     driver.implicitly_wait(1) # 2초 지연
#
#     # 메인 페이지 검색창 선택
#     xpath = '''//*[@id="search"]/div/form/input'''  # 검색창
#     element = driver.find_element_by_xpath(xpath)
#     element.clear() # 비우고
#     driver.implicitly_wait(1)
#
#     # 검색창 입력
#
#     # value = input("지역을 입력하세요")
#     value = region
#     element.send_keys(value) # 검색창에 region 입력
#     driver.implicitly_wait(1)
#
#     # 검색버튼 클릭
#     search_xpath = '''//*[@id="button_search_address"]/button[2]'''
#     search = driver.find_element_by_xpath(search_xpath) # 검색버튼
#     driver.execute_script("arguments[0].click();", search) # 클릭
#
#
#     # 검색 콤보상자 선택
#     search_result_selector = '#search > div > form > ul > li:nth-child(3) > a'
#     search_result = driver.find_element_by_css_selector(search_result_selector) # 검색 콤보상자
#     driver.execute_script("arguments[0].click();", search_result) #클릭
#     driver.implicitly_wait(3)

def before_get_review(region, store_limit=4):
    store_total_num = go_page(region)
    store_num = store_total_num
    # store_num = [i for i in range(store_limit)]
    return store_num


def get_clean_mark(num) -> bool:
    # 가게 목록들을 보여주는 창에서의 xpath
    is_clean_mark_xpath = f'//*[@id="content"]/div/div[4]/div/div[2]/div[{num+1}]/div/table/tbody/tr/td[2]/div/ul/li/*[@class="ico-cesco"]'
    result = True

    # cesco 마크를 찾지 못한다면 NoSuchElementException 예외 발생
    try:
        driver.find_element_by_xpath(is_clean_mark_xpath)

    except NoSuchElementException:
        result = False

    print(f"위생인증여부 {result}")

    return True


def get_delivery_cost() -> tuple[int, int]:
    # 가게 진입 -> 리뷰탭으로 이동한 후, 최소주문금액, 배달비 찾기

    delivery_cost = -1
    least_cost = -1

    # 최소주문금액과 배달비 xpath
    least_cost_xpath = '//*[@id="content"]/div[2]/div[1]/div[1]/div[2]/ul/li[3]/span'
    delivery_cost_xpath = '//*[@id="content"]/div[2]/div[2]/ng-include/div/div[2]/div[4]/span[1]'

    # 쉼표와 한글이 섞인 가격 문자열 (15,000원, 4,000원 ...)을 걸러내기 위한 정규식
    extract_cost = r'\d{1,3}(,\d{3})*'

    # 최소 주문금액 가져오기
    try:
        least_cost_element = driver.find_element_by_xpath(least_cost_xpath)
        least_cost_str = least_cost_element.text # ex) 14,000원
        match = re.search(extract_cost, least_cost_str)
        least_cost = int(match.group().replace(',', ''))

    except NoSuchElementException:
        least_cost = -1

    except AttributeError:
        least_cost = -1

    # 배달비 가져오기
    try:
        delivery_cost_element = driver.find_element_by_xpath(delivery_cost_xpath)
        delivery_cost_str = delivery_cost_element.text
        match = re.search(extract_cost, delivery_cost_str)
        delivery_cost = int(match.group().replace(',', ''))

    except NoSuchElementException:
        delivery_cost = -1

    except AttributeError:
        delivery_cost = -1

    print(f"배달금액 : {delivery_cost}, 최소주문금액 : {least_cost}")

    return delivery_cost, least_cost

def go_info_tab():
    info_tab_xpath = f'//*[@id="content"]/div[2]/div[1]/ul/li[3]/a'
    info_tab = driver.find_element_by_xpath(info_tab_xpath)
    driver.execute_script("arguments[0].click();", info_tab)

def get_review_event() -> bool:
    review_recognition = ['리뷰','ㄹI뷰', 'ㄹI 뷰', 'ㄹl 뷰']
    event_recognition = ["이벤트", "2벤트", "E벤트", "e벤트", "ㅇl벤트", "ㅇI벤트"]

    is_review = False
    is_event = False

    go_info_tab()

    description_xpath = '//*[@id="info"]/div[1]/div[2]'
    description = driver.find_element_by_xpath(description_xpath)

    # description.text에 review_recognition에 있는 단어가 하나라도 있으면 is_review를 True로 설정
    for word in review_recognition:
        if word in description.text:
            is_review = True
            break

    # description.text에 event_recognition에 있는 단어가 하나라도 있으면 is_event를 True로 설정
    for word in event_recognition:
        if word in description.text:
            is_event = True
            break

    # review_recognition과 event_recognition에 모두 있는 경우에만 True, 아니면 False
    return (is_review and is_event)



def isServiceProvide(num : int) -> bool :
    logo_xpath = f'''//*[@id="content"]/div/div[4]/div/div[2]/div[{num+1}]/div/table/tbody/tr/td[1]'''
    logo = driver.find_element_by_xpath(logo_xpath)


    if("현재 요기요" in logo.text):
        return False
    else:
        return True


def get_total_data(parameter: list):
    # list로 입력받은 param 분해
    region = parameter[0]
    num = parameter[1]

    # 리턴할 값 정의
    store_name = ""
    isClean = False
    delivery_cost = -1
    least_cost = -1
    isReviewEvent = False
    reviews = ""
    stars = {}

    # 대기 후, 검색 페이지 이동
    driver.implicitly_wait(2)
    go_page(region)  # before_get_review(region)

    # 위생 마크 유무 체크
    isClean = get_clean_mark(num)

    # 가게 이름 가져오면서 가게 페이지로 이동
    # 이때 요기요 서비스를 제공하지 않는 가게라면, 리뷰를 가져오지 않는다.
    if isServiceProvide(num):
        store_name = goto_store(num)
        print(f"{num + 1} go to store completed")

        # 배송비, 최소주문금액 가져오기
        delivery_cost, least_cost = get_delivery_cost()

        # 리뷰 및 별점 가져오기
        reviews, stars = get_reviews(store_name)

        # 리뷰이벤트 유무 가져오기
        isReviewEvent = get_review_event()

        # 뒤로가기
        driver.back()
        driver.implicitly_wait(3)
        print(num + 1, '뒤로가기 완료')

        # 작업 끝
        print(f'finish {store_name} job completed')

    else:
        print(f"{store_name} : Currently not providing service - job failed")

    # 반환
    return store_name, reviews, stars, isClean, delivery_cost, least_cost, isReviewEvent