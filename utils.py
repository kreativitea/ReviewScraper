import os
import time

from datetime import datetime as dt
from tests import ReviewTest as test

# selenium is the module which drives the webbrowser, in this case, chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException

def import_from(module, name):
    """ Imports name from module. """ 
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def class_chooser(website):
    """ Chooses the appropriate class for any given website supported by this program. 
    Add websites as neccesary. """
    modules = {"drugstore" : ("Drugstore", "PowerReview"),
               "amazon" : ("Amazon", "AmazonReview"),
               "target" : ("Target", "TargetReview"),
               "ulta" : ("Ulta", "PowerReview"),
               "neutrogena" : ("Neutrogena", "BazaarReview"),
               "qvc" : ("QVC", "BazaarReview"),
               "cvs" : ("CVS", "BazaarReview"),
               "walmart" : ("Walmart", "BazaarReview"),
               "walgreens" : ("Walgreens", "BazaarReview"),
               "clean and clear" : ("Clean and Clear", "BazaarReview")}
    while True:
        if website.lower() not in modules:
            print "Please pick one of the availible websites."
            cwk = modules.keys()
            print "Valid websites: " + ", ".join(cwk[:-1]) + " or "+ cwk[-1] + "."
            website = raw_input('--> ')
        else:
            site, engine = modules[website.lower()]
            s = import_from(site.lower(), site)
            e = import_from(engine.lower(), engine)
            return s, e

def browser_setup(engine):
    browser = engine.browser
    """ Sets up a browser instance.  
    
    Usage:
    driver = browser_setup("Chrome") 
    driver.do_something()
    driver.quit()
    """
    if browser == "Chrome":
        options = webdriver.ChromeOptions()
        if len(webdriver.ChromeOptions().arguments) == 7:
            pass
        else:
            executepath = os.getcwd() + "\\Selenium" # creates a local file for Chrome Options
            options.add_argument("--user-data-dir=" + executepath)
            options.add_argument("--no-first-run")
            options.add_argument("--disable-default-apps")
            options.add_argument("--login-screen")
            options.add_argument("--incognito")
            options.add_argument("--disable-translate")
            options.add_argument("--window-size=1024,1000")
        driver = webdriver.Chrome(chrome_options=options)
        return driver
    elif browser == "Firefox":
        driver = webdriver.Firefox()
        return driver

def print_choices(choices):
    """ Prints a dictionary of choices. """
    for i in sorted(choices):
        if len(i) != 0:
            print i, ":", choices[i]

def user_choice(choices, text, n):
    """ A generic function for user input.  
    
    Text prompt, with a dict of choices, with n number of maximum choices. """
    print text
    print_choices(choices)
    while True:
        answer = raw_input("> ")
        if len(answer) > n:
            print "I'm sorry, you have made too many choices.  Try again."
        else:
            try:
                return list(set([choices[i] for i in answer]))
            except KeyError:
                print "I'm sorry, that is an invalid submission.  Try again."

def user_input(text):
    print text
    return raw_input("> ")

def search_input():
    """ Input function for a product to search for. """
    text = "Please input a search term. "
    return user_input(text)

def pid_input():
    """ Input function for a product id. """
    text = """ 
    Please enter a product id.

    www.amazon.com/dp/ + id
    www.target.com/p/-/ + id
    www.drugstore.com/ + id
    www.ulta.com/ulta/browse/productDetail.jsp?skuId= + id + &productId=prod + id2
    www.neutrogena.com/product/ + id + .do? 
    www.qvc.com/webapp/wcs/stores/servlet/ProductDisplay?partNumber= + id
    www.cvs.com/shop/product-detail/?skuId= + id
    www.walmart.com/ip/ + id
    www.walgreens.com/store/c/-/ID= + id + -product 
    """
    return user_input(text)

def brand_input():
    """ Input function for brands. """
    text = "Please input the brand name of the search term."
    return user_input(text)

def website_input():
    """ Input function for a website. """
    websites = {"1" : "Drugstore",
                "2" : "Amazon",
                "3" : "Target",
                "4" : "Ulta",
                "5" : "Neutrogena",
                "6" : "QVC",
                "7" : "CVS",
                "8" : "Walmart",
                "9" : "Walgreens"}
    text = """
    Which website do you want to download from?
    """
    while True:
        for i in sorted(websites):
            print i, ":", websites[i]
        print text
        answer = user_input(text)
        if len(answer) == 1:
            return websites[answer]

