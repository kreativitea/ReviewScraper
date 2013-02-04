import time

from review import Review

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException

class AmazonReview(Review):
    def review_frame(self, driver):
        """ Returns the review frame element of a review powered by amazon. """
        time.sleep(0.5) # prevents errors
        try:
            return driver.find_element_by_id("productReviews")
        except NoSuchElementException:
            raise NoSuchElementException
        
    def get_review_wrappers(self, frame):
        """ Pass in an Amazon Review frame eleemnt to return all the wrappers in a list. """
        if frame == None:
            return []
        else:
            return frame.find_elements_by_xpath('*/*/*/div[@style="margin-left:0.5em;"]')

    def get_author_name(self, wrapper):
        """ Pass in a Amazon Review wrapper to return the author name. """
        try:
            # finds the linked css'ed author name
            return wrapper.find_element_by_xpath('.//span[@style="font-weight: bold;"]').text
        except NoSuchElementException:
            # finds the non-linked, possibly all anonymous author name. ("A Customer").
            return wrapper.find_elements_by_xpath(".//b")[1].text

    def get_author_loc(self, wrapper):
        """ Pass in a Amazon Review wrapper to return the author location. """
        loc_init = wrapper.find_elements_by_xpath('.//div[@style="float:left;"]')
        # split by ' - ' 
        # forces see all my reviews to be an entry, allowing slice 2 to have the parenthesis
        remove_flair = []
        for i in loc_init:
            remove_flair.extend(i.text.split(' - '))
        # split by newline
        newliner = []
        for i in remove_flair:
            newliner.extend(i.split('\n'))
        # if parenthesis in slice 2, that's the authorloc
        if '(' not in newliner[1]:
            return ""
        else:
            return newliner[1][newliner[1].find('(')+1:newliner[1].find(')')]

    def get_review_date(self, wrapper):
        """ Pass in an Amazon Review wrapper to return the review date. """
        try:
            return wrapper.find_element_by_xpath('.//nobr').text
        except NoSuchElementException:
            return ""

    def get_brand_affinity(self, wrapper):
        """ No brand affinity for the Amazon Review Engine. """
        return ""

    def get_review_short(self, wrapper):
        """ Pass in an Amazon Review wrapper to return the review summary. """
        try:
            return wrapper.find_element_by_xpath('.//b').text
        except NoSuchElementException:
            return ""

    def get_star_value(self, wrapper):
        """ Pass in an Amazon Review wrapper to return the star value. """ 
        star_string = wrapper.find_element_by_class_name('swSprite').text
        star_split = star_string.split()
        return star_split[0]

    def get_pros(self, wrapper):
        """ No pros on Amazon.com. """
        return ""
    
    def get_cons(self, wrapper):
        """ No cons on Amazon.com. """
        return ""

    def get_best(self, wrapper):
        """ No best uses on Amazon.com. """
        return ""

    def get_reviews(self, wrapper):
        """ Pass in an Amazon Review wrapper to return the review. """
        negative = wrapper.find_elements_by_xpath('./div')
        review = wrapper.text
        for i in negative:
            review = review.replace(i.text,"")
        return review.strip()
