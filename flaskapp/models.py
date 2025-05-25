from flaskapp import db
from datetime import datetime


# Defining a model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.id}'')"


# 2010-2019 BES Constituency Results with Census and Candidate Data
# from: https://www.britishelectionstudy.com/data-objects/linked-data/
# citation: Fieldhouse, E., J. Green., G. Evans., J. Mellon & C. Prosser (2019) British Election Study 2019 Constituency  Results file, version 1.1, DOI: 10.48420/20278599
class UkData(db.Model):
    id = db.Column(db.String(9), primary_key=True)  # UK parliamentary constituency ID
    constituency_name = db.Column(db.Text, nullable=False)  # UK parliamentary constituency
    country = db.Column(db.String(8), nullable=False)  # England, Scotland, Wales
    region = db.Column(db.String(24), nullable=False)  # UK Region
    Turnout19 = db.Column(db.Float, nullable=False)  # General Election 2019 Turnout (pct of electorate)
    ConVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Conservative votes
    LabVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Labour Party votes
    LDVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Liberal Democrat votes
    SNPVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 SNP Party votes (Scottish National Party)
    PCVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Plaid Cymru Party votes (only in Wales)
    UKIPVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 UKIP Party votes
    GreenVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Green Party votes
    BrexitVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 Brexit Party votes
    TotalVote19 = db.Column(db.Float, nullable=False)  # General Election 2019 total number of votes
    c11PopulationDensity = db.Column(db.Float, nullable=False)  # UK census 2011 population density
    c11Female = db.Column(db.Float, nullable=False)  # UK census 2011 - percentage of population who are female
    c11FulltimeStudent = db.Column(db.Float, nullable=False)  # UK census 2011 - percentage of pop who are students
    c11Retired = db.Column(db.Float, nullable=False)  # UK census 2011 - percentage of population who are retired
    c11HouseOwned = db.Column(db.Float, nullable=False)  # UK census 2011 - percentage of population who own their home
    c11HouseholdMarried = db.Column(db.Float, nullable=False)  # UK census 2011 - percentage of pop who are married