def link_input_proc(link):
    """ Returns the website and pid from a given link. """
    slash = link.split("/")
    website = [i for i in slash if "www" in i][0].split(".")[1]
    if website == "amazon":
        qid = [i for i in slash if 'B00' in i][0]
    if website == "drugstore":
        qid =  [i for i in slash if "catid" in i][0].split("?")[0]
    if website == "target":
        qid =  slash[-1]
    if website == "ulta":
        qid =  ",".join([i.split("=")[-1] for i in slash[-1].split("&")][0:2])
    if website == "neutrogena":
        qid =  slash[slash.index("product") + 1].split(".")[0]
    if website == "qvc":
        periods = [i for i in slash if "product" in i][0].split(".")
        qid =  periods[periods.index("product")+1]
    if website == "cvs":
        qid =  [i for i in slash if "skuId" in i][0].split("=")[-1]
    if website == "walmart":
        qid =  slash[-1]
    if website == "walgreens":
        qid =  [i.split("=")[-1].split("-")[0] for i in slash if "ID" in i][0]
    try:
        return website, qid
    except:
        return None, None

def link_input():
    """ Returns the website and product id from a link. """
    text = """
    Please input a link.
    """
    while True:
        print text
        try:
            website, link = link_input_proc(raw_input("> "))
            return website, link
        except IndexError:
            print "I'm sorry, that is not a valid link. Try again. \n"        
    
def websites_input():
    """ Input function for websites. """
    websites = {"1" : "Drugstore",
                "2" : "Amazon",
                "3" : "Target",
                "4" : "Ulta",
                "5" : "Neutrogena",
                "6" : "QVC",
                "7" : "CVS",
                "8" : "Walmart",
                "9" : "Walgreens"}
    text = """
    Which website do you want to download from?
    Type the numbers associated with each entry into the entry field to select.
    You may select as many websites as you wish.
    For example, '1235' selects Drugstore, Amazon, Target, and Neutrogena.
    """
    return user_choice(websites, text, 9)

def browser_input():
    """ Input function for browser. """
    browsers = {"" : "Chrome",
                "1" : "Chrome",
                "2" : "Firefox"}
    text = """
    Which browser do you want to use?
    Type the number associated with each entry into the entry field to select.
    You may only select one website.
    For example, '1' selects Chrome.
    """
    return user_choice(browsers,text,1)[0]

def timerstart():
    """ Creates a timer object.  """
    return dt.now()

def timerend(start):
    """ Takes a timer object and returns the timer output. """
    end = dt.now()
    program_lapse = end - start
    tl_h = int(str(program_lapse)[0:1])
    tl_m = int(str(program_lapse)[2:4])
    tl_s = int(str(program_lapse)[5:7])

    # Generates a string for each unit
    tl_hourstring = str(tl_h)+" hour"
    tl_minstring = str(tl_m)+" minute"
    tl_secstring = str(tl_s)+" second"
    tl_plural = "s"

    # Generates text strings
    if tl_h != 1:
        hourstring = tl_hourstring+tl_plural
    else:
        hourstring = tl_hourstring

    if tl_m != 1:
        minstring = tl_minstring+tl_plural
    else:
        minstring = tl_minstring

    if tl_s != 1:
        secstring = tl_secstring+tl_plural
    else: 
        secstring = tl_secstring

    # Generates final text
    if tl_h > 0:
        print "This program took " + hourstring+", " + minstring + ", and " + secstring +"."
    elif tl_m > 0:
        print "This program took " + minstring + ", and " + secstring + "."
    else:
        print "This program took " + secstring+ "."

def pages_to_search(browser, input, engine):
    """ Wrapper.  Returns the search results pages via links of the input products. """
    driver = browser_setup(browser)
    s = engine[0]
    pages = s.go_search(driver, input)
    driver.quit()
    return pages

