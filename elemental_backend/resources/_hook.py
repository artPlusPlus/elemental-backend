import weakref


class Hook(object):
    def __init__(self):
        self._handler_refs = []

    def add_handler(self, handler):
        handler_died_handler = weakref.WeakMethod(self._handler_ref_died)

        try:
            handler_ref = weakref.WeakMethod(handler, handler_died_handler)
        except TypeError:
            handler_ref = weakref.ref(handler, handler_died_handler)

        self._handler_refs.append(handler_ref)

    def remove_handler(self, handler):
        try:
            handler_ref = weakref.WeakMethod(handler)
        except TypeError:
            handler_ref = weakref.ref(handler)

        self._handler_refs.remove(handler_ref)

    def __call__(self, sender, data):
        try:
            sender = weakref.proxy(sender)
        except TypeError:
            pass

        for handler_ref in self._handler_refs:
            handler = handler_ref()
            if handler:
                handler(sender, data)

    def _handler_ref_died(self, handler_ref):
        try:
            self._handler_refs.remove(handler_ref)
        except ValueError:
            pass
