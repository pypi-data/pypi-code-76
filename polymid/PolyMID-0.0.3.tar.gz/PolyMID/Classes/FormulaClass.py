class Formula:
    # Initializer a Formula Instance and its attributes
    def __init__(self,formula,Tracer,HighRes):
        self.FormulaInput = formula
        self.formula = None
        self.AtomArray = None
        self.NaturalMID = None
        self.Tracer = Tracer # A Tracer object with information about the tracer
        self.HighRes = HighRes # A numpy array indicating which elements have heavy isotopes whose mass differences are resolved from the mass differences due to heavy isotopes of the tracer element
        self.FormatFormula()
        self.CreateAtomArray()

    def FormatFormula(self):
        # This method redefines the formula attribute of the Formula class
        #     This method adds 1s (ones) where they are implied to the input string representing the chemical formula (self.FormulaInput)

        import re
        from pdb import set_trace

        # Find the flanking characters where a 1 should be inserted (1s that are internal to the formula)
        FormulaToEdit = self.FormulaInput
        missing1s = re.findall('(?:[A-Z]|[a-z])[A-Z]',FormulaToEdit)
        #    '(?:)' in '(?:RegExpHere)' denotes a non-capturing group, i.e. it is used for specifying order of operations as opposed to just '()'

        # Insert the internal 1s
        for entry in missing1s:
            NewEntry = entry[0] + '1' + entry[1]
            FormulaToEdit = re.sub(entry,NewEntry,FormulaToEdit)

        # Append an external 1 if necessary
        #     If there is a letter at the end of the string, replace it with that letter and a 1
        LetterAtEnd = re.findall('(?:[A-Z]|[a-z])$',FormulaToEdit)
        #    '(?:)' in '(?:RegExpHere)' denotes a non-capturing group, i.e. it is used for specifying order of operations as opposed to just '()'
        if (len(LetterAtEnd) > 0):
            FormulaToEdit = re.sub(LetterAtEnd[0]+'$',LetterAtEnd[0]+'1',FormulaToEdit)

        # Redefine the formula attribute of the Formula obeject
        self.formula = FormulaToEdit

    def CreateAtomArray(self):
        # This method creates an array of atom objects corresponding to the formula

        # Import required modules
        from pdb import set_trace
        import numpy as np
        import re
        from PolyMID import Atom

        # Break the fragment formula up into its atomic symbol and letter components
        broken_formula = np.array(re.findall('[A-Z][a-z]?|[0-9]+', self.formula))
        #    '[A-Z][a-z]?|[0-9]+': A capital letter [A-Z], followed by a lowercase letter [a-z], which is optional '?', or '|' a number '[0-9]', and possibly more numbers '+'
        #    example: this command will take formula = C6H12N1O3Si1 and return broken_formula = array(['C','6','H','12','N','1','O','3','Si','1'])
        #        all components are strings

        # Get separate arrays containing the atomic symbols and corresponding formula numbers
        odd_indices = np.array(range(1,len(broken_formula),2)) #all of the odd indices of the array broken_formula
        even_indices = np.array(range(0,len(broken_formula),2)) #all of the even indices of the array broken_formula
        formula_numbers = broken_formula[odd_indices].astype(np.int) #the atomic numbers array
        formula_atoms = broken_formula[even_indices] #the atomic symbols array

        AtomArray = []
        AtomCounter = 0
        for atom in formula_atoms:
            AtomStoich = formula_numbers[AtomCounter]
            AtomArray.append(Atom(atom,AtomStoich,Tracer=self.Tracer,HighRes=self.HighRes))
            AtomCounter = AtomCounter + 1

        self.AtomArray = AtomArray


    # Method for calculating natural MID of a Formula object
    def calc_natural_mid(self):
        # This method defines the NatrualMID attribute of the Formula class
        # self.formula: the formula for the fragment whose natural isotopic abundance is being calculated
        #    each atomic symbol must start with a capital letter, if there is a second letter it must be lowercase
        #    if there is no number following an atomic symbol, that number is assumed to be 1

        # Import required modules
        from pdb import set_trace
        import numpy as np
        from PolyMID import expand_polynomial

        # Perform the polynomial expansion; expanding and collecting like terms for two MIDs (atoms) at a time
        expanded_placeholder = np.array([1])
        for AtomObject in self.AtomArray:
            for stoich in list(range(AtomObject.stoich)):
                expanded = expand_polynomial(expanded_placeholder,AtomObject.MID)
                expanded_placeholder = np.array(expanded['prob'])

        # Define the NaturalMID attribute of the Formula object
        natural_mid = np.array(expanded['prob'])
        self.NaturalMID = natural_mid
