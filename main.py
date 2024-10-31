import region as re
import club as cc
import json
import numpy as np



def run(init_coalition, carbon_price, tariff, method, rounds = 20, mu = 1, distribution = 0.5): 
    #Main function of the model, takes as input the initial coalition of club members, a carbon price, a BCA, the method for BCA revenue distribution and a myopia rate (mu, set by default at 1).
    #Possible methods for BCA revenue distribution: equal, export, abatement, WTO
    # If the chosen method is "abatement," the distribution variable can be explicitly defined (set by default at 0.5) to indicate how benefits are distributed among members and non-members.
    #A higher distribution value leads to more benefits for non-members and less for members.
  
    #Creating regions and the club, calling the club and region classes
    regions = re.create_regions()
    club, non_members = cc.create_club(regions, init_coalition, tariff, carbon_price)
    regionsname = [region.name for region in regions]
    regionsemissions = [region.e for region in regions]
    regionscp = [region.cp for region in regions]
    status = [[] for _ in range(len(regionsname))]
    implicitcp = {m: cp for m, cp in zip(regionsname, regionscp)}
    previous_abatement = {}
    original_nm = {}; original_m = {}
    i = 0
    previous_revenue_ab = 0
    
    #Importing the data on Marginal Abatement Costs (MAC)
    MAC2025 = {}; iMAC2025 = {}
    MAC2030 = {}; iMAC2030 = {}
    MAC2040 = {}; iMAC2040 = {}
    MAC2050 = {}; iMAC2050 = {}
    for region in regions:
        MAC2025[region.name], MAC2030[region.name], MAC2040[region.name], MAC2050[region.name] = get_MAC(region)
        iMAC2025[region.name], iMAC2030[region.name], iMAC2040[region.name], iMAC2050[region.name] = get_inverseMAC(region)

    #initiating the rounds and defining/reinitiating variables
    while i<rounds:       
        year = i + 2025       
        club_trade_size = calc_size(club.members,non_members)
        di = distribution*club_trade_size    
        cm_size = len(club.members) 
        min_cp = min([region.cp for region in regions])
        join_dictm = {}
        join_dictnm = {}
        
        #Launching the appropriate MAC curves for the year in place
        if year < 2030:    
            MACeq = MAC2025
            iMACeq = iMAC2025
        elif year < 2040:
            MACeq = MAC2030
            iMACeq = iMAC2030
        elif year < 2050:
            MACeq = MAC2040
            iMACeq = iMAC2040
        else:
            MACeq = MAC2050
            iMACeq = iMAC2050
            
        #Calculating the exports to the rest of the world and the exports to the club    
        exp_club = {}
        exp_ROW = {}
        for region in regions:
            exp_club[region.name] = exports_club(region,club.members)
            exp_ROW[region.name] = exports_ROW(region, non_members)

        #Calculating the cost of staying out and the abatement costs for joinigng the club for non-members
        total_revenue = 0
        abatement_cost = {}
        cost_staying_nm = {}
        total_abatement_nm = sum(previous_abatement[nm.name] for nm in original_nm)
        for nm in non_members:   
            cost_staying_nm[nm.name] = nm.cost_staying(club.tariff, club.cp, exp_club[nm.name], cm_size, min_cp, method)       
            total_revenue += cost_staying_nm[nm.name]
            if method == "abatement":                
                if nm.cp >= club.cp:                    
                    abatement_cost[nm.name] = 0
                else:    
                    if nm.name in previous_abatement:                        
                        if nm in original_nm:
                            if total_abatement_nm == 0:
                                abatement_cost[nm.name] = 0
                            else:
                                share = previous_abatement[nm.name]/total_abatement_nm
                                abatement_cost[nm.name] = previous_abatement[nm.name] - previous_revenue_ab*share 
                        else:    
                            abatement_cost[nm.name] = previous_abatement[nm.name]
                    else:
                        abatement_cost[nm.name] = nm.cost_abatement(club.cp, MACeq[nm.name], iMACeq[nm.name])
                if abatement_cost[nm.name] < 0:
                    abatement_cost[nm.name] = 0
            else:    
                abatement_cost[nm.name] = nm.cost_abatement(club.cp, MACeq[nm.name], iMACeq[nm.name])
                
        for m in club.members:
            if method == "abatement":                
                if m.cp >= club.cp:                    
                    abatement_cost[m.name] = 0
                else:    
                    if m.name in previous_abatement:
                        if m in original_nm:
                            if total_abatement_nm == 0:
                                abatement_cost[m.name] = 0
                            else:
                                share = previous_abatement[m.name]/total_abatement_nm
                                abatement_cost[m.name] = previous_abatement[m.name] - previous_revenue_ab*share
                        else:    
                            abatement_cost[m.name] = previous_abatement[m.name]
                    else:
                        abatement_cost[m.name] = m.cost_abatement(club.cp, MACeq[m.name], iMACeq[m.name])
                if abatement_cost[m.name] < 0:
                    abatement_cost[m.name] = 0
            else:    
                abatement_cost[m.name] = m.cost_abatement(club.cp, MACeq[m.name], iMACeq[m.name]) 
        
        previous_abatement = abatement_cost.copy()               
        previous_revenue_ab = sum(cost_staying_nm.values())*di
        
        #saving the members and non-members of the club in each round
        original_nm = [region for region in non_members]
        original_m = [region for region in club.members]
        
        #cost-benefit analysis for memebrs of the club using the cost_analysis_m function
        for m in original_m:
            print("Name:", m.name)            
            print("Carbon price:", m.cp, "US-$/tCO2")
            potentialm = [ms for ms in original_m if ms != m]
            #potential_cp_original = calc_original_cp(originalcp, potentialm)
            cost = cost_analysis_m(m, exp_club[m.name], exp_ROW[m.name], cost_staying_nm, abatement_cost,
                                   implicitcp[m.name], club_trade_size, cm_size, method, club, original_nm, original_m, mu, di, min_cp)
            join_dictm[m.name] = cost
            status[regionsname.index(m.name)].append(1)
            #if costs are higher than the benefits region m leaves the club:
            if join_dictm[m.name]>0: #and i>0:
               non_members.append(m)
               club.members = [region for region in club.members if region != m]
               print("LEAVING THE CLUB")
            else: 
                m.cp = club.cp
            print("")
        
        #cost-benefit analysis for non-members of the club
        print("Non Members:")
        for nm in original_nm:
            print("Name:", nm.name)
            print("Carbon price:", nm.cp, "US-$/tCO2")
            potentialnm = [nms for nms in original_nm if nms != nm]
            potentialm = original_m.copy()
            potentialm.append(nm)
            pt_club_trade_size = calc_size(potentialm,potentialnm)
            #pt_cp_original = calc_original_cp(originalcp, potentialm)  
            pt_di = distribution*pt_club_trade_size       
            print(nm.name, ":", pt_di)
            cost = cost_analysis(nm, exp_ROW[nm.name], cost_staying_nm, abatement_cost, implicitcp[nm.name],
                                 pt_club_trade_size, potentialm, cm_size, method, club, original_nm, mu, pt_di)
            join_dictnm[nm.name] = cost
            status[regionsname.index(nm.name)].append(0)
            #if benefits are higher than the costs region nm joins the club:
            if join_dictnm[nm.name]<=0:
                club.members.append(nm)
                non_members = [region for region in non_members if region != nm]
                print("ENTERING THE CLUB")
            print("")
        
        #Saving the membership status of regions this round
        istatus=[sublist[i] for sublist in status]
        iprevstatus=[sublist[i-1] for sublist in status]
        #stopping the code if stability is reached (full club, empty club or no changes in two consecutive rounds)
        if all(s == 0 for s in istatus) or all(s == 1 for s in istatus):
            break        
        if i>1 and istatus == iprevstatus:
            status = [sublist[:-1] for sublist in status]
            break            
        i += 1

    
    return regionsname, regionsemissions, status


