import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import matplotlib.patches as mplp

def MembershipGrid(regions, status, carbon_price, bca):
    #Plots the grid for one simulation
    cmap = colors.ListedColormap(['grey', 'green'])
    bounds = [0,1,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(len(status[0]), len(status)))
    ax.imshow(status, cmap=cmap, norm=norm)

    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, len(status[0]), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(status), 1), minor=True)
    ax.set_yticks(np.arange(len(regions)))
    ax.set_yticklabels(regions)
    ax.set_xticklabels(np.arange(2024, 2025+len(status[0]), 1))
    ax.set_xlabel('Year')
    ax.set_ylabel('Region')
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.text(-0.7, 0.999, f"Carbon price = {str(carbon_price)} \nBCA = {str(bca)}", transform=ax.transAxes, fontsize=12, verticalalignment='top', fontweight = 'bold')
    
    # Add legend
    handles = [mplp.Patch(color='grey', label='Non-member'), mplp.Patch(color='green', label='Member')]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
    
    return plt.show()

def MultipleMembershipGrid (regions, statuses, carbon_price, bca):
    #Plots the grid for several simulations at once for one initial region with changing carbon prices and bcas
    flatstatus = []
    years = []
    for i in range(len(statuses[0])):
        combined_subsublist = []
        for sublist in statuses:
            combined_subsublist.append(sublist[i])
        combined_subsublist = [element for sublist in combined_subsublist for element in sublist]    
        flatstatus.append(combined_subsublist)
    for sublist in statuses:
        #print(sublist[0])
        year = 2024
        for i in range(len(sublist[0])): 
            years.append(year)
            year += 1


    fig, ax = plt.subplots(figsize=(len(flatstatus[0]), len(flatstatus)))
    #Adding a black line and a legend for the different simulations in place
    previous_year = 2025
    n = 0
    color_cycle = ['#006400', 'blue', 'purple']
    start_index = 0
    for i in range(len(years)):
       #print(f"Previous year: {previous_year}, Current year: {years[i]}") # Debug print
       if years[i] < previous_year:
           #print("New simulation detected!") # Debug print
           m_bca = n%3
           color_bca = color_cycle[m_bca]
           #m_cp = n // 3%3
           
           cp_value = carbon_price[n]
           bca_value = bca[n]
           label_text_cp = f"CP{cp_value}"
           label_text_bca = f"BCA{bca_value}"
           midpoint_x = (2*start_index + len(statuses[n][0])) / 2 - 0.5
           # CP text
           ax.text(midpoint_x, len(regions) - 0, label_text_cp, fontsize=26, color=color_bca, ha='center', va='bottom') 
           # BCA text
           ax.text(midpoint_x, len(regions) - 0.5, label_text_bca, fontsize=26, color=color_bca, ha='center', va='bottom')
           if i != 0:
               ax.axvline(x=i -0.5, color='black', linewidth=8)
           
           #Colors in the grid
           cmap = colors.ListedColormap(['lightgrey', color_bca])
           bounds = [0,1,2]
           norm = colors.BoundaryNorm(bounds, cmap.N)
           ax.imshow(statuses[n], cmap=cmap, norm=norm, extent=[start_index -0.5, start_index + len(statuses[n][0])-0.5, -0.5, len(regions)-0.5]) #origin = 'lower')
           #print("Probando:", len(regions))
           start_index += len(statuses[n][0])
           n += 1
       previous_year = years[i]
    mapping = {
    2024: 1, 
    2025: 2, 
    2026: 3, 
    2027: 4, 
    2028: 5, 
    2029: 6, 
    2030: 7,
    2031: 8,
    2032: 9,
    2033: 10,
    2034: 11,
    2035: 12,
    2036: 13,
    2037: 14,
    2038: 15,
    2039: 16,
    2040: 17,
    2041: 18,
    2042: 19,
    2043: 20}
    
    newyears = [mapping.get(x, x) for x in years]
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, len(flatstatus[0]), 1), minor=True)
    ax.set_xticks(np.arange(len(years)))
    ax.set_yticks(np.arange(-.5, len(flatstatus), 1), minor=True)
    ax.set_yticks(np.arange(len(regions)))
    ax.set_yticklabels(regions[::-1])
    ax.set_xticklabels(newyears)
    ax.set_xlabel('Round', fontsize = 26)
    ax.set_ylabel('Region', fontsize = 26)
    ax.tick_params(axis='y', which='major', labelsize=26)
    ax.tick_params(axis='x', which='major', labelsize=26)

    
    #ax.text(-0.7, 0.999, f"Carbon price = {str(carbon_price)} \nBCA = {str(bca)}", transform=ax.transAxes, fontsize=12, verticalalignment='top', fontweight = 'bold')
    
   
    # Add legend
    #handles = [mplp.Patch(color='lightgrey', label='Non-member'), mplp.Patch(color='green', label='Member')]
    #plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
    
    return plt.show()

