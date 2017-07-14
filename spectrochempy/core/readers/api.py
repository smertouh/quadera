# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-
#
# =============================================================================
# Copyright (©) 2015-2017 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =============================================================================



# register to dataset

from ..dataset.api import NDDataset

from .readjdx import read_jdx
from .readomnic import read_omnic
from .readdso import read_dso
from .nmr import read_bruker_nmr

setattr(NDDataset, 'read_dso', read_dso)
setattr(NDDataset, 'read_jdx', read_jdx)
setattr(NDDataset, 'read_omnic', read_omnic)
setattr(NDDataset, 'read_spg', read_omnic)
setattr(NDDataset, 'read_spa', read_omnic)
setattr(NDDataset, 'read_bruker_nmr', read_bruker_nmr)

# make also the reader available for the API
__all__ = ['read_dso','read_jdx','read_omnic',
           'read_bruker_nmr']