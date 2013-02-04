import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class Target(Website):
    def go_search(self, driver, pid):
        """ Returns the search links for Target.com """
        return [self.search_url(website, pid)]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Target.com """
        driver.get(searchlink)
        self.assertion(website, driver)
        
    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from Target.com. """
        main_frame = driver.find_element_by_class_name("productsListView")
        product_element = main_frame.find_elements_by_class_name("productTitle")
        id_list = []
        for i in product_element:
            link = i.find_element_by_xpath('.//a').get_attribute('href')
            id_list.append(link.split('/')[-1])
        productlist.extend(id_list)
            
    def go_product_search_next(self, driver):
        """ Gets the next page of products on the Target.com search results page. 
        Raises NoSuchElementException if not found. """
        pagination = driver.find_element_by_class_name("pagination2")
        pagination.find_element_by_class_name("next").click()

    ## The following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Target.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a Target.com product page. 
        product name, product size (number), product size (units) """
        product_name = driver.find_element_by_class_name("product-name").text
        try:
            item_details = driver.find_element_by_id("item-details").find_element_by_class_name("content")
            details_specs = item_details.find_elements_by_xpath(".//li")
            for i in details_specs:
                if "Capacity" in i.text:
                    size, units = i.text.split(":")[-1].split()
        except NoSuchElementException:
            size, units = "", ""
        return product_name, size, units
        
    def go_product_ingredients_page(self, driver, product_id):
        """ Not needed for Target.com """
        pass

    def get_product_ingredients(self, driver):
        """ Not needed for Target.com """
        pass

    def go_product_reviews_page(self, driver, product_id, website):
        """ Not needed for Target.com """
        pass

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Target.com product page. """
        try:
            return driver.find_element_by_id("ratings-summary").text.split()[0]
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Not needed for Target.com """
        pass