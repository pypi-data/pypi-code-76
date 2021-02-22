        if len(atrm_df) > 5: 
            atrm_df=meas_df[meas_df['method_codes'].str.contains('LT-T-I')]
            atrm_df['original_order']=range(len(atrm_df))
            atrm_df['order']=np.nan
            atrm_df['treat_dc_field_phi']=atrm_df['treat_dc_field_phi'].astype('float')
            atrm_df['treat_dc_field_theta']=atrm_df['treat_dc_field_theta'].astype('float')
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==0) & (atrm_df['treat_dc_field_theta']==0),'order']=0
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==90) & (atrm_df['treat_dc_field_theta']==0),'order']=1
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==0) & (atrm_df['treat_dc_field_theta']==90),'order']=2
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==180) & (atrm_df['treat_dc_field_theta']==0),'order']=3
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==270) & (atrm_df['treat_dc_field_theta']==0),'order']=4
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==0) & (atrm_df['treat_dc_field_theta']==-90),'order']=5
            atrm_df.loc[(atrm_df['treat_dc_field_phi']==90) & (atrm_df['treat_dc_field_theta']==0),'order']=1
            atrm_df.sort_values(by=['order'],inplace=True)    
            if np.array_equal(atrm_df['order'].values[0:6],np.arange(6)):
                atrm_dirs=atrm_df[['dir_dec','dir_inc','magn_moment']].astype('float').values
                M=pmag.dir2cart(atrm_dirs)
                K = np.zeros(3 * n_pos, 'f')
                for i in range(n_pos):
                    K[i * 3] = M[i][0]
                    K[i * 3 + 1] = M[i][1]
                    K[i * 3 + 2] = M[i][2]
                aniso_parameters=calculate_atrm_parameters(K)
                aniso_alt=0
                alt_check_df=meas_df[meas_df['method_codes'].str.contains('LT-PTRM-I')]
                if len(alt_check_df)>0:
                    anis_alt_phi=alt_check_df['treat_dc_field_phi'].astype('float').values[-1]
                    anis_alt_theta=alt_check_df['treat_dc_field_theta'].astype('float').values[-1]
                    base1=atrm_df[atrm_df['treat_dc_field_phi'].astype('float')==anis_alt_phi]
                    base1=base1[base1['treat_dc_field_theta']==anis_alt_theta]
                    if len(base1)>0:
                        base1_M=base1[['magn_moment']].astype('float').values[0]
                        base2_M=alt_check_df[['magn_moment']].astype('float').values[0]
                        aniso_alt=100*np.abs(base1_M-base2_M)/np.mean([base1_M,base2_M]) # anisotropy alteration percent
                new_spec_df=pd.DataFrame.from_dict([aniso_parameters])
                new_spec_df['specimen']=spec
                new_spec_df['citations']='This study'
                new_spec_df['method_codes']='LP-AN-TRM' 
                new_spec_df['aniso_alt']='%5.2f'%(aniso_alt)
                new_spec_df['software_packages']=pmag.get_version()
                new_spec_df['citations']='This study'
                if old_specs and 'aniso_s' in old_spec_df.columns and old_spec_df.loc[(old_spec_df['specimen']==spec)&
                    (old_spec_df['aniso_type']=='ATRM')].empty==False: # there is a previous record of ATRM for this specimen
                        print ('replacing existing ATRM data for ',spec)
                        for col in ['aniso_alt','aniso_ftest','aniso_ftest12','aniso_ftest23','aniso_p','aniso_s','aniso_s_n_measurements','aniso_s_sigma','aniso_type','aniso_v1','aniso_v2','aniso_v3','aniso_ftest_quality','aniso_tilt_correction','description','software_packages','citations']:
                            old_spec_df.loc[(old_spec_df['specimen']==spec)&(old_spec_df['aniso_type']=='ATRM')&
                                (old_spec_df[col].notnull()),col]=new_spec_df[col].values[0] # replace existing ATRM data for this specimen
                elif old_specs and 'aniso_s' in old_spec_df.columns and old_spec_df.loc[old_spec_df['specimen']==spec].empty==False: # there is a no previous record of ATRM for this specimen
                    print ('adding ATRM data for ',spec)
                    for col in ['aniso_alt','aniso_ftest','aniso_ftest12','aniso_ftest23','aniso_p','aniso_s','aniso_s_n_measurements','aniso_s_sigma','aniso_type','aniso_v1','aniso_v2','aniso_v3','aniso_ftest_quality','aniso_tilt_correction','description','software_packages','citations']:
                        old_spec_df.loc[old_spec_df['specimen']==spec,col]=new_spec_df[col].values[0] # add ATRM data for this specimen
                else: # no record of this specimen, just append to the end of the existing data frame
                    print ('creating new record for specimen ',spec)
                    old_spec_df=pd.concat([old_spec_df,new_spec_df]) # add in new record      
            else:
                print ('something wrong with measurements for: ',spec)
    old_spec_df.fillna("",inplace=True)
    spec_dicts=old_spec_df.to_dict('records')
    pmag.magic_write(output_spec_file,spec_dicts,'specimens')
