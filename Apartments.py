import psycopg2
import pandas as pd
from config import config

# Starts connection to database and new cursor

params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

# ************************ HELPER FUNCTIONS ************************


# Gives the user a list of choices, and returns the chosen integer
def mainOptions():
    userChoice = input("Please make an initial choice, the option to filter further beyond each option will be offered after the initial selection: \n0. Show all apartment complexes in database \n1. Search by number of bedrooms \n2. Search by amenities \n3. Search by cost \n4. Custom Query \n5. Exit Application\n\n")
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

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

# ************************ MAIN FUNCTIONS ************************


def showAll(conn, cur):
    apartmentInfo = create_pandas_table('SELECT * FROM public."Apartment"')
    print(apartmentInfo)
def byBedrooms():
    print("By bedrooms!")

def byAmenities():
    print("By amenities!")
    
def byCost():
    print("By cost!")

def customQuery():
    inputString = input("\nYou can enter filters for apartment name (aName), number of bedrooms (bedCount), and maximum cost (maxCost). \nEnter your filters as a list in the previous order and all fields must be accurate and complete or the query will fail.  \nFor instance:  Nexa 3 1200 will return all apartments in Nexa that are under 1,200\n" )
    inputList = inputString.split()
    queryResult = create_pandas_table('SELECT public."Apartment".apartment_name, bedrooms_cost, public."Room".floor_plan, bedrooms FROM public."Apartment", public."Apartment_Type", public."Room", public."Room_Plan", public."Room_Cost" WHERE public."Apartment".apartment_name = public."Apartment_Type".apartment_name AND public."Apartment".apartment_name = public."Room".apartment_name AND public."Apartment".apartment_name = public."Room_Plan".apartment_name AND public."Apartment".apartment_name = public."Room_Cost".apartment_name AND public."Room".floor_plan = public."Room_Cost".floor_plan AND public."Apartment".apartment_name = ' + "'" + inputList[0] + "'" +' AND public."Room_Plan".bedrooms = '+ inputList[1] + ' AND bedrooms_cost < ' + inputList[2] + ';')
    print(queryResult)
    



# ************************ DRIVER CODE ************************

# Intro message and user makes initial choice

print("\n*********** Welcome to the Tempe Apartment Assist Tool ***********")
menuChoice = mainOptions()



# Allows user to make multiple queries 

while(menuChoice != "5" and menuChoice != "exit"):
    # valid input
    if(menuChoice == "0"):
        showAll(conn, cur)
        menuChoice = newSearch()
    elif(menuChoice == "1"):
        byAmenities()
        menuChoice = newSearch()
    elif(menuChoice == "2"):
        byAmenities()
        menuChoice = newSearch()
    elif (menuChoice == "3"):
        byCost()
        menuChoice = newSearch()
    elif(menuChoice == "4"):
        customQuery()
        menuChoice = newSearch()
    else:
        menuChoice = input("Sorry, that is not a valid input.  Please try again\n")

cur.close()
conn.close()
print("Thank you for using the Tempe Apartment Assist Tool!")

