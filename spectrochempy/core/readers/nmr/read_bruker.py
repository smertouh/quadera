# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2016 Christian Fernandez
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
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

""" Bruker file (single dimension FID or multidimensional SER) importers
"""

# =============================================================================
# Standard python imports
# =============================================================================
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import glob
import logging
import os

# =============================================================================
# Third party imports
# =============================================================================
import numpy as np

from nmrglue.fileio.bruker import read, read_pdata, read_lowmem

#TODO: make a conda install for nmrglue

# unit_conversion,
# =============================================================================
# Local imports
# =============================================================================
from ...dataset import Meta
from ...dataset import Axis
from ...units import ur, Quantity
from .parameter import nmr_valid_meta

import logging
log = logging.getLogger()
print('log_level', log.level)
# =============================================================================
# Constants
# =============================================================================

FnMODE = ["undefined", "QF", "QSEQ", "TPPI", "STATES", "STATES-TPPI",
          "ECHO-ANTIECHO"]
AQ_mod = ["QF", "QSIM", "QSEQ", "DQD"]

# =============================================================================
# Utilities
# =============================================================================

def _get_par_files(_dir, _procno, _processed=False):
    # get all possible parameters files
    parfiles = []
    pdir = os.path.join(_dir, "pdata", _procno)
    la = glob.glob(os.path.join(_dir, "acqu*"))
    la = map(os.path.basename, la)
    for _item in la:
        if not _processed:
            parfiles.append(_item)
        else:
            parfiles.append(os.path.join('..', '..', _item))
    lp = glob.glob(os.path.join(pdir, "proc*"))
    lp = map(os.path.basename, lp)
    for _item in lp:
        if not _processed:
            parfiles.append(os.path.join('pdata', _procno, _item))
        else:
            parfiles.append(_item)
    if _processed:
        _dir = pdir
    return _dir, parfiles

# =============================================================================
# Digital filter functions
# =============================================================================
# Extracted from nmrglue.fileio.bruker.py (BSD License)

# Table of points to frequency shift Bruker data to remove digital filter
# (Phase is 360 degrees * num_pts)
# This table is an 'un-rounded' version base on the table by
# W.M. Westler and F. Abildgaard's offline processing note, online at:
# http://www.boc.chem.uu.nl/static/local/prospectnd/dmx_digital_filters.html
# and the updated table with additional entries at:
# http://sbtools.uchc.edu/help/nmr/nmr_toolkit/bruker_dsp_table.asp

# The rounding in the above tables appear to be based on k / (2*DECIM)
# for example 2 : 44.75   = 44 + 3/4
#             4 : 66.625  = 66 + 5/8
#             8 : 68.563 ~= 68 + 9/16 = 68.5625
# Using this the un-rounded table was created by checking possible unrounded
# fracions which would round to those in the original table.

bruker_dsp_table = {
    10: {
        2    : 44.75,
        3    : 33.5,
        4    : 66.625,
        6    : 59.083333333333333,
        8    : 68.5625,
        12   : 60.375,
        16   : 69.53125,
        24   : 61.020833333333333,
        32   : 70.015625,
        48   : 61.34375,
        64   : 70.2578125,
        96   : 61.505208333333333,
        128  : 70.37890625,
        192  : 61.5859375,
        256  : 70.439453125,
        384  : 61.626302083333333,
        512  : 70.4697265625,
        768  : 61.646484375,
        1024 : 70.48486328125,
        1536 : 61.656575520833333,
        2048 : 70.492431640625,
    },
    11: {
        2    : 46.,
        3    : 36.5,
        4    : 48.,
        6    : 50.166666666666667,
        8    : 53.25,
        12   : 69.5,
        16   : 72.25,
        24   : 70.166666666666667,
        32   : 72.75,
        48   : 70.5,
        64   : 73.,
        96   : 70.666666666666667,
        128  : 72.5,
        192  : 71.333333333333333,
        256  : 72.25,
        384  : 71.666666666666667,
        512  : 72.125,
        768  : 71.833333333333333,
        1024 : 72.0625,
        1536 : 71.916666666666667,
        2048 : 72.03125
    },
    12: {
        2    : 46.,
        3    : 36.5,
        4    : 48.,
        6    : 50.166666666666667,
        8    : 53.25,
        12   : 69.5,
        16   : 71.625,
        24   : 70.166666666666667,
        32   : 72.125,
        48   : 70.5,
        64   : 72.375,
        96   : 70.666666666666667,
        128  : 72.5,
        192  : 71.333333333333333,
        256  : 72.25,
        384  : 71.666666666666667,
        512  : 72.125,
        768  : 71.833333333333333,
        1024 : 72.0625,
        1536 : 71.916666666666667,
        2048 : 72.03125
    },
    13: {
        2    : 2.75,
        3    : 2.8333333333333333,
        4    : 2.875,
        6    : 2.9166666666666667,
        8    : 2.9375,
        12   : 2.9583333333333333,
        16   : 2.96875,
        24   : 2.9791666666666667,
        32   : 2.984375,
        48   : 2.9895833333333333,
        64   : 2.9921875,
        96   : 2.9947916666666667
    }
}

