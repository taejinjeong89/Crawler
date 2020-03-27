from selenium import webdriver
from Crawler_Functions import crawl_dict_function

## Set-up Chunk

cd = crawl_dict_function
domain = open('./Domain_English.txt', 'r')
domain = domain.read().splitlines()
## 크롬옵션입니다.
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# main_dir = os.getcwd()

## Crawl Part

for word in domain:
    ## 리눅스 서버에서는 디렉토리를 이런식으로 잡아주는 게 좋을겁니다.
    # main_dir = os.path.join(main_dir, word)
    # if not os.path.exists(main_dir):
    #     os.mkdir(main_dir)
    main_dir = './data_line/ENTH'
    main_dir = main_dir + '/' + str(domain.index(word) + 1)
    data = open(main_dir, 'a', encoding='UTF-8')
    browser = webdriver.Chrome()
    ## 언어는 이것들 중에 하나 쓰시면 됩니다. 'en', 'th'
    ## 라인딕셔너리는 영어가 기본 도메인입니다.
    cd.get_into_line_dict(browser,'th', word)
    ## 라인은 100페이지가 끝입니다.
    for k,_ in enumerate(range(100), start=1):
        try:
            cd.write_contents_line(browser,data,word,'th',k)
            print("[downloaded pages]: " + '\t' + word + '\t' + str(k))
            try:
                cd.wait(browser, xpath='//*[@id="example_paginate"]/a[' + str(k + 1) + ']', slp=5)
                cd.get_page(browser, xpath='//*[@id="example_paginate"]/a[' + str(k + 1) + ']').click()
            except:
                print("The last page of the word is " + '\t' + str(k))
                break
        except Exception as e:
            print(e)
            break

    browser.quit()