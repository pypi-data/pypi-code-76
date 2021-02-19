import os
from glob import glob
import toml
import shutil
from markdown import markdown
import jinja2
import sys

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(('_layouts','_includes')),
    # autoescape=jinja2.select_autoescape(['html', 'xml', 'html'])
)

meta = {
	"version": "0.1.0"
}

def ensure(path):
	prevpaths = ['_build']
	for part in path.split(os.sep):
		prevpaths.append(part)
		if not os.path.isdir(os.sep.join(prevpaths)):
			os.mkdir(os.sep.join(prevpaths))

if os.path.isdir('_build'):
	shutil.rmtree('_build')

shutil.copytree('_static', '_build')

# Load data files to `data` variable
data = toml.load('_config.toml')
collections = {}
for datafile in glob('_data/*.toml'):
	data[datafile.replace('_data/','')[:-5]] = toml.load(datafile)

# Move collections
for collection in data['collection']:
	collections[collection['name']] = []
	for collectionfile in glob("_"+collection['name']+os.sep+'*'):
		with open(collectionfile) as filedata:
			splitdata = filedata.read().split('\n')
			tomldata = ""
			mdata = ""
			linemode = 'toml'
			if splitdata[0] != '---':
				continue
			for count, line in enumerate(splitdata[1:]):
				if line == '---':
					linemode = "md"
				elif linemode == "toml":
					tomldata += line + "\n"
				elif linemode == "md":
					mdata += line + "\n"
		if tomldata == "":
			continue
		tomlparsed = toml.loads(tomldata)
		output_path = collection['scheme'].format(**tomlparsed, filename = collectionfile.replace("_"+collection['name']+os.sep,''))
		tomlparsed['url'] = output_path
		if 'defaults' in collection:
			for default_key in collection['defaults']:
				if default_key not in tomlparsed:
					tomlparsed[default_key] = collection['defaults'][default_key]
		collections[collection['name']].append(tomlparsed)
		ensure(output_path)
		shutil.copy(collectionfile,"_build"+output_path+os.sep+"index.html")
		with open("_build"+output_path+os.sep+"index.html", "w+") as file:
			file.write('---\n')
			file.write(toml.dumps(tomlparsed))
			file.write('---\n\n')
			if collectionfile.endswith('.md'):
				file.write(markdown(mdata))
			else:
				file.write(mdata)
# JINJA!!!
if '--debug' in sys.argv or '-d' in sys.argv:
	input('Waiting...')
for root, dirs, files in os.walk('_build'):
	for filename in files:
		filename = root + os.sep + filename
		tomldata = ""
		body = ""
		mode = "toml"
		with open(filename) as file:
			split = file.read().split('\n')
			if split[0] != "---":
				continue
			for line in split[1:]:
				if line == "---":
					mode = "body"
					continue
				elif mode == "toml":
					tomldata += line + "\n"
				else:
					body += line + "\n"
		tomldata = toml.loads(tomldata)
		if 'layout' not in tomldata:
			tomldata['layout'] = 'default'
		t = "{% extends '"+tomldata['layout']+".html' %}"+"\n{% block content %}"+body+"{% endblock content %}"
		t = env.from_string(t)
		with open(filename, 'w+') as outputfile:
			outputfile.write(t.render(
				site = data,
				collections = collections,
				meta = meta,
				page = tomldata
			))

