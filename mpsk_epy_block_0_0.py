import numpy as np
from gnuradio import gr
import math

class blk(gr.interp_block):  
    """
    M-PSK Modulator con interpolación correcta

    Input: bits (float)
    Output:
        0: baseband complejo
        1: RF real
    """

    def __init__(self, M=4, A=1.0, fc=1000, fs=32000, Rs=1000):  
        
        self.k = int(np.log2(M))      # bits por símbolo
        self.Ns = int(fs / Rs)        # samples por símbolo
        self.interp = self.Ns // self.k  # factor de interpolación
        
        gr.interp_block.__init__(
            self,
            name='MPSK_Modulator',
            in_sig=[np.float32],
            out_sig=[np.complex64, np.float32],
            interp=self.interp
        )
        
        self.M = M
        self.A = A
        self.fc = fc
        self.fs = fs
        
        self.n_m = 0

    def work(self, input_items, output_items):
        x = input_items[0]
        bb_out = output_items[0]
        rf_out = output_items[1]

        # float → bits
        bits = (x > 0.5).astype(np.int8)

        N = len(bits)
        num_symbols = N // self.k

        if num_symbols == 0:
            return 0

        bits = bits[:num_symbols * self.k]
        bits_reshaped = bits.reshape((num_symbols, self.k))

        # bits → símbolos
        symbols = np.zeros(num_symbols, dtype=np.int32)
        for i in range(self.k):
            symbols += bits_reshaped[:, i] << (self.k - i - 1)

        # fases
        phases = 2 * np.pi * symbols / self.M + math.pi / 16

        # expandir
        phases_up = np.repeat(phases, self.Ns)

        # baseband
        bb = self.A * np.exp(1j * phases_up)

        # tiempo continuo
        N_out = len(bb)
        n = np.arange(self.n_m, self.n_m + N_out)
        self.n_m += N_out

        # RF
        rf = self.A * np.cos(2 * np.pi * self.fc * n / self.fs + phases_up)

        # salida
        bb_out[:N_out] = bb
        rf_out[:N_out] = rf

        return N
