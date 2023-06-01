import pandas as pd
import json
import os

directory_json = str(input("Where is located your json? Dont forget to add *filename*.json in the directory? \n"))
directoryFormatedPricing = str (input('Where do you want to save the new Excel file? \n')) 
nameFormatedPricingFile = str(input('Give me the project name. \n'))
#nameFormatedPricingFile =  
# if nameFormatedPricingFile[-1] != '/' or nameFormatedPricingFile[-1] != '/':
#     if directoryFormatedPricing.find('/') != -1:
#         nameFormatedPricingFile += '/'



# ./queue/My Estimate.json
# ./output/
#DebtManager

f = open(directory_json)

data = json.load (f)
pricing_groups = []
service_name = []
description = []
region = []
monthly = []
upfront = []
first_year = []
configuration_summary = []
pricingUMY = {}
remainPricing = {}

#It gets the Upfront, Monthly and 12 months pricing values 
def getPricingUMY ():

    for x in data['Total Cost']:
        pricingUMY[x] = data['Total Cost'][x]

def headerCleanUp (trim):
    trim = trim.replace(', ', ",")
    trim = trim.replace("'", "")
    trim = trim.replace("[", "")
    trim = trim.replace("]", "")
    trim = trim.replace('"', "")
    trim = trim.replace('{', "")
    trim = trim.replace('}', "")
    return trim
    
def cleanUp2 (trim) :
    for x in range(0, len(trim)):
        merge = str(trim[x])
        merge = merge.replace(', ', ",")
        merge = merge.replace("'", "")
        merge = merge.replace("[", "")
        merge = merge.replace("]", "")
        merge = merge.replace('"', "")
        merge = merge.replace('{', "")
        merge = merge.replace('}', "")
        trim[x] = merge

def groupInfo (x,a):
    pricing_groups.append(x)
    service_name.append(a['Service Name'])
    description.append(a['Description'])
    region.append(a['Region'])
    monthly.append(a['Service Cost']['monthly'])
    upfront.append(a['Service Cost']['upfront']) 
    first_year.append(a['Service Cost']['12 months'])
    configuration_summary.append(a['Properties'])

def getRemainPricing ():
    for x in data ['Groups']:
        for y in data ['Groups'][x]:
            if x == 'Services':
                    groupInfo(data["Name"],y)
            else:
                for a in data ['Groups'][x][y]:
                    groupInfo(x,a)
    try:    
        if data['Support']:
            pricing_groups.append('All')
            service_name.append(data['Support']['Plan Name'])
            description.append(data['Support']['Support Description'])
            region.append(data['Support']['Region'])
            monthly.append(data['Support']['Service Cost']['monthly'])
            upfront.append(data['Support']['Service Cost']['upfront'])
            first_year.append(data['Support']['Service Cost']['12 months'])
            configuration_summary.append(data['Support']['Summary'])
    except:
        print("No AWS support detected!")
    
def listsToDict ():    
    remainPricing ['Group hierarchy'] = pricing_groups
    remainPricing ['Service']  = service_name
    remainPricing ['Description'] = description
    remainPricing ['Region'] = region
    remainPricing ['Upfront'] = upfront
    remainPricing ['Monthly'] = monthly
    remainPricing ['First 12 months total'] = first_year
    remainPricing ['Configuration summary'] = configuration_summary

    
    cleanUp2(pricing_groups)
    cleanUp2(service_name)
    cleanUp2(description)
    cleanUp2(region)
    cleanUp2(monthly)
    cleanUp2(upfront)
    cleanUp2(first_year)
    cleanUp2(configuration_summary)

