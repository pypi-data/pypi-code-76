def rs3(dir_path=".", mag_file="", meas_file='measurements.txt',
            spec_file="specimens.txt", samp_file="samples.txt", site_file="sites.txt",
            loc_file="locations.txt", or_con='3', specnum=0, samp_con='2', corr='1',specname=False,
            gmeths="FS-FD:SO-POM", location="unknown", inst="", user="", noave=False, input_dir="",
            savelast=False,lat="", lon="",labfield=0, labfield_phi=0, labfield_theta=0,
            experiment="Demag", cooling_times_list=[]):

    """
    Convert remasoft  export file to MagIC file(s)

    Parameters
    ----------
    dir_path : str
        output directory, default "."
    mag_file : str
        input file name
    meas_file : str
        output measurement file name, default "measurements.txt"
    spec_file : str
        output specimen file name, default "specimens.txt"
    samp_file: str
        output sample file name, default "samples.txt"
    site_file : str
        output site file name, default "sites.txt"
    loc_file : str
        output location file name, default "locations.txt"
    or_con : number
        orientation convention, default '3', see info below
    specnum : int
        number of characters to designate a specimen, default 0
    specname : bool
        if True, use file name stem for specimen name, if False, read from within file, default = False
    samp_con : str
        (specimen/)sample/site naming convention, default '2', see info below
    corr: str
        default '1'
    gmeths : str
        sampling method codes, default "FS-FD:SO-POM", see info below
    location : str
        location name, default "unknown"
    inst : str
        instrument, default ""
    user : str
        user name, default ""
    noave : bool
       do not average duplicate measurements, default False (so by default, DO average)
    savelast : bool
       take the last measurement if replicates at treatment step, default is False
    input_dir : str
        input file directory IF different from dir_path, default ""
    lat : float
        latitude, default ""
    lon : float
        longitude, default ""
    labfield : float
        dc lab field (in micro tesla)
    labfield_phi : float
        declination 0-360
    labfield_theta : float
        inclination -90 - 90
    experiment : str
        experiment type, see info below;  default is Demag
    cooling_times_list : list
        cooling times in [K/minutes] seperated by comma,
        ordered at the same order as XXX.10,XXX.20 ...XX.70

    Returns
    ---------
    Tuple : (True or False indicating if conversion was successful, meas_file name written)


    Info
    ----------
    Orientation convention:
        [1] Lab arrow azimuth= mag_azimuth; Lab arrow dip=-field_dip
            i.e., field_dip is degrees from vertical down - the hade [default]
        [2] Lab arrow azimuth = mag_azimuth-90; Lab arrow dip = -field_dip
            i.e., mag_azimuth is strike and field_dip is hade
        [3] Lab arrow azimuth = mag_azimuth; Lab arrow dip = 90-field_dip
            i.e.,  lab arrow same as field arrow, but field_dip was a hade.
        [4] lab azimuth and dip are same as mag_azimuth, field_dip
        [5] lab azimuth is same as mag_azimuth,lab arrow dip=field_dip-90
        [6] Lab arrow azimuth = mag_azimuth-90; Lab arrow dip = 90-field_dip
        [7] all others you will have to either customize your
            self or e-mail ltauxe@ucsd.edu for help.

   Sample naming convention:
        [1] XXXXY: where XXXX is an arbitrary length site designation and Y
            is the single character sample designation.  e.g., TG001a is the
            first sample from site TG001.    [default]
        [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitrary length)
        [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitrary length)
        [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
        [5] site name = sample name
        [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
        [7-Z] [XXX]YYY:  XXX is site designation with Z characters from samples  XXXYYY
       [8] siteName_sample_specimen: the three are differentiated with '_'

    Sampling method codes:
         FS-FD field sampling done with a drill
         FS-H field sampling done with hand samples
         FS-LOC-GPS  field location done with GPS
         FS-LOC-MAP  field location done with map
         SO-POM   a Pomeroy orientation device was used
         SO-ASC   an ASC orientation device was used
         SO-MAG   orientation with magnetic compass
         SO-SUN   orientation with sun compass

    Experiment type:
        Demag:
            AF and/or Thermal
        PI:
            paleointenisty thermal experiment (ZI/IZ/IZZI)
        ATRM n:

            ATRM in n positions (n=6)

        AARM n:
            AARM in n positions
        CR:
            cooling rate experiment
            The treatment coding of the measurement file should be: XXX.00,XXX.10, XXX.20 ...XX.70 etc. (XXX.00 is optional)
            where XXX in the temperature and .10,.20... are running numbers of the cooling rates steps.
            XXX.00 is optional zerofield baseline. XXX.70 is alteration check.
            if using this type, you must also provide cooling rates in [K/minutes] in cooling_times_list
            separated by comma, ordered at the same order as XXX.10,XXX.20 ...XX.70

            No need to specify the cooling rate for the zerofield
            But users need to make sure that there are no duplicate meaurements in the file

        NLT:
            non-linear-TRM experiment



    """

    #
    # initialize variables
    #
    bed_dip, bed_dip_dir = "", ""
    sclass, lithology, _type = "", "", ""
    DecCorr = 0.
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # format and fix variables
    specnum = int(specnum)
    specnum = -specnum
    input_dir_path, dir_path = pmag.fix_directories(input_dir, dir_path)

    if samp_con:
        samp_con=str(samp_con)
        Z = 1
        if "4" in samp_con:
            if "-" not in samp_con:
                print("option [4] must be in form 4-Z where Z is an integer")
                return False, "option [4] must be in form 4-Z where Z is an integer"
            else:
                Z = samp_con.split("-")[1]
                samp_con = "4"
        if "7" in samp_con:
            if "-" not in samp_con:
                print("option [7] must be in form 7-Z where Z is an integer")
                return False, "option [7] must be in form 7-Z where Z is an integer"
            else:
                Z = samp_con.split("-")[1]
                samp_con = "7"
        if "6" in samp_con:
            print('Naming convention option [6] not currently supported')
            return False, 'Naming convention option [6] not currently supported'
    if not mag_file:
        print("mag file is required input")
        return False, "mag file is required input"
    output_dir_path = dir_path
    mag_file_path = pmag.resolve_file_name(mag_file, input_dir_path)

    samplist = []
    try:
        SampRecs, file_type = pmag.magic_read(samp_file)
    except:
        SampRecs = []
    MeasRecs, SpecRecs, SiteRecs, LocRecs = [], [], [], []
    try: # get the metadata line
        f = open(mag_file_path, 'r')
        lines = f.readlines()
        f.close()
    except Exception as ex:
        print('ex', ex)
        print("bad mag file")
        return False, "bad mag file"
    firstline, date,firststep = 1, "",1
    rec = lines[0].split(' ')
        # skip nearly empty lines
        rec_not_null = [i for i in rec if i]
        if len(rec_not_null) < 5:
            continue
        LPcode=""
        if firstline == 1:
            firstline = 0
            spec, vol = "", 1
            el = 51
            #while line[el:el+1] != "\\":
            #    spec = spec+line[el]
            #    el += 1
            spec = rec[7]
            # check for bad sample name
            test = spec.split('.')
            date = ""
            if len(test) > 1:
                spec = test[0]
                kk = 24
                while line[kk] != '\\x01' and line[kk] != '\\x00':
                    kk += 1
                vcc = line[24:kk]
                el = 10
                while rec[el].strip() != '':
                    el += 1
                date, comments = rec[el+7], []
            else:
                el = 9
                while rec[el] != '\\x01':
                    el += 1
                vcc, date, comments = rec[el-3], rec[el+7], []
            if specname:
                specname=mag_file.split('.')[0]
            else:
                specname = spec.lower()
            print('importing ', specname)
            el += 8
            while rec[el].isdigit() == False:
                comments.append(rec[el])
                el += 1
            if rec[el].isdigit(): 
                deccorr=float(rec[el])
                el+=1
            else:
                deccorr=0
            while rec[el] == "":
                print (el, repr(rec[el]))
                el += 1
            az = float(rec[el])
            el += 1
            while rec[el] == "":
                el += 1
            pl = float(rec[el])
            el += 1
            while rec[el] == "":
                el += 1
            bed_dip_dir = float(rec[el])
            el += 1
            while rec[el] == "":
                el += 1
            bed_dip = float(rec[el])
            el += 1
            while rec[el] == "":
                el += 1
            if rec[el] == '\\x01':
                bed_dip = 180.-bed_dip
                el += 1
                while rec[el] == "":
                    el += 1
            fold_az = float(rec[el])
            el += 1
            while rec[el] == "":
                el += 1
            fold_pl = rec[el]
            el += 1
            while rec[el] == "":
                el += 1
            #if rec[el] != "" and rec[el] != '\\x02' and rec[el] != '\\x01':
            #if deccorr!=0:
               # #deccorr = float(rec[el])
               # az += deccorr
               # if bed_dip!=0:bed_dip_dir += deccorr
               # fold_az += deccorr
               # if bed_dip_dir >= 360:
               #     bed_dip_dir = bed_dip_dir-360.
               # if az >= 360.:
               #     az = az-360.
               # if fold_az >= 360.:
               #     fold_az = fold_az-360.
            #else:
            #    deccorr = 0
            if specnum != 0:
                sample = specname[:specnum]
            else:
                sample = specname
            methods = gmeths.split(':')
            if deccorr != "0":
                if 'SO-MAG' in methods:
                    del methods[methods.index('SO-MAG')]
                methods.append('SO-CMD-NORTH')
            meths = reduce(lambda x, y: x+':'+y, methods)
            method_codes = meths
            # parse out the site name
            if samp_con=='8':
                sss = pmag.parse_site(specname, samp_con, Z)
                sample=sss[1]
                site=sss[2]
            else: 
                site = pmag.parse_site(sample, samp_con, Z)
            SpecRec, SampRec, SiteRec, LocRec = {}, {}, {}, {}
            SpecRec["specimen"] = specname
            SpecRec["sample"] = sample
            if vcc.strip() != "":
                vol = float(vcc)*1e-6  # convert to m^3 from cc
            SpecRec["volume"] = '%10.3e' % (vol)
            SpecRec["geologic_classes"] = sclass
            SpecRec["lithologies"] = lithology
            SpecRec["geologic_types"] = _type
            SpecRec["citations"] = "This study"
            SpecRec["method_codes"] = ""
            SpecRecs.append(SpecRec)

            if sample != "" and sample not in [x['sample'] if 'sample' in list(x.keys()) else "" for x in SampRecs]:
                SampRec["sample"] = sample
                SampRec["site"] = site
                # convert to labaz, labpl
                labaz, labdip = pmag.orient(az, pl, or_con)
                SampRec["bed_dip"] = '%7.1f' % (bed_dip)
                SampRec["bed_dip_direction"] = '%7.1f' % (bed_dip_dir)
                SampRec["dip"] = '%7.1f' % (labdip)
                SampRec["azimuth"] = '%7.1f' % (labaz)
                SampRec["azimuth_dec_correction"] = '%7.1f' % (deccorr)
                SampRec["geologic_classes"] = sclass
                SampRec["lithologies"] = lithology
                SampRec["geologic_types"] = _type
                SampRec["method_codes"] = method_codes
                SampRec["citations"] = "This study"
                SampRecs.append(SampRec)
            if site != "" and site not in [x['site'] if 'site' in list(x.keys()) else "" for x in SiteRecs]:
                SiteRec['site'] = site
                SiteRec['location'] = location
                SiteRec['lat'] = lat
                SiteRec['lon'] = lon
                SiteRec["geologic_classes"] = sclass
                SiteRec["lithologies"] = lithology
                SiteRec["geologic_types"] = _type
                SiteRec["age"] ="" 
                SiteRec["age_low"] ="" 
                SiteRec["age_high"] ="" 
                SiteRec["age_unit"] ="" 
                SiteRec["method_codes"] ="" 
                SiteRec["citations"] ="This study" 
                SiteRecs.append(SiteRec)

            if location != "" and location not in [x['location'] if 'location' in list(x.keys()) else "" for x in LocRecs]:
                LocRec['location'] = location
                LocRec['lat_n'] = lat
                LocRec['lon_e'] = lon
                LocRec['lat_s'] = lat
                LocRec['lon_w'] = lon
                LocRec["geologic_classes"]=sclass
                LocRec["lithologies"]=lithology
                LocRec["age"]=""
                LocRec["age_high"]=""
                LocRec["age_low"]=""
                LocRec["age_unit"]=""
                LocRec["citations"]="This study"
                LocRec["method_codes"]=""
                LocRec["location_type"]=""
                LocRecs.append(LocRec)

        else:
            rec_no_spaces=[]
            for k in range(len(rec)):
                if rec[k]!="":
                    rec_no_spaces.append(rec[k])
            if firststep:               
                input_df=pd.DataFrame([rec_no_spaces])
                firststep=0
            else:
                tmp_df=pd.DataFrame([rec_no_spaces])
                input_df=pd.concat([input_df,tmp_df])
    columns=['treat_temp','treat_ac_field','treat_dc_field','treat_dc_field_phi',
             'treat_dc_field_theta','method_codes','treat_type','aniso_type']
    meas_df=pd.DataFrame()
    treat_df=pd.DataFrame(columns=columns)

    meas_df['treat_step_num']=range(len(input_df))
    meas_df['specimen']=specname
    meas_df['quality']='g'
    meas_df['standard']='u'

    treatments=input_df[0].to_list()

    for t in treatments:
        this_treat_df=pd.DataFrame(columns=columns)
        this_treat_df['method_codes']=['LT-NO']
        this_treat_df['treat_ac_field']=[0]
        this_treat_df['treat_temp']=[273]
        this_treat_df['treat_type']=0
        this_treat_df['treat_dc_field']=0
        this_treat_df['treat_dc_field_phi']=0
        this_treat_df['treat_dc_field_theta']=0
        this_treat_df['aniso_type']=""
        if 'mT' in t:        
            treat_code=t.strip('mT').split('.')
            this_treat_df['treat_ac_field']=[float(treat_code[0])*1e-3] # convert to tesla
            if len(treat_code)>1:this_treat_df['treat_type']=int(treat_code[1])
            this_treat_df['treat_temp']=[273]
            if int(treat_code[0])==0:
                this_treat_df['method_codes']=['LT-NO']
            elif labfield==0:
                this_treat_df['method_codes']=['LT-AF-Z']
            elif labfield:
                this_treat_df['method_codes']=['LT-AF-I']
                this_treat_df['treat_dc_field']=labfield*1e-3 # convert to tesla
                this_treat_df['treat_dc_field_phi']=lab_field_phi
                this_treat_df['treat_dc_field_theta']=lab_field_theta




        elif 'C' in t or t!='NRM' and float(t.split('.')[0])!=0: # assume thermal
            treat_code=t.strip('C').split('.')
            if len(treat_code)>1:this_treat_df['treat_type']=int(treat_code[1])
            this_treat_df['method_codes']=['LT-T-Z']
            this_treat_df['treat_ac_field']=0 # convert to tesla
            this_treat_df['treat_temp']=[float(treat_code[0])+273] # convert to kelvin
            if labfield:
                LPcode='LP-PI-TRM'
                if int(treat_code[1])==3:
                    this_treat_df['method_codes']=['LT-T-Z:LT-PTRM-MD']
                elif int(treat_code[1])==1: 
                    this_treat_df['method_codes']=['LT-T-I']
                    this_treat_df['treat_dc_field']=labfield*1e-3 # convert to tesla
                    this_treat_df['treat_dc_field_phi']=lab_field_phi
                    this_treat_df['treat_dc_field_theta']=lab_field_theta


                elif int(treat_code[1])==2: 
                    this_treat_df['method_codes']=['LT-T-I:LT-PTRM-I']
                    this_treat_df['treat_dc_field']=labfield*1e-3 # convert to tesla
                    this_treat_df['treat_dc_field_phi']=lab_field_phi
                    this_treat_df['treat_dc_field_theta']=lab_field_theta
            else:
                LPcode='LP-DIR-T'

        treat_df=pd.concat([treat_df,this_treat_df])
    
    treat_df['treat_step_num']=range(len(input_df))
    meths=treat_df['method_codes'].unique()
    LPcode=""
    if 'LT-AF-Z' in meths:
        if labfield:
            LPcode='LP-PI-ARM'
            treat_df['aniso_type']='AARM'
        else:
            LPcode='LP-DIR-AF'
    elif 'LT-T-Z' in meths:
        if labfield:
            LPcode='LP-PI-TRM'
        else:
            LPcode='LP-DIR-T'
        
    if experiment:
        if 'ATRM' in experiment:
            LPcode='LP-AN-TRM'
            treat_df['aniso_type']='ATRM'
        if 'AARM' in experiment:
            LPcode='LP-AN-AARM'
        if experiment == 'CR':
            if command_line:
                cooling_times = sys.argv[ind+1]
                cooling_times_list = cooling_times.split(',')
            noave = True
            
    meas_df=pd.merge(meas_df,treat_df,on='treat_step_num')
    meas_df['dir_dec']=input_df[1].values # specimen coordinates
    meas_df['dir_inc']=input_df[2].values
    meas_df['magn_moment']=input_df[7].astype('float').values*1e-3 # moment in Am^2 (from emu)
    meas_df['magn_volume']=input_df[8].astype('float').values*1e-3/vol # moment in A/m (from emu)
    meas_df['magn_x_sigma']=input_df[9].astype('float').values*1e-3 # moment in Am^2 (from emu)
    meas_df['magn_y_sigma']=input_df[10].astype('float').values*1e-3 # moment in Am^2 (from emu)
    meas_df['magn_z_sigma']=input_df[11].astype('float').values*1e-3 # moment in Am^2 (from emu
    meas_df['meas_n_orient']=input_df[19].values
    meas_df['citations']='This study'
    meas_df['analysts']=user
    meas_df['instrument_codes']=inst
    meas_df['method_codes']=meas_df['method_codes']+':'+LPcode
    meas_df['measurement']=meas_df['treat_step_num'].astype('str')
    meas_df['experiment']=specname+'_'+LPcode
    meas_df.drop(columns=['treat_type'],inplace=True)
    meas_df.fillna("",inplace=True)
    meas_dicts = meas_df.to_dict('records')                                              
    pmag.magic_write(output_dir_path+'/'+meas_file, meas_dicts, 'measurements')

# save to files
    con = cb.Contribution(output_dir_path, read_tables=[])

    con.add_magic_table_from_data(dtype='specimens', data=SpecRecs)
    con.add_magic_table_from_data(dtype='samples', data=SampRecs)
    con.add_magic_table_from_data(dtype='sites', data=SiteRecs)
    con.add_magic_table_from_data(dtype='locations', data=LocRecs)
    #MeasOuts = pmag.measurements_methods3(meas_dicts, noave,savelast=False)
    #con.add_magic_table_from_data(dtype='measurements', data=MeasOuts)
    con.write_table_to_file('specimens', custom_name=spec_file)
    con.write_table_to_file('samples', custom_name=samp_file)
    con.write_table_to_file('sites', custom_name=site_file)
    con.write_table_to_file('locations', custom_name=loc_file)
    #con.write_table_to_file('measurements', custom_name=meas_file)
    return True, meas_file
