import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()


class PromoSpider(scrapy.Spider):
    name = 'promo'

    start_urls = [
        'https://www.nintendo.com/pt-br/store/games/?p=1&sort=df&f=topLevelFilters&topLevelFilters=Promo%C3%A7%C3%B5es']

    def parse(self, res):
        driver.get(
            'https://www.nintendo.com/pt-br/store/games/?p=1&sort=df&f=topLevelFilters&topLevelFilters=Promo%C3%A7%C3%B5es')


        # driver.execute_script("window.scrollTo(0, 650)")

        try:
            while driver.find_element(By.CLASS_NAME, "LoadMoreSectionstyles__StyledLoadMoreButton-sc-y6xsxn-0"):

                element = driver.find_element(
                    By.CLASS_NAME, "LoadMoreSectionstyles__StyledLoadMoreButton-sc-y6xsxn-0")

                actions = ActionChains(driver)
                actions.move_to_element(element).perform()

                element.click()

        except:
            fullPage = scrapy.Selector(text=driver.page_source)
            for games in fullPage.css('div.BasicTilestyles__Container-sc-sh8sf3-0'):
                discount = int(
                    games.css('div.Pricestyles__SaleTagText-sc-afjfk5-7::text').get()[1:-1])

                if discount >= 70:
                    yield {
                        'name': games.css('h3.BasicTilestyles__Title-sc-sh8sf3-11::text').get(),
                        'img': games.css('img.Imagestyles__CloudinaryImage-sc-1oi2gnz-1').xpath('@src').get(),
                        'link': games.css('a.BasicTilestyles__Tile-sc-sh8sf3-15').attrib['href'],
                        'discount': games.css('div.Pricestyles__SaleTagText-sc-afjfk5-7::text').get(),
                        'price': games.css('span.Pricestyles__SalePrice-sc-afjfk5-9::text').get().replace('\u00a0', '')
                    }

            driver.quit()