def tableFormating (): #directoryFormatedPricing + data["Name"] + '_AWS_Pricing.xlsx'
    with pd.ExcelWriter(directoryFormatedPricing + nameFormatedPricingFile + '_Pricing_AWS.xlsx' , engine='xlsxwriter') as writer:
            dfA.to_excel(writer, sheet_name='AWS Pricing', index=False, startrow=5, startcol=1)
            column_settings = [{'header': headerCleanUp(column)} for column in dfA.columns] 
            (max_row, max_col) = dfA.shape
            workbook = writer.book
            money_format = workbook.add_format({'num_format': '$###,##0.00'})
            border_format = workbook.add_format({
                                'border':1,
                                'align':'left',
                                'font_size':10
                            })
            merge_format = workbook.add_format({
                                "bold": 1,
                                "border": 1,
                                "align": "center",
                                "valign": "vcenter",
                                "fg_color": "orange",
                            })
            merge_format2 = workbook.add_format({
                                "border": 1,
                                "align": "center",
                                "valign": "vcenter"
                            })

            bold_format = workbook.add_format({'bold': True})

            
            worksheet = writer.sheets['AWS Pricing']
            
            upfrontLetter = 'F'
            MonthlyLetter = 'G'
            
            sumUpfront = dfA['Upfront'].sum()
            sumMonthly = dfA['Monthly'].sum()
            sumFirstMonth = sumUpfront + sumMonthly
            sum12Months = dfA['First 12 months total'].sum()
            
            worksheet.add_table(5, 1, max_row+5, max_col, {'columns': column_settings})
            
            totalUpfrontStr = upfrontLetter + str(max_row+8)
            totalUpfrontCalc = MonthlyLetter + str(max_row+8)
            firstMonthStr = upfrontLetter + str(max_row+9)
            firstMonthCalc = MonthlyLetter + str(max_row+9)
            MonthStr = upfrontLetter + str(max_row+10)
            MonthCalc = MonthlyLetter + str(max_row+10)
            firstYearStr = upfrontLetter + str(max_row+11)
            firstYearCalc = MonthlyLetter + str(max_row+11)
            total3YearsStr = upfrontLetter + str(max_row+12)
            total3YearsCalc = MonthlyLetter + str(max_row+12)
            worksheet.write(totalUpfrontStr, "Total Upfront", None)
            worksheet.write(totalUpfrontCalc, sumUpfront, money_format)
            worksheet.write(firstMonthStr, "Total First Month", None)
            worksheet.write(firstMonthCalc, sumFirstMonth, money_format)
            worksheet.write(MonthStr, "Total Monthly", None)
            worksheet.write(MonthCalc, sumMonthly, money_format)
            worksheet.write(firstYearStr, "Total First Year", None)
            worksheet.write(firstYearCalc, sum12Months, money_format)
            worksheet.write(total3YearsStr, "Total 3 Years", None)
            worksheet.write(total3YearsCalc, (sum12Months+(sumFirstMonth*24)), money_format) #FAZ ESTA CONTA

            #worksheet.write("A1", "Group hierarchy")
            #worksheet.write("H1", "Configuration summary")

            moneyStrMerge =  "F6"+":"+"H"+str(max_row+6)
            worksheet.conditional_format(moneyStrMerge, {'type': 'cell',
                                            'criteria' : '>', 
                                            'value' : -99999999999,
                                            'format' : money_format})

            borderStrMerge = totalUpfrontStr+":"+total3YearsCalc
            worksheet.conditional_format(borderStrMerge, {'type': 'no_blanks',
                                            'format' : border_format})
                                            
            #VAIS TER QUE ALTERAR O A1 PARA UMA COISA MAIS AUTOMÁTICA
            geralBorderStrMerge = "B6"+":"+"I"+str(max_row+6)
            worksheet.conditional_format(geralBorderStrMerge, {'type': 'no_blanks',
                                            'format' : border_format})
            boldStrMerge = totalUpfrontStr+":"+total3YearsStr
            worksheet.conditional_format(boldStrMerge, {'type': 'no_blanks',
                                            'format' : bold_format})
            
            #Pricing Model and calculator link
            #worksheet.set_column("B:D", None)
            worksheet.merge_range("B2:E2", str(data["Name"]), merge_format)
            worksheet.merge_range("B3:E3", str(data["Metadata"]["Share Url"]), merge_format2)
            #worksheet.write_url("B3", )
            worksheet.conditional_format("B2:E3", {'type': 'blanks',
                                            'format' : border_format})
            worksheet.autofit()
    
getPricingUMY ()
getRemainPricing ()
# getSupport ()
listsToDict()


dfA = pd.DataFrame.from_dict(remainPricing)
dfA.fillna(' ',inplace=True)
dfA ['Upfront'] = dfA ['Upfront'].astype('float')
dfA ['Monthly'] = dfA ['Monthly'].astype('float')
dfA ['First 12 months total'] = dfA ['First 12 months total'].astype('float')
tableFormating ()

print("All done. Enjoy :)")
#print(len(data['Metadata']))#utiliza isto no for das descriptions


# json = pd.read_json('./My Estimate.json')
# print (json)
#https://pandas.pydata.org/docs/reference/api/pandas.read_json.html