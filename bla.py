import threading

l = threading.RLock()
print("before first acquire")
l.acquire()
print("before second acquire")
# l.release()
l.acquire()
print("acquired lock twice")
l.release()
# l.release()