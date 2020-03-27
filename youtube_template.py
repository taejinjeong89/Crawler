from selenium import webdriver
from Crawler_Functions import crawl_youtube_function


## Set-up Chunk

cy = crawl_youtube_function
# domain_idol = open('./idol_list.txt', 'r')
# domain_idol = domain_idol.read().splitlines()
# main_dir = os.getcwd()

#test
domain_idol = ['IU', 'BTS', 'Zico']

##

## Crawl Part
for r,_ in enumerate(range(2), start=1):
    for idol in domain_idol:
        # main_dir = os.path.join(main_dir, idol)
        # if not os.path.exists(main_dir):
        #     os.mkdir(main_dir)
        main_dir = './data_youtube/'
        url = 'https://www.youtube.com/results?search_query=' + idol + '&sp=CAM%253D'
        try:
            check_du = open(main_dir + 'duplication_check.txt', 'r', encoding='UTF-8').read().splitlines()
        except Exception as e:
            print(e)
            print("Failed to call duplication_check.txt file")
            pass
        browser = webdriver.Firefox()
        try:
            browser.get(url)
            browser.maximize_window()
        except:
            print("Failed to open page")
        try:
            cy.wait(browser,selector='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string',slp = 5)
        except:
            pass

        title = browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text

        if cy.get_page(browser,selector='html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-search.style-scope.ytd-page-manager div#container.style-scope.ytd-search ytd-two-column-search-results-renderer.style-scope.ytd-search div#primary.style-scope.ytd-two-column-search-results-renderer ytd-section-list-renderer.style-scope.ytd-two-column-search-results-renderer div#contents.style-scope.ytd-section-list-renderer ytd-item-section-renderer.style-scope.ytd-section-list-renderer div#contents.style-scope.ytd-item-section-renderer ytd-search-pyv-renderer.style-scope.ytd-item-section-renderer div#contents.style-scope.ytd-search-pyv-renderer ytd-promoted-video-renderer.style-scope.ytd-search-pyv-renderer div#text-container.style-scope.ytd-promoted-video-renderer a#endpoint.yt-simple-endpoint.style-scope.ytd-promoted-video-renderer div#meta.style-scope.ytd-promoted-video-renderer div#title-wrapper.style-scope.ytd-promoted-video-renderer h3#video-title.style-scope.ytd-promoted-video-renderer'):
            if check_du.count(cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text) == 0:
                try:
                    cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').click()
                    skip = False
                except Exception as e:
                    print(e)
                    print("Error in getting into the Page - 1")
                    skip = True
                    pass
                print(cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text)
            else:
                print("Skipped Duplicated Page : " + cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text)
                skip = True
        else:
            if check_du.count(cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text) == 0:
                try:
                    cy.get_page(browser, selector='ytd-video-renderer.style-scope:nth-child(' + str(r) + ') > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(2) > yt-formatted-string:nth-child(1)').click()
                    skip = False
                except Exception as e:
                    print(e)
                    print("Error in getting into the Page - 2")
                    skip = True
                    pass
            else:
                print("Skipped Duplicated Page : " + cy.get_page(browser,xpath='/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(r) + ']/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text)
                skip = True

        if not skip:
            print("Current Page: " + title)

            data_title = open(main_dir + idol + '/Titles', 'a', encoding='UTF-8')
            data_title.write(idol + '\t' + str(r) + '\t' + str(r) + '\t' + title + '\n')
            data_title.close()

            check_title = open(main_dir + 'duplication_check.txt', 'a', encoding='UTF-8')
            check_title.write(title + '\n')
            check_title.close()

            data = open(main_dir + idol + '/' + str(r), 'a', encoding='UTF-8')
            cy.auto_play_off(browser)
            cy.write_replies(browser, data, idol)
            data.close()
        else:
            pass

        browser.quit()