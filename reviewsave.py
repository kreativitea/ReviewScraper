import xml.etree.cElementTree as xml
from docx import *

class ReviewSave():
    """ Saves a matrix object into an xml file as follows:
    
    <root>
        <product>
            <brand>brandname</brand>
            <name>product_name</name>
            <id>product_id</id>
            <site>website</site>
            <size>product_size_num</size>
            <units>product_size_units</units>
            <ingredients>product_ingredients</ingredients>
            <reviews>
                <review>
                    <review_number>review_number</review_number>
                    <author_name>db_author_name</author_name>
                    <author_location>db_author_loc</author_location>
                    <review_date>db_review_date</review_date>
                    <brand_affinity>db_brand_affinity</brand_affinity>
                    <short_review>db_review_short</short_review>
                    <review_stars>db_star_value</review_stars>
                    <pros>db_kw_pros</pros>
                    <cons>db_kw_cons</cons>
                    <best_uses>db_kw_best</best_uses>
                    <review_full>db_review_list</review_full>
                </review>
                <review>
                ...
                ...
                </review>
            </reviews>
        </product>
    </root>

    """ 
    def matrix(self, author_name, author_loc, review_date, brand_affinity, review_short, 
           star_value, kw_pros, kw_cons, kw_best, review_list):
        """ Creates a matrix of the objects passed into it, and transposes them. """
        matrix = [
            author_name,
            author_loc,
            review_date,
            brand_affinity,
            review_short,
            star_value,
            kw_pros,
            kw_cons,
            kw_best,
            review_list,
            ]
        neo = zip(*matrix)  # become one with the matrix
        return neo

    def initialize(self):
        """ Utility function of Class ReviewSave. 
            Initialize an xml document. """
        return xml.Element('root')

    def create_branch(self, parent, name):
        """ Utility function of Class ReviewSave. 
            Adds branch 'name' to an xml element 'parent'. """
        child = xml.Element(name)
        parent.append(child)
        return child

    def create_leaf(self, parent, name, element_text):
        """ Utility function of Class ReviewSave. 
            Adds branch 'name' to an xml element 'parent', with text 'element_text'. """
        child = self.create_branch(parent, name)
        child.text = unicode(element_text) # converts to unicode before writing.
        return child

    def create_xml(self, neo, pid, site, brand, name, size, 
                   units, ingredients):
        """ Creates and saves an xml file with all the information into a file with the filename "id",
            in the data folder as specified in 'filelocation'.  """

        # initialization
        root = self.initialize()
        filelocation = "data\\"

        # add product 
        product = self.create_branch(root, 'product')

        # add main information fields to product
        fields = [
                  ('brand', brand), ('name', name),
                  ("id", pid), ('site', site),
                  ('size', size), ('units' , units),
                  ('ingredients', ingredients)
                 ]

        for i in fields:
            self.create_leaf(product, i[0], i[1])

        # add review field
        reviews = self.create_branch(product, 'reviews')

        # iteration
        for i in range(1, len(neo)+1):
            # creates an xml Element named 'review' + whatever number the i iter is on.
            review = self.create_branch(reviews, 'review')

            # pulls items in sequence from the matrix to process
            current_pull = neo[i-1]

            # creates review number
            self.create_leaf(review, 'review_number', str(i))

            # adds fields to the review
            reviewfields = [
                            'author_name', 'author_location',
                            'review_date', 'brand_affinity',
                            'short_review', 'review_stars', 
                            'pros', 'cons', 'best_uses', 'review_full'
                            ]
            for j in range(len(current_pull)):
                self.create_leaf(review, reviewfields[j], current_pull[j])

        # writing to file
        matrixfile_name = filelocation + pid + ".xml"
        matrixfile = open(matrixfile_name, "w")
        if os.path.exists(matrixfile_name) == "True":
            print product_id + ".xml has been successfully created!"
        else:
            pass
        xml.ElementTree(root).write(matrixfile, encoding="utf-8")
        matrixfile.close()

    def create_docx(self, neo, pid, site, brand, name, size, 
                    units, ingredients):
        relationships = relationshiplist()
        document = newdocument()
        docbody = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
        docbody.append(neo)
        coreprops = coreproperties(title='',subject='',creator='',keywords=[])
        appprops = appproperties()
        contenttypes = contenttypes()
        websettings = websettings()
        wordrelationships = wordrelationships(relationships)
        savedocx(document,coreprops,appprops,contenttypes,websettings,wordrelationships,pid+'.docx')


def docx_config():
    """ creates a cactus object and a document object.  cactus is the options of the docx module. """
    document = newdocument()
    docbody = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
    relationships = relationshiplist()
    coreprops = coreproperties(title='Reviews for Product',subject='Review',creator='Mike Omoto',keywords=['Selenium','Office Open XML','Word'])
    appprops = appproperties()
    ctypes = contenttypes()
    webset = websettings()
    wordrels = wordrelationships(relationships)
    return (coreprops, appprops, ctypes, webset, wordrels), document

def save_docx(cactus, document, filename):
    c, a, ct, ws, wr = cactus
    savedocx(document,c,a,ct,ws,wr,filename)

def makebody_docx(document):
    body = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
    return body

def create_docx(data, filename):
    cactus, document = docx_config()
    docbody = makebody_docx(document)
    docbody.append(heading('''Test''',1))
    docbody.append(table([['this','is','a'],['list','of','stuff']]))
    save_docx(cactus, document, filename)
