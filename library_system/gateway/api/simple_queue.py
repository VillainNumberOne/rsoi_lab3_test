import queue
from threading import Thread
import time
import requests

class Queue:
    def __init__(self, timeout=60):
        self.timeout = timeout
        self.services = ["library_system", "rating_system"]
        self.queues = {
            "library_system": queue.Queue(),
            "rating_system": queue.Queue()
        }

    def put(self, system, method, *args, **kwargs):
        assert system in self.services
        self._put(system, method, time.time(), *args, **kwargs)
        
    def _put(self, system, method, initial_time, *args, **kwargs):
        self.queues[system].put([initial_time, method, list(args), dict(kwargs)])

    def join_all(self):
        for q in self.queues.values():
            q.join()

    def system_queue(self, system):
        t, method, args, kwargs = self.queues[system].get()
        if time.time() - t < self.timeout:
            print("\nsystem:", system, flush=True)
            try:
                status = method(*args, **kwargs).status_code
            except requests.exceptions.ConnectionError:
                print("\nunable to connect, retrying...", flush=True)
                status = 404
            except Exception:
                status = 500
                
            if status == 404:
                self._put(system, method, t, *args, **kwargs)
        else:
            print("Timeout reached")

        self.queues[system].task_done()
        time.sleep(0.1)
            

    def library_system_queue(self):
        while True:
            self.system_queue("library_system")

    def rating_system_queue(self):
        while True:
            self.system_queue("rating_system")

services_queue = Queue()
Thread(target=services_queue.library_system_queue, daemon=True).start()
Thread(target=services_queue.rating_system_queue, daemon=True).start()
services_queue.join_all()