def cost_analysis(region, exp_ROW, cost_staying_nm, abatement_cost_nm, implicitcp, pt_club_trade_size, potentialm, cm_size, method, club, original_nm, mu, di):
    #Cost-benefit analysis for non-members of the club
    abatement_cost = abatement_cost_nm[region.name]
    cost_staying = cost_staying_nm[region.name]    
    loss_competitiveness = region.cost_competitiveness_nm(club.cp, pt_club_trade_size, exp_ROW, original_nm, implicitcp)
    cost_joining =  abatement_cost + loss_competitiveness 
    benefit_joining = calc_benefit_joining(region, potentialm, method, cm_size, original_nm, cost_staying_nm, di)
    
    print(f"""    
    Cost of staying out: {cost_staying}
    Abatement cost: {abatement_cost}
    Loss of competitiveness = {loss_competitiveness}
    Cost of joining:     {cost_joining}
    Benefit of joining:  {benefit_joining}
    Net cost of joining: {cost_joining - (mu * benefit_joining)}
    Net cost of staying out: {(mu * cost_staying)}
    Net joining - staying out: {int(cost_joining - (mu * benefit_joining) - (mu * cost_staying))} """) 


    return int(cost_joining - (mu * benefit_joining) - (mu * cost_staying))

def cost_analysis_m(region, exp_club, exp_ROW, cost_staying_nm, abatement_cost, implicitcp, club_trade_size, cm_size, method, club, original_nm, original_m, mu, di, min_cp):
#Cost-benefit analysis for members of the club
    cost_leaving = region.cost_leaving(club.tariff, club.cp, exp_club, cm_size, min_cp, method) #needs to be changed and adapted for club members
    abatement_cost = abatement_cost[region.name]
    loss_competitiveness = region.cost_competitiveness(club.cp, club_trade_size, exp_ROW, original_nm, implicitcp)
    cost_staying_in =  abatement_cost + loss_competitiveness     
    benefit_staying_in = calc_benefit_staying_in(region, original_m, method, cm_size, original_nm, cost_staying_nm, di) 

    print(f"""
    Cost of leaving: {cost_leaving}
    Abatement cost: {abatement_cost}
    Loss of competitiveness: {loss_competitiveness}
    Cost of staying in:     {cost_staying_in}
    Benefit of staying in:  {benefit_staying_in}
    Net cost of staying in: {cost_staying_in - (mu * benefit_staying_in)}
    Net cost of leaving: {(mu * cost_leaving)}
    Net staying in - leaving: {int(cost_staying_in - (mu * benefit_staying_in) - (mu * cost_leaving))} """) 


    return int(cost_staying_in - (mu * benefit_staying_in) - (mu * cost_leaving))


