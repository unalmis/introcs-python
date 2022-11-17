# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 particle.py
# ------------------------------------------------------------------------------


class Particle:
    _m: int or float  # mass
    _s: tuple  # position
    _v: tuple  # velocity

    def __init__(self, m, s, v):
        # make particle with mass m and given position, velocity
        _dim_match(s, v)
        self._m = m
        self._s = tuple(s)
        self._v = tuple(v)

    def kinetic_energy(self) -> int or float:
        # return kinetic energy
        return 0.5 * self._m * _dot(self._v, self._v)

    def __str__(self) -> str:
        # return string representation
        return "\n".join((str(self._m), str(self._s), str(self._v)))


def _dot(v, w) -> int or float:
    # dot product of v and w
    _dim_match(v, w)
    result = 0
    for i in range(len(v)):
        result += v[i] * w[i].conjugate()  # for complex dot product
    return result


def _dim_match(v, w):
    # ensure dimension match between v and w
    if len(v) != len(w):
        raise Exception("dimension mismatch")


def main():
    # unit tests

    m = 200
    s = (0, 0, 0)
    v = (1, 2, 3)
    particle = Particle(m, s, v)
    assert particle.kinetic_energy() == 1400
    print(particle)


if __name__ == "__main__":
    main()
