class ReviewTest():
    """ A collection of tests for Scraper. """
    def test_reviews_length(self, reviews_on_page, author_name, append_list, pid):
        """ Returns True if Pass, False if Fail. """
        if reviews_on_page == len(author_name):
            return True
        else:
            print "Possible error detected in file " + pid + ". Incorrect number of entries."
            append_list.append(pid)
            return False

    def test_multiple_entries(self, inputlist, append_list, pid):
        """ Returns True if Pass, False if Fail. """
        testlist = inputlist[:]
        testlist = list(set(testlist))
        if len(testlist) == len(inputlist):
            return True
        else:
            print "Possible error detected in file " + pid + ". Review duplication."
            append_list.append(pid)
            return False

    def test_len_all(self, listoflists, append_list, pid):
        """ Returns True if Pass, False if Fail. """
        for i in listoflists:
            if len(listoflists[0]) != len(i):
                print "Error detected in file " + pid + ". Incorrect matrix size."
                append_list.append(pid)
                return False
        return True

    def test_name_check(self, input_brand, product_name, website, remove_list, pid):
        """ Returns True if pass, False if Fail. """
        # sites with product names that include the product brand
        sites = ["Amazon Drugstore".split()]
        if website in sites:
            test_input = input_brand[:]
            while True:
                if len(test_input) == 5:
                    # at least the first five letters of the product must match.  
                    self.remove_from_product_list(pid, remove_list)
                    print "Product " + pid + " not of target brand. (" + name + ")"
                    return False
                elif test_input.title() in product_name.title():
                    return True
                else:
                    test_input = test_input[:-1]
        else:
            return True

    def remove_from_product_list(self, input_id, productlist):
        try:
            productlist.remove(input_id)
        except ValueError:
            pass

    def test_product_name(self, product_search, name):
        """ Returns True if pass, False if fail. """
        namelist = product_search.split()
        for i in namelist:
            if i not in name:
                print product_search + " not found in " + name + "."
                return False
            else:
                pass
        return True