# CSE412_Apartments
Command Line Tempe Apartment Finding Application

# Options

So, I wasnt sure how we wanted the user to interact with the command line so I did a couple of things. Theres a menu option that sort of works and also a custom query that works in a super basic but easy to break way.  Idk how much we care to change stuff

## Here are the ways I queried things

First, you can see how to do a really simple query in showAll on line 38.  

A more complicated query is in customQuery on line 50.

Basically, the user can either choose a structured filter option or they can do a quick query by apartment, bedroom count, and cost (option 4)

# Notes

There are bugs in the logic but I'm not going to fix them rn since I'm not sure if you guys even want the menu option or if you just want a user to input of list of what they care about. 

Hypothetically, another way this could work is a user could just input keywords and we have working dictionaries. For instance, if a user inputs [Nexa, 1300, Park Place, 4, 1, Sauna]  we would look up each value so wed look up nexa in all our dictionaries and find its an apartment and so on.  So we'd have
Apartments: Nexa, Park Place
Room Count: 4, 1
Cost: 1300
Amenities: Sauna

And then have code that knows how to make the query out of that.  That could also just replace the customQuery function that I currently have if we wanted to add that, it would just take a bit of work