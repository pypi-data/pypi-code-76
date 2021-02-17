def Natural(formula,LabeledElement='C',HighRes=False):
    # Inputs:
    # formula: a string representing the formula whose natural MID is being calculated
    # LabeledElement: A character that is the chemical symbol of the atom which is assumed to be labeled in the fragment whose MID is being corrected for natural isotopic abundances
    # HighRes: A booleon indicating whether the data is high resoloution or not
    #     i.e. whether M1, M2, M3 are aggregate measurements of heavy isotopes of all atoms (not HighRes) or just the atom that is labeled (HighRes)
    #     This input is only used if the fragment information is read from a text file
    #         Otherwise HighRes is already an attribute of the fragment input
    #     Note: Correcting high resolution data is achieved by setting all atom MIDs in the atom objects to [1 0 0] except that of the LabeledElement
    #         This is accomplished in the definition of an Atom object where atom MIDs for high resolution data are taken from a separate file

    # Outputs:
    # formula.NaturalMID: the MID corresponding to the chemical formula resulting from natural heavy isotope abundances

    #Import necessary packages and object classes
    from PolyMID import Formula
    from pdb import set_trace

    #Create a formula object
    formula = Formula(formula=formula,LabeledElement=LabeledElement,HighRes=HighRes)
    #     The Formula object designation takes LabeledElement and HighRes inputs
    #         If HighRes is False, LabeledElement does not matter (which is default behaviour)
    #         High resolution natural MIDs can be calculated by specifying HighRes and LabeledElement, where LabeledElement is the atom contributing heavy isotopes

    #Determine the NaturalMID attribute of the formula object using the calc_natural_mid() method
    formula.calc_natural_mid()

    #Return the natural MID
    return(formula.NaturalMID)
