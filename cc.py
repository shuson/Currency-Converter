import requests
from wox import Wox,WoxAPI
import clipboard
from os.path import dirname, join
import pycountry
from bs4 import BeautifulSoup
import re

a=""

class Main(Wox):
	icon = join(dirname(__file__), 'Images', 'plugin.png')
	def request(self,url):
		#f*k off auto extraction prohibited error
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
		return requests.get(url, headers=headers)
	
	def query(self,query):
		results=[]
		args = query.split(' ')
		if len(args)==3 and len(args[1])==3 and len(args[2])==3:
			url = ('http://www.xe.com/currencyconverter/convert/?Amount=1&From=%s&To=%s') % (args[1], args[2])
			r = self.request(url)
			soup = BeautifulSoup(r.text, "html.parser")
			data = soup.find('span', attrs={'class':'uccResultAmount'})
			m=re.findall(r'[\w.]+',data.text)
			a=m[0]
			try:
				a=float(a)
				b=float(args[0])*a
				c=args[2]
				pass
			except Exception, e:
				b="Invalid amount"
				c="" 
				pass
			finally:
				pass
			results=[]
			if b>0.000001 and b!="Invalid amount":
				c=c.upper()
				c=pycountry.currencies.get(letter=c)
				x=str(c.name)
				b="{0:.2f}".format(b)
				b=str(b)
				results.append({
   					"Title": b+" "+x+"s",
    				"SubTitle":"Copy to clipboard",
    				"IcoPath":"Images/plugin.png",
    				"JsonRPCAction":{'method': 'copy', 'parameters': [b],'dontHideAfterAction': False}
				})
				return results
				
			if args[0] == "0":
				str(b)
				results.append({
   				"Title": "Please enter an ammount other than 0",
    			"SubTitle":"We can't convert nothing...",
    			"IcoPath":"Images/plugin.png"
				})
				return results
			if b<=0:
				str(b)
				results.append({
   				"Title": "Please enter valid currency codes",
    			"SubTitle":"One of those currencies doesn't exist",
    			"IcoPath":"Images/plugin.png"
				})
				return results
			if b=="Invalid amount":
				results.append({
   				"Title": "Invalid amount",
    			"SubTitle":"Enter a number",
    			"IcoPath":"Images/plugin.png"
				})
				return results
		else:
			results=[]
			results.append({
       			"Title":"Currency Converter",
        		"SubTitle":"How may I take your order?",
        		"IcoPath":"Images/plugin.png"
        	})
    		return results		
   
	def copy(self, data):
		clipboard.put(data)
		WoxAPI.show_msg("Value has been copied to clipboard.", '', self.icon)

if __name__ == "__main__":
	Main()
