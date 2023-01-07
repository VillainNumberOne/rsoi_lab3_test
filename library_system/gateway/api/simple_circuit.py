import time

class Circuit():
    def __init__(self, f, fallback = None, threshold=5, delay=10, expected_exception=Exception):
        self.states = ["open", "closed", "halfopen"]

        self.f = f
        self.expected_exception = expected_exception
        self.threshold = threshold
        self.delay = delay
        if fallback is None:
            self.fallback = lambda *args, **kwargs: None
        else:
            self.fallback = fallback

        self.state = "closed"
        self.threshold_counter = 0
        self.t1 = 0

    def open(self):
        print("open", flush=True)
        self.state = "open"
        self.threshold_counter = 0
        self.t1 = time.time()

    def half_open(self):
        print("halfopen", flush=True)
        self.state = "halfopen"
        self.time = 0

    def close(self):
        print("closed", flush=True)
        self.state = "closed"
        self.threshold_counter = 0

    def call(self, *args, **kwargs):
        result = 222
        
        if self.state == "closed":
            self.threshold_counter += 1
            try:
                print("try", self.threshold_counter, flush=True)
                result = self.f(*args, **kwargs)
            except Exception as ex:
                if issubclass(type(ex), self.expected_exception):
                    if self.threshold_counter < self.threshold:
                        result = self.call(*args, **kwargs)
                    else:
                        self.open()
                        result = self.call(*args, **kwargs)
                else:
                    raise ex
            else:
                self.close()

        elif self.state == "open":
            if time.time() - self.t1 > self.delay:
                self.half_open()
                result = self.call(*args, **kwargs)
            else:
                result = self.fallback(*args, **kwargs)

        elif self.state == "halfopen":
            try:
                result = self.f(*args, **kwargs)
            except Exception as ex:
                if issubclass(type(ex), self.expected_exception):
                    self.open()
                    result = self.call(*args, **kwargs)
                else:
                    raise ex
            else:
                self.close()

        return result
