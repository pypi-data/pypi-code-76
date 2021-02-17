def Correct(CorrectInput=None):

    # Inputs:
    #     CorrectInput:
    #         Can be a fragment object containing information of the fragment whose MID is being corrected for natural isotopic abundances
    #         Can be a string representing a path to a text file contining the information to make a fragment object
    #         Can be None, in which case the user is prompted to select a text file containing the above information using a GUI

    #     Defined within the fragment object:
    #         LabeledElement: A character that is the chemical symbol of the atom which is assumed to be labeled in the fragment whose MID is being corrected for natural isotopic abundances
    #         TracerEnrichment: The percent of the molecule assumed to be the tracer that is actually the tracer (e.g. 50% of glucose is [U-13C6]glucose)
    #         LabelEnrichment: The percent of the atom that is assumed to be labeled that is actually labeled (e.g. 99% of the atoms said to be 13C in [U-13C6]glucose are actually 13C)
    #         HighRes: A  list of strings indicating which elements have heavy isotopes whose mass differences are resolved from the mass differences due to heavy isotopes of the tracer element
    #             can also be 'all' or 'none'
    #             i.e. whether M1, M2, M3 are aggregate measurements of heavy isotopes of all atoms (low resolution, indicated by HighRes='none') or just the atom that is labeled and those not indicated in HighRes
    #             Note: Correcting high resolution data is achieved by setting all atom MIDs, for the elements indicated in HighRes, in the atom objects to [1 0 0] except that of the LabeledElement
    #                 This is accomplished in the definition of an Atom object where atom MIDs for high resolution data are taken from a separate file
    #             Note: this is now entered as a list separated by spaces in the input text file


    # Outputs:
    #     fragment: A fragment object where the corrected MID is stored as a numpy array in fragment.MIDc

    import numpy as np
    import pandas as pd
    import pdb
    from PolyMID import Fragment
    from PolyMID import InputClass
    from PolyMID import Tracer
    from pdb import set_trace

    #Initialize the Inputs variable as an Input object
    InputObject = InputClass(CorrectInput)

    print('\nCalculating the corrected MID...')

    #Create a Fragment object
    #    If a fragment object was passed to this function, this will be equivalent
    fragment = InputObject.fragment

    #Create a correction matrix and calculate its inverse
    fragment.create_correction_matrix()

    #Calculate the corrected MID
    fragment.calc_corrected_mid()

    #Print the corrected MID
    print('The corrected MID is as follows:\n')
    MIDc = pd.DataFrame(fragment.MIDc)
    MIDc = MIDc.transpose()
    nColumns = MIDc.shape[1]
    MIDcColumns = np.array([])
    ColumnNumbersList = list(range(nColumns))
    for i in ColumnNumbersList:
        MIDc = MIDc.rename(columns={i:'M'+ str(i)})
    MIDc.index=[fragment.name]
    pd.set_option("display.precision", 3) #set to print 8 decimals by default
    print(MIDc)
    print('\n\n')

    return(fragment)
