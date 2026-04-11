import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block is a CE VCO or baseband VCO and works as following: It implements 
    a complex exponential generator that takes as inputs the amplitude and phase of 
    a baseband signal.  Specifically, the block computes a complex phasor of the form 
    A·exp(jQ), where A is the input amplitude and Q is the input phase. This 
    representation is commonly used in complex envelope modulation schemes and is 
    fundamental in digital communications for QPSK, PSK, and other baseband modulation
    techniques."""

    def __init__(self,):  
        gr.sync_block.__init__(
            self,
            name='e_CE_VCO_fc',   
            in_sig=[np.float32, np.float32],
            out_sig=[np.complex64]
        )
        
    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)
        y[:]=A*np.exp(1j*Q)
        return len(y)
