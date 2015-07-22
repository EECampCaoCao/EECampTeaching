import traceback

class Testcase:

    def __init__(self, a, b, c, info):
        self.a = a
        self.b = b
        self.c = c
        self.info = info

    def __str__(self):
        return json.dumps({
            'a': a,
            'b': b,
            'c': c,
        })

    def apply(self):
        ans = None
        err = ''
        m = max(self.a, self.b, self.c)
        try:
            from maximum import maximum
            ans = maximum(self.a, self.b, self.c)
        except Exception as e:
            err = traceback.format_exc()
        return m == ans, err

if __name__ == '__main__':
    tests = [
        Testcase(1, 2, 3, 'maximum(1, 2, 3) = 3'),
        Testcase(3, 3, 3, 'maximum(3, 3, 3) = 3'),
        Testcase(-3, -2, -5, 'maximum(-3, -2, -5) = -2'),
        Testcase(3.14, 1.41, 2.71, '3.14 最大!'),
        Testcase('A is the smallest', 'B is bigger than A', 
                 'Z is the biggest!', '字串是用字典序(A<B<...<Z)決定大小!'),
    ]

    for i, t in enumerate(tests):
        flag, err = t.apply()
        res = {
            'no': i,
            'result': flag,
            'isError': not err,
            'errMsg': err
        }
