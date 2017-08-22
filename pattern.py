
import numpy as np


class Frame:

    def __init__(self, *args, **kwargs):
        pass


class BasePattern:

    _params = ['canvas', 'frame']

    def __init__(self, *args, **kwargs):
        if type(self) is BasePattern:
            raise NotImplementedError
        super().__init__()

    @staticmethod
    def take_fragment(canvas, frame):
        # TODO: обрезка холста
        return canvas

    def draw(self, canvas, frame=None):
        frame = frame or self.frame
        fragment = self.take_fragment(canvas, frame)
        self._render(context=fragment)

    def _render(self, context):
        raise NotImplementedError

    @property
    def frame(self):
        pass


class Block(BasePattern):

    def _render(self, context):
        context.data[::, 2::3] *= 0
