import re
import psycopg2
import pandas as pd
from config import config

def create_pandas_table(sql_query, database=conn):
    table = pd.read_sql_query(sql_query, database)
    return table

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



filters = {
    "apartments",
    "bedrooms",
    "min",
    "max",
    "type",
    "gym",
    "pool",
    "study",
    "parking",
    "dog",
    "sauna"
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
error_prompt = "Sorry, that is not a valid input. Please try again: "



user_input = ""
filters["apartments"] = ["Park Place", "Vertex", "Rise", "Oliv", "Apollo", "Nine20", "Boulevard 1900", "District", "Union", "Sol", "Nexa"]

while user_input != "exit":
    user_input = input(user_prompt)

    if user_input.lower() == "1" or "apartment complex":
        apt_list = input(apt_prompt).title().split(', ')
        filters["apartments"] = apt_list

    elif user_input.lower() == "2" or "number of bedrooms":
        num_bedrooms = input(bedroom_prompt).split(', ')
        if re.match("^[0-4 ]+$", num_bedrooms):
            filters["bedrooms"] = num_bedrooms
        else:
            num_bedrooms = input(error_prompt)

    elif user_input.lower() == "3" or "minimum payment":
        min_payment = int(input(min_prompt))
        if 0 <= min_payment <= 1400:
            filters["min"] = min_payment
        else:
            min_payment = input(error_prompt)

    elif user_input.lower() == "4" or "maximum payment":
        max_payment = int(input(max_prompt))
        if 0 <= max_payment <= 1400:
            filters["max"] = max_payment
        else:
            max_payment = input(error_prompt)

    elif user_input.lower() == "5" or "luxury or budget":
        apt_type = input(type_prompt)
        if apt_type.lower() == "luxury" or "budget":
            filters["type"] = apt_type
        else:
            apt_type = input(error_prompt)

    elif user_input.lower() == "6" or "gym":
        apt_gym = input(gym_prompt)
        if apt_gym.lower() == "yes" or "no":
            filters["gym"] = apt_gym
        else:
            apt_gym = input(error_prompt)

    elif user_input.lower() == "7" or "pool":
        apt_pool = input(pool_prompt)
        if apt_pool.lower() == "yes" or "no":
            filters["pool"] = apt_pool
        else:
            apt_pool = input(error_prompt)

    elif user_input.lower() == "8" or "study room":
        apt_study = input(study_prompt)
        if apt_study.lower() == "yes" or "no":
            filters["study"] = apt_study
        else:
            apt_study = input(error_prompt)

    elif user_input.lower() == "9" or "parking":
        apt_parking = input(parking_prompt)
        if apt_parking.lower() == "yes" or "no":
            filters["parking"] = apt_parking
        else:
            apt_parking = input(error_prompt)

    elif user_input.lower() == "10" or "dog park":
        apt_dog = input(dog_prompt)
        if apt_dog.lower() == "yes" or "no":
            filters["dog"] = apt_dog
        else:
            apt_dog = input(error_prompt)

    elif user_input.lower() == "11" or "sauna":
        apt_sauna = input(sauna_prompt)
        if apt_sauna.lower() == "yes" or "no":
            filters["sauna"] = apt_sauna
        else:
            apt_sauna = input(error_prompt)

    elif user_input.lower() == "continue":
        merged_db = apartment.merge(amenities).merge(apartment_type).merge(rating).merge(room).merge(room_cost).merge(room_plan).merge(social_media).merge(staff)

        if filters["apartment"]:
            merged_db = merged_db[merged_db.apartment_name.isin(filters.get("apartment"))]

        if filters["bedrooms"]:
            merged_db = merged_db[merged_db.bedrooms.isin(filters.get("apartment"))]

        if filters["min"]:
            merged_db = merged_db[merged_db.total_mandatory_cost.ge(int(filters.get("min")))]

        if filters["max"]:
            merged_db = merged_db[merged_db.total_mandatory_cost.le(int(filters.get("max")))]

        if filters["type"]:
            merged_db = merged_db[merged_db.budget_luxury.isin(filters.get("type"))]

        if filters["gym"]:
            merged_db = merged_db[merged_db.gym.isin(filters.get("gym"))]

        if filters["pool"]:
            merged_db = merged_db[merged_db.pool.isin(filters.get("pool"))]

        if filters["study"]:
            merged_db = merged_db[merged_db.study_rooms.isin(filters.get("study"))]

        if filters["parking"]:
            merged_db = merged_db[merged_db.parking.isin(filters.get("parking"))]

        if filters["dog"]:
            merged_db = merged_db[merged_db.dog_park.isin(filters.get("dog"))]

        if filters["sauna"]:
            merged_db = merged_db[merged_db.sauna.isin(filters.get("sauna"))]

        if merged_db.empty:
            print("\nThere are no apartments available with these filters.")

        else:
            print(merged_db)

    else:
        user_input = input(error_prompt)
