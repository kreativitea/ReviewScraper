import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class QVC(Website):
    ## the following functions deal with the search page.
    def go_search(self, driver, pid):
        """ Returns the search links for QVC.com """
        return [self.search_url(website, pid)]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on QVC.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from QVC.com. """
        try:
            frame = driver.find_element_by_class_name("divBorder")
            products = frame.find_elements_by_class_name("divProduct")
            for i in products:
                productlist.append(i.find_element_by_class_name('divItemNumber').text)
        except NoSuchElementException:
            # No product_ids were found.
            pass

    def go_product_search_next(self, driver):
        """ Gets the next page of products on the QVC.com search results page. """
        try:
            pagination = driver.find_element_by_class_name("divPageLinks")
            pagination.find_element_by_class_name("next").click()
        except NoSuchElementException:
            raise NoSuchElementException

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a QVC.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a product page. 
        Product name, product size (number), product size (units) """
        detailsframe = driver.find_element_by_id("divProductDetailDescriptionAreaDisplay1")
        li_tags = detailsframe.find_elements_by_xpath('.//li')
        for i in li_tags:
            if "weight" in i.text:
                size_info = i.text.split()[2:]
                size = size_info[0]
                units = " ".join(size_info[1:])
            else:
                size, units = "", ""
        product_name = driver.find_element_by_class_name("fn").text
        return product_name, size, units

    def go_product_ingredients_page(self, driver, product_id):
        """ Not needed for QVC.com """
        pass

    def get_product_ingredients(self, driver):
        """ Not needed for QVC.com """
        pass

    def go_product_reviews_page(self, driver, product_id, website):
        """ Changes a page to the QVC.com reviews panel. """
        try:
            tab_list = driver.find_element_by_id("divProductDetailsCustomerReviewOptions")
            review_tab = tab_list.find_element_by_id("tabProductDetailCustomerReviewNav1")
            review_tab.click()
        except (NoSuchElementException, ElementNotVisibleException):
            pass
        time.sleep(1)

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a QVC.com product page. """
        try:
            frame = driver.find_element_by_id("BVRRRatingSummaryLinkReadID")
            total_reviews = frame.find_element_by_class_name("BVRRNumber").text
            return total_reviews
        except NoSuchElementException:
            return 0

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of QVC.com product reviews. """
        paginator = driver.find_element_by_class_name("BVRRPager")
        next_link = paginator.find_element_by_class_name("BVRRNextPage")
        next_link.find_element_by_name("BV_TrackingTag_Review_Display_NextPage").click()
        time.sleep(1)