#from __future__ import annotations


class Point:
    def __init__(self, x, y, modulus=None):
        self.x = x
        self.y = y
        self.modulus = modulus
    
    def __add__(self, other):
        zero = Point(0, 0)
        if self.x == zero.x and self.y == zero.y:
            return other
        elif other.x == zero.x and other.y == zero.y:
            return self
        else:
            if self.x == other.x and self.y == -other.y:
                return zero
            else:
                if self.x == other.x and self.y == other.y:
                    lmbda = (((3 * self.x ** 2 + 497)) * pow((2 * self.y), -1, self.modulus)) % self.modulus
                else:
                    lmbda = (((other.y - self.y)) * pow((other.x - self.x), -1, self.modulus)) % self.modulus
                x = (lmbda ** 2 - self.x - other.x) % self.modulus
                y = (lmbda * (self.x - x) - self.y) % self.modulus
                new = Point(x, y, self.modulus)
                return new


if __name__=='__main__':
    modulus = 9739
    p = Point(493, 5564, modulus)
    q = Point(1539, 4742, modulus)
    r = Point(4403, 5202, modulus)
    temp = p + p
    temp = temp + q
    s = temp + r
    print(s.x, s.y)