def MultipleMembershipGridWTO (regions, statuses, carbon_price, init_region):
    #Plots the grid for several simulations at once for several initial regions, carbon prices and bcas
    flatstatus = []
    years = []
    for i in range(len(statuses[0])):
        combined_subsublist = []
        for sublist in statuses:
            combined_subsublist.append(sublist[i])
        combined_subsublist = [element for sublist in combined_subsublist for element in sublist]    
        flatstatus.append(combined_subsublist)
    for sublist in statuses:
        #print(sublist[0])
        year = 2024
        for i in range(len(sublist[0])): 
            years.append(year)
            year += 1


    fig, ax = plt.subplots(figsize=(len(flatstatus[0]), len(flatstatus)))
    #Adding a black line and a legend for the different simulations in place
    previous_year = 2025
    n = 0
    m = 0
    t = 0
    # color_cycle = ['deepskyblue','dodgerblue', 'blue']
    #color_cycle = ['dodgerblue','#183EFA', 'blue']
    color_cycle = ['dodgerblue','blue', 'mediumblue']
    start_index = 0
    for i in range(len(years)):
       #print(f"Previous year: {previous_year}, Current year: {years[i]}") # Debug print
       if years[i] < previous_year:           
           #print("New simulation detected!") # Debug print
           #m_cp = n // 3%3

           # Label text
           cp_value = carbon_price[m]
           m_cp = n%3
           color_cp = color_cycle[m_cp]
           midpoint_x = (2*start_index + len(statuses[n][0])) / 2 - 0.5
           label_text_cp = f"CP{cp_value}"
           label_text_bca = f"BCA{cp_value}"
           midpoint_x = (2*start_index + len(statuses[n][0])) / 2 - 0.5
           # CP text
           ax.text(midpoint_x, len(regions) - 0, label_text_cp, fontsize=26, color=color_cp, ha='center', va='bottom') 
           # BCA text
           ax.text(midpoint_x, len(regions) - 0.5, label_text_bca, fontsize=26, color=color_cp, ha='center', va='bottom')
           m += 1
    
           m_cycle = n%3
           if m_cycle == 1: 
               print(t)
               initial_region = init_region[t]
               print(initial_region)
               label_text = f"Initial region: {initial_region}"
               midpoint_x = (2*start_index + len(statuses[n][0])) / 2 - 0.5
               ax.text(midpoint_x, len(regions) + 0.7, label_text, fontsize=32, ha='center', va='bottom', color = 'blue')
               t += 1
    
           if i != 0:
               ax.axvline(x=i -0.5, color='black', linewidth=8)
        
           #Colors in the grid
           cmap = colors.ListedColormap(['lightgrey', color_cp])
           bounds = [0,1,2]
           norm = colors.BoundaryNorm(bounds, cmap.N)
           ax.imshow(statuses[n], cmap=cmap, norm=norm, extent=[start_index -0.5, start_index + len(statuses[n][0])-0.5, -0.5, len(regions)-0.5]) #origin = 'lower')
           #print("Probando:", len(regions))
           start_index += len(statuses[n][0])
           
           if cp_value == 400 and n < (len(statuses) - 1):
               #ax.imshow(np.ones_like(statuses[n]) * -1, cmap=cmap, norm=norm, extent=[start_index - 0.5, start_index + 0.5, -0.5, len(regions) - 0.5], alpha=0)  # alpha=0 makes it transparent
               ax.axvspan(start_index - 0.5, start_index + 0.5, facecolor='white', edgecolor='white', alpha=1)
               ax.axvline(start_index, color='white', linewidth=50, ymin = -5, ymax = len(regions) +5)
              # ax.axvline(x=start_index + 0.5, color='black', linewidth=8)
               start_index += 1
               years.insert(i + len(statuses[n][0]), 0)
               
               
           
           n += 1
       previous_year = years[i]
    mapping = {
    0: None, 
    2024: 1, 
    2025: 2, 
    2026: 3, 
    2027: 4, 
    2028: 5, 
    2029: 6, 
    2030: 7,
    2031: 8,
    2032: 9,
    2033: 10,
    2034: 11,
    2035: 12,
    2036: 13,
    2037: 14,
    2038: 15,
    2039: 16,
    2040: 17,
    2041: 18,
    2042: 19,
    2043: 20}
    
    newyears = [mapping.get(x, x) for x in years]
    ax.set_xticks(np.arange(-.5, len(flatstatus[0]) + 1, 1), minor=True)
    ax.set_xticks(np.arange(len(years)))
    ax.set_yticks(np.arange(-.5, len(flatstatus), 1), minor=True)
    ax.set_yticks(np.arange(len(regions)))
    ax.set_yticklabels(regions[::-1])
    ax.set_xticklabels(newyears)
    ax.set_xlabel('Round', fontsize = 26)
    ax.set_ylabel('Region', fontsize = 26)
    ax.tick_params(axis='y', which='major', labelsize=26)
    ax.tick_params(axis='x', which='major', labelsize=26)
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
    
    #ax.text(-0.7, 0.999, f"Carbon price = {str(carbon_price)} \nBCA = {str(bca)}", transform=ax.transAxes, fontsize=12, verticalalignment='top', fontweight = 'bold')
    
   
    # Add legend
    #handles = [mplp.Patch(color='lightgrey', label='Non-member'), mplp.Patch(color='green', label='Member')]
    #plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
    
    return plt.show()



def MembershipGraph (regions, status, carbon_price, bca):
    #Plots a graph with the simulation outcomes for each region
    y_positions = [2 * i for i in range(len(regions))]
    y_position_labels = [y + 0.5 for y in y_positions]
    
    fig, ax = plt.subplots(figsize=(6, 20))
    ax.set_xlabel('Year')
    ax.set_ylabel('Membership Status')
    ax.set_yticks(y_position_labels)
    ax.set_yticklabels(regions)
    ax.set_ylim([-2, 2 * len(regions)])  # adjust axis limits to provide some buffer

    # set xticks
    xticks = range(len(status[0]))
    xtick_labels = [str(2025 + i) for i in range(len(status[0]))]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)

    # plot each region with the specified vertical offset
    for i, r in enumerate(regions):
        y_pos = y_positions[i]
        s = status[i]
        ax.plot(range(len(s)), [y_pos + val for val in s], label=r)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks([y_pos, y_pos+1])
        ax2.set_yticklabels(['Non-Member', 'Member'], fontsize=7)
        ax.text(-0.4, 0.995, f"Carbon price = {str(carbon_price)} \nBCA = {str(bca)}", transform=ax.transAxes, fontsize=11, verticalalignment='top')

    return plt.show()