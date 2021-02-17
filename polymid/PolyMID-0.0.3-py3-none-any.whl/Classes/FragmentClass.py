class Fragment:

    # Initializer and Instance Attributes
    def __init__(self,FragmentName,FragmentFormula,CanAcquireLabel,MIDm,LabeledElement,TracerEnrichment,LabelEnrichment,HighRes,MIDc=None,PeakArea=None,CM=None):

        from PolyMID import Formula
        from PolyMID import Tracer
        import numpy as np
        from pdb import set_trace

        # MIDm and HighRes may be passed as python lists
        #     They must be converted to numpy arrays
        MIDm = np.array(MIDm)
        HighRes = np.array(HighRes)

        self.name = FragmentName
        self.MIDm = MIDm
        self.MIDc = MIDc
        self.CM = CM
        self.CMi = None
        self.PeakArea = PeakArea
        self.Tracer = Tracer(LabeledElement,TracerEnrichment,LabelEnrichment)
        self.HighRes = HighRes # A numpy array indicating which elements have heavy isotopes whose mass differences are resolved from the mass differences due to heavy isotopes of the tracer element
        self.Formula = Formula(formula=FragmentFormula,Tracer=self.Tracer,HighRes=self.HighRes)
        self.CanAcquireLabel = Formula(formula=CanAcquireLabel,Tracer=self.Tracer,HighRes=self.HighRes)

    # instance method to assign new values to a Fragment object
    def assign(self,attribute,NewValue):
        if attribute == 'name':
            self.name = NewValue
        if attribute == 'formula':
            self.formula = NewValue
        if attribute == 'CanAcquireLabel':
            self.CanAcquireLabel = NewValue
        if attribute == 'MIDm':
            self.MIDm = NewValue
        if attribute == 'MIDc':
            self.MIDc = NewValue
        if attribute == 'CM':
            self.CM = NewValue
        if attribute == 'CMi':
            self.CMi = NewValue
        if attribute == 'PeakArea':
            self.PeakArea = NewValue

    # instance method to create correction matrix for a Fragment object
    def create_correction_matrix(self):

        from pdb import set_trace
        import numpy as np
        import re
        import copy
        from PolyMID import quantity_of_atom
        from PolyMID import Formula

        #break the formula up so atoms and quantities are consecutive entries in a numpy array
        broken_formula = np.array(re.findall('[A-Z][a-z]?|[0-9]+', self.Formula.formula))
        #    '[A-Z][a-z]?|[0-9]+': A capital letter [A-Z], followed by a lowercase letter [a-z], which is optional '?', or '|' a number '[0-9]', and possibly more numbers '+'
        #    example: this command will take formula = C6H12N1O3Si1 and return broken_formula = array(['C','6','H','12','N','1','O','3','Si','1'])
        #        all components are strings
        n_formula_entries = len(broken_formula)

        #find the index of the number of the atom which can acquire a label in the formula for the full fragment
        #    it is used in creating the correction matrix below because successive quantities of this atom need to be subtracted and a heavy atom put in its place
        atom_index = np.where(broken_formula==self.Tracer.LabeledElement)[0][0]
        atom_quantity_index = atom_index+1 #refering to full fragment

        #the number of rows of the correction matrix is equal to the quantity of the atom being corrected for that are in the fragment and the original metabolite
        atom_quantity = quantity_of_atom(self.CanAcquireLabel.formula,self.Tracer.LabeledElement) #this does not refer to the full fragment!

        #add the "heavy atom to the end of the broken formula array", initially its quantity is 0
        broken_formula = np.append(broken_formula,np.array(['Hv','0']))
        n_formula_entries_heavy = len(broken_formula)

        #replace each atom of interest with a heavy atom and get the natural mid of the result
        #    these mids fill the rows of the correction matrix
        broken_formula_correct = copy.copy(broken_formula) #initialize the array to carry the formula with a heavy atom
        correction_matrix_dict = dict() #initialize a dictionary to hold the rows of the correction matrix
        for i in range(0,atom_quantity+1):
            #subtract an atom of interest from the formula
            broken_formula_correct[atom_quantity_index] = broken_formula[atom_quantity_index].astype(np.int) - i
            broken_formula_correct[atom_quantity_index] = broken_formula_correct[atom_quantity_index].astype(np.str)

            #replace that atom with a heavy atom
            broken_formula_correct[n_formula_entries+1] = broken_formula[n_formula_entries+1].astype(np.int) + i
            broken_formula_correct[n_formula_entries+1] = broken_formula_correct[n_formula_entries+1].astype(np.str)

            #update the string version of the formula from the array version
            new_formula = ''
            for j in range(0,n_formula_entries_heavy):
                new_formula = new_formula + broken_formula_correct[j]

            #make a Formula object
            new_formula = Formula(formula=new_formula,Tracer=self.Tracer,HighRes=self.HighRes)

            #get the mid due to natural abundances of the updated formula (with one or more heavy atoms)
            new_formula.calc_natural_mid()
            correction_matrix_dict[i] = new_formula.NaturalMID

            # Keep track of the length of the longest natural MID with heavy atoms
            #     All of the MIDs of the molecule with incorporated heavy atoms must be set to the same length to form a correction matrix
            if i==0:
                n_theoretical_mid_entries = len(correction_matrix_dict[i])

            if i>0:
                if n_theoretical_mid_entries < len(correction_matrix_dict[i]):
                    n_theoretical_mid_entries = len(correction_matrix_dict[i])

        # Make all of the natural MIDs of the molecule with incorporated heavy atoms the same length by appending zeros
        #     This length is referred to as the number of theoretical MID entries
        for i in range(0,atom_quantity+1):
            # The number of theoretical MID entries in the correction matrix must be the same as the number of measured MID entries for the matrix algebra to work
            #     If the number of theoretical MID entries is less, it is increased
            #     The case where n_theoretical_mid_entries is greater (the usual case) is handled later by increasing the number of measured MID entries
            if n_theoretical_mid_entries < len(self.MIDm):
                n_theoretical_mid_entries = len(self.MIDm)

            # Lengthen each theoretical MID with given quantities of heavy atoms to the specified length of the theoretical MIDs
            #     MIDs will NOT have to be shortened here because they are all set to have the same length as the longest theoretical MID
            if len(correction_matrix_dict[i]) < n_theoretical_mid_entries:
                n_zeros_needed = n_theoretical_mid_entries - len(correction_matrix_dict[i])
                correction_matrix_dict[i] = np.pad(correction_matrix_dict[i],(0,n_zeros_needed),mode='constant')

        #make the correction matrix dictionary into a matrix
        n_keys = len(correction_matrix_dict.keys())
        n_MID_entries = len(correction_matrix_dict[0])
        CM = np.zeros((n_MID_entries,n_keys))
        CM_rows = np.arange(0,n_MID_entries)
        for key in correction_matrix_dict.keys():
            CM[CM_rows,key] = correction_matrix_dict[key]

        #find the inverse of the correction matrix
        #    Use the Moore–Penrose pseudo-inverse because the matrix is not necessarily square and the linear problem is "over specified"
        set_trace()
        CMi = np.linalg.pinv(CM)
        #    CMi = np.linalg.inv(CM) would give the inverse of a square matrix


        self.CM = CM
        self.CMi = CMi

    def calc_corrected_mid(self):

        import numpy as np
        from pdb import set_trace

        #find the inverse of the correction matrix
        CMi = self.CMi

        #the theoretical MIDs are the rows of the correction matrix.
        #    Their length corresponds to the number of rows of the right inverse of the correcion matrix
        n_theoretical_mid_entries = CMi.shape[1]

        #the measured MID must have the same number of entries as each of the theoretical MIDs
        #    if it is short, add zeros to make up for the difference
        MIDm = self.MIDm
        if len(MIDm) < n_theoretical_mid_entries:
            mid_u_appendage = np.zeros(n_theoretical_mid_entries-len(MIDm))
            MIDm = np.append(MIDm,mid_u_appendage)

        #calculate corrected MID
        MIDc = np.dot(CMi,MIDm)
        MIDc = MIDc/sum(MIDc)
        self.assign('MIDc',MIDc)
