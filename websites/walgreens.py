import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException

class Walgreens(Website):
    def go_search(self, driver, input):
        """ Returns the search links for Walgreens.com """
        return [self.search_url(website, input)]
    
    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Walgreens.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds prodcutids to the productlist on Walgreens.com """
        frame = driver.find_element_by_id("productGrid")
        products = frame.find_elements_by_class_name("product-container")
        for i in products:
            i_link = i.find_element_by_class_name("SearchLinkBold").get_attribute('href')
            pid = self.page_splitter(i_link,"ID=","-product")
            productlist.append(pid)

    def go_product_search_next(self, driver):
        """ Gets the next page of products on Walgreens.com """
        pagination = driver.find_element_by_class_name("pagination")
        next = pagination.find_element_by_xpath('.//a[@title="Next Page"]')
        # Raises NoSuchElementException if not present
        next.click()

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Walgreens.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)
       
    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a product page. 
        Product name, product size (number), product size (units) """
        # get name
        heading = driver.find_element_by_id("header_bar")
        name = heading.find_element_by_tag_name("h1").text
        # get size and units
        sizeframe = driver.find_element_by_class_name("vpd_overview")
        sizecandidates = sizeframe.find_elements_by_tag_name("p")
        for i in sizecandidates:
            if 'Size' in i.text:
                size = i.text.split()
                size, units = size[1], " ".join(size[2:])
        return name, size, units

    def go_product_ingredients_page(self, driver, product_id):
        """ Goes to the reviews panel on the Walgreens.com product page. """
        frame = driver.find_element_by_class_name("tab-container")
        try:
            frame.find_element_by_id("tab-ingredients").click()
        except NoSuchElementException:
            return None
        
    def get_product_ingredients(self, driver):
        """ Gets the ingredients from the Walgreens.com product page. """
        frame = driver.find_element_by_class_name("tab-container")
        try:
            return frame.find_element_by_id("ingredients-content").text
        except NoSuchElementException:
            return ""

    def go_product_reviews_page(self, driver, product_id, website):
        """ Not needed for Walgreens.com """
        pass

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Walgreens.com product page. """
        try:
            frame = driver.find_element_by_class_name("BVRRRatingSummaryLink")
            return frame.find_element_by_class_name("BVRRNumber").text
        except NoSuchElementException:
            return "0"
    
    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of product reviews on the Walgreens.com product page. """
        pagination = driver.find_element_by_class_name("BVRRPager")
        pagination.find_element_by_class_name("BVRRNextPage").click()
