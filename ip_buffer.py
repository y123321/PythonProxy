from ring_buffer import RingBuffer
import threading
import datetime


class IpBuffer:
    def __init__(self, limit_in_minutes, buffer_size):
        self.dictionary = {}
        self.limit_in_minutes = limit_in_minutes
        self.__lock = threading.Lock()
        self.__buffer_size = buffer_size

    def check_ip(self, ip):
        self.__lock.acquire()
        try:
            if not self.dictionary.__contains__(ip):
                return True
            ring_buffer = self.dictionary[ip]
            time = ring_buffer.get_first()
            is_valid = time is None
            if not is_valid:
                is_valid = datetime.datetime.now() - time > datetime.timedelta(minutes=self.limit_in_minutes)
            return is_valid
        finally:
            self.__lock.release()

    def add_ip(self, ip):
        self.__lock.acquire()
        try:
            current_dt = datetime.datetime.now()

            if not self.dictionary.__contains__(ip):
                self.dictionary[ip] = RingBuffer(self.__buffer_size)
            self.dictionary[ip].append(current_dt)
        finally:
            self.__lock.release()
