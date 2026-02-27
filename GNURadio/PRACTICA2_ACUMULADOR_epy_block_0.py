import numpy as np
from gnuradio import gr

class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='e_Acum',        # Nombre en GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        
        self.acc = 0.0  # Variable de estado (memoria del acumulador)

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        # Acumulador continuo
        for i in range(len(x)):
            self.acc += x[i]
            y[i] = self.acc

        return len(y)