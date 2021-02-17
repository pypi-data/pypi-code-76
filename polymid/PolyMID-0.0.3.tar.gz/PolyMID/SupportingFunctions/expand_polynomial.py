def expand_polynomial(a,b):

# Inputs:
#     a: a python array representing the mass isotopomer abundances of atom a
#        the first entry is the abundance of M0, the second M1, the third M2, ...
#     b: a python array representing the mass isotopomer abundances of atom b
#        the first entry is the abundance of M0, the second M1, the third M2, ...
# Outputs:
#     a Pandas data frame is returned where the rows correspond to mass isotopomers and the column contains the mass isotopomer abundances as 'prob'
#         This retunred mass isotopomer distribution (MID) is for the molecule comprised of the atoms ab
#         Note this can be used in series to get a multi-atom molecule MID
#             Say you have the molecule abc
#             First run this function with the MIDs for the atoms a and b as inputs; the output is then the MID for the combined ab
#             Run the function again with the inputs being the previous output and the MID for c; the output is then the MID for abc

    import numpy as np
    import pandas
    import importlib #allows fresh importing of modules
    from pdb import set_trace

    # Redefine the input polynomial python arrays as numpy row matrices
    mid_a = np.matrix(a) #mass isotopomer distribution for a
    mid_b = np.matrix(b) #mass isotopomer distribution for b

    #find the number of recorded relative mass isotopomer abundances for each atom (the number of columns)
    n_a = mid_a.shape[1] #the second entry of the returned tuple
    n_b = mid_b.shape[1] #the second entry of the returned tuple


    # Create Pandas data frames to hold the mass isotopoer relative abundance and the number of extra neutrons associated with that mass isotopomer in separate columns
    #     The columns are 'prob' and 'm_isotopomer' respectively

    # Arrange information for atom a into a pandas data frame
    mid_a_m = np.zeros([n_a,2]) #initialize the matrix the size of data frame that will be used to hold the information for atom a
    mid_a_df = pandas.DataFrame(mid_a_m,columns=['prob','m_isotopomer']) #initialize the data frame containing the information for atom a
    mid_a_df[['prob']] = np.transpose(mid_a) #enter the relative abundances of each mass isotopomer
    mid_a_df[['m_isotopomer']] = np.transpose(np.matrix(range(0,n_a))) #enter the mz mass isotopomer values corresponding to each mass isotopomer

    # Arrange information for atom b into a pandas DataFrame
    mid_b_m = np.zeros([n_b,2])
    mid_b_df = pandas.DataFrame(mid_b_m,columns=['prob','m_isotopomer'])
    mid_b_df[['prob']] = np.transpose(mid_b)
    mid_b_df[['m_isotopomer']] = np.transpose(np.matrix(range(0,n_b)))

    # Initialize a DataFrame to contain information on all possible combinations of atoms a and b in the molecule ab
    factored_init_m = np.zeros([n_a*n_b,2])
    factored = pandas.DataFrame(factored_init_m,columns=['prob','m_isotopomer'])

    # Fill in the factored_df by expanding the polynomial and keeping track of the mass isotopomer mz value (M0,M1,M2,...) for each term
    #     This is expanding the polynomial and storing each term
    #     The mass isotopomer mz values of each factor are summed for each term to get a new mass isotopomer mz value for each term

    # Initialize the variable to track the row of the factored data frame
    #     This iterates through every possible combination of entries in mid_a_df and mid_b_df
    iterator = 0
    for i in range(0,n_a):
        for k in range(0,n_b):
            # calculate the probalility of a combiniation of mass isotopomers from atom a and b
            factored.loc[iterator,'prob'] = mid_a_df.loc[i,'prob']*mid_b_df.loc[k,'prob']
            # determine the value of the mass isotomer of that combination (i.e. M0, M1, or M2, etc.)
            factored.loc[iterator,'m_isotopomer'] = mid_a_df.loc[i,'m_isotopomer'] + mid_b_df.loc[k,'m_isotopomer']
            iterator = iterator + 1

    # Combine the relative mass isotopmer abundances for ab combinations with the same mass isotopomer mz value
    grouped = factored.groupby('m_isotopomer')
    #     the groupby method of a Pandas data frame returns a group object
    #         a grouped object has the aggregate method that takes a function as an input and returns a Pandas data frame
    factored_aggregated = grouped.aggregate(np.sum)

    # Shorten factored to remove negligible values
    #     Removes all values starting from the end of the MID that are less than the specified cut-off
    cut_off = 1e-4
    factored_aggregated_array = np.array(factored_aggregated)
    factored_aggregated_array[factored_aggregated_array < cut_off] = 0
    factored_aggregated_trimmed = np.trim_zeros(factored_aggregated_array,'b')
    n_factors = len(factored_aggregated_trimmed)
    factored_aggregated = factored_aggregated.iloc[0:n_factors]

    # Return the Pandas data frame containing the mass isotopomer distrubution of the molecule ab
    return(factored_aggregated)
