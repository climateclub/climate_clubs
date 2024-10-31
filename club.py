class Club:
    def __init__(self, init_coalition, tariff, carbon_price):  #init_coalition list of regions that are part of the initial coalition, tariff is a number representing the bca applied to non-members.
        #carbon_price is the carbon price and can be an integer or a function. If it is an integer, it is used directly as the carbon price. If it is a function, it is not yet implemented in the code and an exception will be thrown.        # Initializes climate club
        self.members = init_coalition
        self.tariff = tariff

        if isinstance(carbon_price, (int, float)):
            self.cp = carbon_price
        elif callable(carbon_price):
            raise Exception("Functions not implemented yet.")
        else:
            raise Exception("Invalid initialisation.")

    def __str__(self):
        # Returns basic information of region for print command
        members = [] #list
        for member in self.members:
            members.append(member.name)

        return f"""Club Info

                   Members: {members},
                   Carbon price: {self.cp},
                   Tariff height: {self.tariff}"""

def create_club(regions, init_coalition, tariff, carbon_price):
#create_club is a function within the 'Club' class that is used to create an instance of the 'Club' class and a list of regions that are part of the coalition.
#'region' represents all possible regions that can be part of the coalition.
#if 'init_coalition' is a list of indices, the function creates an instance (an object) of the 'Club' class using the regions corresponding to the indices and the other arguments provided.
#if 'init_coalition' is a number, the function does not yet implement it and throws an exception
#if 'init_coalition' is neither a list nor a number, an exception is also raised.
    if isinstance(init_coalition, list):
        try:
            club = Club([regions[i] for i in init_coalition], tariff, carbon_price)
        except:
            raise Exception("Invalid starting coalition, should be list if indices [0 - 31].")
    elif isinstance(init_coalition, int):
        raise Exception("Random not implemented yet.")
    else:
        raise Exception("Invalid initialisation.")

    non_members = list(set(regions).difference(club.members)) 
    #List of regions that are not part of the coalition, by calculating the difference between the full list of regions and the list of coalition members (with set.difference)

    return club, non_members
