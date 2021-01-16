import os
from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass
import time


@dataclass
class Device:
    ip: str
    ip_local: str
    mac_address: str

    def __hash__(self):
        _hash = hash(self.ip) + hash(self.ip_local) + hash(self.mac_address)
        return _hash

    def __eq__(self, other: 'Device'):
        return (self.ip == other.ip) and (self.ip_local == other.ip_local) and (self.mac_address == other.mac_address)


class DeviceTimeMonitor:

    def __init__(self):
        self.update_time = 15  # secs
        self.devices_time_online = {}

    @staticmethod
    def remove_par(s: str) -> str:
        s = s.replace('(', '')
        s = s.replace(')', '')
        return s

    def get_devices_on_network(self) -> (List[Device], datetime):
        devices: List[Device] = []
        devices_str = os.popen('arp -a')
        ts = datetime.now()
        for line in devices_str:
            words = line.split(' ')
            d = Device(ip=words[0], ip_local=self.remove_par(words[1]), mac_address=words[3])
            devices.append(d)
        return devices

    def count_online_time(self, devices: List[Device], update_time: int) -> Dict[str, int]:
        for d in devices:
            if d in self.devices_time_online.keys():
                self.devices_time_online[d] += update_time
            else:
                self.devices_time_online[d] = update_time
        return self.devices_time_online

    def run(self, iterations: int):
        def _logic():
            start = time.time()
            devices = self.get_devices_on_network()  # TODO: run every second in subprocesses
            end = time.time()
            worked_time = end - start
            if worked_time > self.update_time:
                raise RuntimeError('Command "arp -a" works %f - more than update time %d. Kindly increase update time' %
                                   (worked_time, self.update_time))
            time.sleep(self.update_time - worked_time)
            online_time = self.count_online_time(devices, self.update_time)
            print(online_time)

        if iterations > 0:
            for _ in range(iterations):
                _logic()
        else:
            while True:
                _logic()


def main():
    dtm = DeviceTimeMonitor()
    dtm.run(iterations=-1)


if __name__ == '__main__':
    main()
