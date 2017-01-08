from lxml import html
import requests

page = requests.get('http://www.amazon.com/Catching-Fire-Second-Hunger-Games/dp/0545586178/ref=sr_1_1?s=books&ie=UTF8&qid=1398311376&sr=1-1&keywords=catching+fire')
tree = html.fromstring(page.text)       

title = tree.xpath("//title/text()")[0]
#author = tree.xpath("//span[@class='a-size-medium']/text()")[0].replace('\n','').strip()
price = tree.xpath("//span[@class='price bxgy-item-price']/text()")[0]
pricerent = tree.xpath("//span[@class='rentPrice']/text()")
productdetails2 = tree.xpath("//div[@class='content']/ul/li/b/text()")
productdetails = tree.xpath("//div[@class='content']/ul[not(@class)]/li/text()")
rating = tree.xpath("//div[@class='content']//span[@class='asinReviewsSummary acr-popover']//span/text()")
numcustomer = tree.xpath("//div[@class='content']//span[@class='crAvgStars']/a/text()")
customereview = tree.xpath("//div[@class='drkgry']/text()")
additionalrankings = tree.xpath("//div[@class='content']//ul[@class='zg_hrsr']//text()")

#Handles rent price
if len(pricerent) > 1:
    pricerent = pricerent[-1:]
#Handles additional rankings
y = 0
for x in additionalrankings:
    additionalrankings[y] = x.replace('\n','')
    additionalrankings[y] = additionalrankings[y].strip()
    y = y + 1

additionalrankings = list(filter(None, additionalrankings))


for x in range(0,len(additionalrankings)):
    if '>' in additionalrankings:
        additionalrankings.remove(">")
    if "in" in additionalrankings:
        additionalrankings.remove("in")

#Handles The customers comments
y = 0
for x in customereview:
    customereview[y] = x.replace('\n','')
    customereview[y] = customereview[y].strip()
    y = y + 1

customereview = list(filter(None, customereview))

#Handles the rating and number of customers who rated
if len(rating) > 0:
    rating = rating[0].split()
    rating = float(rating[0])

if len(numcustomer) > 0:
    numcustomer = numcustomer[0].split()
    numcustomer = numcustomer[0].replace(',', '')
    numcustomer = int(numcustomer)

rating = tuple([rating, numcustomer])

y = 0

#Handles product details
for x in productdetails2:
    productdetails2[y] = x.replace('\n','')
    productdetails2[y] = productdetails2[y].strip()
    y = y + 1

y = 0
for x in productdetails:
    productdetails[y] = x.replace('\n','')
    productdetails[y] = productdetails[y].strip()
    if y > 3:
        productdetails[y] = productdetails[y].strip('()')
    y = y + 1

productdetails = list(filter(None, productdetails))

for x in range(0,len(productdetails)):
    if '>' in productdetails:
        productdetails.remove(">")

productdetails.append(rating)
productdetails[-2], productdetails[-1] = productdetails[-1], productdetails[-2]


productdetails3 = list()
for x, y in zip(productdetails,productdetails2):
    productdetails3.append([y, x])
    

#Prints the parsed data
    
print ("Title: ", title)
#print ("Author: ", author)
print ("Price: ", price)
print ("Rent price: ", pricerent)
print ("Product details: ", productdetails3)
print ("Helpful Reviews: ", customereview)
print ("Numbers: ",additionalrankings)