def _remove_digital_filter(dic, data):
    """
    Remove the digital filter from Bruker data.
    nmrglue modified Digital Filter Processing
    """
    log.debug('Bruker digital filter...')

    if 'acqus' not in dic:
        raise ValueError("dictionary does not contain acqus parameters")

    if 'DECIM' not in dic['acqus']:
        raise ValueError("dictionary does not contain DECIM parameter")
    decim = dic['acqus']['DECIM']

    if 'DSPFVS' not in dic['acqus']:
        raise ValueError("dictionary does not contain DSPFVS parameter")
    dspfvs = dic['acqus']['DSPFVS']

    if 'GRPDLY' not in dic['acqus']:
        grpdly = 0
    else:
        grpdly = dic['acqus']['GRPDLY']

    if grpdly > 0:  # use group delay value if provided (not 0 or -1)
        phase = grpdly

    # Determine the phase correction
    else:
        if dspfvs >= 14:  # DSPFVS greater than 14 give no phase correction.
            phase = 0.
        else:  # loop up the phase in the table
            if dspfvs not in bruker_dsp_table:
                raise ValueError("dspfvs not in lookup table")
            if decim not in bruker_dsp_table[dspfvs]:
                raise ValueError("decim not in lookup table")
            phase = bruker_dsp_table[dspfvs][decim]

    # fft
    si = data.shape[-1]
    pdata = np.fft.fftshift(np.fft.fft(data, si, axis=-1), -1) / float(
            si / 2)
    pdata = (pdata.T - pdata.T[0]).T  # TODO: this allow generally to
    # remove Bruker smiles, not so sure actually

    # Phasing
    si = float(pdata.shape[-1])
    ph = 2.0j * np.pi * phase * np.arange(si) / si
    pdata = pdata * np.exp(ph)

    # ifft
    data = np.fft.ifft(np.fft.ifftshift(pdata, -1), si, axis=-1) * float(
            si / 2)

    # remove last points * 2
    rp = 4 * (phase // 2)
    data[..., -int(rp):] = 0j
    td = dic['acqus']['TD'] // 2
    data = data[..., :int(td)]

    log.debug('Bruker digital filter: removed %s points'%rp)

    return data



# def _scale(meta, dim=-1, reverse=None):
#     """
#     private function: Compute scale for a given axis.
#     """
#
#     # import parameter to convert units
#     sw = float(meta.sw_h[dim])
#     sfo1 = float(meta.sfo1[dim])
#     bf1 = float(meta.bf1[dim])
#     sf = float(meta.sf[dim])
#     si = max(float(meta.si[dim])-1, 1)
#     td = float(meta.td[dim])
#
#     sr = (sf - bf1) * 1.0e6
#     o1 = (sfo1 - bf1) * 1.0e6
#
#     # set the spectral parameters
#     # (si,   sw_h, bf1, -sr + o1)
#     # size,   sw, obs,      car)  (correspondance with nmrglue udic)
#
#     # derived units (these are in ppm)
#
#     fact = 2.0 if meta.fnmode[dim] in [3, 4, 5, 6] or else 1.0
#     if meta.isfreq[dim]:
#         delta = -sw * fact / (si * bf1)
#         first = (-sr + o1)/ bf1 - delta * si / 2.
#
#     if reverse is None:
#         reverse = meta.reverse
#
#     if reverse:
#         return scal()[::-1]
#     else:
#         return scal()

# =============================================================================
# bruker import function
# =============================================================================

def read_bruker_nmr(self, *args, **kwargs):
    """
    Import Bruker dataset

    Parameters
    ----------
    path: str, optional
        path of the Bruker directory. It path is None, at least the parameters
        `data_dir`, `user`, `name`, `expno` must be provided.
    data_dir: str,
        main strorage directory, optional
    user: str, optional
        user name of the dataset
    name: str, optional
        name of the dataset
    expno: int, optional
        experiment number
    expnos: A list of expno
    processed: bool, optioanl, default is False
        should we load already bruker processed files
    procno: int
        processing number
    silent: bool
        should we output details

    """

    log.debug('Bruker imports...')

    expnos = False
    data_dir = kwargs.get('data_dir', '')
    user = kwargs.get('user', '')
    name = kwargs.get('name', '')

    # reading single expno
    expno = kwargs.get('expno', None)

    if args:
        # look in args
        path = os.path.expanduser(args[0])

    if not os.path.exists(path):
        # look in kargs
        path = os.path.expanduser(kwargs.get('path', path))

    if not os.path.exists(path):
        # look alternative definitions
        path_alt = os.path.join(str(data_dir), str(user), 'nmr', str(name),
                         str(expno))

        if os.path.exists(path_alt):
            path = path_alt

    if not os.path.exists(path):
        # look multiple
        expnos = kwargs.get('expnos', False)
        if expnos:
             path = os.path.join(str(data_dir), str(user), 'nmr', str(name))

    # path must be pointing to a valid bruker directory
    if not os.path.exists(path):
        raise IOError("This path '{}' doesn't exist".format(path))

    # path is expected to be a directory
    if os.path.isdir(path) is not True:
        raise IOError("directory '{}' does not exist".format(path))

    # Determine some parameter automatically
    processed = kwargs.get('processed', False)  # read unprocessed by default

    #TODO: make a full implementation of read_proc
    if processed:
        raise NotImplementedError('Not yet fully implemented... do not use!')

    lowmem = kwargs.get('lowmem', False)  # load all in memero by default
    if lowmem :
        log.debug('import with low memory handling (lowmem)')

    # -------------------------------------------------------------------------
    # start reading ....
    # -------------------------------------------------------------------------

    procno = '1'
    p = path.split(os.path.sep)
    if 'pdata' in p:
        _pd = p.index('pdata')
        procno = p[_pd + 1]
        if not p[0]:
            p[0] = os.path.sep
        path = os.path.join(*p[:_pd])
        processed = True
    procno = kwargs.get('procno', procno)

    expnos = kwargs.get('expnos', False)  # List of expnos?
    paths = None
    if expnos:
        paths = [os.path.join(path, str(expno)) for expno in expnos]
    else:
        paths = [path, ]

    # start loop on the paths

    list_data = []
    list_meta = []
    list_axes = []

    for idx, path in enumerate(paths):

        log.debug('Reading %d:%s'%(idx, path))

        # Acquisition parameters

        if os.path.isfile(os.path.join(path, "fid")):
            datatype = 'FID'
        elif os.path.isfile(os.path.join(path, "ser")):
            datatype = 'SER'
        elif expno is not None:
            if os.path.isfile(os.path.join(path, str(expno), "fid")):
                datatype = 'FID'
                path = os.path.join(path, str(expno))
            elif os.path.isfile(os.path.join(path, str(expno), "ser")):
                datatype = 'SER'
                path = os.path.join(path, str(expno))
        else:
            if not processed:
                log.warning('No binary fid or ser found in %s.\n'
                               'Try processed files...' % path)
                processed = True

        if os.path.isfile(os.path.join(path, 'pdata', procno, '1r')):
            if not datatype or processed:
                datatype = '1D'
        elif os.path.isfile(os.path.join(path, 'pdata', procno, '2rr')):
            if not datatype or processed:
                datatype = '2D'
        elif os.path.isfile(os.path.join(path, 'pdata', procno, '3rrr')):
            if not datatype or processed:
                datatype = '3D'
        else:
            if not datatype:
                raise IOError(
                        "No Bruker binary file could be found in %s" % path)
            elif processed:
                log.warning("No processed Bruker binary file could be found"
                               " in %s. Use fid's." % path)

        # we read all parameters file whatever the datatype
        npath, par_files = _get_par_files(path, procno, processed)

        if datatype in ['FID', 'SER']:
            if not lowmem:
                dic, data = read(npath, acqus_files=par_files,
                             read_pulseprogram=False)
            else:
                dic, data = read_lowmem(npath, acqus_files=par_files,
                             read_pulseprogram=False)

            # # look the case whn the reshaping was not correct
            # # for example, this happen when the number
            # # of accumulated row was incomplete
            # if datatype in ['SER'] and data.ndim == 1:
            #     # we must reshape using the acqu parameters
            #     td1 = dic['acqu2']['TD']
            #     try:
            #         data = data.reshape(td1, -1)
            #     except ValueError:
            #         try:
            #             td = dic['acqu']['TD'] // 2
            #             data = data.reshape(-1, td)
            #         except ValueError:
            #             raise ValueError(
            #                     "Inconsistency between TD's and data size")
            #
            # # reduce to td
            # ntd = dic['acqus']['TD'] // 2
            # data = data[...,
            #               :ntd]  # necessary for agreement with bruker data and
            # phase
        else:

            log.debug('Reading processed %d:%s'%(idx, path))

            dic, data = read_pdata(npath, procs_files=par_files, )

        # Clean dict for pdata keys
        for key in dic.keys():
            if key.startswith('pdata'):
                newkey = key.split(os.path.sep)[-1]
                dic[newkey] = dic.pop(key)

        # Eliminate the digital filter
        if datatype in ['FID', 'SER'] and kwargs.get('remove_digital_filter', True):
            data = _remove_digital_filter(dic, data)

        # we now make some rearrangement of the dic
        # to have something more user friendly
        # we assume that all experiments have similar (important)
        # parameters so that the experiments are
        # compatibles

        meta = Meta()  # This is the parameter dictionary

        keys = sorted(dic.keys())

        # we need the ndim of the data
        parmode = int(dic['acqus']['PARMODE'])

        # read the acqu and proc
        valid_keys = list(zip(*nmr_valid_meta))[0]
        keys_units = dict(nmr_valid_meta)

        for item in keys:

            if item[:4] in ['acqu', 'proc']:
                dim = parmode
                if len(item) > 4 and item[4] in ['2', '3']:
                    dim = parmode - int(item[4])

                for key in sorted(dic[item]):
                    if key.startswith('_') or key.lower() not in valid_keys:
                        continue

                    value = dic[item][key]
                    units = ur(keys_units[key.lower()]) \
                                            if keys_units[key.lower()] else None
                    #print( key, value, units)
                    if units is not None:
                        if isinstance(value, (float, int)):
                            value = value * units # make a quantity
                        elif isinstance(value, list) and isinstance(value[0],
                                                                    (float,int)):
                            value = np.array(value) * units

                    if not item.endswith('s'): # initial parameter

                        if dim == parmode:
                            meta[key.lower()] = [value, ]
                        else:
                            meta[key.lower()].insert(0, value)

                    else: # status parameters (replace initial)
                        try:
                            meta[key.lower()][dim] = value
                        except:
                            pass

            else:

                meta[item.lower()] = dic[item]

        # Warning: from now all parameter keys are lowercase.

        # correct some initial values

        meta.encoding = [0]*(parmode+1)
        meta.iscomplex = [False] * (parmode + 1)

        if datatype in ['FID', 'SER']:
            meta.td[-1] = data.shape[-1]
            if meta.tdeff is None:
                meta.tdeff = meta.td
            meta.tdeff[-1] = meta.td[-1]
            meta.isfreq = [False]
            meta.encoding[-1] = AQ_mod[meta.aq_mod[-1]]
            meta.iscomplex[-1] = meta.aq_mod[-1] > 0

        if datatype in ['SER']:
            meta.td[-2] = data.shape[-2]
            meta.tdeff[-2] = meta.td[-2]
            meta.isfreq.insert(0, False)

            if meta.fnmode[-2] == 0:
                # For historical reasons,
                # MC2 is interpreted when the acquisition status
                # parameter FnMODE has the value undefined, i.e. 0
                if meta.mc2 is not None:
                    meta.fnmode[-2] = meta.mc2[-2] + 1

            meta.encoding[-2] = FnMODE[meta.fnmode[-2]]
            meta.iscomplex[-2] = meta.fnmode[-2] > 1

            if parmode == 2:
                meta.td[-3] = data.shape[-3]
                meta.tdeff[-3] = meta.td[-3]
                meta.isfreq.insert(0, False)
                if meta.fnmode[-3] == 0 and  meta.mc2 is not None:
                    meta.fnmode[-3] = meta.mc2[-3] + 1
                meta.encoding[-3] = FnMODE[meta.fnmode[-3]]
                meta.iscomplex[-3] = meta.fnmode[-3] > 1

        # correct TD, so it is the number of complex points, not the number of data
        # not for the last dimension which is already correct
        for axis in range(parmode):
            if meta.iscomplex[axis]:
                meta.td[axis] = meta.td[axis] //2

        if datatype in ['1D', '2D', '3D']:
            meta.si = [si for si in data.shape]
            meta.isfreq = [True]*(parmode+1)  # at least we assume this


        # this transformation is to make data coherent with bruker processsing
        if meta.iscomplex[-1]:
            data = np.conj(data * np.exp(np.pi*1j/2.))

        # normalised amplitudes to ns=1 and rg=1
        def _norm(dat):
            fac = float(meta.ns[-1]) * float(meta.rg[-1])
            meta.rgold = [meta.rg[-1]]
            meta.rg[-1] = 1.
            meta.nsold = [meta.ns[-1]]  # store the old value of NS
            meta.ns[-1] = 1
            dat /= fac
            return dat

        data = _norm(data)

        # add some additional inforation in meta
        meta.expno = [int(os.path.basename(path))]

        # and the metadata (and make them readonly)
        meta.datatype = datatype
        meta.pathname = path
        list_meta.append(meta)

        # make the corresponding axis
        log.debug('Create axis...')
        axes = []
        axe_range = range(parmode+1)
        for axis in axe_range:
            if not meta.isfreq[axis]:
                # the axis is in time units
                dw = (1./meta.sw_h[axis]).to('us')
                axespoints = np.arange(meta.td[axis])
                axe = Axis(axespoints*dw,
                           name = 'F{}'.format(axis),
                           title = "acquisition time")
                axes.append(axe)
            else:
                raise NotImplementedError('Not yet implemented')
        list_axes.append(axes)

        # # store also the varpars of the series
        # varpars = kargs.get('varpars')
        # if isinstance(varpars, str):
        #     varpars = varpars.split()
        #     if len(varpars) == 1:
        #         # this should be one of the dic parameters
        #         lvarpars.append(adic.par[varpars[0]])  # store the variable
        #     elif len(varpars) == 2:
        #         lvarpars.append(adic.par[varpars[0]][
        #                             int(varpars[1])])  # store the variable
        #     ldates.append(adic.par.DATE)  # and the date
        # elif isinstance(varpars, list):
        #     # this should be a list of parameters
        #     p = []
        #     for var in varpars:
        #         p.append(adic.par[var])
        #     lvarpars.append(p)  # store the variable
        #     ldates.append(adic.par.DATE)  # and the date

        # store temporarily these data
        log.debug('data read finished: type: %s' % datatype)

        list_data.append(data)

    if len(list_data) == 1:
        log.debug('One experiment read. Make it the current dataset')

        self.data = list_data[0]  # complex data will be transformed
                                  # automatically into an interleaved
                                  # data array
        for axis, cplex in enumerate(meta.iscomplex):
            if cplex:
                self.set_complex(axis)

        self.meta.update(list_meta[0])
        self.meta.readonly = True
        self.axes = list_axes[0]

    else:
        # case of multiple experiments to merge

        #find difference in data.shape

        diff = False
        shape = list_data[0].shape
        for data in list_data[1:]:
            if np.any(data.shape != shape):
                diff = True

        if not diff:
            # find difference in axes
            axes = list_axes[0]
            for a in list_axes[1:]:
                if np.any(a != axes):
                    diff = True

        if not diff:
            log.info('the experiments look perfectly compatibles'
                        ' regarding the shape and the axis!')

        # find what are the differences in meta
        meta= list_meta[0]

        mkeys = set()  # will stroe the modified keys
        from spectrochempy.core.utils import dict_compare
        for i, d1 in enumerate(list_meta):
            for j, d2 in enumerate(list_meta[i+1:]):
                added, removed, modified, _ = \
                dict_compare(d1.to_dict(), d2.to_dict(), check_equal_only=False)
                mkeys = mkeys.union(added)
                mkeys = mkeys.union(removed)
                mkeys = mkeys.union(modified)

        # some keys should not vary for homogeneous data but lets the
        # user decide
        log.info("keys which have varied: %s" % mkeys)

        mkeys = list(mkeys)
        meta_diffs = {}
        for key in mkeys:
            # find the key variation
            # WARNING: restriction is that we use only the direct observation
            # dimension to get the values (so a variation in another dimension
            # will not be seen!
            if isinstance(meta[key][-1], Quantity):
                meta_diffs[key] = [meta[key][-1].m for meta in list_meta]
                meta_diffs[key] = meta_diffs[key] * meta[key][-1].units
            else:
                meta_diffs[key] = [meta[key][-1] for meta in list_meta]

        # we can now store the meta for the datset object
        self.meta.update(list_meta[-1])
        # we additionaly set the list of variable parameters whch will indicate
        # the orders of the labels for the new axis
        self.meta.labels = mkeys
        self.meta.readonly = True  # and from now no more modifications in metas

        # by default and if it is possible we try to create an homogeneous
        # NDDataset (needs same TD, SFO1, etc.. and of course same data.shape)
        merge_method = kwargs.get('merge_method', 'create_array')
        if merge_method == 'create_array' and not diff:
            # we create un array with the list of array
            newdata = np.stack(list_data, axis=0)

            # store it in the current datset
            self.data = newdata
            # complexity?
            complexity = [False] + meta.iscomplex
            for axis, iscomplex in enumerate(complexity):
                if iscomplex:
                    self.set_complex(axis)

            # new axes
            vkey = kwargs.get('var_key', None)
            vkey = vkey.lower()

            if vkey is not None and vkey in mkeys:
                ax = meta_diffs[vkey]
                title = vkey
            else:
                ax = np.arange(newdata.shape[0])
                title = '-nd-'
            axis = Axis(ax, title = title)

            labels = []
            for i in range(len(ax)):
                if len(mkeys)>1:
                    label = []
                    for key in mkeys:
                        label.append(meta_diffs[key][i])
                else:
                    label = meta_diffs[mkeys[-1]][i]
                labels.append(label)
            labels = np.array(labels, dtype=object)
            axis.labels = labels

            # now make the axes it in the current dataset
            # only one axes of the list is taken: they are all the same
            # in principle... if not problem above or the experiments
            # are not compatibles
            self.axes = [axis]+list_axes[-1]

###EOF######################################################################