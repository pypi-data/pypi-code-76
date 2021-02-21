import os
import re
import pybars
import errno
import markdown
import json
import sys
import shutil
from watchgod import watch
from bloggo import hbs

__version__ = "1.2.0"
resources_dir = './resources'
out_dir = './public'


def get_paths(from_path):
    paths = []
    items = os.listdir(from_path)

    for item in items:
        if item.endswith(".md"):
            complete_path = (from_path + "/" + item)
            path = complete_path.replace(resources_dir + '/content', '')
            paths.append(path)
        elif os.path.isdir(from_path + '/' + item):
            paths.extend(get_paths(from_path + '/' + item))
        else:
            pass

    return paths


def remove_all_occurrences_from_list(given_list, to_remove):
    result = []

    for item in given_list:
        if item != to_remove:
            result.append(item)

    return result


def remove_spaces_from_around_items_in_list(given_list):
    result = []

    for item in given_list:
        result.append(re.sub(r'^\s+|\s+$', '', item, flags=re.UNICODE))

    return result


def get_content_meta(content):
    meta_block = re.search('(?s)^---(.*?)---*', content)

    if meta_block:
        match = meta_block.group(0)
        meta_lines = match.splitlines()
        meta_lines = remove_spaces_from_around_items_in_list(meta_lines)
        meta_lines = remove_all_occurrences_from_list(meta_lines, '---')
        meta = {}

        for meta_line in meta_lines:
            if ':' in meta_line:
                key = meta_line.split(':')[0].strip().replace(' ', '_')
                key = re.sub('[^a-zA-Z_]', '', key)
                value = meta_line.split(':')[1].strip()
                meta[key] = value

        return meta
    else:
        return {}


def get_content_entry(content):
    entry = re.sub('(?s)^---(.*?)---*', '', content)
    return entry.strip()


def get_contents(paths, site_url=None):
    contents = []

    for path in paths:
        with open(resources_dir + "/content" + path, 'r') as reader:
            content = reader.read()
            meta = get_content_meta(content)
            entry = get_content_entry(content)
            data = {
                'path': path.replace('.md', ''),
                **meta,
                'entry': markdown.markdown(entry, extensions=['extra'])
            }

            if site_url is not None:
                data['url'] = site_url + data['path']

            contents.append(data)

    # Make sure that every item has `date`, and then sort
    sort = True

    for content in contents:
        if 'date' not in content:
            sort = False

    if sort:
        return sorted(contents, key=lambda k: k['date'], reverse=True)

    # Otherwise return as-is
    else:
        return contents


def write(file_path, contents):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    file = open(file_path, 'w')
    file.write(contents)
    file.close()


def generate_feed(blog_path, site_config):
    print('Generating XML feed')
    blog_paths = get_paths(blog_path)
    blog_contents = get_contents(blog_paths, site_config['site_url'])
    template = """
    <?xml version="1.0" encoding="UTF-8"?><rss version="2.0"
        xmlns:content="http://purl.org/rss/1.0/modules/content/"
        xmlns:wfw="http://wellformedweb.org/CommentAPI/"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:atom="http://www.w3.org/2005/Atom"
        xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
        xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
        >
    <channel>
        <title>{{site_title}}</title>
        <atom:link href="{{url}}/feed.xml" rel="self" type="application/rss+xml"></atom:link>
        <link>{{site_url}}</link>
        <description>{{site_description}}</description>
        <lastBuildDate>Fri, 05 Feb 2021 21:41:44 +0000</lastBuildDate>
        <language>en</language>
        <sy:updatePeriod>hourly</sy:updatePeriod>
        <sy:updateFrequency>1</sy:updateFrequency>
        {{#entries}}
        <item>
            <title>{{title}}</title>
            <link>{{url}}</link>
            <pubDate>{{date}}</pubDate>
            <description>{{description}}</description>
            <content:encoded><![CDATA[{{{entry}}}]]></content:encoded>
        </item>
        {{/entries}}
    </channel>
    </rss>
    """
    compiler = pybars.Compiler()
    compiled_template = compiler.compile(template)
    output = compiled_template({**site_config, 'entries': blog_contents})
    file_path = out_dir + '/feed.xml'

    write(file_path, output)


def generate_file(content, config, template, helpers):
    print('Generating ' + content['path'])
    compiler = pybars.Compiler()
    compiled_template = compiler.compile(template)
    output = compiled_template({**config, **content}, helpers=helpers)
    file_path = out_dir + content['path'] + '/index.html'

    write(file_path, output)


def generate_files(contents):
    with open(resources_dir + '/template.hbs', 'r') as template_file, \
            open(resources_dir + '/config.json', 'r') as config_file:
        template = template_file.read()
        site_config = json.loads(config_file.read())

        # Before we go further, let's make sure required config exists
        if not site_config['site_title']:
            sys.exit('site_title does not exist in config.json')

        if not site_config['site_description']:
            sys.exit('site_description does not exist in config.json')

        if not site_config['site_url']:
            sys.exit('site_url does not exist in config.json')

        blog_paths = get_paths(resources_dir + '/content/blog')
        blog_contents = get_contents(blog_paths, site_config['site_url'])
        helpers = {'format_date': hbs.format_date}
        post_config = {'is_home': False, 'is_post': True}
        home_config = {
            'is_home': True,
            'is_post': False,
            'posts': blog_contents
        }

        # Generate all content
        for content in contents:
            generate_file(content,
                          {**post_config, **site_config},
                          template,
                          helpers)

        # Generate home page
        generate_file({'path': '/', 'entry': ''},
                      {**home_config, **site_config},
                      template,
                      helpers)

        # Generate XML feed for blog posts
        generate_feed(resources_dir + '/content/blog', site_config)


def generate():
    # Before we do anything let's make sure needed files exist
    if not os.path.exists(resources_dir + '/config.json'):
        sys.exit(resources_dir + '/config.json file does not exist.')

    if not os.path.exists(resources_dir + '/template.hbs'):
        sys.exit(resources_dir + '/template.hbs file does not exist.')

    # We are victorious!
    print('Generating...')

    try:
        paths_to_files = get_paths(resources_dir + '/content')
        contents_of_files = get_contents(paths_to_files)

        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        shutil.copytree(resources_dir + '/assets', out_dir + '/assets')
        generate_files(contents_of_files)

        print('All done :)')
    except Exception as e:
        print('Are you sure the directories are correct?')
        print(e)


def run(argv=None):
    global resources_dir
    global out_dir

    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = argv[1:]

    if '--help' in argv:
        print('##################################################')
        print('# You can run Bloggo with the following arguments:')
        print('##################################################')
        print('# Change the resources directory:')
        print('# --resources-dir {directory}')
        print('# ')
        print('# Change the out directory:')
        print('# --out-dir {directory}')
        print('# ')
        print('# Watch for file changes and auto-compile:')
        print('# --watch')
        print('# ')
        print('# Get the current version of Bloggo:')
        print('# --version')
        print('##################################################')
        exit()

    if '--version' in argv:
        print(__version__)
        exit()

    if '--out-dir' in argv:
        out_dir_index = argv.index('--out-dir')
        out_dir = argv[out_dir_index + 1]

    if '--resources-dir' in argv:
        resources_dir_index = argv.index('--resources-dir')
        resources_dir = argv[resources_dir_index + 1]

    if '--watch' in argv:
        generate()
        print('Watching for changes...')
        for _ in watch(resources_dir):
            generate()

        exit()

    generate()
