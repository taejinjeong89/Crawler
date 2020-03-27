from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import secrets
from selenium.webdriver.common.keys import Keys

class crawl_dict_function:

    def get_page(browser, selector = None, xpath = None, class_name = None):
        if selector:
            try:
                page_tag = browser.find_element_by_css_selector(selector)
                return (page_tag)
            except:

                page_tag = None
                return (page_tag)
        if xpath:
            try:
                page_tag = browser.find_element_by_xpath(xpath)
                page_tag = page_tag
                return (page_tag)
            except:
                page_tag = None
                return (page_tag)
        if class_name:
            try:
                page_tag = browser.find_elements_by_class_name(class_name)
                return (page_tag)
            except:
                page_tag = None
                return (page_tag)

    def get_len(browser, cls):
        try:
            length = len(browser.find_elements_by_class_name(cls))
            return(length)
        except:
            length = 0
            return(length)

    def wait(browser, selector = None, xpath = None, slp = 3):
        if selector:
            WebDriverWait(browser, slp).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        if xpath:
            WebDriverWait(browser, slp).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def jump(browser, selector, scroll_up=False):
        target = browser.find_element_by_css_selector(selector)
        browser.execute_script("arguments[0].scrollIntoView();", target)
        if scroll_up:
            browser.execute_script("window.scrollBy(0,-400);")

    def get_into_naver_dict(browser, language, target_word):
        check_language = ['en', 'ko', 'hanja', 'ja', 'zh', 'fr', 'es', 'de', 'vi']
        if check_language.count(language) == 0:
            print("The language needs to be one of the following")
            print(check_language)
        sleep(3)
        if language == 'hanja':
            url_dict = 'https://hanja.dict.naver.com/'
        elif language in ['fr', 'es', 'de', 'vi']:
            url_dict = 'https://dict.naver.com/' + language + 'kodict/#/main'
        else:
            url_dict = 'https://' + language + '.dict.naver.com/#/main'
        sleep(3)
        browser.get(url_dict)
        browser.maximize_window()
        sleep(3)
        type_word = browser.find_element_by_xpath('//*[@id="ac_input"]')

        # if browser.find_element_by_xpath('//*[@id="wrap"]/div[4]/div[1]/button[1]'):
        #     browser.find_element_by_xpath('//*[@id="wrap"]/div[4]/div[1]/button[1]').click()
        try:
            browser.find_element_by_xpath('//*[@id="wrap"]/div[4]/div[1]/button[1]').click()
        except:
            pass
        try:
            type_word.send_keys(target_word)
            sleep(3)
            browser.find_element_by_xpath('//*[@id="searchArea"]/div/button').click()
        except:
            print("Error in typing target_word into Dictionary" + '\t' + target_word)
            pass
        sleep(3)
        if language in ['vi', 'es', 'de', 'fr', 'ko']:
            browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div/div/a[5]').click()
        else:
            browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div/div/a[4]').click()
        sleep(3)

        #번역문 있는 예문만 보기
        try:
            if browser.find_elements_by_class_name('inp_label_check'):
                browser.find_element_by_xpath('//*[@id="searchPage_example"]/div[1]/div/span[5]/label').click()
        except:
            pass
        sleep(3)

        #예문 더보기
        try:

            if browser.find_element_by_xpath('//*[@id="searchPage_example_more"]'):
                browser.find_element_by_xpath('//*[@id="searchPage_example_more"]').click()
        except:
            pass

        # 후리가나
        if language == 'ja':
            sleep(3)
            try:
                if browser.find_elements_by_class_name('is-shown-furigana'):
                    browser.find_element_by_css_selector('#content > div.option_area > div.sort_option > div > div > div > div.pinyin_generator > label').click()
            except:
                pass

    # def save_data(dir, mode='a', encoding='UTF-8'):
    #     data = open(dir, mode, encoding=encoding)
    #     return (data)


    def get_into_line_dict(browser, language, target_word):
        if language in ['th', 'zh']:
            url = 'https://dict.naver.com/linedict/en' + language + 'dict/#/encn/home'
        else:
            print("Language should be one of the following: 'th', 'zh'")
        browser.get(url)
        browser.maximize_window()
        sleep(3)
        browser.find_element_by_xpath('//*[@id="ac_form"]/fieldset/ul/li[2]/span/span').click()
        sleep(3)
        type_word = browser.find_element_by_xpath('//*[@id="ac_input"]')
        sleep(3)
        type_word.send_keys(target_word)
        sleep(3)
        try:
            browser.find_element_by_xpath('//*[@id="ac_form"]/fieldset/div/a').click()
        except:
            print("Error in typing target_word into Dictionary" + '\t' + target_word)
            pass

    def write_contents_line(browser, data, target_word, language, k, cls = 'exam'):
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'exam')))
        except :
            pass
        length = len(browser.find_elements_by_class_name(cls))
        if length == 0:
            print("No corpus on the page")
        else:
            for l, _ in enumerate(range(length), start=1):
                try:
                    language1 = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/ul/li[' + str(l) + ']/div/p[1]')[0].text
                    language2 = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/ul/li[' + str(l) + ']/div/p[2]')[0].text
                    data.write(language1 + '\t' + language2 + '\t' + "EN" + language.upper() + '\t' + target_word + '\t' + str(k) + '\n')
                    # data.write(target_word + '\t' + str(k) + '\t' + language1 + '\t' + language2 + '\n')
                except Exception as exc:
                    print('Error in scraping contents' + '\t' + exc)
                    pass

    def write_contents_naver(browser, data, target_word, language, k, trans = 'Not Specified', cls = 'row'):
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row')))
        except :
            pass
        length = len(browser.find_elements_by_class_name(cls))
        if language == 'zh':
            num = [1, 3]
        else:
            num = [1, 2]
        if length == 0:
            print("No corpus on the page")
        else:
            if language in ['vi', 'es', 'de', 'fr']:
                for l, _ in enumerate(range(length), start=1):
                    try:
                        language1 = browser.find_elements_by_xpath('//*[@id="searchPage_example"]/div/div[' + str(l) + ']/div[' + str(num[1]) + ']/p')[0].text
                        language2 = browser.find_elements_by_xpath('//*[@id="searchPage_example"]/div/div[' + str(l) + ']/div[' + str(num[0]) + ']/p')[0].text
                        data.write(language1 + '\t' + language2 + '\t' + trans + '\t' + target_word + '\t' + str(k) + '\n')
                        # data.write(target_word + '\t' + str(k) + '\t' + language1 + '\t' + language2 + '\n')
                    except Exception as exc:
                        print('Error in scraping contents' + '\t' + exc)
                        pass
            else:
                for l, _ in enumerate(range(length), start=1):
                    try:
                        language1 = browser.find_elements_by_xpath('//*[@id="searchPage_example"]/div[2]/div[' + str(l) + ']/div[' + str(num[1]) + ']/p')[0].text
                        language2 = browser.find_elements_by_xpath('//*[@id="searchPage_example"]/div[2]/div[' + str(l) + ']/div[' + str(num[0]) + ']/p')[0].text
                        data.write(language1 + '\t' + language2 + '\t' + trans + '\t' + target_word + '\t' + str(k) + '\n')
                        # data.write(target_word + '\t' + str(k) + '\t' + language1 + '\t' + language2 + '\n')
                    except Exception as exc:
                        print('Error in scraping contents' + '\t' + exc)
                        pass

