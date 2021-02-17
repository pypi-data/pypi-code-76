import math
from steam_nb_api.roxie_parser import CableDatabase


class ConductorSigma:
    '''
        Class for SIGMA conductor parameters
    '''
    def __init__(self, name, wInsulNarrow, wInsulWide, dFilament, dstrand, fracCu, fracSc, RRR, TupRRR, Top, Rc, Ra, fRhoEff, lTp, wBare, hInBare, hOutBare, noOfStrands, noOfStrandsPerLayer, noOfLayers, lTpStrand, wCore, hCore, thetaTpStrand, degradation, C1, C2, fracHe, fracFillInnerVoids, fracFillOuterVoids):
        self.name =  name
        self.wInsulNarrow = wInsulNarrow
        self.wInsulWide = wInsulWide
        self.dFilament = dFilament
        self.dstrand = dstrand
        self.fracCu = fracCu
        self.fracSc = fracSc
        self.RRR = RRR
        self.TupRRR = TupRRR
        self.Top = Top
        self.Rc = Rc
        self.Ra = Ra
        self.fRhoEff = fRhoEff
        self.lTp = lTp
        self.wBare = wBare
        self.hInBare = hInBare
        self.hOutBare = hOutBare
        self.noOfStrands = noOfStrands
        self.noOfStrandsPerLayer = noOfStrandsPerLayer
        self.noOfLayers = noOfLayers
        self.lTpStrand = lTpStrand
        self.wCore = wCore
        self.hCore = hCore
        self.thetaTpStrand = thetaTpStrand
        self.degradation = degradation
        self.C1 = C1
        self.C2 = C2
        self.fracHe = fracHe
        self.fracFillInnerVoids = fracFillInnerVoids
        self.fracFillOuterVoids = fracFillOuterVoids


    def printConductorDataSigma(self):
        '''
            Print SIGMA conductor data.
        '''

        print('Name = {}'.format(self.name))
        print('wInsulNarrow = {}'.format(self.wInsulNarrow))
        print('wInsulWide = {}'.format(self.wInsulWide))
        print('dFilament = {}'.format(self.dFilament))
        print('dstrand = {}'.format(self.dstrand))
        print('fracCu = {}'.format(self.fracCu))
        print('fracSc = {}'.format(self.fracSc))
        print('RRR = {}'.format(self.RRR))
        print('TupRRR = {}'.format(self.TupRRR))
        print('Top = {}'.format(self.Top))
        print('Rc = {}'.format(self.Rc))
        print('Ra = {}'.format(self.Ra))
        print('fRhoEff = {}'.format(self.fRhoEff))
        print('lTp = {}'.format(self.lTp))
        print('wBare = {}'.format(self.wBare))
        print('hInBare = {}'.format(self.hInBare))
        print('hOutBare = {}'.format(self.hOutBare))
        print('noOfStrands = {}'.format(self.noOfStrands))
        print('noOfStrandsPerLayer = {}'.format(self.noOfStrandsPerLayer))
        print('noOfLayers = {}'.format(self.noOfLayers))
        print('lTpStrand = {}'.format(self.lTpStrand))
        print('wCore = {}'.format(self.wCore))
        print('hCore = {}'.format(self.hCore))
        print('thetaTpStrand = {}'.format(self.thetaTpStrand))
        print('degradation = {}'.format(self.degradation))
        print('C1 = {}'.format(self.C1))
        print('C2 = {}'.format(self.C2))
        print('fracHe = {}'.format(self.fracHe))
        print('fracFillInnerVoids = {}'.format(self.fracFillInnerVoids))
        print('fracFillOuterVoids = {}'.format(self.fracFillOuterVoids))


def getConductorSigmaFromCableDatabase(cadatabase: CableDatabase, selectedConductorName: str) -> ConductorSigma:
    '''
        ** Get the SIGMA parameters of the selected conductor from an existing CableDatabase object **

        Function returns an outputConductorSigma object with the SIGMA parameters of the selected conductor

        parameter cadatabase: CableDatabase object containing information about the conductor database
        type cadatabase: CableDatabase
        parameter selectedConductorName: Name of the conductor whose parameters need to be extracted
        type selectedConductorName: string
        return: ConductorSigma
    '''

    name = selectedConductorName

    insulations = cadatabase.insulations
    filaments = cadatabase.filaments
    strands = cadatabase.strands
    cables = cadatabase.cables
    transients = cadatabase.transients
    quenches = cadatabase.quenches
    conductors = cadatabase.conductors

    # Select conductor by name
    conductorSelected = conductors[selectedConductorName]

    # Parameters defining Insulation
    wInsulNarrow = insulations[conductorSelected.insul].radial * 1e-3
    wInsulWide = insulations[conductorSelected.insul].azimut * 1e-3

    # Parameters defining Filament
    dFilament = filaments[conductorSelected.filament].fildiao * 1e-6

    # Parameters defining Strand
    dstrand = strands[conductorSelected.strand].diam * 1e-3
    fracCu = strands[conductorSelected.strand].cu_sc / (1 + strands[conductorSelected.strand].cu_sc);
    fracSc = 1 / (1 + strands[conductorSelected.strand].cu_sc);
    RRR = strands[conductorSelected.strand].RRR
    TupRRR = []
    Top = []

    # Parameters defining Transient
    Rc = transients[conductorSelected.trans].Rc
    Ra = transients[conductorSelected.trans].Ra
    fRhoEff = 1
    lTp = transients[conductorSelected.trans].filTwistp

    # Parameters defining Cable
    wBare = cables[conductorSelected.cableGeom].height * 1e-3
    hInBare = cables[conductorSelected.cableGeom].width_i * 1e-3
    hOutBare = cables[conductorSelected.cableGeom].width_o * 1e-3
    noOfStrands = cables[conductorSelected.cableGeom].ns
    if noOfStrands == 1:
        noOfStrandsPerLayer = 1
        noOfLayers = 1
    else:  # Rutherford cable assumed
        noOfStrandsPerLayer = int(noOfStrands / 2)
        noOfLayers = 2
    lTpStrand = cables[conductorSelected.cableGeom].transp * 1e-3
    wCore = []
    hCore = []
    if lTpStrand != 0:
        thetaTpStrand = math.atan2((wBare - dstrand), (lTpStrand / 2))
    else:
        thetaTpStrand = []
    degradation = cables[conductorSelected.cableGeom].degrd / 100
    C1 = []
    C2 = []
    fracHe = []
    fracFillInnerVoids = []
    fracFillOuterVoids = []

    outputConductorSigma = ConductorSigma(name, wInsulNarrow, wInsulWide, dFilament, dstrand, fracCu, fracSc, RRR,
                                          TupRRR, Top, Rc, Ra, fRhoEff, lTp, wBare, hInBare, hOutBare, noOfStrands,
                                          noOfStrandsPerLayer, noOfLayers, lTpStrand, wCore, hCore, thetaTpStrand,
                                          degradation, C1, C2, fracHe, fracFillInnerVoids, fracFillOuterVoids)

    return outputConductorSigma

