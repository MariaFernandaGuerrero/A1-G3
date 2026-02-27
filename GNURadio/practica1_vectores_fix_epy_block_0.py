import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, vlen=7):
        gr.sync_block.__init__(
            self,
            name="Promedios_de_tiempos",
            in_sig=[(np.float32, vlen)],
            out_sig=[
                (np.float32, vlen),
                (np.float32, vlen),
                (np.float32, vlen),
                (np.float32, vlen),
                (np.float32, vlen)
            ]
        )

        self.acum = np.zeros(vlen)
        self.acum2 = np.zeros(vlen)
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]

        y0 = output_items[0]
        y1 = output_items[1]
        y2 = output_items[2]
        y3 = output_items[3]
        y4 = output_items[4]

        n_items = x.shape[0]

        for i in range(n_items):
            xi = x[i]

            self.Ntotales += 1
            self.acum += xi
            self.acum2 += xi**2

            media = self.acum / self.Ntotales
            media_cuad = self.acum2 / self.Ntotales

            rms = np.sqrt(media_cuad)
            potencia = media_cuad

            var = np.maximum(media_cuad - media**2, 0)
            std = np.sqrt(var)

            y0[i] = media
            y1[i] = media_cuad
            y2[i] = rms
            y3[i] = potencia
            y4[i] = std

        return n_items
