#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# navis documentation build configuration file, created by
# sphinx-quickstart on Sun Jul  9 22:17:00 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import numpydoc
import sphinx_bootstrap_theme
import json

import matplotlib as mpl
mpl.use("Agg")

import matplotlib.sphinxext.plot_directive
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

#This needs to be removed in order to built locally
import mock
MOCK_MODULES = ['sklearn', 'igraph' , 'tqdm', 'pandas', 'bpy', 'bmesh',
                'pyoctree', 'PyQt5', 'pyqt5', 'scipy.sparse', 'scipy.cluster',
                'scipy.cluster.hierarchy', 'scipy.interpolate',
                'scipy.spatial.distance',
                'numpy', 'scipy', 'scipy.spatial', 'ConvexHull', 'scipy.spatial.ConvexHull',
                'rpy2', 'rpy2.robjects','rpy2.robjects.packages', 'png',
                'rpy2.robjects.packages.importr', 'rpy2.robjects.pandas2ri' ,
                'plotly', 'plotly.plotly', 'plotly.offline', 'plotly.graph_objs',
                'matplotlib.pyplot', 'plt', 'matplotlib.externals',
                'matplotlib.externals.six', 'matplotlib.externals.six.moves',
                'matplotlib.collections','matplotlib.collections.PolyCollection', 'matplotlib.lines', 'matplotlib.patches', 'matplotlib.colors',
                'mpl_toolkits.mplot3d','mpl_toolkits.mplot3d.proj3d','matplotlib.colors', 'mpl_toolkits.mplot3d.art3d',
                'mpl_toolkits.mplot3d.art3d.Line3DCollection', 'proj3d', 'pylab',
                'mlines','mpatches','mcollections', 'mcl','Line3DCollection',
                'mathutils',
                'networkx', 'nx', 'requests', 'requests-futures', 'requests.exceptions',
                'imageio', 'py2cytoscape', 'py2cytoscape.data.cyrest_client', 'CyRestClient',
                'requests_futures.sessions', 'requests_futures.sessions.FuturesSession',
                'vispy','seaborn','vispy.geometry', 'vispy.gloo.util', 'vispy.gloo.util._screenshot']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

import navis
from navis.interfaces import cytoscape
from navis.interfaces import blender


# -- Make execution numbers in Jupyter notebooks ascending -------------------
source_path = os.path.dirname(os.path.abspath(__file__)) + '/source'
all_nb = [f for f in os.listdir(source_path) if f.endswith('.ipynb')]

for nb in all_nb:
    with open(os.path.join(source_path, nb), 'r') as f:
        data = json.load(f)
        i = 1
        for c in data['cells']:
            if c['cell_type'] == 'code':
                if 'execution_count' in c:
                    c['execution_count'] = i
                for o in c['outputs']:
                    if 'execution_count' in o:
                        o['execution_count'] = i
                i += 1

    with open(os.path.join(source_path, nb), 'w') as f:
        json.dump(data, f, indent=3)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    #'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    #'sphinx.ext.mathjax', # mathjax is interactive and configurable but can also misbehave when rendering - switched to imgmath instead
    'sphinx.ext.imgmath',
    'matplotlib.sphinxext.plot_directive',
    #'numpydoc'
]

# Include the example source for plots in API docs
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False

# generate autosummary pages
autosummary_generate = True
autoclass_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'navis'
copyright = '2018, Philipp Schlegel'
author = 'Philipp Schlegel'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = navis.__version__
# The full version, including alpha/beta/rc tags.
release = navis.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#
# today = ''
#
# Else, today_fmt is used as the format for a strftime call.
#
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
#html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_theme_options = {
    'source_link_position': "footer",
    'bootswatch_theme': "paper",
    'navbar_sidebarrel': False,
    'bootstrap_version': "3",
    'navbar_links': [
                     ("Install", "source/install"),
                     ("Tutorial", "source/intro"),
                     ("Examples", "source/example_gallery"),
                     ("API", "source/api"),
                     ],

    }

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
#
# html_title = 'navis v0.8'

# A shorter title for the navigation bar.  Default is the same as html_title.
#
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = '_static/favicon.png'

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
#
# html_last_updated_fmt = None

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#
# html_additional_pages = {}

# If false, no module index is generated.
#
# html_domain_indices = True

# If false, no index is generated.
#
# html_use_index = True

# If true, the index is split into individual pages for each letter.
#
# html_split_index = False

# If true, links to the reST sources are added to the pages.
#
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr', 'zh'
#
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
#
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'navisdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
     # The paper size ('letterpaper' or 'a4paper').
     #
     # 'papersize': 'letterpaper',

     # The font size ('10pt', '11pt' or '12pt').
     #
     # 'pointsize': '10pt',

     # Additional stuff for the LaTeX preamble.
     #
     # 'preamble': '',

     # Latex figure (float) alignment
     #
     # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'navis.tex', 'navis Documentation',
     'Philipp Schlegel', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#
# latex_use_parts = False

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# It false, will not define \strong, \code, 	itleref, \crossref ... but only
# \sphinxstrong, ..., \sphinxtitleref, ... To help avoid clash with user added
# packages.
#
# latex_keep_old_macro_names = True

# If false, no module index is generated.
#
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'navis', 'navis Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'navis', 'navis Documentation',
     author, 'navis', 'Neuron analysis toolbox for CATMAID data.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#
# texinfo_appendices = []

# If false, no module index is generated.
#
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#
# texinfo_no_detailmenu = False

def setup(app):
    app.add_stylesheet('style.css')