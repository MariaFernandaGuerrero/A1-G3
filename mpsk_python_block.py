import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block)  
    
    M-PSK Modulator
    - Output 0 envolvente compleja (1 samplesymbol)
    - Output 1 RF real (bien muestreada)
    

    def __init__(self, M=4, A=1.0, fc=32000, fs=256000, sps=8)  
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
        self.sps = sps  # samples per symbol
        
        self.k = int(np.log2(M))
        self.n_m = 0  # contador global de muestras RF

    def work(self, input_items, output_items)
        bits = input_items[0]
        bb_out = output_items[0]
        rf_out = output_items[1]

        N = len(bits)
        num_symbols = N  self.k

        if num_symbols == 0
            return 0

        bits = bits[num_symbols  self.k]
        bits_reshaped = bits.reshape((num_symbols, self.k))

        # bits → símbolos
        symbols = np.zeros(num_symbols, dtype=np.int32)
        for i in range(self.k)
            symbols += bits_reshaped[, i]  (self.k - i - 1)

        # fases
        phases = 2  np.pi  symbols  self.M

        # envolvente compleja (NO tocar esto)
        bb = self.A  np.exp(1j  phases)

        # generar RF correctamente
        total_samples = num_symbols  self.sps
        n = np.arange(self.n_m, self.n_m + total_samples)
        self.n_m += total_samples

        # expandir fases PERO alineadas con muestras RF
        phases_expanded = np.repeat(phases, self.sps)

        rf = self.A  np.cos(2  np.pi  self.fc  n  self.fs + phases_expanded)

        # salidas
        out_len = min(len(rf_out), total_samples, len(bb_out))

        bb_out[num_symbols] = bb[num_symbols]
        rf_out[out_len] = rf[out_len]

        return out_len