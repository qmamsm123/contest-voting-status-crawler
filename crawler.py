from yattag import Doc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_urls(driver: webdriver.Chrome):
  driver.get('https://store.whale.naver.com/event/wallpaper-contest/')
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'main__entries__btn'))).click()
  entry_list = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'main__contest__list')))
  entries = entry_list.find_elements(by=By.CSS_SELECTOR, value='p.main__contest__ttl > a')
  urls = [entry.get_attribute('href') for entry in entries]
  return urls

def get_page(driver: webdriver.Chrome, page_url):
  driver.get(page_url)
  try:
    title_text = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detail__head__ttl > h1'))).text
    developer_text = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detail__head__ttl > p'))).text
    like_count = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'like_count'))).text
    user_count = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'user_count'))).text
    return (title_text, developer_text, int(like_count.replace(',', '')), int(user_count.replace(',', '')), page_url)
  except:
    print('cannot load the page.', page_url)
    return None

def get_entries(driver: webdriver.Chrome):
  entries = []
  urls = get_urls(driver)
  for i in range(len(urls)):
    print(f'{i+1}/{len(urls)}')
    page = get_page(driver, urls[i])
    if page == None:
      return None
    entries.append(page)
  return entries

def reform_entries(entries: list):
  size = len(entries)
  entries.sort(reverse=True, key=lambda e: e[2])
  for i in range(size):
    entries[i] = (i + 1, (i + 1) / size * 100) + entries[i]
  return entries

def write_result(entries: list):
  doc, tag, text = Doc().tagtext()
  with tag('html'):
    with tag('body'):
      with tag('table'):
        with tag('tr'):
          with tag('th'):
            text('등수')
          with tag('th'):
            text('퍼센트')
          with tag('th'):
            text('작품명/작가')
          with tag('th'):
            text('좋아요 수')
          with tag('th'):
            text('등록 사용자 수')
            for entry in entries:
              number, percent, title_text, developer_text, like_count, user_count, page_url = entry
              if title_text == 0:
                continue
              with tag('tr'):
                with tag('th'):
                  text(number)
                with tag('th'):
                  text('{0:2.2f}%'.format(percent))
                with tag('th'):
                  with tag('p'):
                    with tag('a', href=page_url):
                      text(title_text)
                    text(' ' + developer_text)
                with tag('th'):
                  text(like_count)
                with tag('th'):
                  text(user_count)
  return doc.getvalue()

def main():
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  entries = get_entries(driver)
  if entries == None:
    return
  entries = reform_entries(entries)
  driver.quit()

  report = write_result(entries)
  file = open('result.html', mode='w', encoding='utf-8')
  file.write(report)
  file.close()

if __name__ == '__main__':
  main()