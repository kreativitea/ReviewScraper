import time

from review import Review

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException


class TargetReview(Review):
    # incomplete, not implemeneted.  
    def review_frame(self, driver):
        """ Returns the review frame element of a Target review. """
        try:
            time.sleep(0.5) # prevents errors
            reviewframe = driver.find_element_by_id("reviews-container")
            return reviewframe
        except NoSuchElementException:
            raise NoSuchElementException

    def get_review_wrappers(self, frame):
        """ Pass in a Target Review frame element to return all the wrappers in a list. """
        return frame.find_elements_by_class_name("review-content")