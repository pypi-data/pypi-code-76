import pip
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def download_requirements(requirements_file: Path, destination: Path):
	with TemporaryDirectory() as tmp:
		pip_args = [
			'download',
			'--requirement', str(requirements_file),
			'--dest', tmp,
		]
		pip.main(pip_args)
		for tmp_wheel in Path(tmp).iterdir():
			wheel_path = destination.joinpath(tmp_wheel.name)
			yield tmp_wheel.rename(wheel_path)


def wheel_package_name(wheel: Path):
	with ZipFile(wheel) as wheel_zip:
		metadata_items = []
		for item_info in wheel_zip.infolist():
			item_path = Path(item_info.filename)
			try:
				parent_name, name = item_path.parts
			except ValueError:
				continue

			if name != 'METADATA':
				continue

			if not parent_name.endswith('.dist-info'):
				continue

			metadata_items.append(item_info.filename)

		try:
			metadata_path, = metadata_items
		except ValueError:
			raise ValueError(
				'Unable to resolve metadata file from candidates'
				f' {metadata_items}'
			)

		with wheel_zip.open(metadata_path) as metadata:
			for line in metadata.readlines():
				if line.startswith(b'Name: '):
					_, package_name = line.strip().split(b': ')
					return package_name.decode()
			else:
				raise KeyError("No 'Name' entry in wheel metadata")


if __name__ == '__main__':
	import sys
	print(wheel_package_name(sys.argv[1]))