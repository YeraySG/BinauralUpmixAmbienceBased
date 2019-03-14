#
# Based on Merimaa, J., Goodwin, M. M., & Jot, J.-M. (2007). Correlation-Based Ambience Extraction from Stereo Recordings. AES 123rd Convention, 1–15.
#

# K = num frequency bins
# M = num time frames


import numpy as np


def herm(ndarray):
    return np.conj(np.transpose(ndarray))


def autocorrelation(X,K,M,l=0.5):
    res = np.zeros((K,M),dtype='complex')
    for k in range(K):
        for m in range(M):
            r_last = res[k,m-1] if m>0 else 0
            r_now = np.power(np.abs(X[k,m]),2)
            res[k,m] = ( l * r_last) + ( (1-l) * r_now )
    return res


def cross_correlation(X1,X2,K,M,l=0.5):
    res = np.zeros((K,M),dtype='complex')
    for k in range(K):
        for m in range(M):
            r_last = res[k,m-1] if m>0 else 0
            r_now = X1[k,m]*np.conj(X2[k,m])
            res[k,m] = ( l * r_last) + ( (1-l) * r_now )
    return res


def cross_correlation_coef(X1,X2,K,M,l=0.5):
    num = cross_correlation(X1,X2,K,M,l)
    den = np.sqrt(autocorrelation(X1,K,M,l)*autocorrelation(X2,K,M,l))
    return num/den



def equal_ratios_mask(L,R,K,M,l=0.5):
    c = cross_correlation_coef(L,R,K,M,l)
    x = 1 - np.abs(c)
    for k in range(K):
        for m in range(M):
            if x[k,m]<=0:
                x[k,m] = 1e-8
    return np.sqrt( x )


def equal_levels(L,R,K,M,l=0.5):

    c_l = autocorrelation(L,K,M,l)
    c_r = autocorrelation(R,K,M,l)
    c_x = cross_correlation(L,R,K,M,l)

    I = np.sqrt( 0.5 * ( c_l + c_r - np.sqrt( np.power( c_l-c_r, 2) + (4*np.power(np.abs(c_x),2)) ) ) )

    a_l = I / np.sqrt(c_l)
    a_r = I / np.sqrt(c_r)

    return np.asarray([a_l,a_r])