class CableDatabase:
    """
        Class for .cadata cable database
    """

    def __init__(self, insulations, filaments, strands, cables, transients, quenches, conductors):
        self.insulations = insulations
        self.filaments = filaments
        self.strands = strands
        self.cables = cables
        self.transients = transients
        self.quenches = quenches
        self.conductors = conductors

    def toString(self):
        return str(self.insulation.name)

    def printConductorData(self, selectedConductorName):
        '''
            Print data of the selected conductor, using data in a list of Conductor objects.

            :param selectedConductorName: String defining the name of the conductor whose properties will be printed
            :type selectedConductorName: str

            :return:
        '''

        insulations = self.insulations
        filaments = self.filaments
        strands = self.strands
        cables = self.cables
        transients = self.transients
        quenches = self.quenches
        conductors = self.conductors

        # Info about the selected conductor
        conductorSelected = conductors[selectedConductorName]
        print('Name = {}'.format(conductorSelected))
        #     print("Conductor name: " + conductorSelected.cableGeom)
        print("Conductor: " + conductorSelected.toString())
        print("Insulation: " + insulations[conductorSelected.insul].toString())
        print("Filament: " + filaments[conductorSelected.filament].toString())
        print("Strand: " + strands[conductorSelected.strand].toString())
        #     print("Strand diameter: " + str(strands[conductorSelected.strand].diam))
        print("Transient: " + transients[conductorSelected.trans].toString())
        print("Quench: " + quenches[conductorSelected.quenchMat].toString())
        print("Cable: " + cables[conductorSelected.cableGeom].toString())


class Insulation:
    '''
        Class for insulations
    '''
    def __init__(self, name, radial, azimut, comment):
        self.name =  name
        self.radial = radial
        self.azimut = azimut
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.radial) + ", " + str(self.azimut) + ", " + self.comment


class Filament:
    '''
        Class for filaments
    '''
    def __init__(self, name, fildiao, fildiai, Jc_Fit, Fit, comment):
        self.name =  name
        self.fildiao = fildiao
        self.fildiai = fildiai
        self.Jc_Fit = Jc_Fit
        self.Fit = Fit
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.fildiao) + ", " + str(self.fildiai) + ", " + str(self.Jc_Fit) + ", " + str(self.Fit) + ", " + self.comment


class Strand:
    '''
        Class for strands
    '''
    def __init__(self, name, diam, cu_sc, RRR, Tref, Bref, Jc_BrTr, dJc_dB, comment):
        self.name =  name
        self.diam = diam
        self.cu_sc = cu_sc
        self.RRR = RRR
        self.Tref = Tref
        self.Bref = Bref
        self.Jc_BrTr = Jc_BrTr
        self.dJc_dB = dJc_dB
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.diam) + ", " + str(self.cu_sc) + ", " + str(self.RRR) + ", " + str(self.Tref) + ", " + str(self.Bref) + ", " + str(self.Jc_BrTr) + ", " + str(self.dJc_dB) + ", " + self.comment


class Cable:
    '''
        Class for cables
    '''
    def __init__(self, name, height, width_i, width_o, ns, transp, degrd, comment):
        self.name =  name
        self.height = height
        self.width_i = width_i
        self.width_o = width_o
        self.ns = ns
        self.transp = transp
        self.degrd = degrd
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.height) + ", " + str(self.width_i) + ", " + str(self.width_o) + ", " + str(self.ns) + ", " + str(self.transp) + ", " + str(self.degrd) + ", " + self.comment


class Transient:
    '''
        Class for transients
    '''
    def __init__(self, name, Rc, Ra, filTwistp, filR0, fil_dRdB, strandfillFac, comment):
        self.name =  name
        self.Rc = Rc
        self.Ra = Ra
        self.filTwistp = filTwistp
        self.filR0 = filR0
        self.fil_dRdB = fil_dRdB
        self.strandfillFac = strandfillFac
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.Rc) + ", " + str(self.Ra) + ", " + str(self.filTwistp) + ", " + str(self.filR0) + ", " + str(self.fil_dRdB) + ", " + str(self.strandfillFac) + ", " + self.comment


