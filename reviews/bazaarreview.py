import time

from review import Review

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class BazaarReview(Review):
    def review_frame(self, driver):
        """ Returns the review frame element of a review powered by Bazaar Voice. """
        try:
            time.sleep(0.5)
            reviewframe = driver.find_element_by_class_name("BVRRContainer")
            return reviewframe
        except NoSuchElementException:
            raise NoSuchElementException
    
    def get_review_wrappers(self, frame):
        """ Pass in an Bazzar Voice Review frame eleemnt to return all the wrappers in a list. """
        return frame.find_elements_by_class_name("BVRRContentReview")

    def get_author_name(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the author name. """
        return wrapper.find_element_by_class_name("BVRRNickname").text

    def get_author_loc(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the author location. """
        try:
            author_loc = wrapper.find_element_by_class_name("BVRRUserLocation").text
        except NoSuchElementException:
            author_loc = ""
        return author_loc

    def get_review_date(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the review date. """
        return wrapper.find_element_by_class_name("BVRRReviewDate").text

    def get_brand_affinity(self, wrapper):
        """ No brand affinity for the Bazaar Voice Review Engine. """
        return ""

    def get_review_short(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the review summary. """
        try:
            return wrapper.find_element_by_class_name("BVRRReviewTitle").text
        except NoSuchElementException:
            return ""

    def get_star_value(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the star value.  """
        star_value_init = wrapper.find_element_by_class_name("BVRRRatingNormalImage")
        star_value = star_value_init.find_element_by_xpath('.//img').get_attribute('title')
        return star_value.split()[0]

    def get_pros(self, wrapper):
        """ No pros for the Bazaar Voice Review Engine. """
        return ""
    
    def get_cons(self, wrapper):
        """ No cons for the Bazaar Voice Review Engine. """
        return ""

    def get_best(self, wrapper):
        """ No best uses for the Bazaar Voice Review Engine. """
        return ""

    def get_reviews(self, wrapper):
        """ Pass in a Bazaar Voice wrapper to return the review.  """
        try:
            return wrapper.find_element_by_class_name("BVRRReviewText").text
        except NoSuchElementException:
            return "" # This customer did not provide a text review; may have provided a video review