def get_MAC(region): #x):
    #Open the file with the MACC coefficients
    f = open('mac.json') 
    MACs = json.load(f)
    c1 = MACs['2025'][region.name] #MACC 2025
    c2 = MACs['2030'][region.name] #MACC 2030
    c3 = MACs['2040'][region.name] #MACC 2040
    c4 = MACs['2050'][region.name] #MACC 2050

    return np.poly1d(c1),np.poly1d(c2),np.poly1d(c3),np.poly1d(c4) #(x) #poly1d crea un polinomio con los valores que se le asignan

def get_inverseMAC(region): #x):
    #Open the file with the coefficients for the inverse MACC)
    f = open('invertedmac.json') 
    MACs = json.load(f)
    c1 = MACs['2025'][region.name] #MACC 2025
    c2 = MACs['2030'][region.name] #MACC 2030
    c3 = MACs['2040'][region.name] #MACC 2040
    c4 = MACs['2050'][region.name] #MACC 2050

    return np.poly1d(c1),np.poly1d(c2),np.poly1d(c3),np.poly1d(c4) #(x) #poly1d crea un polinomio con los valores que se le asignan


def exports_club(region,club_members):
    #calculates the percentage of a region's trade that is within the club
    exports = sum(region.trade_partners[m.name] for m in club_members)

    return exports 


