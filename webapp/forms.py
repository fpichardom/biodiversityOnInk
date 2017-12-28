from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, BooleanField, TextAreaField,
                    SelectField, DecimalField, FormField, SubmitField, FieldList)
from wtforms.validators import InputRequired, Length, Optional


class Person(FlaskForm):
    """
    Person model form.
    """
    lastname = StringField('Last Name', validators=[InputRequired(), Length(max =50)])
    firstname = StringField('First Name', validators=[InputRequired(), Length(max =50)])
    middlename = StringField('Middle Name', validators=[Optional(), Length(max =50)])


######## Publication forms ############
class Publication(mongo.Document):
    """
    General publication model
    """

    key = mongo.StringField(required=True, unique=True, max_length=50)
    title = mongo.StringField(required=True)
    author = mongo.EmbeddedDocumentListField(Person, required=True)
    year = mongo.StringField(require = True, max_length=4)
    date = mongo.DateTimeField(required=True)
    doi = mongo.StringField(required=False, unique=True, max_length=100)
    calalog_date = mongo.DateTimeField(default=datetime.datetime.utcnow())
    cataloger = mongo.EmbeddedDocumentField(Person, required=True)

    meta = {'allow_inheritance':True}

    def create_key(self):
        if entry_type = 'article':
            self.key = ':'.join[unidecode(self.author.lower()), self.year,self.volume, self.pages]


class Article(Publication):
    """

    """
    entry_type = "article"
    volume = mongo.StringField(max_length=5)
    number = mongo.StringField(max_length=5)
    journal = mongo.StringField()
    shortjournal = mongo.StringField()
    pages = mongo.StringField(max_length=10)