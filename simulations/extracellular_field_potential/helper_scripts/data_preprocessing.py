import scipy.signal as ss

def get_mua(ecp, filter_order = 5, fs = 20000, fc = 500, q = 20):
    '''
        This function gives you the MUA from the ECP
        Arguments:
                ecp: extracellular potential
                filter_order: order of butterworth filter
                fs: sampling frequency (Hz)
                fc: cut-off frequency
                q: downsampling order
        Output:
                mua: multi-unit activity
    '''
    # creating high-pass filter
    Wn = fc/fs/2
    
    b, a = ss.butter(filter_order, Wn, btype = 'highpass')
    
    mua = ss.filtfilt(b, a, ecp, axis = 0)

    # downsample to 1 kHz
    for q_ in [10, q // 10]:
        mua = ss.decimate(mua, q_, axis = 0)
    
    mua = abs(mua)
    
    return mua

def get_lfp(ecp, filter_order = 5, fs = 20000, fc = 500, q = 20):
    '''
        This function gives you the LFP from the ECP
        Arguments:
                ecp: extracellular potential
                filter_order: order of butterworth filter
                fs: sampling frequency (Hz)
                fc: cut-off frequency
                q: downsampling order
        Output:
                lfp: local field potential
    '''
    # creating high-pass filter
    Wn = fc/fs/2
    
    b, a = ss.butter(filter_order, Wn, btype = 'low')
    
    lfp = ss.filtfilt(b, a, ecp, axis = 0)

    for q_ in [10, q // 10]:
        lfp = ss.decimate(lfp, q_, axis = 0)
    
    return lfp