from flask_mongoengine import MongoEngine

#import mongoengine as mongo
import requests
import datetime
from unidecode import unidecode

mongo = MongoEngine()

mongo.connect('test-biodiversityOnInk')

class Person(mongo.EmbeddedDocument):
    """
    Model representing a person in the database.
    """
    lastname = mongo.StringField(required=True, max_length=50)
    firstname = mongo.StringField(required=True, max_length=50)
    middlename = mongo.StringField(required=False, max_length=50)


######## Publication documents definitions ############
class Publication(mongo.Document):
    """
    General publication model
    """

    citation_key = mongo.StringField(required=True, unique=True, max_length=50)
    title = mongo.StringField(required=True)
    author = mongo.EmbeddedDocumentListField(Person, required=True)
    year = mongo.StringField(required=True, max_length=4)
    #date = mongo.DateTimeField(required=True)
    doi = mongo.StringField(required=False, unique=True, max_length=100)
    calalog_date = mongo.DateTimeField(required=True, default=datetime.datetime.utcnow())
    cataloger = mongo.EmbeddedDocumentField(Person, required=True)

    meta = {
        'allow_inheritance':True,
        'indexes':[
            {
                'fields':[
                    'year','author', 'title'
                ],
                'unique':True
            }
        ]
    }

    def create_key(self):
        auth_ini = ''.join([auth.lastname[0].lower() for auth in self.author])
        modtitle = unidecode(self.title.lower().replace(' ', ''))
        summa_title = '{}...{}'.format(modtitle[0:5], modtitle[-5:])
        self.citation_key = '{}{}:{}'.format(auth_ini, self.year, summa_title)


class Article(Publication):
    """

    """
    entry_type = "article"
    journal = mongo.StringField(required=True, max_length=100)
    shortjournal = mongo.StringField(required=False, max_length=50)
    volume = mongo.StringField(required=False, max_length=5)
    number = mongo.StringField(required=False, max_length=5)
    pages = mongo.StringField(required=False, max_length=10)
    meta = {
        'indexes':[
            {
                'fields':[
                    'journal', 'volume', 'number', 'pages'
                ],
                'unique':True
            }
        ]
    }

class Book(Publication):
    """
    """
    entry_type = "book"
    publisher = mongo.StringField(required=True)
    isbn = mongo.StringField(required=False, unique=True, max_length=20)

######## Taxonomy documents definitions ##############

class GrowthForm(mongo.EmbeddedDocument):
    habit = mongo.ListField(mongo.StringField(required=True, max_length=20))
    source = mongo.ReferenceField(Publication, required=True)

class StatusBiogeo(mongo.EmbeddedDocument):
    status = mongo.StringField(required=True, max_length=20)
    locality_range = mongo.ListField(mongo.StringField(required=True, max_length=100))
    locality_range_code = mongo.ListField(mongo.StringField(required=False, max_length=10))
    source = mongo.ReferenceField(Publication, required=True)

