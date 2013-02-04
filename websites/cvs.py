import time

from website import Website

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class CVS(Website):
    def go_search(self, driver, pid):
        """ Returns the search links for CVS.com """
        searchlink = self.search_url(website, pid)
        self.go_and_assert(driver, searchlink, website)
        if 'promo' in driver.current_url: # may redirect to a promotional page without links.
            frame_candidates = driver.find_elements_by_class_name("trm_table")
            for i in frame_candidates:
                if len(i.text) > 0:
                    frame = i
            links = []
            links_candidates = frame.find_elements_by_xpath(".//a")
            for i in links_candidates:
                link = i.get_attribute('href') 
                try:
                    if "searchTerm" in link:
                        links.append(link + "&pt=product&navNum=100000")
                except TypeError:
                    pass
            return links
        else:
            return [searchlink]

    def go_search_results(self, driver, searchlink):
        """ Goes to the search link on CVS.com """
        self.go_and_assert(driver, searchlink, website)

    def add_product_ids(self, driver, productlist):
        """ Adds products to the productlist, given a search result page from CVS.com. """
        frame = driver.find_element_by_id("searchResults")
        wrappers = frame.find_elements_by_class_name("productBrand")
        for i in wrappers:
            productlist.append(i.find_element_by_xpath('.//a').get_attribute('href').split("skuId=")[-1])
    
    def go_product_search_next(self, driver):
        """ Not needed on CVS.com """
        # but should probably write one anyway.  #IMPLEMENT
        raise NoSuchElementException

    ## the following functions deal with the product page.
    def go_product_page(self, driver, product_id, website):
        """ Goes to a CVS.com product page. """
        link = self.product_url(website, product_id)
        self.go_and_assert(driver, link, website)

    def get_product_name_and_size(self, driver):
        """ Gets the name and size of a product from a product page. 
        Product name, product size (number), product size (units) """
        # size and units
        frame = driver.find_element_by_class_name("priceTable")
        details = frame.find_elements_by_xpath('.//tr')
        for i in details:
            if "Size:" in i.text:
                size, units = i.text.replace("Size: ", "").split()
        # name
        description_frame = driver.find_element_by_id("prodDescription")
        name = description_frame.find_element_by_class_name("prodName").text
        return name, size, units

    def go_product_ingredients_page(self, driver, product_id):
        """ Goes to a CVS.com ingredients page. """
        tabs = driver.find_element_by_id("resultsTabs")
        tablist = tabs.find_elements_by_class_name("ui-state-default")
        for i in tablist:
            if "Ingredients" in i.text:
                i.click()
                time.sleep(2)
            else:
                pass

    def get_product_ingredients(self, driver):
        """ Gets the ingredients from the CVS.com product page. """
        frame = driver.find_element_by_class_name("textBlockBottom")
        ingredients = frame.find_element_by_id("prodIngd").text
        return ingredients

    def go_product_reviews_page(self, driver, product_id, website):
        """ Goes to a CVS.com reviews page. """
        tabs = driver.find_element_by_id("resultsTabs")
        tablist = tabs.find_elements_by_class_name("ui-state-default")
        for i in tablist:
            if "Reviews" in i.text:
                i.click()
                time.sleep(2)
            else:
                pass

    def get_product_total_reviews(self, driver):
        """ Gets the total number of reviews from a CVS.com product page. """
        try:
            frame = driver.find_element_by_class_name("BVRRRatingSummary")
            number = frame.find_element_by_class_name("BVRRNumber").text
            return number
        except NoSuchElementException:
            return "0"

    def go_product_reviews_next(self, driver, website):
        """ Gets the next page of CVS.com product reviews. """
        paginator = driver.find_element_by_class_name("BVRRPager")
        next_link = paginator.find_element_by_class_name("BVRRNextPage")
        next_link.find_element_by_name("BV_TrackingTag_Review_Display_NextPage").click()
        time.sleep(1)