class crawl_youtube_function:

    def get_page(browser, selector = None, xpath = None, class_name = None):
        if selector:
            try:
                page_tag = browser.find_element_by_css_selector(selector)
                return (page_tag)
            except:

                page_tag = None
                return (page_tag)
        if xpath:
            try:
                page_tag = browser.find_element_by_xpath(xpath)
                page_tag = page_tag
                return (page_tag)
            except:
                page_tag = None
                return (page_tag)
        if class_name:
            try:
                page_tag = browser.find_elements_by_class_name(class_name)
                return (page_tag)
            except:
                page_tag = None
                return (page_tag)

    def get_len(browser, cls):
        try:
            length = len(browser.find_elements_by_class_name(cls))
            return(length)
        except:
            length = 0
            return(length)

    def wait(browser, selector = None, xpath = None, slp = 3):
        if selector:
            WebDriverWait(browser, slp).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        if xpath:
            WebDriverWait(browser, slp).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def jump(browser, selector, scroll_up=False):
        target = browser.find_element_by_css_selector(selector)
        browser.execute_script("arguments[0].scrollIntoView();", target)
        if scroll_up:
            browser.execute_script("window.scrollBy(0,-400);")

    def exit_pop_up(browser):
        z = 0
        try:
            browser.find_element_by_css_selector('ytd-button-renderer.ytd-mealbar-promo-renderer:nth-child(1) > a:nth-child(1) > paper-button:nth-child(1)').click()
        except:
            z += 1
            pass
        try:
            browser.find_element_by_css_selector('ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > paper-button:nth-child(1) > yt-formatted-string:nth-child(1)').click()
        except:
            z += 1
            pass
        try:
            browser.find_element_by_css_selector('yt-icon.ytd-single-option-survey-renderer').click()
        except:
            z += 1
            pass
        if z < 3:
            print("Closed Pop up")

    def scrolldown(browser, interval = 700, xpath = None):
        x = 0
        while browser.find_element_by_xpath(xpath):
            y = x + interval
            scroll_range = 'window.scrollTo({}, {});'.format(x, y)
            browser.execute_script(scroll_range)
            sleep(3)

    def get_title(browser, data, check, r, selector = None, xpath = None):
        if selector:
            data.write('Title - ' + str(r) + '\t' + browser.find_element_by_css_selector(selector).text + '\n')
            check.append(browser.find_element_by_css_selector(selector).text)
        if xpath:
            data.write('Title - ' + str(r) + '\t' + browser.find_element_by_xpath(xpath).text + '\n')
            check.append(browser.find_element_by_xpath(xpath).text)

    def get_keyword(browser, data, r, selector = None, xpath = None):
        if selector:
            data.write('Keywords - ' + str(r) + '\t' + browser.find_element_by_css_selector(selector).text + '\n')
        if xpath:
            data.write('Keywords - ' + str(r) + '\t' + browser.find_element_by_xpath(xpath).text + '\n')

    def auto_play_off(browser):
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#toggleButton')))
            browser.find_element_by_css_selector('#toggleButton').click()
        except:
            pass

    def random_click(browser, check_title, range):
        check = []
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        sleep(2)
        i = 3
        while i < 13:
            jump_title = 'ytd-compact-video-renderer.style-scope:nth-child(' + str(i) + ') > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h3:nth-child(1)'
            try:
                check.append(browser.find_element_by_css_selector(jump_title).text)
            except:
                pass
            i += 1

        while True:
            try:
                rand = list(range)
                rand_num = secrets.choice(rand)
                rand_jump = 'ytd-compact-video-renderer.style-scope:nth-child(' + str(rand_num) + ') > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h3:nth-child(1) > span:nth-child(2)'
                browser.find_element_by_css_selector(rand_jump).click()
                sleep(5)
                if check_title.count(browser.find_element_by_css_selector('yt-formatted-string.ytd-video-primary-info-renderer:nth-child(1)').text) == 0:
                    break
                else:
                    print("Skipping duplicate page")
                    pass
            except:
                pass

    def write_replies(browser, data, target):

        sleep(3)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        sleep(3)
        # Open replies and append data
        k = 1
        reply_length = 0
        while k < 5:
        # while True:
            # Set up GUIs
            target_selector1 = 'ytd-comment-thread-renderer.style-scope:nth-child(' + str(k) + ') > ytd-comment-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)'
            target_selector2 = 'ytd-comment-thread-renderer.style-scope:nth-child(' + str(k + 1) + ') > ytd-comment-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)'
            re_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/div/ytd-comment-replies-renderer/div[1]/ytd-button-renderer[1]/a/paper-button/yt-icon'
            more_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/div/ytd-comment-replies-renderer/div[1]/div/div[2]/yt-next-continuation/paper-button/yt-icon'
            main_comment_selector = 'ytd-comment-thread-renderer.style-scope:nth-child(' + str(k) + ') > ytd-comment-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ytd-expander:nth-child(2) > div:nth-child(1) > yt-formatted-string:nth-child(2)'
            open_main_comment_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/ytd-comment-renderer/div[1]/div[2]/ytd-expander/paper-button[2]/span'

            # Open Replies
            try:
                browser.execute_script("arguments[0].scrollIntoView();",browser.find_element_by_css_selector(target_selector1))
                browser.execute_script("window.scrollBy(0,-400);")
            except Exception as e:
                print(e)
                print("Crawling Done")
                break
            try:
                browser.find_element_by_css_selector('ytd-button-renderer.ytd-mealbar-promo-renderer:nth-child(1) > a:nth-child(1) > paper-button:nth-child(1)').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > paper-button:nth-child(1) > yt-formatted-string:nth-child(1)').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('yt-icon.ytd-single-option-survey-renderer').click()
            except:
                pass
            try:
                browser.find_element_by_xpath(open_main_comment_xpath).click()
            except:
                pass
            # Crawl main comment
            main_text = browser.find_element_by_css_selector(main_comment_selector).text
            main_text = main_text.split('\n')
            for i,_ in enumerate(range(len(main_text))):
                if len(main_text[i]) > 0:
                    main_text[i] = main_text[i].strip()
                    data.write(target + '\t' + str(k) + '-' + str(0) + '-' + str(i) + '\t' + main_text[i] + '\n')
            sleep(3)

            # Open re-replies

            WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, re_xpath)))
            try:
                browser.find_element_by_css_selector('ytd-button-renderer.ytd-mealbar-promo-renderer:nth-child(1) > a:nth-child(1) > paper-button:nth-child(1)').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > paper-button:nth-child(1) > yt-formatted-string:nth-child(1)').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('yt-icon.ytd-single-option-survey-renderer').click()
            except:
                pass
            browser.find_element_by_xpath(re_xpath).click()
            while True:
                try:
                    sleep(3)
                    WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, target_selector2)))
                    browser.execute_script("arguments[0].scrollIntoView();",browser.find_element_by_css_selector(target_selector2))
                    browser.execute_script("window.scrollBy(0,-400);")
                    WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, more_xpath)))
                    browser.find_element_by_xpath(more_xpath).click()
                except:
                    break
            for i, _ in enumerate(range(len(browser.find_elements_by_class_name('style-scope ytd-comment-renderer')))):
                open_reply_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/div/ytd-comment-replies-renderer/div[1]/div/div[1]/ytd-comment-renderer[' + str(i) + ']/div[1]/div[2]/ytd-expander/paper-button[2]/span'
                try:
                    browser.find_element_by_xpath(open_reply_xpath).click()
                except:
                    pass

            # Append Replies
            for l,_ in enumerate(range(len(browser.find_elements_by_class_name('style-scope ytd-comment-renderer')) - reply_length), start = 1):
                h = 1
                try:
                    if browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/div/ytd-comment-replies-renderer/div[1]/div/div[1]/ytd-comment-renderer[' + str(l) + ']/div[1]/div[2]/ytd-expander/div/yt-formatted-string[2]/span[' + str(h) + ']'):
                        while True:
                            try:
                                reply_text = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[' + str(k) + ']/div/ytd-comment-replies-renderer/div[1]/div/div[1]/ytd-comment-renderer[' + str(l) + ']/div[1]/div[2]/ytd-expander/div/yt-formatted-string[2]/span[' + str(h) + ']'
                                reply_text = browser.find_element_by_xpath(reply_text).text
                                if len(reply_text) > 0:
                                    reply_text = reply_text.strip()
                                    data.write(target + '\t' + str(k) + '-' + str(l) + '-' + str(h) + '\t' + reply_text + '\n')
                                h += 1
                            except:
                                break
                except:
                    try:
                        reply_text = 'ytd-comment-thread-renderer.style-scope:nth-child(' + str(k) + ') > div:nth-child(2) > ytd-comment-replies-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > ytd-comment-renderer:nth-child(' + str(l) + ') > div:nth-child(1) > div:nth-child(2) > ytd-expander:nth-child(2) > div:nth-child(1)'
                        reply_text = browser.find_element_by_css_selector(reply_text).text
                        reply_text = reply_text.strip()
                        data.write(target + '\t' + str(k) + '-' + str(l) + '-' + str(0) + '\t' + reply_text + '\n')
                    except:
                        break

            reply_length = len(browser.find_elements_by_class_name('style-scope ytd-comment-renderer'))
            print("Replies Done" + '\t' + target + '\t' + str(k))
            k += 1