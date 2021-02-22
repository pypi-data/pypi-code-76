from oa_data_package.hellofresh_data.google_drive_tools import GoogleDrive


if __name__ == '__main__':
    g_obj = GoogleDrive()
    g_obj.get_folder_metadata(['1t6kDx-lovKh-uWD85BzpfXpxrnjvDjMF', '1aSZJSuKw2HBiIXj2JD90rXrq_mUWQIw1'],
                              '2021-01-01T00:00:00')