import pandas as pd
import json
import os

f = open('./queue/My Estimate.json')
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

def headerCleanUp (trim):
    trim = trim.replace(', ', ",")
    trim = trim.replace("'", "")
    trim = trim.replace("[", "")
    trim = trim.replace("]", "")
    trim = trim.replace('"', "")
    trim = trim.replace('{', "")
    trim = trim.replace('}', "")
    return trim

#Here you have to add any procedure to check if support exists
def getSupport ():

    support ['Service Name'] = data['Support']['Plan Name']
    support ['Region'] = data['Support']['Region']
    support ['Configuration Summary'] = data['Support']['Summary']
    for x in data['Support']['Service Cost']:
        pricingUMY[x] = data['Support']['Service Cost'][x]

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

def getRemainPricing ():
    for x in data ['Groups']:
        for y in data ['Groups'][x]:
            for a in data ['Groups'][x][y]:
                pricing_groups.append(x)
                service_name.append(a['Service Name'])
                description.append(a['Description'])
                region.append(a['Region'])
                monthly.append(a['Service Cost']['monthly'])
                upfront.append(a['Service Cost']['upfront']) 
                first_year.append(a['Service Cost']['12 months'])
                configuration_summary.append(a['Properties'])

def listsToDict ():    
    remainPricing ['Group hierarchy'] = pricing_groups
    remainPricing ['Service']  = service_name
    remainPricing ['Description'] = description
    remainPricing ['Region'] = region
    remainPricing ['Monthly'] = monthly
    remainPricing ['Upfront'] = upfront
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

def tableFormating ():
    with pd.ExcelWriter('./output/My Estimate - Phase 1.xlsx', engine='xlsxwriter') as writer:
            dfA.to_excel(writer, sheet_name='Sheet1', index=False, startrow=0, startcol=0)
            column_settings = [{'header': headerCleanUp(column)} for column in dfA.columns] 
            (max_row, max_col) = dfA.shape
            workbook = writer.book
            money_format = workbook.add_format({'num_format': '$###,##0.00'})
            border_format = workbook.add_format({
                                'border':1,
                                'align':'left',
                                'font_size':10
                            })

            bold_format = workbook.add_format({'bold': True})

            
            worksheet = writer.sheets['Sheet1']
            
            upfrontLetter = 'E'
            MonthlyLetter = 'F'
            
            sumUpfront = dfA['Upfront'].sum()
            sumMonthly = dfA['Monthly'].sum()
            sumFirstMonth = sumUpfront + sumMonthly
            sum12Months = dfA['First 12 months total'].sum()
            
            worksheet.add_table(0, 0, max_row, max_col-1, {'columns': column_settings})
            
            totalUpfrontStr = upfrontLetter + str(max_row+3)
            totalUpfrontCalc = MonthlyLetter + str(max_row+3)
            firstMonthStr = upfrontLetter + str(max_row+4)
            firstMonthCalc = MonthlyLetter + str(max_row+4)
            MonthStr = upfrontLetter + str(max_row+5)
            MonthCalc = MonthlyLetter + str(max_row+5)
            firstYearStr = upfrontLetter + str(max_row+6)
            firstYearCalc = MonthlyLetter + str(max_row+6)
            total3YearsStr = upfrontLetter + str(max_row+7)
            total3YearsCalc = MonthlyLetter + str(max_row+7)
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

            moneyStrMerge =  "E2"+":"+"G"+str(max_row+1)
            worksheet.conditional_format(moneyStrMerge, {'type': 'cell',
                                            'criteria' : '>', 
                                            'value' : -99999999999,
                                            'format' : money_format})

            borderStrMerge = totalUpfrontStr+":"+total3YearsCalc
            worksheet.conditional_format(borderStrMerge, {'type': 'no_blanks',
                                            'format' : border_format})
                                            
            #VAIS TER QUE ALTERAR O A1 PARA UMA COISA MAIS AUTOMÁTICA
            geralBorderStrMerge = "A1"+":"+"H"+str(max_row+1)
            worksheet.conditional_format(geralBorderStrMerge, {'type': 'no_blanks',
                                            'format' : border_format})
            boldStrMerge = totalUpfrontStr+":"+total3YearsStr
            worksheet.conditional_format(boldStrMerge, {'type': 'no_blanks',
                                            'format' : bold_format})

            worksheet.autofit()
    
getPricingUMY ()
getSupport ()
getRemainPricing ()
listsToDict()

dfA = pd.DataFrame.from_dict(remainPricing)
dfA.fillna(' ',inplace=True)
dfA ['Upfront'] = dfA ['Upfront'].astype('float')
dfA ['Monthly'] = dfA ['Monthly'].astype('float')
dfA ['First 12 months total'] = dfA ['First 12 months total'].astype('float')
tableFormating ()

#print(len(data['Metadata']))#utiliza isto no for das descriptions


# json = pd.read_json('./My Estimate.json')
# print (json)
#https://pandas.pydata.org/docs/reference/api/pandas.read_json.html