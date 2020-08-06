from selenium import webdriver

driver = webdriver.Chrome('./Tool/chromedriver_win32/chromedriver') # Chromedriver 위치지정
# driver = webdriver.PhantomJS('‪./Tool/phantomjs-2.1.1-windows/bin/phantomjs') # PhantomJS의 위치지정
driver.implicitly_wait(3) # 웹자원 로드를 위한 대기시간 3초
driver.get('https://nid.naver.com/nidlogin.login')