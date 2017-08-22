
import numpy as np
import png


class Canvas:

    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height
        self.data = np.empty([height, width*3], dtype='uint8')

    def save(self, name='test.png'):
        png.from_array(self.data, 'RGB').save(name)

    def impose(self, pattern, *args, **kwargs):
        pattern.draw(*args, **kwargs, canvas=self)







if __name__ == '__main__':
    c = Canvas()

    from pattern import BasePattern
    f = BasePattern()

    c.impose(f)
    c.save()