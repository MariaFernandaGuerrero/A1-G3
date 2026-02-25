import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="e_Diff",  # Nombre en GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        # Guardamos la última muestra del bloque anterior
        self.x_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]      # Señal de entrada
        y = output_items[0]     # Señal diferenciada

        # Diferenciador discreto:
        # y[n] = x[n] - x[n-1]
        y[:] = np.diff(x, prepend=self.x_anterior)

        # Guardamos la última muestra para el siguiente bloque
        self.x_anterior = x[-1]

        return len(y)
