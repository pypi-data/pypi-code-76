import numpy as np
from ..utils import dprint

def tryReadImage(path:str, imgLib:str="opencv", count:int=5) -> np.ndarray:
	assert imgLib in ("opencv", "PIL", "pillow", "lycon")
	if imgLib == "opencv":
		from .libs.opencv import readImage
	elif imgLib in ("PIL", "pillow"):
		from .libs.pil import readImage
	elif imgLib == "lycon":
		from .libs.lycon import readImage

	i = 0
	while True:
		try:
			return readImage(path)
		except Exception as e:
			dprint("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception(e)