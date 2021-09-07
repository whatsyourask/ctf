class Point:
    def __init__(self, x, y, modulus):
        self.x = x
        self.y = y
        self.modulus = modulus

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


    def __add__(self, other):
        if self.x == other.x and self.y == other.y:
            lmbda = 



if __name__=='__main__':
    p = (493, 5564)
    q = (1539, 4742)
    r = (4403, 5202)
    modulus = 9739
    temp = point_addition(p, p, modulus)
    temp = point_addition(temp, q, modulus)
    s_point = point_addition(temp, r, modulus)
    print(s_point)
