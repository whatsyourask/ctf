from point_addition import Point


class PointWithMultOp(Point):
    def __init__(self, x, y, modulus=None):
        super().__init__(x, y, modulus)
    
    def mul(self, n):
        q = self
        zero = PointWithMultOp(0, 0)
        r = zero
        while n > 0:
            if n % 2 == 1:
                r = r + q
            q = q + q
            n = n // 2
            if n > 0:
                continue
        return r


if __name__=='__main__':
    modulus = 9739
    p = PointWithMultOp(2339, 2213, modulus)
    r = p.mul(7863)
    print(r.x, r.y)
