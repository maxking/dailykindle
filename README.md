# DailyKindle

DailyKindle is a Python scripts which, given a set of RSS/Atom feeds URLs,
creates a MOBI file that you can directly use on you Amazon Kindle (or any other
device that supports MOBI documents).

Want to see what it looks like? Take a look at `examples/mobi_doc/`!


## Requirements

* A working Python 3 environment (tested on OS X + Python 3.2 + Virtualenv).
* [Amazon's KindleGen](http://www.amazon.com/gp/feature.html?docId=1000234621)
  binary.

## Installation

1. Grab the script code. Choose one of the following:
   * [https://bitbucket.org/pelletier/dailykindle/get/tip.zip](https://bitbucket.org/pelletier/dailykindle/get/tip.zip)
   * [https://github.com/pelletier/dailykindle/zipball/master](https://github.com/pelletier/dailykindle/zipball/master)
   * `hg clone https://bitbucket.org/pelletier/dailykindle`
   * `git clone git://github.com/pelletier/dailykindle.git`
2. (optional) Source your virtualenv.
3. `pip install -r requirements.txt`

## Usage

```
usage: dailykindle.py [-h] [-a INT] [-k EXEC_PATH] [-o OUTPUT_DIR]
                      [feed [feed ...]]

positional arguments:
  feed                  One or more feed urls

optional arguments:
  -h, --help            show this help message and exit
  -a INT, --age INT     Max age of posts to be used
  -k EXEC_PATH, --kindlegen EXEC_PATH
                        Path to the kindlegen binary if not on sys path
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output path for created ebook and other files
```

## Example

    python dailykindle.py -o ~/Desktop/temp/ -a 7 \
    -k "~/Downloads/KindleGen_Mac_i386_v1.2/kindleGen" \
    "http://feeds.feedburner.com/b-list-entries" \
    "http://lucumr.pocoo.org/feed.atom"

## Want more?

Run the script as a cron job: see `/examples/cronjob/`.
