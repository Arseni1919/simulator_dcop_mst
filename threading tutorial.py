# import logging
# import threading
# import time
# import concurrent.futures
from CONSTANTS import *
print(threading.get_ident())


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        # print('in update:',threading.get_ident())
        logging.info("Thread %s no %s: starting update", threading.get_ident(), name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        print(self.value)
        logging.info("Thread %s: finishing update", name)

    def locked_update(self, name):
        logging.info("Thread %s no %s: starting update", threading.get_ident(), name)
        logging.debug("Thread %s about to lock", name)
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    print(threading.get_ident())
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for index in range(10):
            executor.submit(database.locked_update, index)
    logging.info("Testing update. Ending value is %d.", database.value)
    import dis

    # dis.dis(database.update)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))


