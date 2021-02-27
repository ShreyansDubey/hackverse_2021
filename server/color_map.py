from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

cdict = {'red':  ((0.0, 0.8, 0.8),   # no red at 0
                  (0.2, 0, 0),
                  (1.0, 0.0, 0.0)),  # set to 0.8 so its not too bright at 1

        'green': ((0.0, 0.0, 0.0),   # set to 0.8 so its not too bright at 0
                  (0.2, 0, 0),
                  (1.0, 0.8, 0.8)),  # no green at 1

        'blue':  ((0.0, 0.0, 0.0),   # no blue at 0
                  (1.0, 0.0, 0.0))   # no blue at 1
       }

color_map = colors.LinearSegmentedColormap('GnRd', cdict)
plt.register_cmap('GnRd', color_map)
_cm = plt.get_cmap("GnRd")

def apply_colormap(tile):
    tile = tile.astype(np.float32) / 255
    tile = _cm(tile)
    tile *= 255
    return tile.astype(np.uint8)

if __name__ == '__main__':
    import PIL.Image as Image
    # tile = np.random.rand(16, 16)
    tile = np.ones((16, 16)) * 20
    print(tile.shape)
    tile = apply_colormap(tile)
    print(tile.shape, np.max(tile), np.min(tile))

    img = Image.fromarray(tile.astype(np.uint8))
    img = img.resize((256, 256))
    img.save('test.png')

    