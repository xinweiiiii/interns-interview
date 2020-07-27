import mysql.connector
import xlrd
import math

data = xlrd.open_workbook("10 Years Financial Data.xlsx")
sheet = data.sheet_by_name("Financial Data")

database = mysql.connector.connect(host="localhost", user="root", password="root", port=8889, db="financial_data")

cursor = database.cursor() #Read the database

# query = "INSERT INTO Profit & Loss ("
db_name = "Profit_Loss"
for row in range(3, sheet.nrows):

    accouting_name = sheet.cell_value(row, 0)
    if accouting_name == "Balance Sheet (SGD '000)":
        db_name = "Balance_Sheet"
    if accouting_name == "Cash Flow (SGD '000)":
        db_name = "Cash_Flow"
    if accouting_name == "Financial Ratios (SGD)":
        db_name = "Financial_Ratio"
     
    year_2005 = sheet.cell_value(row, 2)
    year_2006 = sheet.cell_value(row, 3)
    year_2007 = sheet.cell_value(row, 4)
    year_2008 = sheet.cell_value(row, 5)
    year_2009 = sheet.cell_value(row, 6)
    year_2010 = sheet.cell_value(row, 7)
    year_2011 = sheet.cell_value(row, 8)
    year_2012 = sheet.cell_value(row, 9)
    year_2013 = sheet.cell_value(row, 10)
    year_2014 = sheet.cell_value(row, 11)
    year_2015 = sheet.cell_value(row, 12)
    year_2016 = sheet.cell_value(row, 13)
    year_2017 = sheet.cell_value(row, 14)
    year_2018 = sheet.cell_value(row, 15)
    year_2019 = sheet.cell_value(row, 16)

    query = "INSERT INTO " + db_name +  "(Account_Info, Year_2005, Year_2006, Year_2007, Year_2008, Year_2009, Year_2010, Year_2011, Year_2012, Year_2013, Year_2014, Year_2015, Year_2016, Year_2017, Year_2018, Year_2019) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    
    value = [accouting_name, year_2005, year_2006, year_2007, year_2008, year_2009, year_2010, year_2011, year_2012, year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019]
    temp_min = []
    for check_data in value[1:]:
        if check_data != "n.a." and check_data != "" and check_data != "-" and str(check_data).find("SGD") == -1 and check_data != "n.m." and str(check_data).find("Net Cash") == -1:
            temp_min.append(int(check_data))
    
    if len(temp_min) > 1:
        get_min = sum(temp_min)/len(temp_min)
    else:
        get_min = 0
    
    final_value = []
    for check_data in value: 
        if check_data == "n.a.":
            check_data = get_min
        if check_data == "":
            break
        final_value.append(str(check_data))
        print(final_value)
    if len(final_value) > 1:
        cursor.execute(query, final_value)
    

cursor.close()
database.commit()
database.close()

print("Successfully Added into DB")