def exports_ROW(region,non_members): 
    #calculates the percentage of a region's trade that is outside the club
    exports = sum(region.trade_partners[nm.name] for nm in non_members)

    return exports

def calc_size(members,non_members):
    # Calculates the relative size of the club compared to non-members, in terms of trade.
    total_row = 0
    for region in members: #club trade with the rest of the world
        total_row += sum(region.trade_partners[reg.name] for reg in non_members)

    for region in non_members: #rest of the world trade with the rest of the world
        total_row += sum(region.trade_partners[reg.name] for reg in non_members) 
        #añade al segundo total_row el valor del primero con +=

    total_club = 0
    for region in members: #club trade with the club
        total_club += sum(region.trade_partners[reg.name] for reg in members)

    for region in non_members: #rest of the world trade with the club
        total_club += sum(region.trade_partners[reg.name] for reg in members)

    return total_row / (total_row + total_club)

def calc_original_cp(originalcp,clubmembers): # Based on GDP
    #GDP-weighted average of the original (implicit) carbon price of all members.
    cps, gdps= [], []
    for m in clubmembers:
      #  if m.gdp is None:
      #      m.gdp = 0
        cps.append(originalcp[m.name])
        gdps.append(m.gdp)
       
    tot_gdp, avg_gdp = sum(gdps), 0
    for i, cp in enumerate(cps):
        avg_gdp += cp * (gdps[i] / tot_gdp)

    return avg_gdp

def calc_benefit_joining(region, potentialm, method, cm_size, non_members, cost_staying_nm, di): 
    #Benefits of joining the club
    revenue = 0
    #equal revenue distribution method
    if method == "equal":
        for nm in non_members:
            if nm != region: 
                revenue += cost_staying_nm[nm.name]
        return revenue / (cm_size + 1)
    #export or WTO renenue distribution methods
    elif method == "export" or method == "WTO":    
        for nm in non_members:
            if nm != region:
                share = nm.trade_partners[region.name]/(sum(nm.trade_partners[m.name] for m in potentialm))
                revenue += share*cost_staying_nm[nm.name]  
        return revenue
    #returning part of the revenue to non-members for abatement costs method
    elif method == "abatement":
        for nm in non_members:
            if nm != region:
                share = nm.trade_partners[region.name]/(sum(nm.trade_partners[m.name] for m in potentialm))
                revenue += share*cost_staying_nm[nm.name]   
        return revenue*(1-di) 
    else:
        raise Exception("No other methods implemented.")
        

def calc_benefit_staying_in(region, club_members, method, cm_size, non_members, cost_staying_nm, di): #I am doing the same as in calc_benefit_joining but dividing among members
    #Benefits of being in the club
    revenue = 0
    #equal revenue distribution method
    if method == "equal":
      revenue = sum(cost_staying_nm[nm.name] for nm in non_members)
      return revenue / (cm_size)
    
    #export or WTO renenue distribution methods
    elif method == "export" or method == "WTO": 
      for nm in non_members:
              share = nm.trade_partners[region.name]/sum(nm.trade_partners[m.name] for m in club_members) 
              revenue += share*cost_staying_nm[nm.name] 
      return revenue 
  
    #returning part of the revenue to non-members for abatement costs method
    elif method == "abatement":
      for nm in non_members:
              share = nm.trade_partners[region.name]/sum(nm.trade_partners[m.name] for m in club_members) 
              revenue += share*cost_staying_nm[nm.name]   
      return revenue*(1-di)         
        
    
    else:
        raise Exception("No other methods implemented.")

