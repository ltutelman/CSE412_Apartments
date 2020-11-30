import psycopg2
import pandas as pd
from config import config

# Gives the user a list of choices, and returns the chosen integer
def mainOptions():
    userChoice = input("Please select one of the following options: \n1. Search by number of bedrooms \n2. Search by amenities \n3. Search by cost \n4. Search by rating \n5. Exit Application\n\n")
    return userChoice

def newSearch():
    userChoice = input("\nWould you like to start a new search or exit? Please type either 'continue' or 'exit'\n")
    returnNewChoice = ""
    if userChoice == "continue":
        returnNewChoice = mainOptions()
    elif userChoice == "exit":
        returnNewChoice = "5"
    else:
        print("Please enter a valid response. ")
        newSearch()
    return returnNewChoice

def byBedrooms():
    print("By bedrooms!")


def byAmenities():
    print("By amenities!")
    
def byCost():
    print("By cost!")

def byRating():
    print("By ratings!")

# DRIVER CODE

print("\n*********** Welcome to the Tempe Apartment Assist Tool ***********")
menuChoice = mainOptions()

while(menuChoice != "5" and menuChoice != "exit"):
    # valid input
    if(menuChoice == "1"):
        byBedrooms()
        menuChoice = newSearch()
    elif(menuChoice == "2"):
        byAmenities()
        menuChoice = newSearch()
    elif (menuChoice == "3"):
        byCost()
        menuChoice = newSearch()
    elif(menuChoice == "4"):
        byRating()
        menuChoice = newSearch()

    else:
        menuChoice = input("Sorry, that is not a valid input.  Please try again\n")

print("Thank you for using the Tempe Apartment Assist Tool!")

