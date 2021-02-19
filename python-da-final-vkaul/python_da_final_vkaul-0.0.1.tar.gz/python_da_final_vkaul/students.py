# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 15:57:51 2021

@author: Vibhesh
"""

import pandas as pd

def compute_student_per_teacher_stats(filtered_school_df):
    if filtered_school_df.empty:
        raise ValueError('Dataset cannot be empty')
    '''
    We need to filter out the rows with value 0 for total teacher count in order to avoid dividing by 0
    '''

    filtered_school_df = filtered_school_df[filtered_school_df['total_teachers_per_school'] != 0]  # filter out the rows with 0 teacher count
    filtered_school_df['students_per_teacher'] = filtered_school_df['students_per_school']/filtered_school_df['total_teachers_per_school'] #calculate students per teacher for each school
    
    df_required_measures = filtered_school_df[["Nazwa typu","Gmina","Typ gminy","students_per_school","total_teachers_per_school","students_per_teacher"]].copy()

    stats_district = df_required_measures.groupby(["Gmina","Nazwa typu"]).agg(min_spt=('students_per_teacher', 'min'),max_spt=('students_per_teacher', 'max'),avg_spt=('students_per_teacher','mean'))
    stats_district = stats_district.reset_index() #students per teacher broken down by the type of school in each district (polish ‘gmina’)
    print("Students per teacher broken down by the type of school in each district (polish ‘gmina’)\n========================================================\n")
    print(stats_district.head(20))
    print("\nFull results for students per teacher broken down by the type of school in each district (gmina) can be found in 'student_per_teacher_stats_district.xlsx'")
    stats_district.to_excel('student_per_teacher_stats_district.xlsx')
    
    df_required_measures["Typ gminy"] = df_required_measures["Typ gminy"].astype(str)
    df_required_measures = df_required_measures.assign(District_type="City")
    df_required_measures.loc[df_required_measures["Typ gminy"] == "Gm", 'District_type'] = "Rural"
    stats_by_type_city_rural = df_required_measures.groupby(["District_type","Nazwa typu"]).agg(min_spt=('students_per_teacher', 'min'),max_spt=('students_per_teacher', 'max'),avg_spt=('students_per_teacher','mean'))
    stats_by_type_city_rural = stats_by_type_city_rural.reset_index() #students per teacher broken down by the type of school in for cities and rural districts
    print("students per teacher broken down by the type of school in for cities and rural districts\n========================================================\n")
    print(stats_by_type_city_rural.head(20))
    print("\n========================================================\n Full results for students per teacher broken down by the type of school in for cities and rural districts can be found in 'student_per_teacher_stats_district_type.xlsx'")
    stats_by_type_city_rural.to_excel('student_per_teacher_stats_district_type.xlsx')
    
    stats_in_total_city_rural = df_required_measures.groupby(["District_type"]).agg(min_spt=('students_per_teacher', 'min'),max_spt=('students_per_teacher', 'max'),avg_spt=('students_per_teacher','mean'))
    stats_in_total_city_rural = stats_in_total_city_rural.reset_index()
    print("students per teacher in total for cities and rural districts\n========================================================\n")
    print(stats_in_total_city_rural)
    return stats_in_total_city_rural
    
    

    
def compute_student_per_school_stats(filtered_school_df,districts_info_df):
    if filtered_school_df.empty or districts_info_df.empty:
        raise ValueError('Datasets cannot be empty')
   
    filtered_school_df = filtered_school_df[['Nazwa szkoły, placówki','Województwo','Gmina','students_per_school','Typ gminy']]

    df_merged = pd.merge(filtered_school_df, districts_info_df,  how='left', left_on=['Województwo','Gmina'], right_on = ['Województwo','Gmina'])
    stat_cols = df_merged.filter(like='20').columns.values
    df_merged[stat_cols] = (df_merged[stat_cols].multiply(df_merged["students_per_school"], axis="index"))/100
    print("Students per school broken down by the birth year in each district (polish ‘gmina’)\n========================================================\n")
    print(df_merged.head(20))
    df_merged.to_excel('school_student_birthYear.xlsx')
    print("\n========================================================\n Full results for students per school broken down by the birth year in each district (polish ‘gmina’) can be found in 'school_student_birthYear.xlsx'")
    df_merged = df_merged.assign(District_type="City")
    df_merged.loc[df_merged["Typ gminy"] == "Gm", 'District_type'] = "Rural"
    stats_in_total_city_rural = df_merged.groupby(["District_type"]).agg(group_count=('District_type', 'count'),
                                                                         tot_stu=('students_per_school', 'sum'))
    stats_in_total_city_rural = stats_in_total_city_rural.reset_index()
    students_per_school_district_type = pd.DataFrame(stats_in_total_city_rural.loc[:, 'District_type'].copy())
    students_per_school_district_type['students_per_school'] = stats_in_total_city_rural['tot_stu'] /stats_in_total_city_rural['group_count']
    print("students per school in total for cities and rural districts\n========================================================\n")
    print(students_per_school_district_type)
    return students_per_school_district_type