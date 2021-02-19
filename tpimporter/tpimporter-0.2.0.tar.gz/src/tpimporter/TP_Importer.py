from .Excel_Importer import Excel_Importer
from openpyxl import Workbook
from typing import List, Dict



class TP_Importer(Excel_Importer):
    callback_status_signal = None
    callback_progress_signal = None
    tp_map = {
        "status": 0,
        "did": 1,
        "tnr": 2,
        "titel_local": 3,
        "titel_ov": 6,
        "lg": 7,
        "deal_type": 9,
        "info_link": 11,
        "mandant": 12,
        "trailer_link": 11,
        "vertrieb_physisch": 13,
        "release_actuality": 15,
        "release_origin": 16,
        "quality": 18,
        "production_country": 19,
        "production_year": 20,
        "genre": 21,
        "theatrical_start": 22,
        "theatrical_admissions": 23,
        "runtime": 24,
        "rating": 25,
        "language_local": 26,
        "language_ov": 27,
        "dvd_start": 29,
        "est_start": 46,
        "est_start_4k": 181,
        "est_end": 48,
        "tvod_start": 50,
        "tvod_start_4k": 182,
        "tvod_end": 51,
        "country_de": 42,
        "country_at": 43,
        "country_ch": 44,
        "country_lux": 59,
        "country_lie": 60,
        "right_est": 45,
        "right_tvod": 49,
        "right_svod": 52,
        "right_avod": 55,
        "premium_vod_start": 64,
        "premium_vod_end": 65,
        "premium_vod_price_tier": 66,
        "holdback_est_start": 67,
        "holdback_est_end": 68,
        "holdback_tvod_start": 69,
        "holdback_tvod_end": 70,
        "change_reason": 79,
        "pf_status_itunes": 81,
        "pf_status_amazon": 105,
        "pf_status_google": 97,
        "pf_status_microsoft": 88,
        "pf_status_videoload": 84,
        "pf_status_sony": 86,
        "pf_status_ondemand": 99,
        "studio": 108,
        "vendor_id": 118,
        "vendor_id_itunes": 120,
        "vendor_id_google": 133,
        "vendor_id_amazon": 151,
        "vendor_id_microsoft": 129,
        "vendor_id_sky": 130,
        "vendor_id_sony": 131,
        "vendor_id_vodafone": 134,
        "vendor_id_maxdome": 135,
        "vendor_id_ondemand": 136,
        "vendor_id_videoload": 146,
        "vendor_id_wuaki": 147,
        "vendor_id_hollystar": 148,
        "vendor_id_chili": 149,
        "vendor_id_videociety": 116,
        "vendor_id_videobuster": 115,
        "vendor_id_teleclub": 114,
        "vendor_id_cablecom": 113,
        "vendor_id_magenta_at": 112,
        "vendor_id_unitymedia": 111,
        "ov": 144,
        "full_delete": 139,
        "full_delete_4k_amazon": 140,
        "full_delete_poest": 141,
        "isan": 170,
        "imdb_link": 175,
        "eidr": 176,
        "pricing_initial_4k_de": 179,
        "pricing_initial_4k_ch": 180,
        "pricing_1streprice_4k_de": 183,
        "pricing_1streprice_4k_ch": 184,
        "pricing_1streprice_4k_start": 185,
        "pricing_initial_hd_de": 190,
        "pricing_initial_sd_de": 191,
        "pricing_1streprice_start": 193,
        "pricing_1streprice_hd": 236,
        "pricing_1streprice_sd": 237,
        "wsp_initial_sd_de_amazon": 201,
        "wsp_initial_hd_de_amazon": 202,
        "wsp_1streprice_sd_de_amazon": 240,
        "wsp_1streprice_hd_de_amazon": 241,
        "wsp_special_amazon_start": 310,
        "wsp_special_amazon_end": 311,
        "wsp_special_amazon_est_sd": 312,
        "wsp_special_amazon_est_hd": 313,
        "wsp_special_amazon_est_4k": 314,
        "wsp_special_amazon_tvod_sd": 315,
        "wsp_special_amazon_tvod_hd": 316,
        "wsp_special_amazon_tvod_4k": 317,
        "pricetier_initial_itunes_est_sd_de": 195,
        "pricetier_initial_itunes_est_hd_de": 196,
        "pricetier_initial_itunes_est_sd_ch": 228,
        "pricetier_initial_itunes_est_hd_ch": 229,
        "pricetier_1streprice_itunes_est_sd_de": 238,
        "pricetier_1streprice_itunes_est_hd_de": 239,
        "pricetier_1streprice_itunes_est_sd_ch": 250,
        "pricetier_1streprice_itunes_est_hd_ch": 251,
        "channel_type": 0,  # wird nicht aus Excel gelesen
    }

    def __init__(self, valid_statuses=("ok", "change", "new")):
        super().__init__(valid_statuses)


    def _get_data_from_wb(self,
                          workbook: Workbook,
                          first_row: int = 8,
                          worksheet_name: str = "TP",
                          channel_type='transactional') -> List[Dict]:
        """
        fetches data from the given Excel Workbook instance
        :param workbook: a Workbook instance
        :param first_row: the first row where we should expect the data to begin
        :param worksheet_name: name of the worksheet that should be read
        :param channel_type: possible values: transactional/filmtastic/arthousecnma/homeofhorror
        :return:
        """
        tp_data = []
        ws = workbook[worksheet_name]
        i = first_row
        for row in ws['A' + str(first_row):'QF10000']:
            try:
                i += 1
                if row[self.tp_map.get('tnr')].value and row[self.tp_map.get('status')].value in self.valid_statuses:
                    row_data = dict()
                    for key, col_nr in self.tp_map.items():
                        if key == 'channel_type':
                            row_data[key] = channel_type
                        else:
                            try:
                                row_data[key] = row[col_nr].value
                            except:
                                row_data[key] = ""
                    tp_data.append(row_data)

            except:
                self.callback_status(f'ERRROR reading in row nr: {i}')
        self.callback_progress(100)
        self.callback_status('reading data from TP - COMPLETE')
        return tp_data


if __name__ == '__main__':
    tp_data = TP_Importer().get_tp_data_from_file('G:\Listen\TPDD aktuell absolutiert.xlsm')
