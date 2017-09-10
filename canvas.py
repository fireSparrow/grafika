
import numpy as np
import png


def frame_points(xy0, xy1):
    return xy0[0], xy1[0], xy0[1], xy1[1]


class Canvas:

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self._data = np.zeros([height, width, 3])

    def fragment(self, frame):
        x0, y0, x1, y1 = frame_points(*frame)
        # TODO: переработать механику фрагментов
        f = Canvas(width=abs(x1-x0), height=abs(y1-y0))
        # TODO: Посмотреть - не обрежется ли последний символ
        # TODO: Вообще, продумать инструментарий работы с координатами
        f.data = self._data[x0:x1, y0:y1, 3]
        return f

    def save(self, name='test.png'):
        data = self._data
        data[data<0] = 0
        data[data>1] = 1
        data[:, :] *= 255

        np.fix(data)
        data = np.array(data, dtype='uint8')
        png.from_array(data, 'RGB').save(name)

    def impose(self, artist, *args, **kwargs):
        artist.draw(*args, **kwargs, canvas=self)

    def pixel(self, x, y, color=(1, 1, 1)):
        self._data[x, y, :3] = color

    @property
    def image(self):
        return self._data