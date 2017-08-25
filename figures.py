
from artist import BaseArtist
from math import floor, ceil


def mix_color(old, new, v):
    return tuple(o*(1-v) + n*v for o, n in zip(old, new))


class BaseFigure(BaseArtist):

    def _actual_fragment(self):
        """ Возвращает прямоугольный фрагмент холста,
            за пределы которого рендеринг гарантированно не выйдет.
            Для базового класса это холст целиком, в потомках крайне рекомендуется найти эвристики,
            обрезающие его, иначе будет нехилый оверхед по памяти и процессору,
            особенно при отрисовке маленьких фигур """
        p = self._params
        return p.canvas.image

    def _create_mask(self):
        fragment = self._actual_fragment()
        # TODO

    def _pixel(self, canvas, x, y, color, value):
        """ Окрашивает пиксель в заданный цвет.
            Если value < 1, цвет будет частично разбавлен прежним цветом пикселя """
        value = max(0, min(value, 1))
        old_color = tuple(canvas.image[x, y])
        new_color = mix_color(old_color, color, value)
        canvas._pixel(x, y, color=new_color)


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

    def _render(self):
        pass