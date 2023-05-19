import pandas as pd
import json
import os

f = open('./My Estimate.json')
data = json.load (f)
pricing_groups = []
service_name = []
description = []
region = []
monthly = []
upfront = []
first_year = []
configuration_summary = []

#print (data['Name'])
pricingUMY = {}
support = {}
remainPricing = {}
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

#O TEU PROBLEMA AGORA É PERCEBER SE EXISTE MAIS QUE UM GRUPO, ENTÃO ASSOCIAR O GRUPO CERTO AO SERVIÇO
def getRemainPricing ():
    cnt = 0
    for x in data ['Groups']:
        pricing_groups.append(x)
        for y in data ['Groups'][x]:
            # print (y)
            # print(len(y) ,'\n')
            for a in data ['Groups'][x][y]:
                if a['Service Name']:
                    print(a['Service Name'])
                #print (a)
                #print(len(a) ,'\n')
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
                configuration_summary.append(str_to_merge)
                
def listsToDict ():
    # for x in range(1, len(service_name)):
    #     return "teste"
    remainPricing ['Group hierarchy'] = pricing_groups
    remainPricing ['Service'] = service_name
    remainPricing ['Description'] = description
    remainPricing ['Region'] = region
    remainPricing ['Monthly'] = monthly
    remainPricing ['Upfront'] = upfront
    remainPricing ['First 12 months total'] = first_year
    remainPricing ['Configuration summary'] = configuration_summary
    
    print(len(pricing_groups))
    print(len(service_name))
    print(len(description))
    print(len(region))
    print(len(monthly))
    print(len(upfront))
    print(len(first_year))
    print(len(configuration_summary))


    




getPricingUMY ()
getSupport ()
getRemainPricing ()

listsToDict()

#print (remainPricing)

pd.DataFrame.from_dict(remainPricing)
#print(len(data['Metadata']))#utiliza isto no for das descriptions


# json = pd.read_json('./My Estimate.json')
# print (json)
#https://pandas.pydata.org/docs/reference/api/pandas.read_json.html