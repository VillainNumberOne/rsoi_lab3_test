from circuitbreaker import circuit

def r():
    raise ConnectionError()

def cirquit_error(thrown_type, thrown_value):
    # print("Yea?", issubclass(thrown_type, ConnectionError))
    return issubclass(thrown_type, ConnectionError)

def fallback():
    print("Fallback")

@circuit()
def f():
    r()
    print("Yea")

while True:
    f()