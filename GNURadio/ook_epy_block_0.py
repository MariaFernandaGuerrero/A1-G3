import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block is a RF VCO and works as following: It implements a controlled oscilator for RF taking as inputs the phase and amplitude fo a signal, 
    as well as a carrier frequency and sampling rate as parameters. the phase of the signal is added to a carrier phase computed from the parameters,
    that signal is then multiplied by the amplitude of the original signal. This algorithm along with the differents block in the diagram result on a
    modulations such as OOK, BPSK y FSK"""

    def __init__(self, fc=128000, samp_rate=320000):  
        gr.sync_block.__init__(
            self,
            name='e_RF_VCO_ff',   
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32]
        )
        self.fc = fc
        self.samp_rate = samp_rate
        self.n_m=0

    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)
        n=np.linspace(self.n_m,self.n_m+N-1,N)
        self.n_m += N
        y[:]=A*np.cos(2*math.pi*self.fc*n/self.samp_rate+Q)
        return len(output_items[0])


