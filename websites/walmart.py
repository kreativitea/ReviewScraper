import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class Walmart(Website):
    def go_search(self, driver, input):
        """ Returns the search links for Walmart.com """
        return [self.search_url(website, input)]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Walmart.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds prodcutids to the productlist on Walmart.com """
        frame = driver.find_element_by_id("shelfDiv")
        items = frame.find_elements_by_class_name("item")
        for i in items:
            pid = i.find_element_by_tag_name("a").get_attribute("href").split("/")[-1]
            productlist.append(pid)

    def go_product_search_next(self, driver):
        """ Goes to the next page of products on the product search page on Walmart.com """
        frame = driver.find_element_by_class_name("SPPagination")
        next = frame.find_element_by_class_name("next")
        try:
            next.find_element_by_tag_name("a")
            next.click()
        except NoSuchElementException:
            raise NoSuchElementException # if no next page is found

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Walmart.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)
       
    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a product page. 
        Product name, product size (number), product size (units) """
        return driver.find_element_by_class_name("productTitle").text, "", ""

    def go_product_ingredients_page(self, driver, product_id):
        """ Not needed on Walmart.com """
        pass

    def get_product_ingredients(self, driver):
        """ Gets the ingredients from the Walmart.com product page. """
        try:
            ingredients = driver.find_element_by_class_name("ProductIngredients").text
            return ingredients
        except NoSuchElementException:
            return ""

    def go_product_reviews_page(self, driver, product_id, website):
        """ Goes to the reviews panel on the Walmart.com product page. """
        link = self.product_url("WalmartReview", product_id)
        self.go_and_assert(driver, link, website)
        self.show_full_reviews(driver, "class", "BVDILinkSpan", "read full review")

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Walmart.com product page. """
        try:
            frame = driver.find_element_by_class_name("BVRRRatingSummaryLinkReadWithCountID")
            return frame.find_element_by_class_name("BVRRNumber").text
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of product reviews on the Walmart.com product page. """
        pagination = driver.find_element_by_class_name("BVRRPager")
        next = pagination.find_element_by_class_name("BVRRNextPage").click()
        self.show_full_reviews(driver, "class", "BVDILinkSpan", "read full review")
            