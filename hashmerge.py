import copy


LEFT_PRECEDENT = 'LEFT_PRECEDENT'
RIGHT_PRECEDENT = 'RIGHT_PRECEDENT'
STORAGE_PRECEDENT = 'STORAGE_PRECEDENT'
RETAINMENT_PRECEDENT = 'RETAINMENT_PRECEDENT'


class InvalidBehaviour(Exception):
    pass


class HashMerge:
    """
    Merges two arbitrarily deep hashes into a single hash.
    """

    ARRAY = 'array'
    HASH = 'hash'
    SCALAR = 'scalar'

    behaviours = {
        LEFT_PRECEDENT: {
            SCALAR: {
                SCALAR: lambda h, a, b: a,
                ARRAY: lambda h, a, b: a,
                HASH: lambda h, a, b: a
            },
            ARRAY: {
                SCALAR: lambda h, a, b: list(a)+[b],
                ARRAY: lambda h, a, b: list(a)+list(b),
                HASH: lambda h, a, b: list(a)+b.values()
            },
            HASH: {
                SCALAR: lambda h, a, b: a,
                ARRAY: lambda h, a, b: a,
                HASH: lambda h, a, b: h.merge_hashes(a, b)
            }
        },

        RIGHT_PRECEDENT: {
            SCALAR: {
                SCALAR: lambda h, a, b: b,
                ARRAY: lambda h, a, b: [a]+list(b),
                HASH: lambda h, a, b: b
            },
            ARRAY: {
                SCALAR: lambda h, a, b: b,
                ARRAY: lambda h, a, b: list(a)+list(b),
                HASH: lambda h, a, b: b
            },
            HASH: {
                SCALAR: lambda h, a, b: b,
                ARRAY: lambda h, a, b: a.values()+list(b),
                HASH: lambda h, a, b: h.merge_hashes(a, b)
            }
        },

        STORAGE_PRECEDENT: {
            SCALAR: {
                SCALAR: lambda h, a, b: a,
                ARRAY: lambda h, a, b: [a]+list(b),
                HASH: lambda h, a, b: b
            },
            ARRAY: {
                SCALAR: lambda h, a, b: list(a)+[b],
                ARRAY: lambda h, a, b: list(a)+list(b),
                HASH: lambda h, a, b: b
            },
            HASH: {
                SCALAR: lambda h, a, b: a,
                ARRAY: lambda h, a, b: a,
                HASH: lambda h, a, b: h.merge_hashes(a, b)
            }
        },

        RETAINMENT_PRECEDENT: {
            SCALAR: {
                SCALAR: lambda h, a, b: [a, b],
                ARRAY: lambda h, a, b: [a]+list(b),
                HASH: lambda h, a, b: h.merge_hashes(h._hashify(a), b)
            },
            ARRAY: {
                SCALAR: lambda h, a, b: list(a)+[b],
                ARRAY: lambda h, a, b: list(a)+list(b),
                HASH: lambda h, a, b: h.merge_hashes(h._hashify(a), b)
            },
            HASH: {
                SCALAR: lambda h, a, b: h.merge_hashes(a, h._hashify(b)),
                ARRAY: lambda h, a, b: h.merge_hashes(a, h._hashify(b)),
                HASH: lambda h, a, b: h.merge_hashes(a, b)
            }
        }

    }

    @staticmethod
    def _typeof(value):
        if isinstance(value, list) or isinstance(value, tuple):
            return HashMerge.ARRAY
        elif isinstance(value, dict):
            return HashMerge.HASH
        else:
            return HashMerge.SCALAR

    @staticmethod
    def _hashify(value):
        if HashMerge._typeof(value) == HashMerge.ARRAY:
            result = {}
            for item in value:
                suffix = 2
                name = item
                while name in result:
                    name = str(item) + str(suffix)
                result[name] = item
        else:
            return {value: value}

    def __init__(self, behaviour=LEFT_PRECEDENT, clone_method=copy.deepcopy):
        self.set_behaviour(behaviour)
        self.set_clone_behaviour(clone_method)

    def set_behaviour(self, behaviour):
        if behaviour not in self.behaviours:
            raise InvalidBehaviour

        self.behaviour = behaviour

    def get_behaviour(self):
        return self.behaviour

    def set_clone_behaviour(self, clone):
        self.clone = clone

    def get_clone_behaviour(self):
        return self.clone

    def merge(self, left, right):
        left_type = self._typeof(left)
        right_type = self._typeof(right)

        if self.get_clone_behaviour():
            left = copy.deepcopy(left)
            right = copy.deepcopy(right)

        return self.behaviours[self.behaviour][left_type][right_type](
            self, left, right
        )

    def merge_hashes(self, left, right):
        result = {}

        for key, value in left.items():
            if key in right:
                result[key] = self.merge(value, right[key])
            else:
                result[key] = value

        for key, value in right.items():
            if key not in left:
                result[key] = value

        return result
