'''Module is supposed to convert dict to class with corresponding attributes.'''
from copy import copy
from typing import Dict, Any
from pprint import pprint


class Void:
    '''Class to be a placeholder as return'''


class Converter:
    '''Class to perform conversions'''

    @classmethod
    def __class_builder(cls, item: Void, sourse: Dict):
        '''Recursive class from dictionary builder'''
        for key, value in sourse.items():
            if isinstance(value, dict):
                inner_cls = Void()
                cls.__class_builder(inner_cls, value)
                item.__setattr__(key, inner_cls)
            elif isinstance(value, (tuple, list)):
                iterable = copy(value)
                for i, elem in enumerate(iterable):
                    if isinstance(elem, (tuple, list)) or isinstance(elem, dict):
                        inner_cls = Void()
                        cls.__class_builder(inner_cls, elem)
                        iterable[i] = inner_cls
                    else:
                        iterable[i] = elem
                item.__setattr__(key, iterable)
            else:
                if not isinstance(key, str):
                    raise TypeError("key must be a string")
                item.__setattr__(key, value)

    @classmethod
    def dict2class(cls, sourse: Dict) -> Void:
        '''gets dictionary as intput and returs corresponding class'''
        out = Void()
        cls.__class_builder(out, sourse)
        return out

    @classmethod
    def class2dict(cls, item: Any) -> Dict:
        '''gets class as intput and returs corresponding dictionary. Works recursively'''
        try:
            out = vars(item)
            for key, value in out.items():
                out[key] = cls.class2dict(value)
        except TypeError:
            if isinstance(item, (tuple, list)):
                item = copy(item)
                for i, elem in enumerate(item):
                    item[i] = cls.class2dict(elem)
            return item
        return out


def main():
    '''main function'''
    test = {
        'a': 123,
        'b': {
            'd': [
                1,
                {
                    'h': [1, 2, 3],
                    'i': [4, 5, 6]
                },
                3
            ],
            'e': {
                'f': 456,
                'g': 789
            }
        },
        'c': {7, 8, (9, 9)}
    }
    ret = Converter.dict2class(test)
    ret2 = Converter.class2dict(ret)
    pprint(ret2)


if __name__ == '__main__':
    main()
