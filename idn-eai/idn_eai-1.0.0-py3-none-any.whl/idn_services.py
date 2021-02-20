#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Arpit Gupta
Created-Date : 27-April-2020
Modified-Date : 27-April-2020
Description : This module contains core IDN services :
1. Generate Blocked Variants
2. Generate Coallocatable Variants
"""

import itertools


class IDNService:

    @staticmethod
    def generate_homograph_variants(word):
        """
        # GENERATE BLOCKED VARIANTS
        :param word: valid word
        :return: string of multiple blocked variants
        """
        devanagari_variants = [['ऱ्य', '-य'], ['ऱ्ह', '-ह'], ['द्ग', 'द्र', 'द्न'], ['द्ध', 'द्घ'], ['ष्ट', 'ष्ठ'],
                               ['श्व', 'श्र्व'], ['श्न', 'श्र्न'], ['श्च', 'श्र्च'], ['श्ल', 'श्र्ल'], ['त्त', 'त'],
                               ['ँ', 'ॅं'], ['द्व', 'द्ब']]

        for i in range(len(devanagari_variants)):
            devanagari_variants[i] = sorted(devanagari_variants[i], key=len, reverse=True)

        to_process_list = [word]

        for current_variants in devanagari_variants:

            new_process_list = []
            for word in to_process_list:
                temp_word = word
                count = 0
                for pos_var in current_variants:
                    while pos_var in temp_word:
                        temp_word = temp_word.replace(pos_var, "{" + str(count) + "}", 1)
                        count += 1
                all_params = [current_variants for i in range(count)]
                total_permutations = itertools.product(*all_params)
                for i in total_permutations:
                    new_process_list.append(temp_word.format(*i))
            to_process_list = new_process_list

        return ",".join(to_process_list)

    @staticmethod
    def generate_similar_phonic_variants(word):
        """
        # GENERATE COALLOCATABLE VARIANTS
        :param word:valid word
        :return: string of multiple coallocatable variants
        """
        devanagari_variants = [['ि', 'ी'], ['ु', 'ू'], ['ृ', 'ॄ'], ['ॲं', 'अँ'], ['ऑं', 'आँ'], ['इ', 'ई'], ['उ', 'ऊ'],
                               ['ऋ', 'ॠ']]

        for i in range(len(devanagari_variants)):
            devanagari_variants[i] = sorted(devanagari_variants[i], key=len, reverse=True)

        to_process_list = [word]

        for current_variants in devanagari_variants:

            new_process_list = []
            for word in to_process_list:
                temp_word = word
                count = 0
                for pos_var in current_variants:
                    while pos_var in temp_word:
                        temp_word = temp_word.replace(pos_var, "{" + str(count) + "}", 1)
                        count += 1

                all_params = [current_variants for i in range(count)]
                total_permutations = itertools.product(*all_params)
                for i in total_permutations:
                    new_process_list.append(temp_word.format(*i))
            to_process_list = new_process_list

        return ",".join(to_process_list)