class Taxa(mongo.Document):
    family = mongo.StringField(required=True, max_length=100)
    genus = mongo.StringField(required=True, max_length=100)
    #, unique_with=['specific_epithet', 'infraspecific_epithet'])
    specific_epithet = mongo.StringField(required=False, max_length=100, default='sp.')
    scientific_name_authorship = mongo.StringField(required=False, max_length=100)
    taxon_rank = mongo.StringField(required=True, max_length=50, choices=['genus', 'species', 'subspecies', 'varietas'])
    verbatim_taxon_rank = mongo.StringField(required=False, max_length=100, choices=['subsp.', 'var.'])
    infraspecific_epithet = mongo.StringField(required=False, max_length=100)
    taxonomic_status = mongo.StringField(required=True, choices=['accepted', 'synonym', 'invalid'])
    name_according_to = mongo.ListField(mongo.StringField(required=False, max_length=20))
    accepted_name_usage = mongo.ReferenceField('self', required=False)
    growth_form = mongo.EmbeddedDocumentListField(GrowthForm, required=False)
    status_biogeo = mongo.EmbeddedDocumentListField(StatusBiogeo, required=False)
    calalog_date = mongo.DateTimeField(default=datetime.datetime.utcnow())
    cataloger = mongo.EmbeddedDocumentField(Person, required=True)

    meta={
        'indexes':[
            {
                'fields':[
                    'genus','specific_epithet', 'infraspecific_epithet'
                ],
                'unique':True
            }
        ]
    }

    def parse_accepted(self, fullname):
        '''
        Parse a string with the fullname of a taxon into its separate components
        '''
        parse = fullname.split()
        if len(parse) == 2:
            self.genus = parse[0]
            self.specific_epithet = parse[1]
            self.taxon_rank = 'species'
        elif len(parse) == 4:
            self.genus = parse[0]
            self.specific_epithet = parse[1]
            self.verbatim_taxon_rank = parse[2]
            self.infraspecific_epithet = parse[3]
            if parse[2].lower() == 'var.':
                self.taxon_rank = 'varietas'
            else:
                self.taxon_rank = "subspecies"
        else:
            self.genus = parse[0]
            self.taxon_rank = 'genus'

    def fill_taxon_rank(self):
        """
        Fill the taxonomic rank abbreviation from the taxon rank field
        """
        ranks = {'species':None, 'subspecies':'subsp.', 'varietas':'var.'}
        self.verbatim_taxon_rank = ranks.get(self.taxon_rank, None)

######### Records documents definitions ###########

class Elevation(mongo.EmbeddedDocument):

    minimumElevationInMeters = mongo.IntField()
    maximumElevationInMeters = mongo.IntField()

class Date(mongo.EmbeddedDocument):
    startEventDate = mongo.DateTimeField()
    endEventDate = mongo.DateTimeField()
    isCompleteDate = mongo.BooleanField()


class PointLocation(mongo.EmbeddedDocument):
    geometry = mongo.PointField
    geodeticDatum = mongo.StringField(required=True, max_length=10)
    georeferenceSources = mongo.StringField(required=True, max_length=20)
    georeferenceProtocol = mongo.StringField(required=False)

class LineLocation(mongo.EmbeddedDocument):
    geometry = mongo.LineStringField()
    geodeticDatum = mongo.StringField(required=True, max_length=10)
    georeferenceSources = mongo.StringField(required=True, max_length=20)
    georeferenceProtocol = mongo.StringField(required=False)

class PolygonLocation(mongo.EmbeddedDocument):
    geometry = mongo.PolygonField()
    geodeticDatum = mongo.StringField(required=True, max_length=10)
    georeferenceSources = mongo.StringField(required=True, max_length=20)
    georeferenceProtocol = mongo.StringField(required=False)


class Record (mongo.Document):
    country = mongo.StringField(required=True, max_length=100)
    countryCode = mongo.StringField(required=False, max_length=5)
    stateProvince = mongo.StringField(required=True, max_length=100)
    county = mongo.StringField(required=False, max_length=100)
    geoPlace = mongo.ListField(mongo.StringField(required=False, max_length=100))
    locality = mongo.ListField(mongo.StringField(required=True))
    habitat = mongo.ListField(mongo.StringField(required=True))
    elevation = mongo.EmbeddedDocumentField(Elevation, required=False)
    date = mongo.EmbeddedDocumentField(Date, required=True)
    basisOfRecord = mongo.StringField(required=True, max_length=20)
    taxonId = mongo.ListField(mongo.ReferenceField(Taxa, required=True))
    publicationId = mongo.ReferenceField(Publication)
    geolocaion = mongo.GenericEmbeddedDocumentField(required=False)
    calalogDate = mongo.DateTimeField(default=datetime.datetime.utcnow())
    cataloger = mongo.EmbeddedDocumentField(Person, required=True)

    meta = {'allow_inheritance': True}


class SpecimenRecord(Record):
    associatedTaxa = mongo.ListField(mongo.StringField(required=False, max_length=100))
    description = mongo.StringField(required=False)
    recorddedBy = mongo.EmbeddedDocumentListField(Person, required=False)
    recordNumber = mongo.StringField(required=False, max_length=20)
    ownerInstitutionCode = mongo.ListField(mongo.StringField(required=False, max_length=10))
