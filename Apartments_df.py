import psycopg2
import pandas as pd
from config import config

# Starts connection to database and new cursor

params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

def mainOptions():
    userChoice = input("Please make an initial choice: \n0. Show all apartment complexes in database \n1. Structured Query \n2. Custom Query \n3. Exit Application\n\n")
    return userChoice
    
def newSearch():
    userChoice = input("\nWould you like to start a new search or exit? Please type either 'continue' or 'exit'\n")
    returnNewChoice = ""
    if userChoice == "continue":
        returnNewChoice = mainOptions()
    elif userChoice == "exit":
        returnNewChoice = "exit"
    else:
        print("Please enter a valid response. ")
        newSearch()
    return returnNewChoice



# Creates data frames

apartment = create_pandas_table('SELECT * FROM public."Apartment"')
amenities = create_pandas_table('SELECT * FROM public."Amenities"')
apartmentType = create_pandas_table('SELECT * FROM public."Apartment_Type"')
rating = create_pandas_table('SELECT * FROM public."Rating"')
room  = create_pandas_table('SELECT * FROM public."Room"')
roomCost = create_pandas_table('SELECT * FROM public."Room_Cost"')
roomPlan = create_pandas_table('SELECT * FROM public."Room_Plan"')
socialMedia = create_pandas_table('SELECT * FROM public."Social_Media"')
staff = create_pandas_table('SELECT * FROM public."Staff"')


def showAll():
    print(apartment)

def structuredQuery():
    aList = input("Please enter the apartments you would like to query, delimited with spaces\n").split(', ')
    #halfQuery = apartment.apartment_name.isin(aList)
    #print(apartment[halfQuery])
    filter_by_apartment = apartment[apartment.apartment_name.isin(aList)]
    print(filter_by_apartment)

    bedList = input("Please enter the number of bedrooms that you would like to query, delimited with spaces\n").split(', ')
    filter_by_bed_count = roomPlan[roomPlan.bedrooms.isin(bedList)]
    filter_by_count_apartment = filter_by_bed_count[filter_by_bed_count.apartment_name.isin(aList)]
    print(filter_by_count_apartment)

    ### Select statement for all rooms, bedroom counts, costs, and amenities, associated with the apartments entered
    #apartmentQuery = create_pandas_table('SELECT STATEMENT')  

def customQuery():
    inputString = input("\nYou can enter filters for apartment name (aName), number of bedrooms (bedCount), and maximum cost (maxCost). \nEnter your filters as a list in the previous order and all fields must be accurate and complete or the query will fail.  \nFor instance:  Nexa 3 1200 will return all apartments in Nexa that are under 1,200\n" )
    inputList = inputString.split()
    queryResult = create_pandas_table('SELECT public."Apartment".apartment_name, bedrooms_cost, public."Room".floor_plan, bedrooms FROM public."Apartment", public."Apartment_Type", public."Room", public."Room_Plan", public."Room_Cost" WHERE public."Apartment".apartment_name = public."Apartment_Type".apartment_name AND public."Apartment".apartment_name = public."Room".apartment_name AND public."Apartment".apartment_name = public."Room_Plan".apartment_name AND public."Apartment".apartment_name = public."Room_Cost".apartment_name AND public."Room".floor_plan = public."Room_Cost".floor_plan AND public."Apartment".apartment_name = ' + "'" + inputList[0] + "'" +' AND public."Room_Plan".bedrooms = '+ inputList[1] + ' AND bedrooms_cost < ' + inputList[2] + ';')
    print(queryResult)

print("\n*********** Welcome to the Tempe Apartment Assist Tool ***********")
menuChoice = mainOptions()



while(menuChoice != "3" and menuChoice != "exit"):
    # valid input
    if(menuChoice == "0"):
        showAll()
        menuChoice = newSearch()
    elif(menuChoice == "1"):
        structuredQuery()
        menuChoice = newSearch()
    elif(menuChoice == "2"):
        byAmenities()
        menuChoice = newSearch()
    else:
        menuChoice = input("Sorry, that is not a valid input.  Please try again\n")

cur.close()
conn.close()

print("Thank you for using the Tempe Apartment Assist Tool!")

