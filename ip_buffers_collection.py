from ip_buffer import IpBuffer

ip_buffer_minute = IpBuffer(1, 10)
ip_buffer_day = IpBuffer(60 * 24, 10_000)


def add_ip(ip):
    ip_buffer_minute.add_ip(ip)
    ip_buffer_day.add_ip(ip)


def check_ip(ip):
    return ip_buffer_day.check_ip(ip) & \
           ip_buffer_minute.check_ip(ip)
