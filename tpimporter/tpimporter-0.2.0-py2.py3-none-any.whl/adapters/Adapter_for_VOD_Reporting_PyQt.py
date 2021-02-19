from .Basic_Adapter import Basic_Adapter


class Adapter_For_VOD_Reporting_PyQt(Basic_Adapter):
    """
    a class used to alter the keys from the TP import so that the data can be used within MAM
    """
    transformer_dict = {
        "Tnr": "tnr",
        "Titelname": "titel_local",
        "Lizenzgeber": "lg",
        "ESTStart": "est_start",
        "TVODStart": "tvod_start",
        "VendorID": "vendor_id_itunes",
        "VendorIDAmazon": "vendor_id_amazon",
        "VendorIDGoogle": "vendor_id_google",
        "VendorIDMicrosoft": "vendor_id_microsoft",
        "VendorIDVideoload": "vendor_id_videoload",
        "VendorIDSony": "vendor_id_sony",
        "DE": "country_de",
        "AT": "country_at",
        "CH": "country_ch",
        "Kinostart": "theatrical_start",
        "Studio": "studio",
        "InitialPriceHD": "pricing_initial_hd_de",
        "InitialPriceSD": "pricing_initial_sd_de",
        "Prod_jahr": "production_year",
        "Prod_land": "production_country",
        "Genre": "genre",
        "Admissions": "theatrical_admissions",
        "Deal": "deal_type",
        "FSK": "rating",
    }
