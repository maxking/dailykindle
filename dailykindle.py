import feedparser
import shutil

from argparse import ArgumentParser
from subprocess import call
from datetime import date, timedelta
from os import path, listdir
from jinja2 import Environment, PackageLoader

templates_env = Environment(loader=PackageLoader('dailykindle', 'templates'))
ROOT = path.dirname(path.abspath(__file__))


def build(feed_urls, output_dir, max_old=None):
    """
    Given a list of feeds URLs and the path of a directory, writes the necessary
    for building a MOBI document.

    max_old must be either None or a timedelta. It defines the maximum age of
    posts which should be considered.
    """

    # Convert max_old if needed.
    if max_old == None:
        max_old = timedelta.max

    # Give the feeds URLs to Feedparser to have nicely usable feed objects.
    feeds = [feedparser.parse(feed_url) for feed_url in feed_urls]

    # Parse the feeds and grave useful information to build a structure
    # which will be passed to the templates.
    data = []

    ## Initialize some counters for the TOC IDs.
    ## We start counting at 2 because 1 is the TOC itself.
    feed_number = 1
    play_order = 1

    for feed in feeds:
        feed_number += 1
        play_order += 1
        local = {
            'number': feed_number,
            'play_order': play_order,
            'entries': [],
            'title': feed.feed.title,
        }

        entry_number = 0
        for entry in feed.entries:

            # We don't want old posts, just fresh news.
            if date.today() - date(*entry.date_parsed[0:3]) > max_old:
                continue

            play_order += 1
            entry_number += 1

            local_entry = {
                'number': entry_number,
                'play_order': play_order,
                'title': entry.title,
                'description': entry.description,
            }

            local['entries'].append(local_entry)

        data.append(local)

    # Wrap data and today's date in a dict to use the magic of **.
    wrap = {
        'date': date.today().isoformat(),
        'feeds': data,
    }

    # Render and output templates

    ## TOC (NCX)
    render_and_write('toc.xml', wrap, 'toc.ncx', output_dir)
    ## TOC (HTML)
    render_and_write('toc.html', wrap, 'toc.html', output_dir)
    ## OPF
    render_and_write('opf.xml', wrap, 'daily.opf', output_dir)
    ## Content
    for feed in data:
        render_and_write('feed.html', feed, '%s.html' % feed['number'], output_dir)

    # Copy the assets
    for name in listdir(path.join(ROOT, 'assets')):
        shutil.copy(path.join(ROOT, 'assets', name), path.join(output_dir, name))
    # copytree(path.join(ROOT, 'assets'), output_dir)


def render_and_write(template_name, context, output_name, output_dir):
    """Render `template_name` with `context` and write the result in the file
    `output_dir`/`output_name`."""

    template = templates_env.get_template(template_name)
    f = open(path.join(output_dir, output_name), "w")
    f.write(template.render(**context))
    f.close()

def mobi(input_file, exec_path):
    """Execute the KindleGen binary to create a MOBI file."""
    if exec_path is None:
        exec_path = "kindlegen"
    call([exec_path, input_file])

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-a", "--age", dest="age", default=None,
                      help="Max age of posts to be used", metavar="INT")
    parser.add_argument("-k", "--kindlegen", dest="exec_path", default=None,
                      help="Path to the kindlegen binary if not on sys path")
    parser.add_argument("-o", "--output_dir", dest="output_dir", default="/tmp",
                        help="Output path for created ebook and other files")
    parser.add_argument("feed", nargs="*", help="One or more feed urls")

    try:
        args = parser.parse_args()
    except:
        raise

    if args.age is None:
        length = None
    else:
        length = timedelta(int(args.age))

    print("Running DailyKindle...")
    print("-> Generating files...")
    build(args.feed, args.output_dir, length)
    print("-> Build the MOBI file using KindleGen...")
    mobi(path.join(args.output_dir, 'daily.opf'), args.exec_path)
    print("Done.")
