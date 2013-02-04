#!/usr/bin/env python
# -*- coding: UTF-8 -*-

## STATIC IMPORTS
# basic systems functions
import sys

# namespace organization
from collections import namedtuple

## DOCSTRING
r"""This program takes a product link and supplies you with an xml data file of 
reviews of the brand. 

This program runs fastest on Chrome, but runs with more stability on Firefox.
Some websites dont run at all on Chrome (Neutrogena) due to a ChromeDriver bug.

For best performance, upon first run, execute "driver = chrome_setup()", and install
adblock from google chrome webstore. in chrome://chrome/extensions/, enable
adblock to run while incognito.  Execute "driver.quit()" to close the instance.

Runs on python 2.7. Requires Selenium and ChromeDriver if you use Chrome. 
Works on any browser.  Theroetically. 

"""

## DYNAMIC IMPORTS
# adds neccesary paths for relative imports to sys.path
def sys_append(directory):
    """ Appends directory to sys.path. """
    if directory not in sys.path:
        sys.path.append(directory)

def sys_init():
    """ Adds directory, websites, and reviews to sys.path. """
    basepath = r"C:\Users\toshi\Dropbox\code"
    project = basepath + r"\Scraper\Scraper"
    websites = project + r"\websites"
    reviews = project + r"\reviews"
    for item in [project, websites, reviews]:
        sys_append(item)

sys_init()

## FUNCTIONS
# main utility functions
from utils import browser_setup
from utils import class_chooser

# time utility functions
from utils import timerstart
from utils import timerend

# persistance functions
from reviewsave import ReviewSave

# download functions
from utils import goto_product_page
from utils import product_info
from utils import ingredients_info
from utils import goto_review_page
from utils import get_reviews

# input functions
from utils import brand_input
from utils import link_input

# unittests
# move tests to reviewtests #

## MAIN RUNTIME
def download(product, engine):
    driver = browser_setup(engine)
    save = ReviewSave()

    # go to page
    goto_product_page(driver, engine, product)

    # get product info, ingredients, and review info
    name, size, units = product_info(driver, engine, product)
    ingredients = ingredients_info(driver, engine, product)

    Variables = namedtuple("variables", """author_name, author_loc, review_date, 
                           brand_affinity, review_short, star_value, 
                           kw_pros, kw_cons, kw_best, review_list""") 

    data = Variables([], [], [], [], [], [], [], [], [], [])

    goto_review_page(driver, engine, product)
    get_reviews(driver, engine, product, data)

    # close browser
    driver.quit()

    # prepare to save data
    neo = save.matrix(data.author_name, data.author_loc, data.review_date, data.brand_affinity,
            data.review_short, data.star_value, data.kw_pros, data.kw_cons, data.kw_best,
            data.review_list)

    # save data
    save.create_xml(neo, product.pid, product.website, product.brand, name, size, units, ingredients)

# start the clock

t = timerstart()

# setup
browser = "Chrome"

# objects
Product = namedtuple('product', 'website, pid, brand')
Engine = namedtuple('Engine', 'browser, s, e')

# user input
website, pid = link_input() 
brand = brand_input()
s, e = class_chooser(website)

# tuple instanciation
product = Product(website, pid, brand)
engine = Engine(browser, s(), e())

# execution
download(product, engine)

timerend(t)
# end the clock

## TESTING
sites = "walmart".split()

def reviewtest(sites):
    Product = namedtuple('product', 'website, pid, brand')
    Engine = namedtuple('Engine', 'browser, s, e')
    RapidWrinkle = {"amazon" : Product("amazon", "B004D2C57M", "Neutrogena"),
                    "drugstore" : Product("drugstore", "qxp344205", "Neutrogena"),
                    "walmart" : Product("walmart", "15747280", "Neutrogena")}
    for i in sites:
        product = RapidWrinkle[i]
        t = timerstart()
        browser = "Chrome"
        s, e = class_chooser(product.website)
        engine = Engine(browser, s(), e())
        download(product, engine)
        timerend(t)

# reviewtest(sites)