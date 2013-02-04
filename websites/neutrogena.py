import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class Neutrogena(Website):
    def go_search(self, driver, pid):
        """ Returns the search links for Neutrogena.com """
        if "Neutrogena" in pid:
            return [self.search_url(website, pid)]
        else:
            return []

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Neutrogena.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from Neutrogena.com. """
        main_table = driver.find_element_by_class_name("contenttopbg")
        # currently, the chrome driver doesn't allow getting via 'product' 
        products = main_table.find_elements_by_class_name("thumbheadername")
        product_ids = []
        for product in products:
            link_init = product.find_element_by_xpath(".//a").get_attribute("href")
            product_id = link_init.replace("http://www.neutrogena.com/product/","").split(".do?")[0]
            productlist.append(product_id)
    
    def go_product_search_next(self, driver):
        """ Raises NoSuchElementException (no 'next' function on neutrogena.com) """
        raise NoSuchElementException
       
    ## The following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Neutrogena.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a Neutrogena.com product page. 
        product name, product size (number), product size (units) """
        name = driver.find_element_by_class_name("detailheadernew").text
        try:
            size_init = driver.find_element_by_class_name("ProductSize").text.split()
            size = size_init[0]
            units = " ".join(size_init[1:])
        except NoSuchElementException:
            size, units = "", ""
        return name, size, units

    def go_product_ingredients_page(self, driver, product_id):
        """ Changes to the Neutrogena.com ingredients panel. """
        tab_list = driver.find_element_by_class_name("infoTabSpacer").find_element_by_xpath("..")
        tabs = tab_list.find_elements_by_xpath(".//td")
        for i in tabs:
            if "ingredients" in i.find_element_by_xpath(".//img").get_attribute("src"):
                i.click()

    def get_product_ingredients(self, driver):
        """ Gets the ingredients from Neutrogena.com ingredients panel. """
        frame = driver.find_element_by_id('tabContent')
        italics = frame.find_element_by_xpath(".//i").text
        ingredients = frame.text.replace(italics,"").strip()
        return ingredients
    
    def go_product_reviews_page(self, driver, product_id, website):
        """ Changes a page to the Neutrogena.com reviews panel. """
        tab_list = driver.find_element_by_class_name("infoTabSpacer").find_element_by_xpath("..")
        tabs = tab_list.find_elements_by_xpath(".//td")
        for i in tabs:
            if "customerreviews" in i.find_element_by_xpath(".//img").get_attribute("src"):
                i.click()

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Drugstore.com product page. """
        try:
            frame = driver.find_element_by_class_name("BVRRRatingSummaryLinks")
            return frame.find_element_by_class_name("BVRRNumber").text
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of Neutrogena.com product reviews. """
        pager = driver.find_element_by_class_name("BVRRPager")
        pager.find_element_by_name("BV_TrackingTag_Review_Display_NextPage").click()
