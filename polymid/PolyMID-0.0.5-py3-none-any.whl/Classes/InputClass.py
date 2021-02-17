class InputClass:
    #Initializer a Formula Instance and its attributes
    def __init__(self,CorrectInput):
        from pdb import set_trace
        from PolyMID import Fragment
        from PolyMID import Tracer
        import numpy as np
        from PolyMID import get_directory
        from PolyMID import TextToCM

        # If the input to the Correct() function is a fragment object, than it can be used directly.
        # Otherwise a fragment object must be populated by reading from a text file.
        ReadFromTextFile = (isinstance(CorrectInput,str)) | (CorrectInput is None)

        if not ReadFromTextFile:
            self.fragment=CorrectInput

        if ReadFromTextFile:

            #If there is no input provided, the the user is prompted to select a text file using a GUI.
            if (CorrectInput is None):
                CorrectInput = get_directory('gui_file')

            #Initialize variables
            FragmentName = None
            formula = None
            CanAcquireLabel = None
            MIDm = None
            MIDc = None
            CM = None

            #import values from text file
            with open(CorrectInput, 'r') as read_file:
                for line in read_file:
                    line_split = line.split(':')
                    line_split[0] = line_split[0].strip()
                    line_split[1] = line_split[1].strip()

                    if (line_split[0] == 'FragmentFormula') | (line_split[0] == 'Fragment Formula'):
                        FragmentFormula = line_split[1]

                    if (line_split[0] == 'CanAcquireLabel') | (line_split[0] == 'Metabolite Atoms'):
                        CanAcquireLabel = line_split[1]

                    if (line_split[0] == 'MIDm'):
                        MIDm = line_split[1]
                        MIDm = np.fromstring(MIDm,dtype=float,sep=' ')

                    if (line_split[0] == 'FragmentName') | (line_split[0] == 'Fragment Name'):
                        FragmentName = line_split[1]

                    if (line_split[0] == 'LabeledElement') | (line_split[0] == 'Labeled Element'):
                        LabeledElement = line_split[1]

                    if (line_split[0] == 'TracerEnrichment') | (line_split[0] == 'Tracer Enrichment'):
                        TracerEnrichment = float(line_split[1])

                    if (line_split[0] == 'LabelEnrichment') | (line_split[0] == 'Label Enrichment'):
                        LabelEnrichment = float(line_split[1])

                    if (line_split[0] == 'HighRes') | (line_split[0] == 'High Res'):
                        HighRes = line_split[1]
                        if HighRes == 'none':
                            HighRes = np.array([],dtype='str')
                        # convert to a list of the elements that are resolved with high resolution
                        if (HighRes!='none') & (HighRes!='all'):
                            HighRes = HighRes.strip().split(' ')

            self.fragment = Fragment(FragmentName=FragmentName, FragmentFormula=FragmentFormula, CanAcquireLabel=CanAcquireLabel, MIDm=MIDm, LabeledElement=LabeledElement, TracerEnrichment=TracerEnrichment, LabelEnrichment=LabelEnrichment, HighRes=HighRes, MIDc=None, PeakArea=None, CM=CM)
