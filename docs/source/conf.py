#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import setup as _setup


# -- General configuration ------------------------------------------------
needs_sphinx = '1.3'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode'
]
templates_path = [
    '_templates'
]
source_suffix = [
    '.rst'
]
# source_encoding = 'utf-8-sig'
master_doc = 'index'
project = _setup.__project__.title()
copyright = '2016, {0}'.format(_setup.__author__)
author = _setup.__author__
version = _setup.__version__
release = _setup.__release__
language = None
# today_fmt = '%B %d, %Y'
exclude_patterns = []
# default_role = None
# add_function_parentheses = True
# add_module_names = True
# show_authors = False
pygments_style = 'sphinx'
# modindex_common_prefix = []
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for Napoleon -------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False


# -- Options for HTML output ----------------------------------------------

if _setup.__on_rtd__:
    html_theme = 'sphinx_rtd_theme'
    # html_theme_options = {}
    # html_sidebars = {}
else:
    html_theme = 'alabaster'
    # html_theme_options = {}
    # html_sidebars = {}
# html_theme_path = []
# html_title = None
# html_short_title = None
# html_logo = None
# html_favicon = None
html_static_path = [
    '_static'
]
# html_extra_path = []
# html_last_updated_fmt = '%b %d, %Y'
# html_use_smartypants = True
# html_additional_pages = {}
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_show_sourcelink = True
# html_show_sphinx = True
# html_show_copyright = True
# html_use_opensearch = ''
# html_file_suffix = None
# html_search_language = 'en'
# html_search_options = {'type': 'default'}
# html_search_scorer = 'scorer.js'
htmlhelp_basename = '{0}doc'.format(_setup.__project__)


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # 'papersize': 'letterpaper',
    # 'pointsize': '10pt',
    # 'preamble': '',
    # 'figure_align': 'htbp',
}

latex_documents = [
    (
        master_doc,
        '{0}.tex'.format(_setup.__project__),
        '{0} Documentation'.format(_setup.__project__),
        _setup.__author__,
        'manual'
    ),
]

# latex_logo = None
# latex_use_parts = False
# latex_show_pagerefs = False
# latex_show_urls = False
# latex_appendices = []
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

man_pages = []
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = []
# texinfo_appendices = []
# texinfo_domain_indices = True
# texinfo_show_urls = 'footnote'
# texinfo_no_detailmenu = False
