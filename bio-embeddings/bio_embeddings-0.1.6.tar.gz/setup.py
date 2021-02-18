# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bio_embeddings',
 'bio_embeddings.embed',
 'bio_embeddings.extract',
 'bio_embeddings.extract.annotations',
 'bio_embeddings.extract.basic',
 'bio_embeddings.project',
 'bio_embeddings.utilities',
 'bio_embeddings.utilities.filemanagers',
 'bio_embeddings.visualize']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'biopython>=1.76,<2.0',
 'gensim>=3.8.2,<4.0.0',
 'h5py>=2.10.0,<3.0.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'jaxlib==0.1.57',
 'lock>=2018.3.25,<2019.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'plotly>=4.6.0,<5.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'scikit-learn>=0.22.2.post1,<0.23.0',
 'scipy>=1.4.1,<2.0.0',
 'torch>=1.7.0,<1.8.0',
 'tqdm>=4.45.0,<5.0.0',
 'umap-learn>=0.4.2,<0.5.0',
 'urllib3==1.25.10']

extras_require = \
{'all': ['bio-embeddings-esm==0.2.1',
         'bio-embeddings-cpcprot==0.0.1',
         'bio-embeddings-tape-proteins==0.4',
         'bio-embeddings-plus==0.1.0',
         'bio-embeddings-bepler==0.0.1',
         'bio-embeddings-allennlp==0.9.0',
         'transformers>=4.0.0,<5.0.0',
         'jax-unirep>=1.0.1,<2.0.0'],
 'bepler': ['bio-embeddings-bepler==0.0.1'],
 'cpcprot': ['bio-embeddings-cpcprot==0.0.1',
             'bio-embeddings-tape-proteins==0.4'],
 'esm': ['bio-embeddings-esm==0.2.1'],
 'plus': ['bio-embeddings-plus==0.1.0'],
 'seqvec': ['bio-embeddings-allennlp==0.9.0',
            'boto3==1.14.18',
            'botocore==1.17.18'],
 'transformers': ['transformers>=4.0.0,<5.0.0'],
 'unirep': ['jax-unirep>=1.0.1,<2.0.0'],
 'webserver': ['pymongo>=3.11.2,<4.0.0', 'sentry-sdk[flask]>=0.19.5,<0.20.0']}

entry_points = \
{'console_scripts': ['bio_embeddings = bio_embeddings.utilities.cli:main']}

