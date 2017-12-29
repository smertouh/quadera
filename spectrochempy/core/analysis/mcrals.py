# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2018 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory
# =============================================================================


__all__ = ['McrAls']

__dataset_methods__ = ['McrAls']


import logging

log = logging.getLogger(__name__)
import numpy as np

from spectrochempy.dataset.nddataset import NDDataset


def McrAls(X, guess, **options):
    """Performs MCR-ALS of a dataset knowing the initial C or St matrix

    Parameters
    -----------
    tol : float, optional, default=1e-3
        convergence tolerance
    maxit : maximum number of ALS minimizations
    maxdiv : maximum number of non-converging iteratiobs
    nonnegConc : array or tuple indicating species non-negative concentration
                   profiles. For instance [1, 0, 1] indicates that species #0
                   and #2 have non-negative conc profiles while species #1
                   can have negative concentrations
                   Default [1, ..., 1]  (only non-negative cocentrations)
    unimodConc : array or tuple indicating species having unimodal concentrations
                   profiles.
                   Default [1, ..., 1]  (only unimodal cocentration profiles)
    nonnegSpec : array or tuple indicating species having non-negative spectra
                   Default [1, ..., 1]  (only non-negative spectra)
    unimodSpec : array or tuple indicating species having unimodal spectra
                   Default [0, ..., 0]  (no unimodal cocentration profiles)

    """
    # TODO: cmake a test file

    # check initial data
    initConc, initSpec = False, False
    if X.shape[0] == guess.shape[0]:
        initConc = True
        C = guess.copy()
        nspecies = C.shape[1]

    elif X.guess[1] == guess.shape[1]:
        initSpec = True
        St = guess.copy()
        nspecies = St.shape[0]
    else:
        raise ValueError('the dimensions of initial concentration '
                         'or spectra dataset do not match the data')

    nspc, nwn = X.shape

    # check options

    tol = options.get('tol', 0.001)

    maxit = options.get('maxit', 50)

    maxdiv = options.get('maxdiv', 5)

    nonnegConc = options.get('nonnegConc', [1] * nspecies)

    unimodConc = options.get('unimodConc', [1] * nspecies)

    unimodTol = options.get('unimodTol', 1.1)

    unimodMod = options.get('unimodMod', 'strict')

    monoDecConc = options.get('monoDecConc', [0] * nspecies)

    monoDecTol = options.get('monoDecTol', 1.1)

    monoIncConc = options.get('monoIncConc', [0] * nspecies)

    monoIncTol = options.get('monoIncTol', 1.1)

    nonnegSpec = options.get('nonnegSpec', [1] * nspecies)

    #    if ('unimodSpec' in options): unimodSpec = options['unimodSpec']
    #    else: unimodSpec = np.zeros((1, nspecies))

    # compute initial spectra or concentrations   (first iteration...) 
    if initConc:
        C_i = C.data
        St_i, _, _, _ = np.linalg.lstsq(C_i, X.data)
        St = NDDataset(St_i)
        St.name = C.name + ' \ ' + X.name
        St.axes[0] = C.axes[0]
        St.axes[1] = X.axes[1]
    if initSpec:
        St_i = St.data
        Ct_i, _, _, _ = np.linalg.lstsq(St_i.T, X.data.T)
        C_i = Ct_i.T
        C = NDDataset(C_i)
        C.name = X.name + ' / ' + St.name
        C.axes[0] = St.axes[0]
        C.axes[1] = X.axes[1]

    delta = tol + 1
    niter = 0
    ndiv = 0
    res = np.infty

    while delta >= tol and niter < maxit and ndiv < maxdiv:

        Ct_i, _, _, _ = np.linalg.lstsq(St_i.T, X.data.T)
        C_i = Ct_i.T
        niter += 1

        # Force non-negative concentration
        if np.nonzero(nonnegConc)[0].size != 0:
            for s in np.nditer(np.nonzero(nonnegConc)):
                C_i[:, s] = C_i[:, s].clip(min=0)

        # Force unimodal concentration
        if np.nonzero(unimodConc)[0].size != 0:
            for s in np.nditer(np.nonzero(unimodConc)):
                maxid = np.argmax(C_i[:, s])
                curmax = C_i[maxid, s]
                curid = maxid

                while curid > 0:
                    curid -= 1
                    if C_i[curid, s] > curmax * unimodTol:
                        if unimodMod == 'strict':
                            C_i[curid, s] = C_i[curid + 1, s]
                        if unimodMod == 'smooth':
                            C_i[curid, s] = (C_i[curid, s] + C_i[
                                curid + 1, s]) / 2
                            C_i[curid + 1, s] = C_i[curid, s]
                            curid = curid + 2
                    curmax = C_i[curid, s]

                curid = maxid
                while curid < nspc - 1:
                    curid += 1
                    if C_i[curid, s] > curmax * unimodTol:
                        if unimodMod == 'strict':
                            C_i[curid, s] = C_i[curid - 1, s]
                        if unimodMod == 'smooth':
                            C_i[curid, s] = (C_i[curid, s] + C_i[
                                curid - 1, s]) / 2
                            C_i[curid - 1, s] = C_i[curid, s]
                            curid = curid - 2
                    curmax = C_i[curid, s]

        # Force monotonic increase  
        if np.nonzero(monoIncConc)[0].size != 0:
            for s in np.nditer(np.nonzero(monoIncConc)):
                for curid in np.arange(nspc - 1):
                    if C_i[curid + 1, s] < C_i[curid, s] / monoIncTol:
                        C_i[curid + 1, s] = C_i[curid, s]

        # Force monotonic decrease   
        if np.nonzero(monoDecConc)[0].size != 0:
            for s in np.nditer(np.nonzero(monoDecConc)):
                for curid in np.arange(nspc - 1):
                    if C_i[curid + 1, s] > C_i[curid, s] * monoDecTol:
                        C_i[curid + 1, s] = C_i[curid, s]

        St_i, _, _, _ = np.linalg.lstsq(C_i, X.data)

        # Force non-negative spectra
        if np.nonzero(nonnegSpec)[0].size != 0:
            for s in np.nditer(np.nonzero(nonnegSpec)):
                St_i[s, :] = St_i[s, :].clip(min=0)

        # compute residuals          
        res2 = np.linalg.norm(X.data - np.dot(C_i, St_i))
        delta = res2 - res
        res = res2
        log.info(niter, res2, delta)

        if delta > 0:
            ndiv += 1
        else:
            delta = -delta

    C.data = C_i
    St.data = St_i

    return C, St