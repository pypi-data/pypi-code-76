import click
import requests
import validators
import os
from prettytable import PrettyTable
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ver = "2.2.2"
__author__ = "Athmane Bouazzouni"

@click.group()
@click.version_option()

def main():
    """
    Simple CLI by Athmane Bouazzouni
    """
    pass

@main.command()
@click.argument('url')
def register(url):
    """Registers a URL"""
    valid = validators.url(url)
    if valid == True:
        filename = 'registered.txt'
        if os.path.exists(filename):
            write_var = 'a'
        else:
            write_var = 'w'
        with open(filename, write_var) as reg_file:
            reg_file.write(url + '\n')
            click.echo('URL ' + url + ' was added to registery')
    else:
        print("Invalid url")
        raise click.ClickException('Invalid url')

@main.command()
def measure():
    """Shows body sizes of registered URLs"""
    filepath = 'registered.txt'

    url_list=[]
    with open(filepath) as fp:
        for url in fp:
                url = url.strip()
                headers = {
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'
                }
                #print(url)
                request = requests.get(url, headers=headers)
                url_list.append([url, str(round(len(request.content)/1024,2)) + "KB", str(request.status_code)])
                #print(request.status_code)
                #click.echo(url + '\t %s \t %s' % (len(request.content), request.history))
            #except:
            #    print(url, '\x1b[1;30;41m' + 'Website Timedout' + '\x1b[0m')
        table = PrettyTable(['URL', 'Size', 'Status Code'])
        for rec in url_list:
            table.add_row(rec)
        table.align["URL"]="l"
        table.align["Size"]="r"
        print(table)

@main.command()
def race():
    """Shows page load time of registered URLs"""
    filepath = 'registered.txt'

    url_list=[]
    with open(filepath) as fp:
        for url in fp:
                url = url.strip()
                headers = {
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)'
                }
                #print(url)
                request = requests.get(url + "/page-sitemap.xml", headers=headers)
                page = "/page-sitemap.xml"
                block = "url"
                if request.status_code == 404:
                    request = requests.get(url + "/sitemap.xml", headers=headers)
                    page = "/sitemap.xml"
                    block = "sitemap"
                parsed_uri=urlparse(url + page)
                xml = request.text
                soup = BeautifulSoup(xml, "html.parser")
                sitemapTags = soup.find_all(block)
                #print(xml)
#                if page == "/sitemap.xml":
#                    sitemapTags = soup.find_all("sitemap")
#                if page == "/page-sitemap.xml":
#                    sitemapTags = soup.find_all("url")
                time = 0
                for sitemap in sitemapTags:
                    rpostmap=sitemap.findNext("loc").text
                    time = time + requests.get(rpostmap).elapsed.total_seconds()
                    print("URL is: %s , it took: %s " % (rpostmap, str(requests.get(rpostmap).elapsed.total_seconds())))

                if len(sitemapTags) == 0:
                    average_time = 0
                else:
                    average_time = round(time/len(sitemapTags),2)

                url_list.append([parsed_uri.netloc, str(round(len(request.content)/1024,2)) + "KB", average_time, str(request.history)])
                #print(request.status_code)
                #click.echo(url + '\t %s \t %s' % (len(request.content), request.history))
            #except:
            #    print(url, '\x1b[1;30;41m' + 'Website Timedout' + '\x1b[0m')
        table = PrettyTable(['URL', 'Size', 'Average time', 'Status Code'])
        for rec in url_list:
            table.add_row(rec)
        table.align["URL"]="l"
        table.align["Size"]="r"
        print(table)

@main.command('version', help='Show the package version.')
def print_version():
    """Print the current version of sandman and exit."""
    import pkg_resources
    version = pkg_resources.require("meajur")[0].version
    name = pkg_resources.require("meajur")[0] # prints "meajur 0.0.15"
    del pkg_resources
    click.echo("meajur, version " + version)


if __name__ == "__main__":
    main()