import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="e_Diff_2ndOrder",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        # Frecuencia de muestreo
        self.fs = 10.0
        self.Ts = 1.0 / self.fs

        # Guardamos las dos muestras anteriores
        self.x_prev1 = 0.0
        self.x_prev2 = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        # Extendemos con las dos muestras previas
        x_ext = np.concatenate(([self.x_prev2, self.x_prev1], x))

        # Derivada hacia atrás de orden 2:
        # y[n] = (3x[n] - 4x[n-1] + x[n-2]) / (2Ts)
        y[:] = (3*x_ext[2:] - 4*x_ext[1:-1] + x_ext[:-2]) / (2.0 * self.Ts)

        # Actualizamos memoria
        self.x_prev2 = x_ext[-2]
        self.x_prev1 = x_ext[-1]

        return len(y)
