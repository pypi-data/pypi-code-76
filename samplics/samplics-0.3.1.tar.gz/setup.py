# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samplics',
 'samplics.categorical',
 'samplics.estimation',
 'samplics.sae',
 'samplics.sampling',
 'samplics.utils',
 'samplics.weighting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=1.0,<2.0',
 'scipy>=1.1,<2.0',
 'statsmodels>=0.10,<0.11']

setup_kwargs = {
    'name': 'samplics',
    'version': '0.3.1',
    'description': 'Select, weight and analyze complex sample data',
    'long_description': '<img src="./img/samplics_logo3.png" width="150" height="110" align="left" />\n\n# _Sample Analytics_\n\n[<img src="https://github.com/survey-methods/samplics/workflows/Testing/badge.svg">](https://github.com/survey-methods/samplics/actions?query=workflow%3ATesting)\n[<img src="https://github.com/survey-methods/samplics/workflows/Coverage/badge.svg">](https://github.com/survey-methods/samplics/actions?query=workflow%3ACoverage)\n[![docs](https://readthedocs.org/projects/samplics/badge/?version=latest)](https://samplics.readthedocs.io/en/latest/?badge=latest)\n\nIn large scale surveys, often complex random mechanisms are used to select samples. Estimates derived from such samples must reflect the random mechanism. _Samplics_ is a python package that implements a set of sampling techniques for complex survey designs. These survey sampling techniques are organized into the following four subpackages.\n\n**Sampling** provides a set of random selection techniques used to draw a sample from a population. It also provides procedures for calculating sample sizes. The sampling subpackage contains:\n\n- Sample size calculation and allocation: Wald and Fleiss methods for proportions.\n- Equal probability of selection: simple random sampling (SRS) and systematic selection (SYS)\n- Probability proportional to size (PPS): Systematic, Brewer\'s method, Hanurav-Vijayan method, Murphy\'s method, and Rao-Sampford\'s method.\n\n**Weighting** provides the procedures for adjusting sample weights. More specifically, the weighting subpackage allows the following:\n\n- Weight adjustment due to nonresponse\n- Weight poststratification, calibration and normalization\n- Weight replication i.e. Bootstrap, BRR, and Jackknife\n\n**Estimation** provides methods for estimating the parameters of interest with uncertainty measures that are consistent with the sampling design. The estimation subpackage implements the following types of estimation methods:\n\n- Taylor-based, also called linearization methods\n- Replication-based estimation i.e. Boostrap, BRR, and Jackknife\n- Regression-based e.g. generalized regression (GREG)\n\n**Small https://seneweb.com/news/International/france-l-rsquo-esperance-de-vie-et-le-no_n_338526.htmlArea Estimation (SAE).** When the sample size is not large enough to produce reliable / stable domain level estimates, SAE techniques can be used to model the output variable of interest to produce domain level estimates. This subpackage provides Area-level and Unit-level SAE methods.\n\nFor more details, visit https://samplics.readthedocs.io/en/latest/\n\n## Usage\n\nLet\'s assume that we have a population and we would like to select a sample from it. The goal is to calculate the sample size for an expected proportion of 0.80 with a precision of 0.10.\n\n> ```python\n> import samplics\n> from samplics.sampling import SampleSize\n>\n> sample_size = SampleSize(parameter = "proportion")\n> sample_size.calculate(target=0.80, precision=0.10)\n> ```\n\nFurthermore, the population is located in four natural regions i.e. North, South, East, and West. We could be interested in calculating sample sizes based on region specific requirements e.g. expected proportions, desired precisions and associated design effects.\n\n> ```python\n> import samplics\n> from samplics.sampling import SampleSize\n>\n> sample_size = SampleSize(parameter="proportion", method="wald", stratification=True)\n>\n> expected_proportions = {"North": 0.95, "South": 0.70, "East": 0.30, "West": 0.50}\n> half_ci = {"North": 0.30, "South": 0.10, "East": 0.15, "West": 0.10}\n> deff = {"North": 1, "South": 1.5, "East": 2.5, "West": 2.0}\n>\n> sample_size = SampleSize(parameter = "proportion", method="Fleiss", stratification=True)\n> sample_size.calculate(target=expected_proportions, precision=half_ci, deff=deff)\n> ```\n\nTo select a sample of primary sampling units using PPS method,\nwe can use code similar to:\n\n> ```python\n> import samplics\n> from samplics.sampling import SampleSelection\n>\n> psu_frame = pd.read_csv("psu_frame.csv")\n> psu_sample_size = {"East":3, "West": 2, "North": 2, "South": 3}\n> pps_design = SampleSelection(\n>    method="pps-sys",\n>    stratification=True,\n>    with_replacement=False\n>    )\n>\n> frame["psu_prob"] = pps_design.inclusion_probs(\n>    psu_frame["cluster"],\n>    psu_sample_size,\n>    psu_frame["region"],\n>    psu_frame["number_households_census"]\n>    )\n> ```\n\nTo adjust the design sample weight for nonresponse,\nwe can use code similar to:\n\n> ```python\n> import samplics\n> from samplics.weighting import SampleWeight\n>\n> status_mapping = {\n>    "in": "ineligible",\n>    "rr": "respondent",\n>    "nr": "non-respondent",\n>    "uk":"unknown"\n>    }\n>\n> full_sample["nr_weight"] = SampleWeight().adjust(\n>    samp_weight=full_sample["design_weight"],\n>    adjust_class=full_sample["region"],\n>    resp_status=full_sample["response_status"],\n>    resp_dict=status_mapping\n>    )\n> ```\n\nTo estimate population parameters, we can use code similar to:\n\n> ```python\n> import samplics\n> from samplics.estimation import TaylorEstimation, ReplicateEstimator\n>\n> # Taylor-based\n> zinc_mean_str = TaylorEstimator("mean").estimate(\n>    y=nhanes2f["zinc"],\n>    samp_weight=nhanes2f["finalwgt"],\n>    stratum=nhanes2f["stratid"],\n>    psu=nhanes2f["psuid"],\n>    remove_nan=True\n> )\n>\n> # Replicate-based\n> ratio_wgt_hgt = ReplicateEstimator("brr", "ratio").estimate(\n>    y=nhanes2brr["weight"],\n>    samp_weight=nhanes2brr["finalwgt"],\n>    x=nhanes2brr["height"],\n>    rep_weights=nhanes2brr.loc[:, "brr_1":"brr_32"],\n>    remove_nan = True\n> )\n> ```\n\nTo predict small area parameters, we can use code similar to:\n\n> ```python\n> import samplics\n> from samplics.estimation import EblupAreaModel, EblupUnitModel\n>\n> # Area-level basic method\n> fh_model_reml = EblupAreaModel(method="REML")\n> fh_model_reml.fit(\n>    yhat=yhat, X=X, area=area, intercept=False, error_std=sigma_e, tol=1e-4,\n> )\n> fh_model_reml.predict(X=X, area=area, intercept=False)\n>\n> # Unit-level basic method\n> eblup_bhf_reml = EblupUnitModel()\n> eblup_bhf_reml.fit(ys, Xs, areas,)\n> eblup_bhf_reml.predict(Xmean, areas_list)\n> ```\n\n## Installation\n\n`pip install samplics`\n\nPython 3.6.1 or newer is required and the main dependencies are [numpy](https://numpy.org), [pandas](https://pandas.pydata.org), [scpy](https://www.scipy.org), and [statsmodel](https://www.statsmodels.org/stable/index.html).\n\n## License\n\n[MIT](https://github.com/survey-methods/samplics/blob/master/license.txt)\n\n## Contact\n\ncreated by [Mamadou S. Diallo](https://twitter.com/MamadouSDiallo) - feel free to contact me!\n',
    'author': 'Mamadou S Diallo',
    'author_email': 'msdiallo@quantifyafrica.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://samplics.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
