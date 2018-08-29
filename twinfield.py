import pandas as pd
import xml.etree.ElementTree as ET
from zeep import Client
import query
import authentication

# implement logging to logfile:

import logging

logger = logging.getLogger()
logging.getLogger('zeep').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
handler = logging.FileHandler('./twinfield.log')
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#setup connection to Twinfields, provide credentials and receive cluster:

sessionlogin = r'https://login.twinfield.com/webservices/session.asmx?wsdl'
login = Client(sessionlogin)

auth = login.service.Logon(authentication.username, authentication.password, authentication.organisation)

auth_header = auth['header']['Header']
cluster = auth['body']['cluster']

#Use cluster to create a session:

url_session = cluster + r'/webservices/session.asmx?wsdl'
session = Client(url_session)

#Select a company for the session:

session.service.SelectCompany('NLA000311', _soapheaders={'Header': auth_header})

#And then connect to the actual webservice:

proces_url = cluster + r'/webservices/processxml.asmx?wsdl'
proces = Client(proces_url)

#Send the query and get the twinfield server response (XML):

response = proces.service.ProcessXmlString(query.XML_String,  _soapheaders={'Header': auth_header})

logger.debug('response received of %s characters', len(response))

#Write raw response to XML:

xmlfilename = 'twinfield.xml'

f = open(xmlfilename, 'w')
f.write(response)
f.close()

logger.debug('Raw XML file written: %s', xmlfilename)

tree = ET.parse(xmlfilename)

#Parse XML response to pandas dataframe:

root = tree.getroot()
columns = [element.attrib['label'] for element in root[0]]
columns.append('?')

data = [[field.text for field in row] for row in root[1::]]
df = pd.DataFrame(data, columns=columns)
df = df.drop('?', axis=1)

#Write dataframe to csv:

df.to_csv('twinfield.csv')

logger.debug('CSV file written with %s lines', len(df))





