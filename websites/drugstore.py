import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class Drugstore(Website):
    ## The following functions deal with the search page.
    def go_search(self, driver, pid):
        """ Returns the search links for Drugstore.com  """
        return [self.search_url('Drugstore',pid)]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Drugstore.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        # this is bad design
        """ Adds products to the productlist, given a search result page from Drugstore.com. """
        frame = driver.find_element_by_class_name("GlobalPlistAdTemplateWrapperLeftTD")
        products = frame.find_elements_by_class_name("oesLink")
        for i in products:
            productlist.append(i.get_attribute('href').split('/')[4].split('?')[0])

    def go_product_search_next(self, driver):
        """ Gets the next page of products on the Drugstore.com search results page. 
            Raises NoSuchElementException if not found."""
        try:
            current = driver.find_elements_by_class_name("PaginationActiveLink")
            next_page = driver.find_elements_by_link_text(str(int(current[0].text)+1))
            next_page[0].click()
            self.assertion(website, driver)
        except IndexError:
            raise NoSuchElementException
        
    ## The following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a Drugstore.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a Drugstore.com product page. """
        # get raw strings
        name_init = driver.find_element_by_class_name("captionText").text
        size_init = driver.find_element_by_class_name("captionSizeText").text
        # process strings
        name = name_init[:-len(size_init) - 1]
        size = size_init.split("(")[0].strip()
        size, units = size.split(" ", 1)
        return name, size, units

    def go_product_ingredients_page(self, driver, product_id):
        """ Changes to the Drugstore.com ingredients panel. """
        try:
            driver.find_element_by_css_selector("#btningredientsPDetail").click()
            self.wait_for_element(driver,"id",'TblProdForkIngredients')
        except NoSuchElementException:
            pass
    
    def get_product_ingredients(self, driver):
        """ Gets the ingredients from Drugstore.com ingredients panel. """
        try:
            ingredients = driver.find_element_by_id("TblProdForkIngredients")
            return ingredients.text
        except NoSuchElementException:
            return ""

    def go_product_reviews_page(self, driver, product_id, website):
        """ Changes a page to the Drugstore.com reviews panel. """
        try:
            driver.find_element_by_css_selector("#btnReviews_Page_PDetail").click()
            self.wait_for_element(driver, "class", 'pr-review-engine')
        except NoSuchElementException:
            pass

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a Drugstore.com product page. """
        try:
            reviewcount = driver.find_element_by_id("divRatingWrapper")
            reviewnumber = reviewcount.find_element_by_id('divRating').text
            return filter(lambda x: x.isdigit(), reviewnumber)
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of Drugstore.com product reviews. 
            Raises NoSuchElementException if not found."""
        next = driver.find_element_by_class_name("pr-page-next")
        next.find_element_by_tag_name("a").click()
        self.wait_for_element(driver, "class", 'pr-page-count')
        time.sleep(1)
