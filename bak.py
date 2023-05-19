import pandas as pd
import json
import os

f = open('./My Estimate.json')
data = json.load (f)

#print (data['Name'])
pricingUMY = support = remainPricing = {}
#It gets the Upfront, Monthly and 12 months pricing values 
def getPricingUMY ():

    for x in data['Total Cost']:
        pricingUMY[x] = data['Total Cost'][x]

#Here you have to add any procedure to check if support exists
def getSupport ():

    support ['Service Name'] = data['Support']['Plan Name']
    support ['Region'] = data['Support']['Region']
    support ['Configuration Summary'] = data['Support']['Summary']
    for x in data['Support']['Service Cost']:
        pricingUMY[x] = data['Support']['Service Cost'][x]

def getRemainPricing ():
    pricing_groups = []
    service_name = []
    description = []
    region = []
    monthly = []
    upfront = []
    first_year = []
    configuration_summary = []
    
    for x in data ['Groups']:
        pricing_groups.append(x)
        for y in data ['Groups'][x]:
            #print (y)
            for a in data ['Groups'][x][y]:
                str_to_merge = ""
                #print(a['Service Name'])
                service_name.append(a['Service Name'])
                
                description.append(a['Description'])
                region.append(a['Region'])
                monthly.append(a['Service Cost']['monthly'])
                upfront.append(a['Service Cost']['upfront']) 
                first_year.append(a['Service Cost']['12 months'])

                for i in data ['Groups'][x][y]:
                    str_to_merge = i['Properties']
                #print (str_to_merge)
                configuration_summary.append(str_to_merge)
                
                #print(service_name)
                

                #print (str_to_merge)


                # for e in a:
                #     print (e)
                #     if e == "Service Name":
                #         service_name.append(data['Groups'][x][y][e])
                #     elif e == "Description":
                #         description.append(data['Groups'][x][y][e])
                #     elif e == "Region":
                #         region.append(data['Groups'][x][y][e])
                
                # for b in data ['Groups'][x][y]['Service Cost']:
                #     print (b)
                #     if b == "monthly":
                #         monthly.append(data['Groups'][x][y]['Service Cost'][b])
                #     elif b == "upfront":
                #         upfront.append(data['Groups'][x][y]['Service Cost'][b])
                #     elif b == "12 months":
                #         first_year.append(data['Groups'][x][y]['Service Cost'][b]) 

                # for b in data ['Groups'][x][y]['Properties']:
                #     str_to_merge += ['Groups'][x][y]['Properties'][b]


def listsToDict ():
    return 'teste'

getPricingUMY ()
getSupport ()
getRemainPricing ()
listsToDict()
#print(len(data['Metadata']))#utiliza isto no for das descriptions


# json = pd.read_json('./My Estimate.json')
# print (json)
#https://pandas.pydata.org/docs/reference/api/pandas.read_json.html