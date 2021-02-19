"""Stephan 2020 ROIs module."""

from pathlib import Path
import re

import numpy as np

from .rois import ROIsCollectionWithCategories


DATA = Path(__file__).parent / 'data'

KEY = re.compile(r'\d+_\d+_\d+')


class Stephan2020ROIsCollection(ROIsCollectionWithCategories):
    """Abstract ROIs collection from K. Stephan et al. 2020 - PSS.

    Parameters
    ----------
    csv: str or pathlib.Path
        ROIs CSV file name.
    prefix: str, optional
        ROI key prefix.

    Source
    ------
    K. Stephan et al., PSS (2020) [under review]

    """

    def __init__(self, *args, csv=None, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

        if csv is None:
            raise AttributeError('Missing `csv` attribute')

        self.csv = Path(csv)

        if not self.csv.exists():
            raise FileNotFoundError(self.csv)

        self.prefix = prefix

        self.load_csv()

    def __contains__(self, key):
        return super().__contains__(self.key(key))

    def __getitem__(self, key):
        return super().__getitem__(self.key(key))

    def key(self, cat, subcat=None, roi=None) -> str:
        """ROI key pattern formatter.

        Pattern:
            - ``C`` for category.
            - ``C.S`` for sub-category.
            - ``PREFIX_C_S_RR`` for a full ROI description.

        with:
            - `C` the category.
            - `S` the sub-category.
            - `R` the ROI id.
            - `PREFIX` the ROI prefix.

        Parameters
        ----------
        cat: int or str
            Main category.
        subcat: int or str, optional
            Sub-category. If `0` the sub-category will be omitted.
        roi: int or str, optional
            The ROI id.

        Returns
        -------
        str
            Formatted key.

        """
        if isinstance(cat, tuple):
            return self.key(*cat)

        if hasattr(cat, 'lonlat'):
            return cat

        if str(cat).startswith('# '):
            cat = cat[2:]

        if subcat in (0, '0'):
            subcat = None

        if str(roi).startswith('#'):
            roi = None

        if subcat is None and roi is None:
            if KEY.fullmatch(str(cat)):
                return f'{self.prefix}{cat}'

            return str(cat)

        if roi is None:
            return f'{cat}.{subcat}'

        if subcat is None:
            subcat = 0

        return f'{self.prefix}{cat}_{subcat}_{int(roi):02d}'

    def load_csv(self):  # pylint: disable=too-many-locals
        """Load ROIs from a CSV file."""
        lines = self.csv.read_text(encoding='utf-8').splitlines()

        for line in lines[1:]:
            cat, subcat, roi, name, _, _, _, \
                min_lat, max_lat, min_lon_e, max_lon_e, \
                desc, sc_rat, sp_req = (val.strip() for val in line.split(','))

            key = self.key(cat=cat, subcat=subcat, roi=roi)

            attrs = {
                'name': name,
                'description': desc,
                'science_rationale': sc_rat,
                'special_requirements': sp_req,
            }

            if cat.startswith('#'):
                if subcat == '0':
                    self.add_category(key, **attrs, color=roi)
                else:
                    self.add_subcategory(key, **attrs, category=cat[2:], color=roi)

            else:
                if subcat == '0':
                    category = self.categories[self.key(cat=cat)]
                    cat_attrs = {
                        'category': category,
                        'color': category.color,
                    }
                else:
                    subcategory = self.subcategories[self.key(cat=cat, subcat=subcat)]
                    cat_attrs = {
                        'category': subcategory.category,
                        'subcategory': subcategory,
                        'color': subcategory.category.color,
                    }

                lons_e = np.array([min_lon_e, max_lon_e, max_lon_e, min_lon_e],
                                  dtype=float)
                lats = np.array([min_lat, min_lat, max_lat, max_lat], dtype=float)

                self.add_roi(key, lons_e, lats, **attrs, **cat_attrs)


# Ganymede ROIs from K. Stephan et al., PSS (2020) [under review] - Tab. 2.
GanymedeROIs = Stephan2020ROIsCollection(
    csv=DATA / 'Ganymede_ROIs-Stephan_2020_PSS-Tab_2.csv',
    prefix='JUICE_ROI_GAN_',
)

# Callisto ROIs from K. Stephan et al., PSS (2020) [under review] - Tab. 3.
CallistoROIs = Stephan2020ROIsCollection(
    csv=DATA / 'Callisto_ROIs-Stephan_2020_PSS-Tab_3.csv',
    prefix='JUICE_ROI_CAL_',
)
