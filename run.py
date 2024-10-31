import main
import sys
import plotclub


#This is the file that runs the code for a given carbon price, bca (tariff), initial coalition (regions listed below), method, and maximum number of rounds. 
#Optional inputs: myopia rate (mu; default value mu = 1) and, if returning part of the revenue to non-members, bca revenue distribution (distribution; default value distribution = 0.5)

carbon_price= 50
tariff = 25
filename = f'cp{carbon_price},bca{tariff},CHE,wto.txt'

with open(filename, 'w') as f:
    sys.stdout = f
    regionsname, status = main.run([30], carbon_price, tariff, rounds=12, method = "WTO") #, distribution=0.5)
    sys.stdout = sys.__stdout__


plotclub.MembershipGrid(regionsname,status, carbon_price, tariff) 


"""Regions name:
    0: China
    1: United States
    2: Rest of Europe
    3: India
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