def find_product_ids(pages, engine):
    """ Wrapper.  Returns the product ids of a list of search results links."""
    # iterate over links
    s = engine.s
    product_ids = []
    for page in pages:
        driver = browser_setup(browser)
        s.go_search_results(driver, page)
        while True:
            s.add_product_ids(driver, product_ids)
            try:
                s.go_product_search_next(driver)
            except NoSuchElementException:
                break # last page reached, go to next search_results_pages
        driver.quit()
    product_ids = list(set(product_ids))
    if None in product_ids:
        product_ids.remove(None) # empty spots in rows might return None
    return product_ids

def goto_product_page(driver, engine, product):
    engine.s.go_product_page(driver, product.pid, product.website)

def product_info(driver, engine, product):
    """ Wrapper.  Returns the information of the product, given a product details page. """
    name, size, units = engine.s.get_product_name_and_size(driver)
    return name, size, units

def ingredients_info(driver, engine, product):
    """ Wrapper.  Returns the ingredients of the product, given a product details page. """
    engine.s.go_product_ingredients_page(driver, product.pid)
    ingredients = engine.s.get_product_ingredients(driver)
    return ingredients

def review_info(driver, pid, engine):
    """ Wrapper.  Returns the review information of the product, given a product details page. """
    s, pid, website = engine.s, product.pid, product.website
    s.go_product_reviews_page(driver, pid, website)
    total_reviews = s.get_product_total_reviews(driver)
    return total_reviews

def get_wrappers(driver, engine, filter=None):
    """ Wrapper.  Returns the review wrappers of the product, given a product details page. """
    e = engine.e
    try:
        reviewframe = e.review_frame(driver)
        wrappers = e.get_review_wrappers(reviewframe)
        filter_wrappers(driver, wrappers, engine)
        return wrappers
    except NoSuchElementException:
        return []

def filter_wrappers(driver, wrappers, engine, filter=None):
    e = engine.e
    if filter != None:
        for wrapper in wrappers:
            product_name = e.get_review_wrapper_name(wrapper) #IMPLEMENT
            if test.test_product_name(product_search, product_name) == False:
                wrappers.remove(wrapper)

def get_review_data(wrapper, engine, data):
    """ Wrapper.  Appends the review information of the product to the appropriate lists. """
    e = engine.e
    data.author_name.append(e.get_author_name(wrapper))
    data.author_loc.append(e.get_author_loc(wrapper))
    data.review_date.append(e.get_review_date(wrapper))
    data.brand_affinity.append(e.get_brand_affinity(wrapper))
    data.review_short.append(e.get_review_short(wrapper))
    data.star_value.append(e.get_star_value(wrapper))
    data.kw_pros.append(e.get_pros(wrapper))
    data.kw_cons.append(e.get_cons(wrapper))
    data.kw_best.append(e.get_best(wrapper))
    data.review_list.append(e.get_reviews(wrapper))

def next_page(driver, engine, product):
    """ Wrapper.  Turns to the next product reviews page. """
    try:
        engine.s.go_product_reviews_next(driver, product.website)
        return True
    except NoSuchElementException:
        return False

def test_brand():
    """ Wrapper.  Alias of tests.test_name_check. """
    if test.test_name_check(input_brand, name, website, product_ids_temp, pid) == False:
        return False
    if literal_product == True:
        if test.test_product_name(input, name) == False:
            return False
    return True

def test_battery():
    """ Wrapper.  Executes the test suite. """
    tests.test_reviews_length(review_count, author_name, products_errored, pid)
    tests.test_multiple_entries(review_list, products_errored, pid)
    tests.test_len_all([author_name, author_loc, review_date, brand_affinity, review_short, 
                        star_value, kw_pros, kw_cons, kw_best, review_list], products_to_redo, pid)
        
def goto_review_page(driver, engine, product):
    """ Wrapper.  Goes to the review page. """
    engine.s.go_product_reviews_page(driver, product.pid, product.website)

def get_reviews(driver, engine, product, data):
    """ Wrapper.  Gets all the reviews on a product information page.. """
    while True:
        wrappers = get_wrappers(driver, engine) # 
        for wr in wrappers:
            get_review_data(wr, engine, data)
        wrappers = [] #empty wrappers to prevent duplicates
        if next_page(driver, engine, product) == False:
            break