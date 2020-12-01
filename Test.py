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
min_payment = 0
max_payment = 1400

while user_input != "exit":
    user_input = input(user_prompt)

    if user_input.lower() == "1" or "apartment complex":
        apt_list = input(apt_prompt).capitalize().split(', ')
        filters["apartments"] = apt_list
        # filter_by_apartment = apartment[apartment.apartment_name.isin(apt_list)]
        # print(filter_by_apartment)

    elif user_input.lower() == "2" or "number of bedrooms":
        num_bedrooms = input(bedroom_prompt)
        if num_bedrooms == "0" or "1" or "2" or "3" or "4":
            filters["bedrooms"] = num_bedrooms
        else:
            num_bedrooms = input(error_prompt)

    elif user_input.lower() == "3" or "minimum payment":
        min_payment = input(min_prompt)
        if 0 <= min_payment <= 1400:
            filters["min"] = min_payment
        else:
            min_payment = input(error_prompt)

    elif user_input.lower() == "4" or "maximum payment":
        max_payment = input(max_prompt)
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
        if max_payment < min_payment:
            min_payment = input("Your desired minimum payment exceeds your desired maximum payment. Please enter new minimum payment: ")
            max_payment = input("Please enter new maximum payment: ")

    else:
        user_input = input(error_prompt)
