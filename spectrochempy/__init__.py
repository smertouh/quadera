# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2018 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
# Authors:
# christian.fernandez@ensicaen.fr
# arnaud.travert@ensicaen.fr
#
# This software is a computer program whose purpose is to provide a framework
# for processing, analysing and modelling *Spectro*scopic
# data for *Chem*istry with *Py*thon (SpectroChemPy). It is is a cross
# platform software, running on Linux, Windows or OS X.
#
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL-B
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# =============================================================================

"""During the initialization of this package, a `matplotlib` backend is set
and some `IPython` configurations are made.


"""
import sys
import warnings

from IPython.core.magic import UsageError
from IPython import get_ipython
import matplotlib as mpl

from pkg_resources import get_distribution, DistributionNotFound
from setuptools_scm import get_version
import  subprocess
import datetime

__all__ = ['__version__', '__release__', '__release_date__', '__copyright__']

# ----------------------------------------------------------------------------
# Backend
# ----------------------------------------------------------------------------

# .........................................................................
def _setup_backend_and_ipython(backend=None):
    """Backend and IPython matplotlib environ setup

    Here, we performs this setup before any call to `matplotlib.pyplot`
    that are performed later in this application

    ..Note:: This method is called automatically at the initialization step
        if the application is called from the command line

    Parameters
    ----------
    backend : str, optional
        backend to use, default = ``Qt5Agg``.

    """

    # change backend here before the project module is imported
    if backend == 'spectrochempy_gui':
        # this happen when the GUI is used
        backend = 'module://spectrochempy_gui.backend'
    # the current backend
    backend = mpl.get_backend()
    if backend == 'module://ipykernel.pylab.backend_inline'  or backend == \
             'MacOSX':
         # Force QT5
         backend = 'Qt5Agg'
         mpl.rcParams['backend.qt5'] = 'PyQt5'

    # if we are building the docs, in principle it should be done using
    # the builddocs.py located in the scripts folder
    if not 'builddocs.py' in sys.argv[0]:
        mpl.use(backend, warn = False, force = True)
    else:
        # 'agg' backend is necessary to build docs with sphinx-gallery
        mpl.use('agg', warn = False, force = True)

    ip = get_ipython()
    if ip is not None:
        if getattr(get_ipython(), 'kernel', None) is not None:
            # set the ipython matplotlib environments
            try:
                import ipympl
                ip.magic('matplotlib notebook')
            except UsageError as e:
                try:
                    ip.magic('matplotlib qt5')
                except:
                    pass
        else:
            try:
                ip.magic('matplotlib qt5')
            except:
                 pass

    return (ip, backend)

_setup_backend_and_ipython()

# ----------------------------------------------------------------------------
# Version
# ----------------------------------------------------------------------------

try:
    __release__ = get_distribution('spectrochempy').version
except DistributionNotFound:
    # package is not installed
    __release__ = '0.1.beta'

try:
    __version__ = get_version(root='..', relative_to=__file__)
except:
    __version__ = __release__


# ............................................................................
def _get_copyright():
    current_year = datetime.date.today().year
    copyright = '2014-{}'.format(current_year)
    copyright += ' - A.Travert and C.Fernandez @ LCS'
    return copyright

__copyright__ = _get_copyright()

# .............................................................................
def _get_release_date():
    try:
        return subprocess.getoutput(
            "git log -1 --tags --date='short' --format='%ad'")
    except:
        pass

__release_date__ = _get_release_date()

# ............................................................................
# other info

__url__ = "http://www-lcs.ensicaen.fr/spectrochempy"
__author__ = "C. Fernandez & A. Travert @LCS"
__license__ = "CeCILL-B license"


# ==============================================================================
# For documentation
# ==============================================================================

if __name__ == '__main__':
    print(__version__)
    print(__copyright__)
    print(__license__)
    print(__url__)







