# CSE412_Apartments
Command Line Tempe Apartment Finding Application

# Options

So, I wasnt sure how we wanted the user to interact with the command line so there are two files. (Apartments.py) The first uses raw SQL queries since we have a lot of them written already.  (Apartments_df.py) The second one transforms each table into pandas dataframes first and then uses those to make all the queries.  Personally, I think the second one works way better. 

## Apartments.py

First, you can see how to do a really simple query in showAll on line 38.  

A more complicated query is in customQuery on line 50.

Basically, the user can either choose a structured filter option or they can do a quick query by apartment, bedroom count, and cost (option 4)

See Sample input in Apartments.png


## Apartments_df.py

Much better approach.  Uses dataframes in pandas.  

See Sample input in Apartments_df.png




# Notes

There are bugs in the logic but I'm not going to fix them rn since I'm not sure if you guys even want the menu option or if you just want a user to input of list of what they care about. 

Hypothetically, another way this could work is a user could just input keywords and we have working dictionaries. For instance, if a user inputs [Nexa, 1300, Park Place, 4, 1, Sauna]  we would look up each value so wed look up nexa in all our dictionaries and find its an apartment and so on.  So we'd have
Apartments: Nexa, Park Place
Room Count: 4, 1
Cost: 1300
Amenities: Sauna

And then have code that knows how to make the query out of that.  That could also just replace the customQuery function that I currently have if we wanted to add that, it would just take a bit of work