class Quench:
    '''
        Class for quenches
    '''
    def __init__(self, name, SCHeatCapa, CuHeatCapa, CuThermCond, CuElecRes, InsHeatCapa, InsThermCond, FillHeatCapa, He, comment):
        self.name =  name
        self.SCHeatCapa = SCHeatCapa
        self.CuHeatCapa = CuHeatCapa
        self.CuThermCond = CuThermCond
        self.CuElecRes = CuElecRes
        self.InsHeatCapa = InsHeatCapa
        self.InsThermCond = InsThermCond
        self.FillHeatCapa = FillHeatCapa
        self.He = He
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.SCHeatCapa) + ", " + str(self.CuHeatCapa) + ", " + str(self.CuThermCond) + ", " + str(self.CuElecRes) + ", " + str(self.InsHeatCapa) + ", " + str(self.InsThermCond) + ", " + str(self.FillHeatCapa) + ", " + str(self.He) + ", " + self.comment


class Conductor:
    '''
        Class for conductor
    '''
    def __init__(self, name, conductorType, cableGeom, strand, filament, insul, trans, quenchMat, T_0, comment):
        self.name =  name
        self.conductorType = conductorType
        self.cableGeom = cableGeom
        self.strand = strand
        self.filament = filament
        self.insul = insul
        self.trans = trans
        self.quenchMat = quenchMat
        self.T_0 = T_0
        self.comment = comment
    def toString(self):
        return self.name + ", " + str(self.conductorType) + ", " + str(self.cableGeom) + ", " + str(self.strand) + ", " + str(self.filament) + ", " + str(self.insul) + ", " + str(self.trans) + ", " + str(self.quenchMat)+ ", " + str(self.T_0) + ", " + self.comment
    

