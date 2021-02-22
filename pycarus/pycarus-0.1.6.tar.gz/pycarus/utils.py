"""
Module containing generic utils functions.
"""
import hashlib
import ssl
from pathlib import Path
from shutil import unpack_archive
from typing import Callable, Union
from urllib import request

import numpy as np  # type: ignore
import torch
from matplotlib import cm  # type: ignore
from sklearn.manifold import TSNE  # type: ignore
from tqdm import tqdm  # type: ignore


def download_file(url: str, path: Path, print_progress: bool) -> None:
    """Download file from URL to path.

    Args:
        url: the url from which to download the file.
        path: the path and file name for the downloaded file.
        print_progress: if True print a progress bar while downloading the file.
    """

    def updater_callback() -> Callable[[int, int, int], None]:
        pbar = tqdm(total=None)

        def bar_update(count: int, block_size: int, total_size: int) -> None:
            if pbar.total is None and total_size:
                pbar.total = total_size
            progress_bytes = count * block_size
            pbar.update(progress_bytes - pbar.n)

        return bar_update

    ssl._create_default_https_context = ssl._create_unverified_context
    fn_callback = updater_callback() if print_progress else None
    request.urlretrieve(url, path, reporthook=fn_callback)


def check_integrity(path: Path, md5_hash: str = str(None)) -> bool:
    """Check the integrity of a file.

    The integrity of the file is ensured by checking if the path points to a file. Eventually,
    the md5 digest will be checked if it is not None.

    Args:
        path: the path to the file.
        md5_hash: the Defaults to None.

    Returns:
        True if the check is passed.
    """
    if not path.is_file:
        return False

    if md5_hash is not None:
        return md5_hash == get_md5(path)

    return True


def get_md5(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute the MD5 hash value, to handle big files the function splits the file in chunks.

    Args:
        path: the path to the file.
        chunk_size: the size for the chunk (multiple of 128). Defaults to 1024*1024.

    Returns:
        The hex string representation for the MD5 digest.
    """
    hash_md5 = hashlib.md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def download_and_extract(
    url: str,
    path_file_downloaded: Path,
    path_destination: Path,
    md5_hash: str = str(None),
) -> None:
    """Download a compressed file from the url and extract it into path_destination.

    Args:
        url: the url from which download the file.
        path_file_downloaded: the path in which to save the downloaded file.
        path_destination: the path in which extract the content of the file.
        md5_hash (optional): the hash digest to use to check the integrity of the file.

    Raises:
        RuntimeError: if the downloaded file is not correct.
    """
    path_file_downloaded.parent.mkdir(exist_ok=True)
    download_file(url, path_file_downloaded, True)

    if not check_integrity(path_file_downloaded, md5_hash):
        raise RuntimeError(f"File {str(path_file_downloaded)} not found or corrupted.")

    unpack_archive(str(path_file_downloaded), path_destination)
    path_file_downloaded.unlink()


def get_tsne(
    data: Union[torch.Tensor, np.ndarray],
    n_components: int = 1,
    verbose: int = 1,
    perplexity: float = 40.0,
    n_iter: int = 300,
    random_state: int = 0,
) -> torch.Tensor:
    """Compute the t-SNE for each sample. NaN values converted to zero.

    Args:
        data: The input data with shape (N, N_DIMS)
        n_components: The component for the embedded space. Defaults to 1.
        verbose: The verbosity. Defaults to 1.
        perplexity: The perplexity is related to the number of nearest neighbors used.
                    Defaults to 40.0.
        n_iter: Maximum iterations for the optimization. Should be at least 250. Defaults to 300.
        random_state: The random number generator. Defaults to 0.

    Returns:
        The computed t-SNE with shape (N, n_components) normalized.
    """
    if isinstance(data, torch.Tensor):
        data = data.cpu().numpy()

    data = np.nan_to_num(data)
    tsne = TSNE(
        n_components=n_components,
        verbose=verbose,
        perplexity=perplexity,
        n_iter=n_iter,
        random_state=random_state,
    )
    results = np.squeeze(tsne.fit_transform(data))
    min_val = np.min(results)
    max_val = np.max(results)
    normalized_results = (results - min_val) / (max_val - min_val)

    return torch.tensor(normalized_results)


def apply_color_map(
    values: Union[torch.Tensor, np.ndarray],
    name_map: str = "Spectral",
) -> torch.Tensor:
    """Map each scalar value in values to a color using a color map in matplotlib.

    Args:
        values: The input values as a torch tensor with shape (N,).
        name_map: The color map to use. Defaults to "Spectral".

    Returns:
        RGB color for each sample with shape (N, 3).
    """
    if isinstance(values, torch.Tensor):
        values = values.cpu().numpy()
    cmap = cm.get_cmap(name_map)
    colored = cmap(values)[:, :3]
    return torch.Tensor(colored)
