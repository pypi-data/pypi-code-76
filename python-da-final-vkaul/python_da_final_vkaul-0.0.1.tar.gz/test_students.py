# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:47:38 2021

@author: Vibesh
"""
import unittest
import pandas as pd
import python_da_final_vk.inputs as ip
import python_da_final_vk.students as stu

class InputDFTests(unittest.TestCase):

    df_school = pd.DataFrame()
    df_districts = pd.DataFrame()

    def test_student_dataSet(self):
        self.df_school = ip.get_schools_dataset('schoolsData.xlsx')
        trueVal = not (self.df_school.empty)
        self.assertTrue(trueVal, "Empty student's dataset")

    def test_district_dataSet(self):
        self.df_districts = ip.get_districts_dataset('tabela12.xls')
        trueVal = not(self.df_districts.empty)
        self.assertTrue(trueVal, "Empty district dataset")

    def test_student_per_teacher_calc(self):
        self.df_school = ip.get_schools_dataset('schoolsData.xlsx')
        df = stu.compute_student_per_teacher_stats(self.df_school)
        stat_city = int(8.909394)
        stat_rural = int(7.346803)
        trueVal = (not df.empty) or (int(df.loc[0, "avg_spt"] == stat_city) and (int(df.loc[1, "avg_spt"] == stat_rural)))
        self.assertTrue(trueVal, "Empty student's dataset")

    def test_student_per_school_calc(self):
        self.df_school = ip.get_schools_dataset('schoolsData.xlsx')
        self.df_districts = ip.get_districts_dataset('tabela12.xls')
        df = stu.compute_student_per_school_stats(self.df_school, self.df_districts)
        stat_city = int(165.986556)
        stat_rural = int(121.378355)
        trueVal = (not df.empty) or (int(df.loc[0, "students_per_school"] == stat_city) and (int(df.loc[1, "students_per_school"] == stat_rural)))
        self.assertTrue(trueVal, "Empty district dataset")
        

