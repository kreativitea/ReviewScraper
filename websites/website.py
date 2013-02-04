import time

from selenium.webdriver.support.ui import WebDriverWait

class Website():
    """ This is the base class for the Website Classes.  
    Contains functions that are useful across the website classes.  """
      
    def assertion(self, website, driver):
        """" Asserts 'website' against 'driver.title'. """
        assert_website = {"drugstore" : ("drugstore.com",),
                          "amazon" : ("Amazon.com",),
                          "target" : ("Target",),
                          "ulta" : ("ULTA","Ulta"),
                          "neutrogena" : ("Neutrogena",),
                          "qvc" : ("QVC",),
                          "cvs" : ("CVS pharmacy",),
                          "walmart" : ("Walmart.com",),
                          "walgreens" : ("Walgreens",),
                          "buy.com" : ("Buy.com",)}
        # if not present
        if website.lower() in assert_website == False:
            raise AssertionError

        # if present ## RECODE
        else:
            # if one of the assertions in the tuple pass, the assertion clears.
            count = 0
            check_strings = assert_website[website]
            for i in check_strings:
                try:
                    assert i in driver.title
                except AssertionError:
                    count += 1
                finally:
                    if count == len(check_strings):
                        print "AssertionError on " + website + ", " + i + " not in title."

    def search_url(self, website, input):
        """ Generates search strings for the websites that have a simple URL based API. 
            Keeps all the search API strings in the same place.
            Not every website has a search string. (Amazon)
            Websites that generate search strings differently have a customized function within their class. """ 
        input_plus = "+".join(input.split())
        stringdict = {
                      "target" : "http://www.target.com/s?searchTerm=" + input_plus,
                      "drugstore" : "http://www.drugstore.com/search/search_results.asp?Ntx=mode%2bmatchallpartial&Ntk=All&Go.y=0&srchtree=1&ipp=72&N=0&Ntt=" + input_plus + "&Go.x=0",
                      "ulta" : "http://search.ulta.com/search?p=Q&userid=Guest&w=" + input_plus + "&method=and&isort=date&view=grid&cnt=300",
                      "neutrogena" : "http://www.neutrogena.com/search.do?query=" + input_plus + "&sortby=bestSellers&pp=18&page=all",
                      "walmart" : "http://www.walmart.com/search/search-ng.do?ic=32_0&tab_value=all&search_query=" + input_plus + "&ic=16_0&Find=Find&search_constraint=0",
                      "cvs" : "http://www.cvs.com/search/_/N-0?searchTerm=" + input_plus + "&pt=global&navNum=100000",
                      "qvc" : "http://www.qvc.com/CatalogSearch?langId=-1&storeId=10251&catalogId=10151&keyword=" + input_plus,
                      "walgreens" : "http://www.walgreens.com/search/results.jsp?Erp=96&Ntt=" + input_plus + "&x=0&y=0"
                     }
        return stringdict[website]

    def product_url(self, website, product_id_raw):
        """ Generates products strings for the websites that have a simple URL based API. 
            Keeps all the product strings in the same place. """ 
        if website == "Ulta":
            product_id_pre, product_id_post = product_id_raw.split(",")
            product_id = product_id_pre + "&productId=" + product_id_post  # modification to the Ulta product string.
            print product_id_raw + " -> " + product_id
        else:
            product_id = product_id_raw
            print product_id
        stringdict = {
                        "amazon" : "http://www.amazon.com/dp/" + product_id,
                        "AmazonReviews" : "http://www.amazon.com/product-reviews/" + product_id,
                        "target" : "http://www.target.com/p/-/" + product_id,
                        "drugstore" : "http://drugstore.com/" + product_id,
                        "ulta" : "http://www.ulta.com/ulta/browse/productDetail.jsp?skuId=" + product_id,
                        "neutrogena" : "http://www.neutrogena.com/product/" + product_id + ".do?",
                        "qvc" : "http://www.qvc.com/webapp/wcs/stores/servlet/ProductDisplay?partNumber=" + product_id,
                        "cvs" : "http://www.cvs.com/shop/product-detail/?skuId=" + product_id,
                        "walmart" : "http://www.walmart.com/ip/" + product_id,
                        "WalmartReview" : "http://www.walmart.com/catalog/allReviews.do?product_id=" + product_id,
                        "walgreens" : "http://www.walgreens.com/store/c/-/ID=" + product_id + "-product"
                        }
        if "Review" not in website: # Prevents repetition in console
            print " product URL is " + stringdict[website]
        return stringdict[website]

    def go_and_assert(self, driver, link, website):
        """ Goes to a link, and executes an assertion according to the website to ensure loading. """
        driver.get(link)
        self.assertion(website, driver)

    def input_searchbox(self, driver, by, tag, input):
        if by == "id":
            searchbox = driver.find_element_by_id(tag)
            searchbox.send_keys(input + Keys.RETURN)
        if by == "class":
            searchbox = driver.find_element_by_class_name(tag)
            searchbox.send_keys(input + Keys.RETURN)
        self.assertion(website, driver)

    def num_product_pages(self, products, product_per_page):
        """ Returns the number of product pages given the number of products and the products per page. """
        # depreciated
        product_pages = (int(products) + int(product_per_page) - 1) / int(product_per_page)
        return product_pages

    def page_splitter(self, html, start, end):
        """ Returns the html text between start and end. """
        # still used in one place, but plan to depreciate
        splitme = re.split(start, html)
        splitshort = splitme[1]
        splitme2 = re.split(end,splitshort)
        return splitme2[0]
    
    def wait_for_element(self, driver, by, tag):
        """ Wrapper for selenium. """
        wait = WebDriverWait(driver,10)
        if by == "id":
            wait.until(lambda driver: driver.find_element_by_id(tag))
        if by == "class":
            wait.until(lambda driver: driver.find_element_by_class_name(tag))
        else:
            pass

    def numerals(self, p):
        return filter(lambda x: x.isdigit(), p)

    def show_full_reviews(self, driver, by, tag, link_text):
        """ Shows 'full' reviews. """
        time.sleep(2)
        try:
            if by == "class":
                elements = driver.find_elements_by_class_name(tag)
            if by == "id":
                elements = driver.find_elements_by_id(tag)
        except NoSuchElementException:
            return None
        for i in elements:
            if link_text in i.text:
                i.click()
        time.sleep(2)
        return True