def getConductorDataFromCadataFile(fileNameCadata) -> CableDatabase:
    '''
        **Parse the content of the entire .cadata file and store it in a CableDatabase object**

        Function returns a CableDatabase object that contains information about all conductors

        parameter fileNameCadata: name to assign to the cable database
        type fileNameCadata: str
        return: CableDatabase
    '''
    print('File with cable database: {}'.format(fileNameCadata))

    file = open(fileNameCadata, "r")
    fileContent = file.read()

    # separate rows
    fileContentByRow = fileContent.split("\n")

    insulations = {}
    filaments = {}
    strands = {}
    transients = {}
    quenches = {}
    cables = {}
    conductors = {}

    for index in range(len(fileContentByRow)):
        fc = fileContentByRow[index]

        if "INSUL" in fc and fc[0:5]=="INSUL":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                insulationParameters = fcTemp.split()
                name = insulationParameters[1]
                radial = float(insulationParameters[2])
                azimut = float(insulationParameters[3])
                comment = " ".join(insulationParameters[4:])

                insulations[name] = Insulation(name, radial, azimut, comment)

        if "FILAMENT" in fc and fc[0:8]=="FILAMENT":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                filamentParameters = fcTemp.split()
                name = filamentParameters[1]
                fildiao = float(filamentParameters[2])
                fildiai = float(filamentParameters[3])
                Jc_Fit = filamentParameters[4]
                Fit = filamentParameters[5]
                comment = " ".join(filamentParameters[6:])

                filaments[name] = Filament(name, fildiao, fildiai, Jc_Fit, Fit, comment)

        if "STRAND" in fc and fc[0:6]=="STRAND":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                strandParameters = fcTemp.split()
                name = strandParameters[1]
                diam = float(strandParameters[2])
                cu_sc = float(strandParameters[3])
                RRR = float(strandParameters[4])
                Tref = float(strandParameters[5])
                Bref = float(strandParameters[6])
                Jc_BrTr = float(strandParameters[7])
                dJc_dB = float(strandParameters[8])
                comment = " ".join(strandParameters[9:])

                strands[name] = Strand(name, diam, cu_sc, RRR, Tref, Bref, Jc_BrTr, dJc_dB, comment)

        if "TRANSIENT" in fc and fc[0:9]=="TRANSIENT":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                transientParameters = fcTemp.split()
                name = transientParameters[1]
                Rc = float(transientParameters[2])
                Ra = float(transientParameters[3])
                filTwistp = float(transientParameters[4])
                filR0 = float(transientParameters[5])
                fil_dRdB = float(transientParameters[6])
                strandfillFac = float(transientParameters[7])
                comment = " ".join(transientParameters[8:])

                transients[name] = Transient(name, Rc, Ra, filTwistp, filR0, fil_dRdB, strandfillFac, comment)
            # Add entry "NONE"
            name = "NONE"
            Rc = []
            Ra = []
            filTwistp = []
            filR0 = []
            fil_dRdB = []
            strandfillFac = []
            comment = ""
            transients[name] = Transient(name, Rc, Ra, filTwistp, filR0, fil_dRdB, strandfillFac, comment)

        if "QUENCH" in fc and fc[0:6]=="QUENCH":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                quenchParameters = fcTemp.split()
                name = quenchParameters[1]
                SCHeatCapa = float(quenchParameters[2])
                CuHeatCapa = float(quenchParameters[3])
                CuThermCond = float(quenchParameters[4])
                CuElecRes = float(quenchParameters[5])
                InsHeatCapa = float(quenchParameters[6])
                InsThermCond = float(quenchParameters[7])
                FillHeatCapa = float(quenchParameters[8])
                He = float(quenchParameters[9])
                comment = " ".join(quenchParameters[10:])

                quenches[name] = Quench(name, SCHeatCapa, CuHeatCapa, CuThermCond, CuElecRes, InsHeatCapa, InsThermCond, FillHeatCapa, He, comment)
            # Add entry "NONE"
            name = "NONE"
            SCHeatCapa = []
            CuHeatCapa = []
            CuThermCond = []
            CuElecRes = []
            InsHeatCapa = []
            InsThermCond = []
            FillHeatCapa = []
            He = []
            comment = ""
            quenches[name] = Quench(name, SCHeatCapa, CuHeatCapa, CuThermCond, CuElecRes, InsHeatCapa, InsThermCond, FillHeatCapa, He, comment)

        if "CABLE" in fc and fc[0:5]=="CABLE":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                cableParameters = fcTemp.split()
                name = cableParameters[1]
                height = float(cableParameters[2])
                width_i = float(cableParameters[3])
                width_o = float(cableParameters[4])
                ns = float(cableParameters[5])
                transp = float(cableParameters[6])
                degrd = float(cableParameters[7])
                comment = " ".join(cableParameters[8:])

                cables[name] = Cable(name, height, width_i, width_o, ns, transp, degrd, comment)

        if "CONDUCTOR" in fc and fc[0:9]=="CONDUCTOR":
            keywordAndRowNumber = fc.split()
            rowNumber = int(keywordAndRowNumber[1])
            for fcTemp in fileContentByRow[index+1:index+1+rowNumber]:
                conductorParameters = fcTemp.split()
                name = conductorParameters[1]
                conductorType = int(conductorParameters[2])
                cableGeom = conductorParameters[3]
                strand = conductorParameters[4]
                filament = conductorParameters[5]
                insul = conductorParameters[6]
                trans = conductorParameters[7]
                quenchMat = conductorParameters[8]
                T_0 = float(conductorParameters[9])
                comment = " ".join(conductorParameters[10:])

                conductors[name] = Conductor(name, conductorType, cableGeom, strand, filament, insul, trans, quenchMat, T_0, comment)

        cadatabase = CableDatabase(insulations, filaments, strands, cables, transients, quenches, conductors)
    return cadatabase


