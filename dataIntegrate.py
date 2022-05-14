import pandas as pd

censusDF=pd.read_csv("acs2017_census_tract_data.csv")


censusDF=pd.DataFrame().assign(County=censusDF["County"],Population=censusDF["TotalPop"],poverty=censusDF["Poverty"],PerCapitalIncome=censusDF["IncomePerCap"],State=censusDF["State"])


def calculate_povertyNumbers(pop,pov):
    return (pov*pop/100)

def calculate_ppoverty(pop,pov):
    return (pov*100/pop)

censusDF["poverty"]=censusDF.apply(lambda x:calculate_povertyNumbers(x['Population'],x['poverty']),axis=1)
censusDF=censusDF.groupby(['County','State'])[['Population','poverty','PerCapitalIncome']].sum().reset_index()

# Add Column Field to uniquely identify each record
keyCounty=[]
feature="County"
for index,row in censusDF.iterrows():
    state=row["State"]
    cData=""
    county=row["County"]
    county=county.split(" ")
    for i in range(len(county)):
        if county[i]!="County":
            if i>0:
                cData+=" "+county[i]
            else:
                cData+=county[i]
    keyCounty.append(cData+" "+state)

censusDF=censusDF.assign(countyState=keyCounty)
censusDF=censusDF.set_index('countyState')
censusDF["poverty"]=censusDF.apply(lambda x:calculate_ppoverty(x['Population'],x['poverty']),axis=1)

# County_Info of Loudoun County in Virginia

print(censusDF.query('(County in ["Loudoun County"]) and (State in ["Virginia"])'))

# County_Info of Washington County in Oregon

print(censusDF.query('(County in ["Washington County"]) and (State in ["Oregon"])'))

# County_Info of Harlan County in Kentucky

print(censusDF.query('(County in ["Harlan County"]) and (State in ["Kentucky"])'))

# County_Info of Malheur County in Oregon

print(censusDF.query('(County in ["Malheur County"]) and (State in ["Oregon"])'))




# Most populous county in the USA

maxPop=censusDF['Population'].max()
print("Most populous county in the USA")

print(censusDF.query(f'Population=={maxPop}'))


# Least populous county in the USA

minPop=censusDF['Population'].min()

print("Least populous county in the USA")

print(censusDF.query(f'Population=={minPop}'))

# Covid Dataframe 

covidDF=pd.read_csv("COVID_county_data.csv")


# Covid_monthly Info of Malheur County Oregon for August 2020

aug_list=[]
for i in range(1,32):
    dateStr=f"2020-08-{i}"
    aug_list.append(dateStr)
augDF=covidDF.query(f'(county in ["Malheur"]) and (date in {aug_list})')

augCases=0
augDeaths=0
for index,row in augDF.iterrows():
    augCases=augCases+row["cases"]
    augDeaths=augDeaths+row["deaths"]
print("# Cases in Aug 2020 :",augCases)
print("# Deaths in aug2020 :",augDeaths)

# Covid_monthly Info of Malheur County Oregon for January 2021
jan_list=[]
for i in range(1,32):
    dateStr=f"2021-01-{i}"
    jan_list.append(dateStr)

janDF=covidDF.query(f'(county in ["Malheur"]) and (date in {jan_list})')
janCases=0
janDeaths=0
for index,row in janDF.iterrows():
    janCases=janCases+row["cases"]
    janDeaths=janDeaths+row["deaths"]

print("# Cases in Jan 2021 :",janCases)
print("# Deaths in Jan 2021 :",janDeaths)


# Covid_monthly Info of Malheur County Oregon for February 2021

feb_list=[]
for i in range(1,39):
    dateStr=f"2021-02-{i}"
    feb_list.append(dateStr)

febDF=covidDF.query(f'(county in ["Malheur"]) and (date in {feb_list})')
febCases=0
febDeaths=0
for index,row in febDF.iterrows():
    febCases=febCases+row["cases"]
    febDeaths=febDeaths+row["deaths"]

print("# Cases in Feb 2021 :",febCases)
print("# Deaths in Feb 2021 :",febDeaths)


covidDF=covidDF.groupby(["county","state"])[["cases","deaths"]].sum().reset_index()

foreignIdx=[]
for index,row in covidDF.iterrows():
    foreignIdx.append(row["county"]+" "+row["state"])

covidDF=covidDF.assign(countyState=foreignIdx)
covidDF=covidDF.set_index('countyState')

covidDF=pd.DataFrame().assign(cases=covidDF["cases"],deaths=covidDF["deaths"])
covidMonthly=pd.merge(censusDF,covidDF,on="countyState",how="left")
covidMonthly=covidMonthly.dropna()


list_idx=[]
sidx=1
for index,row in covidMonthly.iterrows():
    list_idx.append(sidx)
    sidx=sidx+1
covidMonthly=covidMonthly.assign(ID=list_idx)
covidMonthly=covidMonthly.set_index('ID')
casesPer100K=[]
for index,row in covidMonthly.iterrows():
    casesPop=row["cases"]/row["Population"]*0.00001
    casesPer100K.append(casesPop)

covidMonthly["CasesPer100K"]=casesPer100K


# Covid Summary for Washington County and Oregon State
print("Covid Summary for Washington County and Oregon State")
print(covidMonthly.query(f'(County in ["Washington County"]) and (State in ["Oregon"])'))

# Covid Summary for Malheur County and Oregon State
print("Covid Summary for Malheur County and Oregon State")
print(covidMonthly.query(f'(County in ["Malheur County"]) and (State in ["Oregon"])'))

# Covid Summary for Loudoun County and Virginia State
print("Covid Summary for Loudoun County and Oregon State")
print(covidMonthly.query(f'(County in ["Loudoun County"]) and (State in ["Virginia"])'))

# Covid Summary for Harlan County and Kentucky State
print("Covid Summary for Harlan County and Kentucky State")
print(covidMonthly.query(f'(County in ["Harlan County"]) and (State in ["Kentucky"])'))