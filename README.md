# marknow

A lightweight server to browse a collection of Markdown files as a website.


## Installation

Install Marknow with:

```bash
pip install .
```

If you intend to develop on Marknow, install its development dependencies:

```bash
pip install .[dev]
```


## Server-Side Usage

Basic usage:

```bash
marknow sample-site
```

To see a full set of options:

```
$ marknow -h
usage: marknow [-h] [-a ADDRESS] [-p PORT] [-r ROOT] [-s {desert,night,night-serif,default}] [-v] directory

Serve browsable Markdown

positional arguments:
  directory             Path to the top level of Markdown files to serve

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        Bind address
  -p, --port PORT       Port to listen on
  -r, --root ROOT       File to redirect calls to "/" to
  -s, --style {desert,night,night-serif,default}
                        Filename in `static/styles` directory to render
  -v, --verbose         Enable verbose logging
```

If you are developing Marknow, you will have to `pip install .` after every code change for these various `marknow`
commands to work. You can avoid this by using a different invocation:

```bash
python -m marknow.main sample-site
```


## Client-Side Usage

In the browser, you can add the `refresh=#` parameter, where `#` is a number of seconds. This will cause the page to
automatically reload every time that number of seconds elapses. This is useful for watching your documents render live
after editing them in local development mode. For example: `http://localhost:4037/README.md?refresh=5`