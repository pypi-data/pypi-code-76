class Tracer:

    # Initializer and Instance Attributes
    def __init__(self,LabeledElement,TracerEnrichment,LabelEnrichment):
        from pdb import set_trace

        self.LabeledElement = LabeledElement # A string indicating the atom that is considered to be labeled
        self.TracerEnrichment = TracerEnrichment
        self.LabelEnrichment = LabelEnrichment
        self.NaturalLabeledAtomMID = None # The MID of the labeled atom if it were unlabeled (needed when tracer and/or label enrichments are specified)

        self.ReadMID()


    def ReadMID(self):
        # This method opens the text file defining the AtomMIDs and imports that information into the attribute NaturalMID as a numpy array

        import os.path
        import os
        import numpy as np
        import PolyMID
        from pdb import set_trace

        # Get the character used to separate directories in the operating system
        slash = os.sep

        PolyMID_Path = os.path.abspath(PolyMID.__file__)
        PolyMID_Path = PolyMID_Path.split(sep=slash)
        PolyMID_Path = PolyMID_Path[:-1]

        AtomMIDs_txtPath = slash.join(PolyMID_Path) + slash + 'SupportingFiles' + slash + 'AtomIMDs.txt'

        with open(AtomMIDs_txtPath,'r') as AtomMIDsFile:
            for line in AtomMIDsFile:
                line_split = line.split(':')
                FileAtomSymbol = line_split[0].strip()
                FileAtomMID_String = line_split[1].strip()

                if FileAtomSymbol == self.LabeledElement:
                    AtomMID_String = FileAtomMID_String
                    AtomMID_StringArray = AtomMID_String.split(sep=' ')
                    AtomMID_FloatArray = [float(i) for i in AtomMID_StringArray]
                    self.NaturalLabeledAtomMID = np.asarray(AtomMID_FloatArray)
