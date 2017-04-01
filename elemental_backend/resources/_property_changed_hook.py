from collections import namedtuple

from elemental_core import Hook


PropertyChangedData = namedtuple(
    'PropertyChangedEventArgs',
    [
        'original_value',
        'current_value'
    ]
)


class PropertyChangedHook(Hook):
    def __call__(self, sender, original_value, current_value):
        super(PropertyChangedHook, self).__call__(
            sender,
            PropertyChangedData(original_value, current_value))
