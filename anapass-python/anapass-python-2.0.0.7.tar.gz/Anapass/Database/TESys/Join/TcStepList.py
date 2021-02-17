
import pymysql
import enum

class TcStepList :  

    class ColumnID : 
        class Hardware(enum.IntEnum) : 
            HardwareAK=0
            BoardID=1
            SocPcbName=2
            DutPcbName=3
            HardwareVersion=4
        class JobList(enum.IntEnum) : 
            JobListAK=5
            JobID=6
            HardwareAK=7
            DutIndex=8
            TedListAK=9
            SoftwareVersion=10
            BeginTime=11
            EndTime=12
        class Job(enum.IntEnum) : 
            JobID=13
            Desc=14
        class TedList(enum.IntEnum) : 
            TedListAK=15
            TedPN=16
            CID0=17
            CID1=18
            CID2=19
            CID3=20
            CID4=21
            CID5=22
            CID6=23
            CID7=24
            OTPREV0=25
            OTPREV1=26
            OTPREV2=27
            OTPREV3=28
            OTPREV4=29
            OTPREV5=30
            OTPREV6=31
            OTPREV7=32
        class Ted(enum.IntEnum) : 
            TedPN=33
            Max_FrameRate=34
            Max_ClockRate=35
            Res_Width=36
            Res_Height=37
            CID_ByteCount=38
            OTPREV_ByteCount=39
        class ScList(enum.IntEnum) : 
            ScListAK=40
            JobListAK=41
            ScAK=42
            BeginTime=43
            EndTime=44
        class Sc(enum.IntEnum) : 
            ScAK=45
            JobID=46
            ScID=47
            Desc=48
        class TcList(enum.IntEnum) : 
            TcListAK=49
            ScListAK=50
            TcAK=51
            BeginTime=52
            EndTime=53
        class Tc(enum.IntEnum) : 
            TcAK=54
            TcID=55
            TcStepCount=56
            CreateDateTime=57
            Desc=58
        class TcStepList(enum.IntEnum) : 
            TcStepListAK=59
            TcListAK=60
            TcStepAK=61
            BeginTime=62
            EndTime=63
        class TcStep(enum.IntEnum) : 
            TcStepAK=64
            TcAK=65
            TcStepID=66
            Desc=67
        class AdcExtV(enum.IntEnum) : 
            TCStepListAK=68
            Ch0=69
            Ch1=70
            Ch2=71
            Ch3=72
            Ch4=73
            Ch5=74
            Ch6=75
            Ch7=76
            Ch8=77
            Ch9=78
            Ch10=79
            Ch11=80
            Ch12=81
            Ch13=82
            Ch14=83
            Ch15=84
            Ch16=85
            Ch17=86
            Ch18=87
            Ch19=88
        class AdcExtA(enum.IntEnum) : 
            TCStepListAK=89
            Ch0=90
            Ch1=91
            Ch2=92
            Ch3=93
            Ch4=94
            Ch5=95
            Ch6=96
            Ch7=97
            Ch8=98
            Ch9=99
            Ch10=100
            Ch11=101
            Ch12=102
            Ch13=103
            Ch14=104
            Ch15=105
            Ch16=106
            Ch17=107
            Ch18=108
            Ch19=109
        class AdcLdoV(enum.IntEnum) : 
            TCStepListAK=110
            Ch0=111
            Ch1=112
            Ch2=113
            Ch3=114
            Ch4=115
            Ch5=116
            Ch6=117
            Ch7=118
            Ch8=119
            Ch9=120
            Ch10=121
            Ch11=122
            Ch12=123
            Ch13=124
            Ch14=125
            Ch15=126
            Ch16=127
            Ch17=128
            Ch18=129
            Ch19=130
        class AdcRegV(enum.IntEnum) : 
            TCStepListAK=131
            Ch0=132
            Ch1=133
            Ch2=134
            Ch3=135
            Ch4=136
            Ch5=137
            Ch6=138
            Ch7=139
            Ch8=140
            Ch9=141
            Ch10=142
            Ch11=143
            Ch12=144
            Ch13=145
            Ch14=146
            Ch15=147
            Ch16=148
            Ch17=149
            Ch18=150
            Ch19=151
        class AdcSoutV(enum.IntEnum) : 
            TCStepListAK=152
            Ch0=153
            Ch1=154
            Ch2=155
            Ch3=156
            Ch4=157
            Ch5=158
            Ch6=159
            Ch7=160
            Ch8=161
            Ch9=162
            Ch10=163
            Ch11=164
            Ch12=165
            Ch13=166
            Ch14=167
            Ch15=168
            Ch16=169
            Ch17=170
            Ch18=171
            Ch19=172
        class AdcErr(enum.IntEnum) : 
            TCStepListAK=173
            Mipi=174
            T2M=175
            ESD=176
            System=177
            PatterApp=178

    

    def __init__(this, conn) : 

        this.__Conn = conn
        this.__CsvColumnTuple = ( \
            ('BoardID', TcStepList.ColumnID.Hardware.BoardID, TcStepList.ColumnID.Hardware.BoardID), \
            ('DutIdx', TcStepList.ColumnID.JobList.DutIndex, TcStepList.ColumnID.JobList.DutIndex), \
            ('날짜', TcStepList.ColumnID.TcStepList.BeginTime, TcStepList.ColumnID.TcStepList.BeginTime), \
            ('시간', TcStepList.ColumnID.TcStepList.BeginTime, TcStepList.ColumnID.TcStepList.BeginTime), \
            ('JobDur', TcStepList.ColumnID.JobList.BeginTime, TcStepList.ColumnID.TcStepList.EndTime), \
            ('TcDur', TcStepList.ColumnID.TcList.BeginTime, TcStepList.ColumnID.TcStepList.EndTime), \
            ('TcStepDur', TcStepList.ColumnID.TcStepList.BeginTime, TcStepList.ColumnID.TcStepList.EndTime), \
            ('JobID', TcStepList.ColumnID.Job.JobID, TcStepList.ColumnID.Job.JobID), \
            ('ScID', TcStepList.ColumnID.Sc.ScID, TcStepList.ColumnID.Sc.ScID), \
            ('TcID', TcStepList.ColumnID.Tc.TcID, TcStepList.ColumnID.Tc.TcID), \
            ('TcStepID', TcStepList.ColumnID.TcStep.TcStepID, TcStepList.ColumnID.TcStep.TcStepID), \
            ('TcDesc', TcStepList.ColumnID.Tc.Desc, TcStepList.ColumnID.Tc.Desc), \
            ('TcStepDesc', TcStepList.ColumnID.TcStep.Desc, TcStepList.ColumnID.TcStep.Desc), \
            ('Vlin1(V)', TcStepList.ColumnID.AdcExtV.Ch0, TcStepList.ColumnID.AdcExtV.Ch0), \
            ('ELVDD(V)', TcStepList.ColumnID.AdcExtV.Ch1, TcStepList.ColumnID.AdcExtV.Ch1), \
            ('VCI(V)', TcStepList.ColumnID.AdcExtV.Ch2, TcStepList.ColumnID.AdcExtV.Ch2), \
            ('VDDI(V)', TcStepList.ColumnID.AdcExtV.Ch3, TcStepList.ColumnID.AdcExtV.Ch3), \
            ('VDDR(V)', TcStepList.ColumnID.AdcExtV.Ch4, TcStepList.ColumnID.AdcExtV.Ch4), \
            ('Vlin1(mA)', TcStepList.ColumnID.AdcExtA.Ch0, TcStepList.ColumnID.AdcExtA.Ch0), \
            ('ELVDD(mA)', TcStepList.ColumnID.AdcExtA.Ch1, TcStepList.ColumnID.AdcExtA.Ch1), \
            ('VCI(mA)', TcStepList.ColumnID.AdcExtA.Ch2, TcStepList.ColumnID.AdcExtA.Ch2), \
            ('VDDI(mA)', TcStepList.ColumnID.AdcExtA.Ch3, TcStepList.ColumnID.AdcExtA.Ch3), \
            ('VDDR(mA)', TcStepList.ColumnID.AdcExtA.Ch4, TcStepList.ColumnID.AdcExtA.Ch4), \
            ('VDD04_T2M(V)', TcStepList.ColumnID.AdcLdoV.Ch0, TcStepList.ColumnID.AdcLdoV.Ch0), \
            ('VDDC(V)', TcStepList.ColumnID.AdcLdoV.Ch1, TcStepList.ColumnID.AdcLdoV.Ch1), \
            ('VDD10_T2M(V)', TcStepList.ColumnID.AdcLdoV.Ch2, TcStepList.ColumnID.AdcLdoV.Ch2), \
            ('VDD09_T2M(V)', TcStepList.ColumnID.AdcLdoV.Ch3, TcStepList.ColumnID.AdcLdoV.Ch3), \
            ('VDD10_MIPI(V)', TcStepList.ColumnID.AdcLdoV.Ch4, TcStepList.ColumnID.AdcLdoV.Ch4), \
            ('VDD12_LP(V)', TcStepList.ColumnID.AdcLdoV.Ch5, TcStepList.ColumnID.AdcLdoV.Ch5), \
            ('VDD12_OSC(V)', TcStepList.ColumnID.AdcLdoV.Ch6, TcStepList.ColumnID.AdcLdoV.Ch6), \
            ('VDD09_T2MC(V)', TcStepList.ColumnID.AdcLdoV.Ch7, TcStepList.ColumnID.AdcLdoV.Ch7), \
            ('VLOUT3_2(V)', TcStepList.ColumnID.AdcRegV.Ch5, TcStepList.ColumnID.AdcRegV.Ch5), \
            ('VCI1(V)', TcStepList.ColumnID.AdcRegV.Ch4, TcStepList.ColumnID.AdcRegV.Ch4), \
            ('VCIR(V)', TcStepList.ColumnID.AdcRegV.Ch10, TcStepList.ColumnID.AdcRegV.Ch10), \
            ('VREG1(V)', TcStepList.ColumnID.AdcRegV.Ch2, TcStepList.ColumnID.AdcRegV.Ch2), \
            ('VREG1OUT(V)', TcStepList.ColumnID.AdcRegV.Ch3, TcStepList.ColumnID.AdcRegV.Ch3), \
            ('VREF1(V)', TcStepList.ColumnID.AdcRegV.Ch0, TcStepList.ColumnID.AdcRegV.Ch0), \
            ('VBOT(V)', TcStepList.ColumnID.AdcRegV.Ch1, TcStepList.ColumnID.AdcRegV.Ch1), \
            ('VGH(V)', TcStepList.ColumnID.AdcRegV.Ch6, TcStepList.ColumnID.AdcRegV.Ch6), \
            ('VGL(V)', TcStepList.ColumnID.AdcRegV.Ch8, TcStepList.ColumnID.AdcRegV.Ch8), \
            ('VINT(V)', TcStepList.ColumnID.AdcRegV.Ch11, TcStepList.ColumnID.AdcRegV.Ch11), \
            ('VGHH(V)', TcStepList.ColumnID.AdcRegV.Ch7, TcStepList.ColumnID.AdcRegV.Ch7), \
            ('VGLL(V)', TcStepList.ColumnID.AdcRegV.Ch9, TcStepList.ColumnID.AdcRegV.Ch9), \
            ('VEH(V)', TcStepList.ColumnID.AdcRegV.Ch12, TcStepList.ColumnID.AdcRegV.Ch12), \
            ('VAINT(V)', TcStepList.ColumnID.AdcRegV.Ch13, TcStepList.ColumnID.AdcRegV.Ch13), \
            ('BML(V)', TcStepList.ColumnID.AdcRegV.Ch14, TcStepList.ColumnID.AdcRegV.Ch14), \
            ('SOUT_4(V)', TcStepList.ColumnID.AdcSoutV.Ch0, TcStepList.ColumnID.AdcSoutV.Ch0), \
            ('SOUT_5(V)', TcStepList.ColumnID.AdcSoutV.Ch1, TcStepList.ColumnID.AdcSoutV.Ch1), \
            ('SOUT_721(V)', TcStepList.ColumnID.AdcSoutV.Ch2, TcStepList.ColumnID.AdcSoutV.Ch2), \
            ('SOUT_944(V)', TcStepList.ColumnID.AdcSoutV.Ch3, TcStepList.ColumnID.AdcSoutV.Ch3), \
            ('SOUT_948(V)', TcStepList.ColumnID.AdcSoutV.Ch4, TcStepList.ColumnID.AdcSoutV.Ch4), \
            ('SOUT_949(V)', TcStepList.ColumnID.AdcSoutV.Ch5, TcStepList.ColumnID.AdcSoutV.Ch5), \
            ('SOUT_1617(V)', TcStepList.ColumnID.AdcSoutV.Ch6, TcStepList.ColumnID.AdcSoutV.Ch6), \
            ('SOUT_1840(V)', TcStepList.ColumnID.AdcSoutV.Ch7, TcStepList.ColumnID.AdcSoutV.Ch7), \
            ('SOUT_1844(V)', TcStepList.ColumnID.AdcSoutV.Ch8, TcStepList.ColumnID.AdcSoutV.Ch8), \
            ('SOUT_1845(V)', TcStepList.ColumnID.AdcSoutV.Ch9, TcStepList.ColumnID.AdcSoutV.Ch9), \
            ('SOUT_2736(V)', TcStepList.ColumnID.AdcSoutV.Ch10, TcStepList.ColumnID.AdcSoutV.Ch10), \
            ('SOUT_2737(V)', TcStepList.ColumnID.AdcSoutV.Ch11, TcStepList.ColumnID.AdcSoutV.Ch11), \
            ('SOUT_2740(V)', TcStepList.ColumnID.AdcSoutV.Ch12, TcStepList.ColumnID.AdcSoutV.Ch12), \
            ('SOUT_2961(V)', TcStepList.ColumnID.AdcSoutV.Ch13, TcStepList.ColumnID.AdcSoutV.Ch13), \
            ('SOUT_3677(V)', TcStepList.ColumnID.AdcSoutV.Ch14, TcStepList.ColumnID.AdcSoutV.Ch14), \
            ('SOUT_3680(V)', TcStepList.ColumnID.AdcSoutV.Ch15, TcStepList.ColumnID.AdcSoutV.Ch15), \
            ('MipiErr', TcStepList.ColumnID.AdcErr.Mipi, TcStepList.ColumnID.AdcErr.Mipi), \
            ('T2MErr', TcStepList.ColumnID.AdcErr.T2M, TcStepList.ColumnID.AdcErr.T2M), \
            ('ESDErr', TcStepList.ColumnID.AdcErr.ESD, TcStepList.ColumnID.AdcErr.ESD), \
            ('Sys', TcStepList.ColumnID.AdcErr.System, TcStepList.ColumnID.AdcErr.System), \
            ('PtrnErr', TcStepList.ColumnID.AdcErr.PatterApp, TcStepList.ColumnID.AdcErr.PatterApp), \
            ('CHIPID0', TcStepList.ColumnID.TedList.CID0, TcStepList.ColumnID.TedList.CID0), \
            ('CHIPID1', TcStepList.ColumnID.TedList.CID1, TcStepList.ColumnID.TedList.CID1), \
            ('CHIPID2', TcStepList.ColumnID.TedList.CID2, TcStepList.ColumnID.TedList.CID2), \
            ('CHIPID3', TcStepList.ColumnID.TedList.CID3, TcStepList.ColumnID.TedList.CID3), \
            ('CHIPID4', TcStepList.ColumnID.TedList.CID4, TcStepList.ColumnID.TedList.CID4), \
            ('OPTREV0', TcStepList.ColumnID.TedList.OTPREV0, TcStepList.ColumnID.TedList.OTPREV0), \
            ('OPTREV1', TcStepList.ColumnID.TedList.OTPREV1, TcStepList.ColumnID.TedList.OTPREV1), \
            ('OPTREV2', TcStepList.ColumnID.TedList.OTPREV2, TcStepList.ColumnID.TedList.OTPREV2), \
            ('OPTREV3', TcStepList.ColumnID.TedList.OTPREV3, TcStepList.ColumnID.TedList.OTPREV3), \
            ('OPTREV4', TcStepList.ColumnID.TedList.OTPREV4, TcStepList.ColumnID.TedList.OTPREV4), \
            ('OPTREV5', TcStepList.ColumnID.TedList.OTPREV5, TcStepList.ColumnID.TedList.OTPREV5), \
        )  

        this.__FromStatement = """from Hardware
left join JobList on JobList.HardwareAK=Hardware.HardwareAK
right join Job on Job.JobID=JobList.JobID
right join TedList on TedList.TedListAK=JobList.TedListAK
right join Ted on Ted.TedPN=TedList.TedPN
left join ScList on ScList.JobListAK=JobList.JobListAK
right join Sc on Sc.ScAK=ScList.ScAK
left join TcList on TcList.ScListAK=ScList.ScListAK
right join Tc on Tc.TcAK=TcList.TcAK
left join TcStepList on TcStepList.TcListAK=TcList.TcListAK
right join TcStep on TcStep.TcStepAK=TcStepList.TcStepAK
left join AdcExtV on AdcExtV.TCStepListAK=TcStepList.TcStepListAK
left join AdcExtA on AdcExtA.TCStepListAK=TcStepList.TcStepListAK
left join AdcLdoV on AdcLdoV.TCStepListAK=TcStepList.TcStepListAK
left join AdcRegV on AdcRegV.TCStepListAK=TcStepList.TcStepListAK
left join AdcSoutV on AdcSoutV.TCStepListAK=TcStepList.TcStepListAK
left join AdcErr on AdcErr.TCStepListAK=TcStepList.TcStepListAK """
        #where Hardware.HardwareAK='1' and JobList.JobID='20' and ScList.ScAK='15' and TcList.TcAK='1' """


    def ExportToCSV(this, csvFileName,  *, hardwareAk=-1, jobId=-1, scAk=-1, tcAk=-1) : 

        #allocate cursor
        curs = this.__Conn.cursor()

        #wriet csvFile Header
        csvFile = open(csvFileName, "w")
        for csvColProp in this.__CsvColumnTuple :
            colName = csvColProp[0]
            csvFile.write("%s," % colName)
        csvFile.write("\n")
        
        #set where statement
        whereCnt = 0
        whereStatement = "where "
        
        if hardwareAk != -1 :
            if whereCnt > 0 : whereStatement += "and "
            whereStatement += "Hardware.HardwareAK='%d' " % hardwareAk
            whereCnt+=1

        if jobId != -1 :
            if whereCnt > 0 : whereStatement += "and "
            whereStatement += "JobList.JobID='%d' " % jobId
            whereCnt+=1
            
        if scAk != -1 :
            if whereCnt > 0 : whereStatement += "and "
            whereStatement += "ScList.ScAK='%d' " % scAk
            whereCnt+=1

        if tcAk != -1 :
            if whereCnt > 0 : whereStatement += "and "
            whereStatement += "TcList.TcAK='%d' " % tcAk
            whereCnt+=1
        
        #get record Count
        sqlQuery = "select count(TcStepList.TcStepListAK) as cnt "
        sqlQuery += this.__FromStatement
        sqlQuery += whereStatement
        print("---------------------------------------------------------------------------------")
        print("SQL Query ")
        print("---------------------------------------------------------------------------------")
        print(sqlQuery)
        print("---------------------------------------------------------------------------------")
        print("Checking Recrod Count....")
        curs.execute(sqlQuery)
        record = curs.fetchone()
        assert(record != None)
        recordCount = record[0]        
        #print(sqlQuery)
                
        #setgng sqlQuery Statement
        sqlQuery = "select * "
        sqlQuery += this.__FromStatement
        sqlQuery += whereStatement
        print("---------------------------------------------------------------------------------")
        print("SQL Query  recordCount=%d" % recordCount)
        print("---------------------------------------------------------------------------------")
        print(sqlQuery)
        print("---------------------------------------------------------------------------------")
        recordIdx = 0
        print("Query....")
        curs.execute(sqlQuery)

        print("Exprot File Name [%s] " % csvFileName )
        while True :
            record = curs.fetchone()
            if record == None :
                break

            for csvCol in this.__CsvColumnTuple :
                dbColValue0 = record[csvCol[1].value]
                csvColName = csvCol[0]
        
                if csvColName == '날짜' : 
                    #print("%s=%s " % (csvColName, dbColValue0.date()), end='')
                    csvFile.write("%s," % (dbColValue0.date()))

                elif csvColName == '시간' : 
                    #print("%s=%s " % (csvColName, dbColValue0.time()), end='')
                    csvFile.write("%s," % (dbColValue0.time()))

                elif csvColName == 'JobDur' or csvColName == 'ScDur' or csvColName == 'TcDur' or csvColName == 'TcStepDur' : 
                    dbColValue1 = record[csvCol[2].value]
                    diff = dbColValue1 - dbColValue0
                    dur = diff.total_seconds()
                    #print("%s=%d " % (csvColName, dur), end='')
                    csvFile.write("%d," % (dur))

                elif csvColName == 'MipiErr' or csvColName == 'T2MErr' or csvColName == 'ESDErr' or csvColName == 'PtrnErr' : 
                    #print("%s=0x%04X " % (csvColName,  dbColValue0), end='')
                    csvFile.write("0x%04X," % (dbColValue0))

                elif csvColName == 'Sys' : 
                    #print("%s=0x%016X " % (csvColName,  dbColValue0), end='')
                    csvFile.write("0x%016X," % (dbColValue0))


                elif csvColName == 'CHIPID0' or csvColName == 'CHIPID1' or csvColName == 'CHIPID2' or csvColName == 'CHIPID3' or csvColName == 'CHIPID4'  : 
                    #print("%s=0x%02X " % (csvColName,  dbColValue0), end='')
                    csvFile.write("0x%02X," % (dbColValue0))

                elif csvColName == 'OPTREV0' or csvColName == 'OPTREV1' or csvColName == 'OPTREV2' or csvColName == 'OPTREV3' or csvColName == 'OPTREV4' or csvColName == 'OPTREV5' : 
                    #print("%s=0x%02X " % (csvColName,  dbColValue0), end='')
                    csvFile.write("0x%02X," % (dbColValue0))

                else : 
                    #print("%s=%s " % (csvColName,  str(dbColValue0)), end='')
                    csvFile.write("%s," % (str(dbColValue0)))

            csvFile.write("\n")
            print("\r%d/%d (%d%c)  " % (recordIdx+1, recordCount, (recordIdx+1)*100/recordCount, '%' ),  end=' ' )
            recordIdx += 1
            #end of for csvCol in CsvColumnTuple :
        #end of while True :
        print()

        csvFile.close()

        return True  # end of  def ExportToCSV(this, csvFileName,  *, hardwareAk=-1, jobId=-1, scAk=-1, tcAk=-1) : 
