# Created by: Trent Kindvall
#
#Thank you for this oportunity.
#
#Quick note if I had longer I would have added logging and made a more robust
#way to iterate through the xml tree.
#I would also move the more robust iterater to its own file and function so that
#it could be reused for other projects.
#
#There also apears to be an issue with people not filling out the bedroom and bathrooms feild
#Parsing the description apears to have the answers.
# If i had more time I would use the data in the description to create a better
#data set by parsing it.
#
#
import requests
import datetime as dt
import xml.etree.ElementTree as ET
import pandas as pd


#
#with open('feed.xml', 'wb') as file:
#    file.write(response.content)


def xml_down(f,url):
    response = requests.get(url)
    with open(f, 'wb') as file:
        file.write(response.content)

def write_csv(name,xml_out):
    with open(out_file, 'w') as f:
        write

def xml_iter(t):
    df = pd.DataFrame( )
    for listing in t.iter('Listing'):
        l = []
        room = []
        for ListingDetails in listing.iter('ListingDetails'):
            mlsId = ListingDetails.find("MlsId").text
            mlsName = ListingDetails.find("MlsName").text
            dateListed = ListingDetails.find("DateListed").text
            price = ListingDetails.find("Price").text
        for location in listing.iter('Location'):
            StreetAddress = location.find('StreetAddress').text
        for bd in listing.iter('BasicDetails'):
            Bedrooms = bd.find('Bedrooms').text
            Bathrooms = bd.find('Bathrooms').text
            fbath = bd.find('FullBathrooms').text
            hbath = bd.find('HalfBathrooms').text
            tqbath = bd.find('ThreeQuarterBathrooms').text
            description = bd.find('Description').text
        for rd in listing.iter('RichDetails'):
            Appliance = rd.find('Appliances').text
            for r in rd.iter('Rooms'):
                room.append(r.find('Room').text)

        # makes sure there are
        if fbath is None:
            fbath = 0
        else:
            fbath = int(fbath)
        if hbath is None:
            hbath = 0
        else:
            hbath = int(hbath)
        if tqbath is None:
            tqbath = 0
        else:
            tqbath = int(tqbath)
        if Bathrooms is None :
            Broom = fbath + (hbath*.5) + tqbath*.75
        elif Bathrooms < fbath + (hbath*.5) + tqbath*.75:
            Broom = fbath + (hbath*.5) + tqbath*.75
        else:
             Broom = Bathrooms


        l.append( [mlsId,mlsName,dateListed,price,StreetAddress,Bedrooms,Broom,Appliance,room,description])
        if description.find('and') >=0 and dateListed >= '2016-01-01 00:00:00':
            df = df.append(l)

    #df.rename(columns={0:'MlsId',1: 'MlsName',2: 'DateListed',3:'StreetAddress',4:'Price',5:'Bedrooms',6:'Bathrooms',7:'Appliances',8:'Rooms',9:'Description'}, inplace=True)
    return df


def main():
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    xml_down('feed.xml',url) #download the XMl feed from the provied url

    tree = ET.parse('feed.xml') #creates xml document from the download
    root =  tree.getroot() #sets the root of the xml document

    df = xml_iter(tree) #iterates over the xml data structure and returns a DataFrame
    df.sort_values(by = 3) # 3 is the date column



    out_file = str(dt.date.today()) + '.csv' #sets path for output file
    df.to_csv(out_file,header = ['MlsId','MlsName','DateListed','StreetAddress','Price','Bedrooms','Bathrooms','Appliances','Rooms','Description'])#creates a csv with correct headers



if __name__ == "__main__":
    main()
