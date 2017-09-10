
import numpy as np

from artist import BaseArtist
from math import floor, ceil

from collections import deque
import math


def mix_color(old, new, v):
    return tuple(o*(1-v) + n*v for o, n in zip(old, new))


class BaseFigure(BaseArtist):

    _left = None    # equation left part
    _right = None   # equation right part
    _start = None   # function, that returns start point

    def _actual_fragment(self):
        """ Возвращает прямоугольный фрагмент холста,
            за пределы которого рендеринг гарантированно не выйдет.
            Для базового класса это холст целиком, в потомках крайне рекомендуется найти эвристики,
            обрезающие его, иначе будет нехилый оверхед по памяти и процессору,
            особенно при отрисовке множества маленьких фигур """
        p = self._params
        return p.canvas

    @staticmethod
    def _create_mask(fragment):
        w, h, _ = fragment.image.shape
        mask = np.zeros(dtype=bool, shape=(w+1, h+1))
        mask[w, :] = True
        mask[:, h] = True
        return mask

    @staticmethod
    def _pixel(canvas, x, y, color, value):
        """ Окрашивает пиксель в заданный цвет.
            Если value < 1, цвет будет частично разбавлен прежним цветом пикселя """
        value = max(0, min(value, 1))
        # Opt: возможно, при value == 1 делать по упрощённой схеме
        old_color = tuple(canvas.image[x, y])
        new_color = mix_color(old_color, color, value)
        canvas.pixel(x, y, color=new_color)

    def _render(self):
        # Возможно, есть смысл делать слепок актуальных параметров в одну эффективную структуру
        color = (1, 1, 1)  # TODO
        deviation = self._deviation_func()
        fragment = self._actual_fragment()
        visited = self._create_mask(fragment)
        queue = deque()  # сравнить производительность deque и list
        # TODO Поправка координат на смещение фрагмента
        queue.append(self._start())
        while queue:
            point = queue.popleft()
            if not visited[point]:
                value = max(0, min(3 - deviation(*point), 1))
                if value:
                    self._pixel(fragment, point[0], point[1], color, value)
                    # Делать ли проверку visited перед добавлением
                    # Создать ли заранее переменные x и y
                    queue.append((point[0]-1, point[1]))
                    queue.append((point[0]+1, point[1]))
                    queue.append((point[0], point[1]-1))
                    queue.append((point[0], point[1]+1))
                    visited[point] = True


class Point(BaseFigure):
    """ Выводит точку. Если координаты дробные - размазывает её по 4 соседним пикселям """

    def _render(self):
        p = self._params
        color = p.color
        canvas = p.canvas
        x0, x1 = floor(p.x), ceil(p.x)
        y0, y1 = floor(p.y), ceil(p.y)
        rx0, rx1 = p.x - x0, x1 - p.x
        ry0, ry1 = p.y - y0, y1 - p.y
        for x, rx in zip((x0, x1), (rx0, rx1)):
            for y, ry in zip((y0, y1), (ry0, ry1)):
                self._pixel(canvas, x, y, color, rx*ry)

class Line(BaseFigure):

    _start = lambda self: (self._params.x1, self._params.y1)

    def _deviation_func(self):
        p = self._params
        dx, dy = p.x2 - p.x1, p.y2 - p.y1
        adx, ady = abs(dx), abs(dy)
        if adx > ady:
            k = ady / adx
            c = math.cos(math.atan(k))
            y0 = p.y1 - k*p.x1
            d = lambda x, y: abs(((y0 + k*x) - y) * c)
        else:
            k = adx / ady
            c = math.cos(math.atan(k))
            x0 = p.x1 - k*p.y1
            d = lambda x, y: abs(((x0 + k*y) - x) * c)
        return d
