import numpy as np
from ..utils import dprint

def tryWriteImage(file:np.ndarray, path:str, imgLib:str="opencv", count:int=5) -> None:
	assert imgLib in ("opencv", "PIL", "pillow", "lycon")
	if imgLib == "opencv":
		from .libs.opencv import writeImage
	elif imgLib in ("PIL", "pillow"):
		from .libs.pil import writeImage
	elif imgLib == "lycon":
		from .libs.lycon import writeImage

	i = 0
	while True:
		try:
			return writeImage(file, path)
		except Exception as e:
			dprint("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception
