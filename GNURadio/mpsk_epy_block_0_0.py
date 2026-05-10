import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """
    Constelación personalizada:
    Magnitud = 1
    Ángulos:
    75°, 85°, 95°, 105°
    y sus opuestos +180°
    """

    def __init__(self, M=8, A=1.0, fc=32000, fs=256000, sps=8):  
        gr.sync_block.__init__(
            self,
            name='Custom_Constellation_Modulator',
            in_sig=[np.int8],
            out_sig=[np.complex64, np.float32]
        )
        
        self.M = M
        self.A = A
        self.fc = fc
        self.fs = fs
        self.sps = sps
        
        self.k = int(np.log2(M))
        self.n_m = 0

        # ángulos personalizados en grados
        angles_deg = np.array([75, 85, 95, 105, 255, 265, 275, 285])

        # convertir a radianes
        self.phases_table = np.deg2rad(angles_deg)

    def work(self, input_items, output_items):
        bits = input_items[0]
        bb_out = output_items[0]
        rf_out = output_items[1]

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

        # conversión Gray
        gray_symbols = symbols ^ (symbols >> 1)

        # obtener fases personalizadas
        phases = self.phases_table[gray_symbols]

        # envolvente compleja
        bb = self.A * np.exp(1j * phases)

        # generar RF
        total_samples = num_symbols * self.sps

        n = np.arange(self.n_m, self.n_m + total_samples)
        self.n_m += total_samples

        phases_expanded = np.repeat(phases, self.sps)

        rf = self.A * np.cos(
            2 * np.pi * self.fc * n / self.fs + phases_expanded
        )

        # salidas
        out_len = min(len(rf_out), total_samples, len(bb_out))

        bb_out[:num_symbols] = bb[:num_symbols]
        rf_out[:out_len] = rf[:out_len]

        return out_len
