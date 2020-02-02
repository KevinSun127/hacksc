#todo:
#log and exponents


def pi():
    total, next_term, sign = 3, 1/6, 1
    for i in range(2, 100000):
        total += next_term
        sign = -sign
        next_term = sign*4/(8*i*i*i + (12*i*i) + (4*i))
    return total


def factorial(start, finish = 0, final = 1):
    if start < 0:
        return 'Error: Value must be greater than zero.'
    if start != finish:
        return final
    return factorial(start-1, finish, final*start)


def cos(entry, next_term=1, total=0):
    for counter in range(1, 1000):
        total += next_term
        next_term = -next_term * (entry * entry) / (2 * counter * (2 * counter - 1))
    return total

def sin(entry, total=0):
    next_term = entry
    for counter in range(1, 1000):
        total += next_term
        next_term = -next_term * (entry * entry) / ((2 * counter + 1)  * (2 * counter))
    return total


def tan(entry):
    return sin(entry)/cos(entry)

def cot(entry):
    return cos(entry)/sin(entry)

def cosinv(entry, test_val = 0, decimal = .1, pie = pi(), test = 0):
    if entry > 1 or entry < -1:
        return 'Error: Absolute value of input must be less than or equal to one.'
    if 0 <= entry:
        while True:
            test = cos(pie/2 - test_val - decimal)
            if decimal <= .00000000000001 or entry - test == 0:
                return pie/2 - test_val
            if entry - test > 0:
                test_val+=decimal
            else:
                decimal*=.1
    else:
        while True:
            test = cos(pie/2 + test_val + decimal)
            if decimal <= .00000000000001 or entry - test == 0:
                return pie/2 + test_val
            if entry - test < 0:
                test_val+=decimal
            else:
                decimal*=.1


def sininv(entry, test_val = 0, decimal = .1, pie = pi(), test = 0):
    if entry > 1:
        return 'Error: Absolute value of input must be less than or equal to one.'
    if 0 <= entry:
        while True:
            test = sin(test_val + decimal)
            if decimal <= .000000000000001 or entry - test == 0:
                return test_val
            if entry - test > 0:
                test_val+=decimal
            else:
                decimal*=.1
    else:
        while True:
            test = sin(-test_val - decimal)
            if decimal <= .00000000000001 or entry - test == 0:
                return -test_val
            if entry - test < 0:
                test_val+=decimal
            else:
                decimal*=.1

def taninv(entry, test_val = 0, decimal = .1, pie = pi(), test = 0):
    if 0 <= entry:
        while True:
            test = tan(test_val + decimal)
            if decimal <= .000000000000001 or entry - test == 0:
                return test_val
            if entry - test > 0:
                test_val+=decimal
            else:
                decimal*=.1
    else:
        while True:
            test = tan(test_val - decimal)
            if decimal <= .00000000000001 or entry - test == 0:
                return test_val
            if entry - test < 0:
                test_val-=decimal
            else:
                decimal*=.1


def deg(entry):
    return entry*180/pi()

def rad(entry):
    return entry*pi()/180


def sqrt(entry, square = 0.0, decimal = 1.0):
    if entry < 0:
        return 'Error: Entry must be positive.'
    while True:
        if decimal <= .000000000000001 or entry - square*square == 0:
            return square
        if entry - (square + decimal)*(square + decimal) > 0:
            square+=decimal
        else:
            decimal*=.1

def e():
    prod = 1
    for i in range(100000000):
        prod*=(1+(1/100000000))
    return prod

def epow(power, decimal = .000000001, initial = 0, prod = 1, e = e()):
    #use eulers formula to approximate value of e^whatever
    #need to program values for less than 0
    prod, initial = pow(e, int(power)), int(power)
    while initial < power:
        prod+=(prod*decimal)
        initial+=decimal
    return prod

def pow(base, power, prod = 1):
    if power >= 0:
        for i in range(power):
            prod*=base
    else:
        for i in range(-power):
            prod/=base
    return prod

def log(entry, exp = 0.0, decimal = 1.0, e = e()):
    if entry < 0:
        return 'Error: Entry must be positive.'
    if entry > 1:
        while True:
            if decimal <= .000000000000001 or entry - epow(exp) == 0:
                return exp
            elif e - epow(exp + decimal) < e - epow(exp):
                exp+=decimal
            else:
                decimal*=.1
    if entry < 1:
        while True:
            decimal = .000001
            if decimal <= .000000000000001 or entry - epow(exp) == 0:
                return exp
            elif e - epow(exp - decimal) > e - epow(exp):
                exp-=decimal
            else:
                decimal*=.1