setup_kwargs = {
    'name': 'bio-embeddings',
    'version': '0.1.6',
    'description': 'A pipeline for protein embedding generation and visualization',
    'long_description': '<p align="center">\n  <a href="https://chat.bioembeddings.com/">\n    <img src="https://chat.bioembeddings.com/api/v1/shield.svg?type=online&name=chat&icon=false" />\n  </a>\n</p>\n\n# Bio Embeddings\nResources to learn about bio_embeddings:\n\n- Quickly predict protein structure and function from sequence via embeddings: [embed.protein.properties](https://embed.protein.properties).\n- Read the current documentation: [docs.bioembeddings.com](https://docs.bioembeddings.com).\n- Chat with us: [chat.bioembeddings.com](https://chat.bioembeddings.com).\n- We presented the bio_embeddings pipeline as a talk at ISMB 2020 & LMRL 2020. You can [find the talk on YouTube](https://www.youtube.com/watch?v=NucUA0QiOe0&feature=youtu.be), and [the poster on F1000](https://f1000research.com/posters/9-876).\n- Check out the [`examples`](examples) of pipeline configurations a and [`notebooks`](notebooks).\n\nProject aims:\n\n  - Facilitate the use of language model based biological sequence representations for transfer-learning by providing a single, consistent interface and close-to-zero-friction\n  - Reproducible workflows\n  - Depth of representation (different models from different labs trained on different dataset for different purposes)\n  - Extensive examples, handle complexity for users (e.g. CUDA OOM abstraction) and well documented warnings and error messages.\n\nThe project includes:\n\n- General purpose python embedders based on open models trained on biological sequence representations (SeqVec, ProtTrans, UniRep,...)\n- A pipeline which:\n  - embeds sequences into matrix-representations (per-amino-acid) or vector-representations (per-sequence) that can be used to train learning models or for analytical purposes\n  - projects per-sequence embedidngs into lower dimensional representations using UMAP or t-SNE (for lightwieght data handling and visualizations)\n  - visualizes low dimensional sets of per-sequence embeddings onto 2D and 3D interactive plots (with and without annotations)\n  - extracts annotations from per-sequence and per-amino-acid embeddings using supervised (when available) and unsupervised approaches (e.g. by network analysis)\n- A webserver that wraps the pipeline into a distributed API for scalable and consistent workfolws\n\n## Installation\n\nYou can install `bio_embeddings` via pip or use it via docker.\n\n### Pip\n\nInstall the pipeline like so:\n\n```bash\npip install bio-embeddings[all]\n```\n\nTo get the latest features, please install the pipeline like so:\n\n```bash\npip install -U "bio-embeddings[all] @ git+https://github.com/sacdallago/bio_embeddings.git"\n```\n\n### Docker\n\nWe provide a docker image at `ghcr.io/bioembeddings/bio_embeddings`. Simple usage example:\n\n```shell_script\ndocker run --rm --gpus all \\\n    -v "$(pwd)/examples/docker":/mnt \\\n    -u $(id -u ${USER}):$(id -g ${USER}) \\\n    ghcr.io/bioembeddings/bio_embeddings:v0.1.6 /mnt/config.yml\n```\n\nSee the [`docker`](examples/docker) example in the [`examples`](examples) folder for instructions. You can also use `ghcr.io/bioembeddings/bio_embeddings:latest` which is built from the latest commit.\n\n### Installation notes:\n\n`bio_embeddings` was developed for unix machines with GPU capabilities and [CUDA](https://developer.nvidia.com/cuda-zone) installed. If your setup diverges from this, you may encounter some inconsitencies (e.g. speed is significantly affected by the absence of a GPU and CUDA). For Windows users, we strongly recommend the use of [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).\n\n\n## What model is right for you?\n\nEach models has its strengths and weaknesses (speed, specificity, memory footprint...). There isn\'t a "one-fits-all" and we encourage you to at least try two different models when attempting a new exploratory project.\n\nThe models `prottrans_bert_bfd`, `prottrans_albert_bfd`, `seqvec` and `prottrans_xlnet_uniref100` were all trained with the goal of systematic predictions. From this pool, we believe the optimal model to be `prottrans_bert_bfd`, followed by `seqvec`, which has been established for longer and uses a different principle (LSTM vs Transformer).\n\n## Usage and examples\n\nWe highly recommend you to check out the [`examples`](examples) folder for pipeline examples, and the [`notebooks`](notebooks) folder for post-processing pipeline runs and general purpose use of the embedders.\n\nAfter having installed the package, you can:\n\n1. Use the pipeline like:\n\n    ```bash\n    bio_embeddings config.yml\n    ```\n\n    [A blueprint of the configuration file](examples/parameters_blueprint.yml), and an example setup can be found in the [`examples`](examples) directory of this repository.\n\n1. Use the general purpose embedder objects via python, e.g.:\n\n    ```python\n    from bio_embeddings.embed import SeqVecEmbedder\n\n    embedder = SeqVecEmbedder()\n\n    embedding = embedder.embed("SEQVENCE")\n    ```\n\n    More examples can be found in the [`notebooks`](notebooks) folder of this repository.\n    \n## Cite\n\nWhile we are working on a proper publication, if you are already using this tool, we would appreciate if you could cite the following poster:\n\n> Dallago C, Schütze K, Heinzinger M et al. bio_embeddings: python pipeline for fast visualization of protein features extracted by language models [version 1; not peer reviewed]. F1000Research 2020, 9(ISCB Comm J):876 (poster) (doi: [10.7490/f1000research.1118163.1](https://doi.org/10.7490/f1000research.1118163.1))\n\n## Contributors\n\n- Christian Dallago (lead)\n- Konstantin Schütze\n- Tobias Olenyi\n- Michael Heinzinger\n\n----\n\n## Development status\n\n\n<details>\n<summary>Pipeline stages</summary>\n<br>\n\n- embed:\n  - [x] ProtTrans BERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n  - [x] SeqVec (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n  - [x] ProtTrans ALBERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n  - [x] ProtTrans XLNet trained on UniRef100 (https://doi.org/10.1101/2020.07.12.199554)\n  - [ ] Fastext\n  - [ ] Glove\n  - [ ] Word2Vec\n  - [x] UniRep (https://www.nature.com/articles/s41592-019-0598-1)\n  - [x] ESM/ESM1b (https://www.biorxiv.org/content/10.1101/622803v3)\n  - [x] PLUS (https://github.com/mswzeus/PLUS/)\n  - [x] CPCProt (https://www.biorxiv.org/content/10.1101/2020.09.04.283929v1.full.pdf)\n- project:\n  - [x] t-SNE\n  - [x] UMAP\n- visualize:\n  - [x] 2D/3D sequence embedding space\n- extract:\n  - supervised:\n    - [x] SeqVec: DSSP3, DSSP8, disorder, subcellular location and membrane boundness as in https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8\n    - [x] Bert: DSSP3, DSSP8, disorder, subcellular location and membrane boundness as in https://doi.org/10.1101/2020.07.12.199554\n  - unsupervised:\n    - [x] via sequence-level (reduced_embeddings), pairwise distance (euclidean like [goPredSim](https://github.com/Rostlab/goPredSim), more options available, e.g. cosine)\n</details>\n\n<details>\n<summary>Web server (unpublished)</summary>\n<br>\n\n- [x] SeqVec supervised predictions\n- [x] Bert supervised predictions\n- [ ] SeqVec unsupervised predictions for GO: CC, BP,..\n- [ ] Bert unsupervised predictions for GO: CC, BP,..\n- [ ] SeqVec unsupervised predictions for SwissProt (just a link to the 1st-k-nn)\n- [ ] Bert unsupervised predictions for SwissProt (just a link to the 1st-k-nn)\n</details>\n\n<details>\n<summary>General purpose embedders</summary>\n<br>\n\n- [x] ProtTrans BERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n- [x] SeqVec (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n- [x] ProtTrans ALBERT trained on BFD (https://doi.org/10.1101/2020.07.12.199554)\n- [x] ProtTrans XLNet trained on UniRef100 (https://doi.org/10.1101/2020.07.12.199554)\n- [x] Fastext\n- [x] Glove\n- [x] Word2Vec\n- [x] UniRep (https://www.nature.com/articles/s41592-019-0598-1)\n- [x] ESM/ESM1b (https://www.biorxiv.org/content/10.1101/622803v3)\n- [x] PLUS (https://github.com/mswzeus/PLUS/)\n- [x] CPCProt (https://www.biorxiv.org/content/10.1101/2020.09.04.283929v1.full.pdf)\n</details>\n',
    'author': 'Christian Dallago',
    'author_email': 'christian.dallago@tum.de',
    'maintainer': 'Rostlab',
    'maintainer_email': 'admin@rostlab.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.6,<4.0',
}


setup(**setup_kwargs)
