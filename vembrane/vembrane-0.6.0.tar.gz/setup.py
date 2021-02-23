# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vembrane', 'vembrane.modules']

package_data = \
{'': ['*']}

install_requires = \
['pysam>=0.16,<0.17', 'pyyaml>=5.3,<6.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

entry_points = \
{'console_scripts': ['vembrane = vembrane.cli:main']}

setup_kwargs = {
    'name': 'vembrane',
    'version': '0.6.0',
    'description': 'Filter VCF/BCF files with Python expressions.',
    'long_description': '# vembrane: variant filtering using python expressions\n\nvembrane allows to simultaneously filter variants based on any `INFO` field, `CHROM`, `POS`, `REF`, `ALT`, `QUAL`, and the annotation field `ANN`. When filtering based on `ANN`, annotation entries are filtered first. If no annotation entry remains, the entire variant is deleted.\n\n## `vembrane filter`\n\n### Filter expression\nThe filter expression can be any valid python expression that evaluates to `bool`. However, functions and symbols available have been restricted to the following:\n\n * `all`, `any`\n * `abs`, `len`, `max`, `min`, `round`, `sum`\n * `enumerate`, `filter`, `iter`, `map`, `next`, `range`, `reversed`, `sorted`, `zip`\n * `dict`, `list`, `set`, `tuple`\n * `bool`, `chr`, `float`, `int`, `ord`, `str`\n * Any function or symbol from [`math`](https://docs.python.org/3/library/math.html)\n * Regular expressions via [`re`](https://docs.python.org/3/library/re.html)\n\n### Available fields\nThe following VCF fields can be accessed in the filter expression:\n\n|Name|Type|Interpretation|Example expression|\n|---|---|---|---|\n|`INFO`|`Dict[str, Any¹]`| `INFO field -> Value`  | `INFO["DP"] > 0`|\n|`ANN`| `Dict[str, Any²]`| `ANN field -> Value` | `ANN["Gene_Name"] == "CDH2"`|\n|`CHROM`| `str` | Chromosome Name  |  `CHROM == "chr2"` |\n|`POS`| `int` | Chromosomal position  | `24 < POS < 42`|\n|`ID`| `str`  | Variant ID |  `ID == "rs11725853"` |\n|`REF`| `str` |  Reference allele  | `REF == "A"` |\n|`ALT`| `str` |  Alternative allele³  | `ALT == "C"`|\n|`QUAL`| `float`  | Quality |  `QUAL >= 60` |\n|`FILTER`| `List[str]` | Filter tags | `"PASS" in FILTER` |\n|`FORMAT`|`Dict[str, Dict[str, Any¹]]`| `Format -> (Sample -> Value)` | `FORMAT["DP"][SAMPLES[0]] > 0` |\n|`SAMPLES`|`List[str]`| `[Sample]`  |  `"Tumor" in SAMPLES` |\n|`INDEX`|`int`| `Index of variant in the file`  |  `INDEX < 10` |\n\n ¹ depends on type specified in VCF header\n\n ² for the usual snpeff and vep annotations, custom types have been specified; any unknown ANN field will simply be of type `str`. If something lacks a custom parser/type, please consider filing an issue in the [issue tracker](https://github.com/vembrane/vembrane/issues).\n\n ³ vembrane does not handle multi-allelic records itself. Instead, such files should be\n preprocessed by either of the following tools (preferably even before annotation):\n - [`bcftools norm -m-any […]`](http://samtools.github.io/bcftools/bcftools.html#norm)\n - [`gatk LeftAlignAndTrimVariants […] --split-multi-allelics`](https://gatk.broadinstitute.org/hc/en-us/articles/360037225872-LeftAlignAndTrimVariants)\n - [`vcfmulti2oneallele […]`](http://lindenb.github.io/jvarkit/VcfMultiToOneAllele.html)\n\n\n### Examples\n\n* Only keep annotations and variants where gene equals "CDH2" and its impact is "HIGH":\n  ```\n  vembrane filter \'ANN["Gene_Name"] == "CDH2" and ANN["Annotation_Impact"] == "HIGH"\' variants.bcf\n  ```\n* Only keep variants with quality at least 30:\n  ```\n  vembrane filter \'QUAL >= 30\' variants.vcf\n  ```\n* Only keep annotations and variants where feature (transcript) is ENST00000307301:\n  ```\n  vembrane filter \'ANN["Feature"] == "ENST00000307301"\' variants.bcf\n  ```\n* Only keep annotations and variants where protein position is less than 10:\n  ```\n  vembrane filter \'ANN["Protein"].start < 10\' variants.bcf\n  ```\n* Only keep variants where mapping quality is exactly 60:\n  ```\n  vembrane filter \'INFO["MQ"] == 60\' variants.bcf\n  ```\n* Only keep annotations and variants where consequence contains the word "stream" (matching "upstream" and "downstream"):\n  ```\n  vembrane filter \'re.search("(up|down)stream", ANN["Consequence"])\' variants.vcf\n  ```\n* Only keep annotations and variants where CLIN_SIG contains "pathogenic", "likely_pathogenic" or "drug_response":\n  ```\n  vembrane filter \'any(entry in ANN["CLIN_SIG"] for entry in ("pathogenic", "likely_pathogenic", "drug_response"))\' variants.vcf\n  ```\n\n### Custom `ANN` types\n`vembrane` parses entries in the annotation field as outlined in [Types.md](Types.md)\n\n### Missing values in annotations\n\nIf a certain annotation field lacks a value, it will be replaced with the special value of `NA`. Comparing with this value will always result in `False`, e.g.\n`ANN["MOTIF_POS"] > 0` will always evaluate to `False` *if* there was no value in the "MOTIF_POS" field of ANN (otherwise the comparison will be carried out with the usual semantics).\n\nSince you may want to use the regex module to search for matches, `NA` also acts as an empty `str`, such that `re.search("nothing", NA)` returns nothing instead of raising an exception.\n\n*Explicitly* handling missing/optional values in INFO or FORMAT fields can be done by checking for NA, e.g.: `INFO["DP"] is NA`.\n\nHandling missing/optional values in fields other than INFO or FORMAT can be done by checking for None, e.g `ID is not None`.\n\n## `vembrane table`\nIn addition to the `filter` subcommand, vembrane (`≥ 0.5`) also supports writing tabular data with the `table` subcommand.\nIn this case, an expression which evaluates to `tuple` is expected, for example:\n```\nvembrane table \'CHROM, POS, 10**(-QUAL/10)\', ANN["CLIN_SIG"] > table.tsv`.\n```\n\n## Development\n### pre-commit hooks\nSince we enforce code formatting with `black` by checking for that in CI, we can avoid "fmt" commits by ensuring formatting is done upon comitting changes:\n1. make sure `pre-commit` is installed on your machine / in your env (should be available in pip, conda, archlinux repos, ...)\n2. run `pre-commit install`. This will activate pre-commit hooks to your _local_ .git\n\nNow when calling `git commit`, your changed code will be formatted with `black`, checked with`flake8`, get trailing whitespace removed and trailing newlines added (if needed)\n\n## Authors\n\n* Marcel Bargull (@mbargull)\n* Jan Forster (@jafors)\n* Till Hartmann (@tedil)\n* Johannes Köster (@johanneskoester)\n* Elias Kuthe (@eqt)\n* Felix Mölder (@felixmoelder)\n* Christopher Schröder (@christopher-schroeder)\n',
    'author': 'Till Hartmann',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vembrane/vembrane',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
