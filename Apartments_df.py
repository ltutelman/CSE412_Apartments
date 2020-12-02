import psycopg2
import pandas as pd
from config import config

filters = {
    "apartments": None,
    "bedrooms": None,
    "min": None,
    "max": None,
    "type": None,
    "gym": None,
    "pool": None,
    "study": None,
    "parking": None,
    "dog": None,
    "sauna": None
}

user_prompt = """These are the following options you can select from to make your search:
    1. Apartment Complex
    2. Number of Bedrooms
    3. Minimum Payment
    4. Maxmimum Payment
    5. Luxury or Budget
    6. Gym
    7. Pool
    8. Study Room
    9. Parking
    10. Dog Park
    11. Sauna

Type the number for a filter to add a custom filter to your search, 'continue' to see results, or 'exit' to exit the search.

Please enter choice: """

apt_prompt = """These are the apartment choices:
    Park Place
    Vertex
    Rise
    Oliv
    Apollo
    Nine20
    Boulevard 1900
    District
    Union
    Sol
    Nexa

Please enter the apartments you would like to search, delimited with commas: """

bedroom_prompt = """Please enter the number of bedrooms (0-4) you would like to search, delimited with commas.
For example, if you would like to search studio and 1 bedroom apartments, enter '0, 1'.
Choice: """
min_prompt = "Please enter the minimum you would like to pay ($0-1400): "
max_prompt = "Please enter the maximum you would like to pay ($0-1400): "
type_prompt = "Please enter either luxury or budget: "
gym_prompt = "Would you like a gym? Please enter 'yes' or 'no': "
pool_prompt = "Would you like a pool? Please enter 'yes' or 'no': "
study_prompt = "Would you like a study room? Please enter 'yes' or 'no': "
parking_prompt = "Would you like parking? Please enter 'yes' or 'no': "
dog_prompt = "Would you like a dog park? Please enter 'yes' or 'no': "
sauna_prompt = "Would you like a sauna? Please enter 'yes' or 'no': "
error_prompt = "Sorry, that is not a valid input."

filters["apartments"] = ["Park Place", "Vertex", "Rise", "Oliv", "Apollo", "Nine20", "Boulevard 1900", "District", "Union", "Sol", "Nexa"]

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
    apartment_choice = input("\nWould you like to know more about any of these apartments? Please list the name of one below or type 'exit'\n")
    if apartment_choice != "exit":
        # rating: apartment_name, social_media: apartment_name, staff: apartment_name
        getApartment = apartment[apartment.apartment_name == apartment_choice.title()].merge(social_media).merge(rating).merge(staff)
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
    user_input = ""
    while user_input != "exit":
        user_input = input(user_prompt)

        if user_input == "1":
            apt_list = input(apt_prompt).title().split(', ')
            filters["apartments"] = apt_list

        elif user_input == "2":
            num_bedrooms = input(bedroom_prompt).split(', ')
            filters["bedrooms"] = num_bedrooms

        elif user_input == "3":
            min_payment = int(input(min_prompt))
            if type(min_payment) == int:
                filters["min"] = min_payment
            else:
                print(error_prompt)

        elif user_input == "4":
            max_payment = int(input(max_prompt))
            if type(max_payment) == int:
                filters["max"] = max_payment
            else:
                print(error_prompt)

        elif user_input == "5":
            apt_type = input(type_prompt)
            if apt_type.lower() == "luxury" or "budget":
                filters["type"] = apt_type
            else:
                print(error_prompt)

        elif user_input == "6":
            apt_gym = input(gym_prompt)
            if apt_gym.lower() == "yes" or "no":
                filters["gym"] = apt_gym
            else:
                print(error_prompt)

        elif user_input == "7":
            apt_pool = input(pool_prompt)
            if apt_pool.lower() == "yes" or "no":
                filters["pool"] = apt_pool
            else:
                print(error_prompt)

        elif user_input == "8":
            apt_study = input(study_prompt)
            if apt_study.lower() == "yes" or "no":
                filters["study"] = apt_study
            else:
                print(error_prompt)

        elif user_input == "9":
            apt_parking = input(parking_prompt)
            if apt_parking.lower() == "yes" or "no":
                filters["parking"] = apt_parking
            else:
                print(error_prompt)

        elif user_input == "10":
            apt_dog = input(dog_prompt)
            if apt_dog.lower() == "yes" or "no":
                filters["dog"] = apt_dog
            else:
                print(error_prompt)

        elif user_input == "11":
            apt_sauna = input(sauna_prompt)
            if apt_sauna.lower() == "yes" or "no":
                filters["sauna"] = apt_sauna
            else:
                print(error_prompt)

        elif user_input == "continue":
            merged_db = apartment.merge(amenities).merge(apartment_type).merge(rating).merge(room).merge(room_cost).merge(room_plan).merge(social_media).merge(staff)

            if filters["apartments"]:
                merged_db = merged_db[merged_db.apartment_name.isin(filters.get("apartments"))]

            if filters["bedrooms"]:
                merged_db = merged_db[merged_db.bedrooms.isin(filters.get("apartments"))]

            if filters["min"]:
                merged_db = merged_db[merged_db.total_mandatory_cost.ge(int(filters.get("min")))]

            if filters["max"]:
                merged_db = merged_db[merged_db.total_mandatory_cost.le(int(filters.get("max")))]

            if filters["type"]:
                # merged_db = merged_db[merged_db.budget_luxury.isin(filters.get("type"))]
                merged_db = merged_db[merged_db["budget_luxury"] == filters.get("type")]

            if filters["gym"]:
                # merged_db = merged_db[merged_db.gym.isin(filters.get("gym"))]
                merged_db = merged_db[merged_db["gym"] == filters.get("gym")]

            if filters["pool"]:
                # merged_db = merged_db[merged_db.pool.isin(filters.get("pool"))]
                merged_db = merged_db[merged_db["pool"] == filters.get("pool")]

            if filters["study"]:
                # merged_db = merged_db[merged_db.study_rooms.isin(filters.get("study"))]
                merged_db = merged_db[merged_db["study"] == filters.get("study")]

            if filters["parking"]:
                # merged_db = merged_db[merged_db.parking.isin(filters.get("parking"))]
                merged_db = merged_db[merged_db["parking"] == filters.get("parking")]

            if filters["dog"]:
                # merged_db = merged_db[merged_db.dog_park.isin(filters.get("dog"))]
                merged_db = merged_db[merged_db["dog"] == filters.get("dog")]

            if filters["sauna"]:
                # merged_db = merged_db[merged_db.sauna.isin(filters.get("sauna"))]
                merged_db = merged_db[merged_db["sauna"] == filters.get("sauna")]

            if merged_db.empty:
                print("\nThere are no apartments available with these filters.\n")

            else:
                print(merged_db)

        elif user_input == "exit":
            break

        else:
            user_input = input(error_prompt)


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
