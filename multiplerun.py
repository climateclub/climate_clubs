import sys
import main
import plotclub

#This is the file that runs the code to plot several simulations (9; corresponding to an initial member with 3 carbon prices and 3 bcas for each carbon price) on the same grid
carbon_prices = [100, 200, 400]
tariffs_relative = [0.5, 1, 1.5]
statuses = []
carbon_prices_used = []
tariffs_used = []
initial_regs = [[30], [2], [1,2]]
initial_regs_name = ['CHE', 'EU+', 'US & EU+']

#Changing variables
method = 'equal'
#distribution = 1
initial_reg = [1,2]

#for initial_reg in initial_regs:
filename2 = f'{initial_reg}_{method}.txt'
with open(filename2, 'a') as f2:    
    for carbon_price in carbon_prices:    
         for tariff_relative in tariffs_relative:
            tariff = int(carbon_price * tariff_relative)
            filename = f'cp{carbon_price},bca{tariff},{initial_reg},{method}.txt'
            
            with open(filename, 'w') as f:
                sys.stdout = f
                regionsname, regionsemissions, status = main.run(initial_reg, carbon_price, tariff, method, distribution = 0.5)
                sys.stdout = sys.__stdout__
                
            co2_emissions = sum(regionsemissions[i] for i, sublist in enumerate(status) if sublist[-1] == 1)  
            f2.write(f"Carbon Price: {carbon_price}, Tariff: {tariff}\n")
            f2.write(f"Rounds to convergence: {len(status[0])}\n")
            f2.write(f"Final club size: {sum(1 for sublist in status if sublist[-1] == 1)}\n")
            f2.write(f"% CO2 emissions within final club: {co2_emissions}\n")
            f2.write("\n")
            
            # Save status and corresponding carbon price and tariff
            statuses.append(status)
            carbon_prices_used.append(carbon_price)
            tariffs_used.append(tariff)

"""Regions name:                  Methods:
    0: China                     "equal"
    1: United States             "export"
    2: EU+                       "abatement" (with possibility of setting the distribution of revenue)
    3: India                     "WTO"
    4: Russia
    5: Middle East
    6: Japan
    7: Rest of South-East Asia
    8: South Korea
    9: Saudi Arabia
    10: North Africa
    11: Rest of CIS
    12: Indonesia
    13: Canada
    14: Rest of America
    15: Brazil
    16: Pacific
    17: South Africa
    18: Mexico
    19: Turkey
    20: Rest of Africa
    21: Rest of South Asia
    22: Vietnam
    23: United Kingdom
    24: Malaysia
    25: Thailand
    26: Ukraine
    27: Argentina
    28: Chile
    29: Norway
    30: Switzerland    
    """
 
regsname = ["CHN", "USA", "EU+", "IND", "RUS", "ME", "JPN", 
             "XSE", "KOR", "SAU", "NAF", "CIS", 
             "IDN", "CAN", "XAM", "BRA", "PAC", "SAF", 
             "MEX", "TUR", "XAF", "XSA", "VNM", 
             "UK", "MYS", "THA", "UKR", "ARG", "CHL", 
             "NOR", "CHE"]
"""
statusesEUexp = [[[0, 0, 0], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 1]], [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1]], [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 0, 0], [0, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1]]]
statusesUKexp = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1]], [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1]]]
statusesEUUSexp = [[[0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 1, 0]], [[0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 0, 1, 1], [0, 1, 1, 1, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1]], [[0, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1]], [[0, 0, 0], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 0], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 0], [0, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]]]
carbon_prices_used = [50, 50, 50, 200, 200, 200, 400, 400, 400]
tariffs_used = [25, 50, 75, 100, 200, 300, 200, 400, 600] 
statuses = [[[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]], [[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1]], [[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 0, 1], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1]], [[0, 1, 1], [0, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]], [[0, 0, 1], [1, 1, 1], [1, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]]]
carbon_prices_used = [50, 200, 400, 50, 200, 400, 50, 200, 400]
initial_reg_name = ['CHE', 'EU+', 'US and EU+']
"""
plotclub.MultipleMembershipGrid(regsname, statuses, carbon_prices_used, tariffs_used)
#plotclub.MultipleMembershipGridWTO(regsname, statuses, carbon_prices_used, initial_reg_name)