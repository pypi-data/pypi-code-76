from library_dicom.dicom_processor.model.csv_reader.CsvReader import CsvReader


def get_sum_rois_volume(liste):
    """sum all ROIs volume

    Args:
        liste ([list]): [List of every ROI volume]

    Returns:
        [float]: [Return the sum of ROIs volume]
    """
    volume = float(0)
    for i in range(len(liste)):
        volume += float(liste[i][3])

    return volume


def get_difference_volume(csv_path) :
    """Calcul the difference between volume and sum of every ROI volume

    Args:
        csv_path ([str]): [CSV path]

    Returns:
        [float, float, float]: [Return volume, sum of every ROIs volume and difference between the 2]
    """
    csv_objet = CsvReader(csv_path)
    total_volume = float(csv_objet.get_sum_row()[3])

    liste = csv_objet.get_rois_results()

    sum_volume = get_sum_rois_volume(liste)
    return total_volume, sum_volume, abs(sum_volume - total_volume)


