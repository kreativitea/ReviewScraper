import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException

class Amazon(Website):
    ## The following functions deal with the search page.
    def go_search(self, driver, pid):
        """ Returns the search links for Amazon.com """
        driver.get("http://www.amazon.com/")
        self.input_searchbox(driver, "id", "twotabsearchtextbox", pid)
        try:
            expander = driver.find_element_by_class_name("forExpando")
        except NoSuchElementException:
            expander = driver.find_element_by_class_name("noExpando")
        link_elements = expander.find_elements_by_class_name("boldRefinementLink")
        link_list, return_links = [], []
        for i in link_elements:
            link_list.append(expander.find_element_by_link_text(i.text))
        for i in link_list:
            return_links.append(i.get_attribute("href"))
        return return_links

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on Amazon.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from amazon.com. """
        try:
            frame = driver.find_element_by_id("rightResultsATF")
            results = frame.find_elements_by_class_name("results")
            result_candidates = []
            for i in results:
                result_candidates.extend(i.find_elements_by_xpath('.//div'))
            for i in result_candidates:
                if "result" in i.get_attribute('id'):
                    productlist.append(i.get_attribute('name'))
        except StaleElementReferenceException:
            time.sleep(2)
            self.add_product_ids(driver, productlist)

    def go_product_search_next(self, driver):
        """ Gets the next page of products on the amazon.com search results page. """
        driver.find_element_by_class_name("pagnNext").click()
        try:
            # simply by waiting for this to load, you wait a sufficient amount of time.
            testassert = driver.find_element_by_id("btfResults")
        except NoSuchElementException:
            pass
        time.sleep(1)
        self.assertion(website, driver)

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to an Amazon.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a product page. 
            Product name (name), product size (number), product size (units) 
            There is no good way to get product size and units from Amazon.
            Each page displays size in a different way."""
        try:
            name = driver.find_element_by_id("btAsinTitle").text
            size, units = "", ""
            return name, size, units
        except StaleElementReferenceException: 
            # must exist, recurse until complete.
            time.sleep(2)
            self.get_product_name_and_size(driver) #recursion

    def go_product_ingredients_page(self, driver, product_id):
        """ Not needed for Amazon.com """
        pass

    def get_product_ingredients(self, driver):
        """ Gets product ingredients off an Amazon.com product page. """
        try:
            ingredient_element = driver.find_element_by_id("importantInformation").find_element_by_class_name("content")
            ingredients_list = ingredient_element.text.split("\n")
            ingredients = ""
            for i in ingredients_list:
                if "Ingredients:" in i:
                    ingredients += i + " "
            return ingredients
        except NoSuchElementException:
            return ""

    def go_product_reviews_page(self, driver, product_id, website):
        """ Changes a page to the amazon.com reviews panel. """
        link = self.product_url("AmazonReviews", product_id)
        self.go_and_assert(driver, link, website)

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a amazon.com product page. """
        # warning: does not work with reviews tallying over 999.  
        try:
            num_init = driver.find_element_by_class_name("crAvgStars").text
            if num_init.find("customer reviews") == -1:
                return "0"
            else:
                num_init = num_init.split("(")[1]
                num = int(num_init.split()[0]) # this is better written to get a regex compound number
                return num
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of product reviews. 
            Raises NoSuchElementException if not found."""
        paging_element = driver.find_element_by_class_name("paging")
        paging_element.find_element_by_partial_link_text("Next").click()
        self.assertion(website, driver)
