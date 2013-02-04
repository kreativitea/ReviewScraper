import time

from review import Review

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class PowerReview(Review):
    def review_frame(self, driver):
        """ Returns the review frame element of a review powered by Power Review. """
        time.sleep(1) # prevents errors
        try:
            reviewframe = driver.find_element_by_class_name("pr-contents")
            return reviewframe
        except NoSuchElementException:
            raise NoSuchElementException

    def get_review_wrappers(self, frame):
        """ Pass in a Power Review frame element to return all the wrappers in a list. """
        return frame.find_elements_by_class_name("pr-review-wrap")

    def get_author_name(self, wrapper):
        """ Pass in a Power Review wrapper to return the author name. """
        name = wrapper.find_element_by_class_name("pr-review-author-name")
        return name.find_element_by_xpath('.//span').text

    def get_author_loc(self, wrapper):
        """ Pass in a Power Review wrapper to return the author location. """
        try:
            location = wrapper.find_element_by_class_name("pr-review-author-location")
            return location.find_element_by_xpath('.//span').text
        except NoSuchElementException:
            return ""

    def get_review_date(self, wrapper):
        """ Pass in a Power Peview wrapper to return the review date. """
        try:
            return wrapper.find_element_by_class_name("pr-review-author-date").text
        except NoSuchElementException:
            return ""

    def get_brand_affinity(self, wrapper):
        """ Pass in a Power Review wrapper to return the brand affinity. """

        ## something wrong with this.
        brand_affinity_init = wrapper.find_element_by_class_name("pr-review-author-info-wrapper")
        try:
            brand_affinity = brand_affinity_init.find_element_by_class_name("pr-review-author-affinities")
            return brand_affinity.find_element_by_xpath(".//span").text
        except NoSuchElementException:
            return ""

    def get_review_short(self, wrapper):
        """ Pass in a Power Review wrapper to return the review summary. """
        try:
            return wrapper.find_element_by_class_name("pr-review-rating-headline").text
        except NoSuchElementException:
            return ""

    def get_star_value(self, wrapper):
        """ Pass in a Power Review wrapper to return the star value.  """
        try:
            return wrapper.find_element_by_class_name("pr-rating").text
        except NoSuchElementException:
            return ""
    
    def get_pros(self, wrapper):
        """ Pass in a Power Review wrapper to return the pros.  """
        try:
            subwrapper = wrapper.find_element_by_class_name("pr-attribute-pros")
            return subwrapper.find_element_by_class_name("pr-attribute-value").text
        except NoSuchElementException:
            return ""
    
    def get_cons(self, wrapper):
        """ Pass in a Power Review wrapper to return the cons.  """
        try:
            subwrapper = wrapper.find_element_by_class_name("pr-attribute-cons")
            return subwrapper.find_element_by_class_name("pr-attribute-value").text
        except NoSuchElementException:
            return ""

    def get_best(self, wrapper):
        """ Pass in a Power Review wrapper to return the best uses.  """
        try:
            subwrapper = wrapper.find_element_by_class_name("pr-attribute-bestuses")
            return subwrapper.find_element_by_class_name("pr-attribute-value").text
        except NoSuchElementException:
            return ""

    def get_reviews(self, wrapper):
        """ Pass in a Power Review wrapper to return the review.  """
        return self.review_cleaner(wrapper.find_element_by_class_name("pr-comments").text)
