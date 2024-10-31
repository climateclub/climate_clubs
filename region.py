import json
from scipy.integrate import quad
import numpy as np

class Region:
    def __init__(self, name, emissions, carbon_price, gdp, export_change):
        # Initiates region with data
        # Class constructor, used to initialise the attributes of an instance of the class: 'name', 'emissions', 'carbon_price', 'gdp', 'export change'.
        # Assign_trade_partner: method used to assign the trade partners of the region (function defined below)
        self.name = name
        self.e = emissions
        self.cp = carbon_price
        self.gdp = gdp
        self.dexp = export_change/100
        self.assign_trade_partners()

    def __str__(self):
        # Returns basic information of region for print command
        return f"""Region Info

                   Name: {self.name}, Carbon price: {self.cp},
                   Export: {int(self.exp)} USD,
                   Lambda: {self.cp} USD"""

    def assign_trade_partners(self):
        #loads 'matrix.json' (trade of each of the regions with the other regions)
        f = open('matrix.json') 
        matrix = json.load(f)
        self.trade_partners = matrix[self.name]
        self.exp = sum(matrix[self.name].values()) #total exports for each region
        #print(self.name, self.exp)


    def cost_abatement(self, club_cp, MACeq, iMACeq):
        #function to calculate the abatement costs for joining the club
        if self.cp >= club_cp:           
        #If the carbon price in the region is higher than the carbon price in the club, the cost is zero.
            cost = 0
        else:           
            current_emissions = iMACeq(self.cp)
            target_emissions = iMACeq(club_cp)
            cost = quad(MACeq, current_emissions, target_emissions)[0] * 10**6 #integrating the MAC curb between the two abatement levels

        return cost*1.1433 #correcting for inflation from 2015 to 2021 (14.33%)

    def cost_competitiveness(self, cp_club, club_trade_size, exp_ROW, non_members, implicitcp):
         #function for the cost of loss of competitiveness for a region in the club
         if all(nm.cp >= cp_club for nm in non_members) or self.cp >= cp_club:
             cost = 0
         else:
             cost = -((cp_club)/ implicitcp) * self.dexp * exp_ROW * club_trade_size #introducing a negative sign to get positive costs
         #print(cp_club, self.cp, self.dexp, self.exp, ROW_share, club_size)
         return  round(cost, 0) 

    def cost_competitiveness_nm(self, cp_club, club_trade_size, exp_ROW, non_members, implicitcp):
         #function to calculate the cost of loss of competitiveness for a potential member if joining the club
         if all(nm.cp >= cp_club for nm in non_members if nm != self) or self.cp >= cp_club:
             cost = 0
         else:
             cost = -((cp_club)/ implicitcp) * self.dexp * exp_ROW * club_trade_size #introducing a negative sign to get positive costs
         #print(cp_club, self.cp, self.dexp, self.exp, ROW_share, club_size)
         return round(cost, 0) 


 
    def cost_staying(self, tariff, cp_club, exp_club, cm_size, min_cp, method): 
    #function to calculate the cost of staying outside the club
        if cp_club <= self.cp:
            cost = 0
        elif cm_size < 1:
            cost = 0
        else:
            if method == "WTO":
                tau = tariff/cp_club
                cost = -tau * ((cp_club)/(self.cp)) * self.dexp * exp_club 
            else:
                tau = ((cp_club - self.cp)/(cp_club - min_cp)) * tariff/cp_club
                cost = -tau * ((cp_club)/(self.cp)) * self.dexp * exp_club 
            #units: $US 2021 (from the self.exp data!)
 
        return cost
    
    def cost_leaving(self, tariff, cp_club, exp_club, cm_size, min_cp, method): 
    #function to calculate the cost of leaving the club
        if cp_club <= self.cp:
            cost = 0
        elif cm_size < 2:
            cost = 0
        else:
            if method == "WTO":
                tau = tariff/cp_club
                cost = -tau * ((cp_club)/(self.cp)) * self.dexp * exp_club 
            else:
                tau = ((cp_club - self.cp)/(cp_club - min_cp)) * tariff/cp_club
                cost = -tau * ((cp_club)/(self.cp)) * self.dexp * exp_club 
        return cost
    


def create_regions(type="normalized"):
    #Creates a list of region objects, built from the data provided by the JSON file, with the option of setting the type to be original, normalized or corrected.
    #This is where the data for each region is added to the Region class
    f = open('newdata.json')
    data = json.load(f)
    regions = []

    for region in data['GDP']:
        #print(f"Name: {region}")
        if type == "original":
            #in this case, the region objects are built with the original values from the JSON file.
            regions.append(Region(region['name'], region['e'], region['tax'],
                       region['gdp'], region['dexp']))
        elif type == "normalized":
            #in this case, the normalised values from the JSON file are used.
            regions.append(Region(region, data['Emission share'][region], data['lambda_nor'][region],
                       data['GDP'][region], data['dX'][region]))
        elif type == "corrected":
            #in this case, the corrected values from the JSON file are used.
            regions.append(Region(region['name'], region['e'], region['tax_cor'],
                       region['gdp'], region['dexp']))
        else:
            raise Exception("Invalid carbon tax type.")

    return regions
