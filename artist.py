
""" Artist('Художник') - объект, который умеет брать холст и что-то делать с изображением на нём """


class _Params:

    """ Обеспечивает гибкую работу с аргументами для 'artist'
        Произвольная часть аргументов может быть передана при инициализации объекта 'artist'
        и они будут учитываться всегда.
        Остальные могут быть переданы непосредственно в момент отрисовки,
        и учитываются только в процессе этого акта отрисовки.
    """

    def __init__(self, dct):
        self._base = dct
        self._cur = {}

    def __getattr__(self, item):
        return self._cur.get(item, self._base.get(item))

    def use(self, kwargs):
        self._cur = kwargs


class BaseArtist:

    def __init__(self, **kwargs):
        if type(self) is BaseArtist:
            raise NotImplementedError
        super().__init__()
        self._params = _Params(kwargs)

    def draw(self, **kwargs):
        self._params.use(kwargs)
        self._render()
        self._params.use({})

    def _render(self):
        raise NotImplementedError


