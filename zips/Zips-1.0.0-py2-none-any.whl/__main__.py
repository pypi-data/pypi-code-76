from . import Zips

filename, fmt, uz = Zips.argv()
Zips.ziporuzip(filename, fmt, uz)
print("===== Done =====")

