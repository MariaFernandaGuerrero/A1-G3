import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """
    M-PSK Modulator:
    - Input: binary stream (0/1)
    - Outputs:
        0: complex baseband signal
        1: real RF signal
    """

    def __init__(self, M=4, A=1.0, fc=1000, fs=32000):  
        gr.sync_block.__init__(
            self,
            name='MPSK_Modulator',
            in_sig=[np.int8],
            out_sig=[np.complex64, np.float32]
        )
        
        self.M = M
        self.A = A
        self.fc = fc
        self.fs = fs
        self.n_m=0
        
        self.k = int(np.log2(M))  # bits per symbol
        self.phase_acc = 0  # para continuidad de fase si quieres extenderlo

    def work(self, input_items, output_items):
        bits = input_items[0]
        bb_out = output_items[0]
        rf_out = output_items[1]

        N = len(bits)

        # Número de símbolos que podemos formar
        num_symbols = N // self.k

        if num_symbols == 0:
            return 0

        # Agrupar bits
        bits_reshaped = bits[:num_symbols*self.k].reshape((num_symbols, self.k))

        # Convertir bits a enteros
        symbols = np.zeros(num_symbols, dtype=np.int32)
        for i in range(self.k):
            symbols += bits_reshaped[:, i] << (self.k - i - 1)

        # Mapear a fase
        phases = 2 * np.pi * symbols / self.M + math.pi/16

        # Envolvente compleja (baseband)
        bb = self.A * np.exp(1j * phases)

        # Tiempo discreto
        t = np.arange(num_symbols) / self.fs

        #n = np.linspace(self.n_m,self.n_m+N-1,N)
        #self.n_m += N
        #rf = self.A*np.cos(2*math.pi*self.fc*n/self.samp_rate+phases)

        # Señal RF
        rf = self.A * np.cos(2 * np.pi * self.fc * t + phases)

        # Salidas
        bb_out[:num_symbols] = bb
        rf_out[:num_symbols] = rf

        return num_symbols
