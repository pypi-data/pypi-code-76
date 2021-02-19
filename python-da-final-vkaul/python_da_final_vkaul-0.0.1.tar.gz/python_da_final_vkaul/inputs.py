# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 14:43:23 2021

@author: Vibesh
"""
import os
import pandas as pd

def read_data_excel(path):
    df_file = pd.read_excel(path)
    return df_file


def get_schools_dataset(path):
    school_data = read_data_excel(path)
    school_data['total_teachers_per_school'] = school_data['Nauczyciele pełnozatrudnieni'] + school_data[
        'Nauczyciele niepełnozatrudnieni (stos.pracy)']
    school_data['students_per_school'] = pd.to_numeric(school_data['Uczniowie, wychow., słuchacze'], errors='coerce')
    school_data = school_data.drop(0)

    """
    Data Inconsistency:
    Inconsistencies in data were found. Missing values for number of students and teachers were observed in some records. 
    In order to perform the analysis and be able to carry out correct statistical measures, it is required that the data is cleaned up.
    We decide to drop the records with missing values for students count.
    
    """
    # Preprocess data
    filtered_school_df = school_data.copy()
    filtered_school_df = filtered_school_df[
        filtered_school_df['students_per_school'] != 0]  # filter out the rows with 0 student count

    """
    Data Inconsistency:
    Some values in 'Gmina' and 'Województwo' colums have prefixes (M., st., WOJ.) that need to be removed in order
    to have consistent data to perform calculations
    
    """
    # Preprocess the data
    filtered_school_df['Gmina'] = filtered_school_df['Gmina'].str.replace('M. ', '', regex=False)
    filtered_school_df['Gmina'] = filtered_school_df['Gmina'].str.replace('st. ', '', regex=False)
    filtered_school_df['Województwo'] = filtered_school_df['Województwo'].str.replace('WOJ. ', '', regex=False)
    filtered_school_df['Województwo'] = filtered_school_df['Województwo'].str.lower()
    filtered_school_df['Gmina'] = filtered_school_df['Gmina'].str.lower()
    filtered_school_df = filtered_school_df.reset_index(drop=True)

    return filtered_school_df


def get_districts_dataset(path):
    xl = pd.ExcelFile(path)

    """
    Data Inconsistency:
    Data for each Województwo in different sheets of the excel file. 
    Gmina(districts) apeear twice, for Rural and Urban respectively
    In order to have consistent data required for calculations, it's preprocessed
    
    """
    # Preprocess the data
    lst_rows = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        df = (df.loc[7:]).copy()
        df = df.iloc[:, 0:3]
        df.columns = ['age', 'code', 'population']
        df['code'] = pd.to_numeric(df['code'], errors='coerce')
        districts = df[df['code'].notna()]
        districts_rows = districts.index.values
        for i in districts_rows:
            row = df.loc[i, :]
            df_temp = df.loc[i:i + 40, :]
            age_pop = df_temp[['age', 'population']].copy()
            age_pop['age'] = pd.to_numeric(age_pop['age'], errors='coerce')
            age_pop['population'] = pd.to_numeric(age_pop['population'], errors='coerce')
            age_pop = age_pop.dropna()
            age_pop = age_pop[age_pop['age'].between(2, 25, inclusive=False)]
            total_stud_pop = age_pop['population'].sum()
            age_percent = (age_pop['population'] / total_stud_pop) * 100
            lst_rows.append([sheet, row['age']] + age_percent.to_list())
    inhabitants_data_year = 2020
    df_dist_data = pd.DataFrame(lst_rows, columns=['Województwo', 'Gmina'] + list(
        map(str, range(inhabitants_data_year - 3, inhabitants_data_year - 25, -1))))
    df_dist_data['Województwo'] = df_dist_data['Województwo'].str.lower()
    df_dist_data['Gmina'] = df_dist_data['Gmina'].str.lower()
    df_dist_data = df_dist_data.groupby(['Województwo', 'Gmina']).mean().reset_index()

    return df_dist_data
