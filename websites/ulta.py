import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException

    
class Ulta(Website):
    def go_search(self, driver, pid):
        """ Returns the search links for Ulta.com """
        return [self.search_url(website, pid)]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Ulta.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from Ulta.com. """
        product_table = driver.find_element_by_class_name("productsTable")
        products = product_table.find_elements_by_class_name("productTitle")
        product_ids = []
        for i in products:
            element_link = i.find_element_by_xpath(".//a").get_attribute("href")
            splitters = element_link.split("%")
            skuID = splitters[splitters.index("3fskuId")+1][2:]
            productID = splitters[splitters.index("26productId")+1][2:]
            productlist.append(skuID+","+productID)

    def go_product_search_next(self, driver):
        """ Not needed for Ulta.com """
        raise NoSuchElementException

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Ulta.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a Ulta.com product page. 
        Product size information not availible on Ulta.com.  """
        sku = driver.find_element_by_id("sku").text
        product_name_init = driver.find_element_by_id("prodDetailHeader").text
        product_name = " ".join(product_name_init.replace(sku, "").strip().split("\n"))
        return product_name, "", ""

    def go_product_ingredients_page(self, driver, product_id):
        """ Changes to the Ulta.com ingredients panel. """
        try:
            main_frame = driver.find_element_by_id("pdtabs")
            tabs = main_frame.find_elements_by_xpath(".//li")
            for tab in tabs:
                if tab.text == "Ingredients":
                    tab.click()
        except NoSuchElementException:
            pass

    def get_product_ingredients(self, driver):
        """ Gets the ingredients from Ulta.com ingredients panel. """
        try:
            return driver.find_element_by_id("ingredients").find_element_by_class_name("detailsText").text
        except NoSuchElementException:
            return ""

    def go_product_reviews_page(self, driver, product_id, website):
        """ Not needed for Ulta.com """
        pass

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Ulta.com product page. """
        try:
            reviewcount = driver.find_element_by_class_name("pr-snapshot-average-based-on-text").text
            reviewsplit = reviewcount.split()
            for i in reviewsplit:
                try:
                    done = int(i)
                except ValueError:
                    pass
            return str(done)
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of Drugstore.com product reviews. """
        wait = WebDriverWait(driver,10)
        driver.find_element_by_css_selector("span.pr-page-next > a").click()
        time.sleep(1)
        wait.until(lambda driver: driver.find_element_by_class_name("pr-page-count"))