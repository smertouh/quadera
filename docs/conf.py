# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory
# =============================================================================

"""
SpectroChemPy documentation build configuration file

"""

import sys
import sphinx_rtd_theme
import spectrochempy

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation general, use os.path.abspath to make it absolute, like shown
# here : sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*') or your
# custom ones.

# sys.path.append(os.path.abspath('../sphinxext'))

# hack to make import
sys._called_from_sphinx = True

extensions = \
    [
    'spectrochempy.sphinxext.autodocsumm',
    'nbsphinx',
    'sphinx.ext.mathjax',
    'sphinxcontrib.bibtex',
    'sphinx_gallery.gen_gallery',
    #'jupyter_sphinx.embed_widgets',
    'spectrochempy.sphinxext.traitlets_sphinxdoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'matplotlib.sphinxext.plot_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',  # 'sphinx.ext.napoleon',
    'numpydoc',
    ]

# Numpy autodoc attributes
numpydoc_show_class_members = False
numpydoc_use_plots = True
numpydoc_class_members_toctree = True

# # Napoleon settings
# napoleon_google_docstring = False
# napoleon_numpy_docstring = True
# napoleon_include_init_with_doc = False
# napoleon_include_private_with_doc = False
# napoleon_include_special_with_doc = False
# napoleon_use_admonition_for_examples = True
# napoleon_use_admonition_for_notes = True
# napoleon_use_admonition_for_references = True
# napoleon_use_ivar = True
# napoleon_use_param = True
# napoleon_use_rtype = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = "spectrochempy"
copyright = spectrochempy.application.__copyright__

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

version = spectrochempy.application.__version__.split('+')[0]
release = spectrochempy.application.__release__.split('+')[0]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['**.ipynb_checkpoints']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.

from spectrochempy.utils.rstutils import rst_epilog

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = ['_static']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/scpy.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'spectrochempydoc'

trim_doctests_flags = True

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',  # ''letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r"""\usepackage[utf8]{inputenc}
                \usepackage[T1]{fontenc}
             """,
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass  [
# howto/manual]).
latex_documents = [(
'index', 'spectrochempy.tex', 'SpectroChemPy Documentation', 'LCS',
'manual'), ]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/scpy.png"

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'spectrochempy', 'SpectroChemPy Documentation', ['LCS'], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [(
'index', 'spectrochempy', 'SpectroChemPy Documentation', 'LCS',
'SpectroChemPy', 'Online description of project.', 'Miscellaneous'), ]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'


# -- Options for Epub output --------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = 'SpectroChemPy'
epub_author = spectrochempy.application.__author__
epub_publisher = 'LCS'
epub_copyright = copyright

# The language of the text. It defaults to the language option
# or en if the language is not set.
# epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
# epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
# epub_identifier = ''

# A unique identification for the text.
# epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
# epub_cover = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_post_files = []

# A list of files that should not be packed into the epub file.
# epub_exclude_files = []

# The depth of the table of contents in toc.ncx.
# epub_tocdepth = 3

# Allow duplicate toc entries.
# epub_tocdup = True

# ----------------
# Autosummary
# -----------------

autosummary_generate = True

autoclass_content = 'both'  # Both the class’ and the __init__ method’s
# docstring are concatenated and inserted.

autodoc_default_flags = ['autosummary']

exclusions = (
    'with_traceback', 'with_traceback', 'observe', 'unobserve', 'observe',
    'cross_validation_lock', 'unobserve_all', 'class_config_rst_doc',
    'class_config_section', 'class_get_help', 'class_print_help',
    'section_names', 'update_config', 'clear_instance',
    'document_config_options', 'flatten_flags', 'generate_config_file',
    'initialize_subcommand', 'initialized', 'instance',
    'json_config_loader_class', 'launch_instance', 'setup_instance',
    'load_config_file',
    'parse_command_line', 'print_alias_help', 'print_description',
    'print_examples', 'print_flag_help', 'print_help', 'print_subcommands',
    'print_version', 'python_config_loader_class', 'raises',)


def autodoc_skip_member(app, what, name, obj, skip, options):
    exclude = name in exclusions or 'trait' in name
    return skip or exclude


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.add_stylesheet("spectrochempy.css")  # also can be a full URL
    # app.add_stylesheet("ANOTHER.css")
    # app.add_stylesheet("AND_ANOTHER.css")


# Sphinx-gallery ------------------

# Generate the plots for the gallery

sphinx_gallery_conf = {
    'plot_gallery': 'True',
    'backreferences_dir': 'gen_modules/backreferences',
    'doc_module': ('spectrochempy', ), 'reference_url': {
        'spectrochempy': None,
        #'matplotlib': 'https://matplotlib.org',
        'numpy': 'https://docs.scipy.org/doc/numpy',
        'sklearn': 'https://scikit-learn.org/stable',
        'ipython': 'https://ipython.readthedocs.org/en/stable/',
    },

    # path to the examples scripts
    'examples_dirs': 'user/examples',

    # path where to save gallery generated examples
    'gallery_dirs': 'user/auto_examples',
                        'user/expected_failing_examples':
        [],

}

# nbsphinx ---------------------------------------------------
# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

# Execute notebooks before conversion: 'always', 'never', 'auto' (default)
nbsphinx_execute = 'always'
nbsphinx_allow_errors = True

# Use this kernel instead of the one stored in the notebook metadata:
nbsphinx_kernel_name = 'python3'


# configuration for intersphinx -------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7/', None),
    'pytest': ('https://docs.pytest.org/latest/', None),
    'ipython': ('https://ipython.readthedocs.io/en/stable/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    #'matplotlib': ('https://matplotlib.org', None)
}


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return \
    "https://bitbucket.org/spectrocat/spectrochempy/src/spectrochempy/%s.py" \
    % filename


