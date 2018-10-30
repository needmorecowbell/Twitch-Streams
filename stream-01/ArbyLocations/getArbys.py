import requests
from bs4 import BeautifulSoup
import time
import json

class ArbyLocation(object):
    address = None
    phone = None
    url= None
    def __init__(self,address,phone, url):
        if(phone is None):
            self.phone=""
        if(address is None):
            self.address=""
        if(url is None):
            self.url = ""
        self.address = address
        self.phone=  phone
        self.url= url
    def getAddress(self):
        return self.address

    def getPhone(self):
        return self.phone

    def getLink(self):
        return self.url


class ArbyScraper(object):
    """docstring for ArbyScraper."""
    arbyLocationList= []

    def __init__(self):
        pass
    def scrape(self):
        base_url="https://locations.arbys.com/"

        print("Grabbing State Links...")
        arbyLinks= []
        stateLinks, directs = self.getStates(base_url)
        arbyLinks.extend(directs)
        print("State Links Grabbed")
        print("Grabbing Town Links...")
        townLinks,directs = self.getTownships(base_url, stateLinks)
        arbyLinks.extend(directs)
        print("Town Links Grabbed")
        print("Getting Individual Addresses...")

        arbyLinks.extend(self.getAddresses(base_url , townLinks))

        print("Getting Arby Location Information...")


        arbyLinks= [link.replace('../', '') for link in arbyLinks]
        self.parseArbys(arbyLinks) # parses all data into global arby location list


    def isDirectLink(self, url):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

        htmlBody= r.content
        soup = BeautifulSoup(htmlBody, 'html.parser')

        logisticsWrapper = soup.find(class_="logistics-wrapper")

        if logisticsWrapper is None:
            #print(url+":  NOT DIRECT")
            return False
        else:
            #print(url+":  DIRECT")
            return True


    def getStates(self,url):
        r = requests.get(url+"/index.html", headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

        htmlBody = r.content

        soup = BeautifulSoup(htmlBody, 'html.parser')
        states = soup.find(class_= 'state-list-container')
        states =  states.findAll(class_="c-directory-list-content-item-link")

        stateLinks=[]
        arbyLinks= []


        for stateContent in states:
            link = str(stateContent.attrs["href"])

            if(self.isDirectLink(url+link)):
                print(url+link+":   DIRECT" )

                arbyLinks.append(url+link)
            else:
                stateLinks.append(url+link)
                print(url+link+":   STATE" )
        return stateLinks, arbyLinks

    #Get links to single arbys locations.
    def getAddresses(self, base_url, urls):
        arbyLinks = []
        for townLink in urls:
            r = requests.get(townLink)
            htmlBody= r.content
            soup = BeautifulSoup(htmlBody, 'html.parser')
            linkDivs =  soup.findAll(class_="c-location-grid-item-link-visitpage")
            print("URL: "+townLink)
            for div in linkDivs:
                ext= str(div.attrs["href"])
                arbyLinks.append(base_url+ext)

        return arbyLinks

    #Get address from single arby location
    def parseArbys(self, urls):
        for url in urls:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            htmlBody= r.content
            address =None
            phone= None
            soup = BeautifulSoup(htmlBody, 'html.parser')
            print("URL: "+url)
            if soup.find(class_="c-address") is not None:
                address=soup.find(class_="c-address").text
                #print("\tAddress: "+address)
            if soup.find(class_="c-phone-number-link") is not None:
                phone=soup.find(class_="c-phone-number-link").text
                #print("\tPhone: "+phone)
            self.addArbyLocation(ArbyLocation(address,phone,url))
            time.sleep(0.01)

    def addArbyLocation(self, arby):
        self.arbyLocationList.append(arby)

    def getArbyLocations(self):
        return self.arbyLocationList

    def toJSON(self):
        json_data= {}
        json_data["arbyLocation"]=[]

        for arby in self.arbyLocationList:
            json_data["arbyLocation"].append({
                'url':arby.getLink(),
                'address':arby.getAddress(),
                'phone':arby.getPhone()

            })
        return json_data


    def getTownships(self, base_url, exts):
        townLinks= []
        arbyLinks= []
        for extension in exts:
            r = requests.get(extension)

            htmlBody= r.content
            soup = BeautifulSoup(htmlBody, 'html.parser')

            linkDivs = soup.findAll(class_="c-directory-list-content-item-link")

            for div in linkDivs:
                ext= str(div.attrs["href"])

                #Check whether it is direct location
                if(self.isDirectLink(base_url+ext)):
                    print(base_url+ext+":    DIRECT" )
                    arbyLinks.append(base_url+ext)
                else:
                    print(base_url+ext+":   TOWN" )
                    townLinks.append(base_url+ext)
            print("\n\nLinks for "+extension+" grabbed\n\n")

        return townLinks,arbyLinks

if __name__ == '__main__':
    a= ArbyScraper()
    a.scrape()

    print("Sending Data to JSON...")
    with open('arby-locations.json','w') as outfile:
        json.dump(a.toJSON(), outfile, sort_keys=True, indent=4)
    print("Logging Finished, file available in current directory as arby-locations.json")
