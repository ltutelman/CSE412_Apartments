import psycopg2
import pandas as pd
from config import config

# Starts connection to database and new cursor

params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


def create_pandas_table(sql_query, database=conn):
    table = pd.read_sql_query(sql_query, database)
    return table


def main_options():
    user_choice = input("""Please make an initial choice:
    0. Show all apartment complexes in database
    1. Structured Query
    2. Custom Query
    3. Exit Application\n""")

    return user_choice


def new_search():
    user_choice = input("\nWould you like to start a new search or exit? Please type either 'continue' or 'exit'\n")
    return_new_choice = ""
    if user_choice == "continue":
        return_new_choice = main_options()
    elif user_choice == "exit":
        return_new_choice = "exit"
    else:
        print("Please enter a valid response. ")
        new_search()
    return return_new_choice


# Creates data frames

apartment = create_pandas_table('SELECT * FROM public."Apartment"')
amenities = create_pandas_table('SELECT * FROM public."Amenities"')
apartment_type = create_pandas_table('SELECT * FROM public."Apartment_Type"')
rating = create_pandas_table('SELECT * FROM public."Rating"')
room = create_pandas_table('SELECT * FROM public."Room"')
room_cost = create_pandas_table('SELECT * FROM public."Room_Cost"')
room_plan = create_pandas_table('SELECT * FROM public."Room_Plan"')
social_media = create_pandas_table('SELECT * FROM public."Social_Media"')
staff = create_pandas_table('SELECT * FROM public."Staff"')


def show_all():
    print(apartment)
    apartment_choice = input("Would you like to know more about any of these apartments? Please list the name of one below or type 'exit'")
    if apartment_choice != "exit":
        #rating: apartment_name, social_media: apartment_name, staff: apartment_name
        getApartment = apartment[apartment.apartment_name == apartment_choice].merge(social_media).merge(rating).merge(staff)
        print(getApartment)


def structured_query():
    apt_list = input("Please enter the apartments you would like to query, delimited with spaces\n").title().split(', ')
    # halfQuery = apartment.apartment_name.isin(aList)
    # print(apartment[halfQuery])
    filter_by_apartment = apartment[apartment.apartment_name.isin(apt_list)]
    print(filter_by_apartment)

    bed_list = input("Please enter the number of bedrooms that you would like to query, delimited with spaces\n").split(', ')
    filter_by_bed_count = room_plan[room_plan.bedrooms.isin(bed_list)]
    filter_by_count_apartment = filter_by_bed_count[filter_by_bed_count.apartment_name.isin(apt_list)]
    print(filter_by_count_apartment)

    # Select statement for all rooms, bedroom counts, costs, and amenities, associated with the apartments entered
    # apartmentQuery = create_pandas_table('SELECT STATEMENT')

    minPrice = int(input("\nPlease enter the minimum price you would like to pay\n"))

    maxPrice = int(input("\nPlease enter the maximum price you would like to pay\n"))

    merge_bed_count_and_price = filter_by_count_apartment.merge(room_cost)
    filter_by_price = merge_bed_count_and_price[merge_bed_count_and_price.total_mandatory_cost.ge(minPrice)]
    filter_by_price = filter_by_price[filter_by_price.total_mandatory_cost.le(maxPrice)]

    if filter_by_price.empty:
        print("\nThere are no apartments available with these filters.")
    else:
        print(filter_by_price)


def custom_query():
    input_string = input("""\nYou can enter filters for apartment name (aName), number of bedrooms (bedCount), and maximum cost (maxCost).
    Enter your filters as a list in the previous order and all fields must be accurate and complete or the query will fail.
    For instance:  Nexa 3 1200 will return all apartments in Nexa that are under 1,200\n""")
    input_list = input_string.split()
    query_result = create_pandas_table('SELECT public."Apartment".apartment_name, bedrooms_cost, public."Room".floor_plan, bedrooms FROM public."Apartment", public."Apartment_Type", public."Room", public."Room_Plan", public."Room_Cost" WHERE public."Apartment".apartment_name = public."Apartment_Type".apartment_name AND public."Apartment".apartment_name = public."Room".apartment_name AND public."Apartment".apartment_name = public."Room_Plan".apartment_name AND public."Apartment".apartment_name = public."Room_Cost".apartment_name AND public."Room".floor_plan = public."Room_Cost".floor_plan AND public."Apartment".apartment_name = ' + "'" + inputList[0] + "'" + ' AND public."Room_Plan".bedrooms = ' + inputList[1] + ' AND bedrooms_cost < ' + inputList[2] + ';')
    print(query_result)


print("\n*********** Welcome to the Tempe Apartment Assist Tool ***********")

menu_choice = main_options()


while menu_choice != "3" and menu_choice != "exit":
    # valid input
    if menu_choice == "0":
        show_all()
        menu_choice = new_search()
    elif menu_choice == "1":
        structured_query()
        menu_choice = new_search()
    elif menu_choice == "2":
        custom_query()
        menu_choice = new_search()
    else:
        menu_choice = input("Sorry, that is not a valid input. Please try again\n")

cur.close()
conn.close()

print("Thank you for using the Tempe Apartment Assist Tool!")
