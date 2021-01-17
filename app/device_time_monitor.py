import os
from typing import Dict, List
import time
import pickle

from loguru import logger

from models.device import Device


class DeviceTimeMonitor:
    persistance_filename = 'data.pickle'

    def __init__(self):
        self.update_time = 15  # secs
        self.devices_time_online = {}

        if os.path.exists(self.persistance_filename):
            self.load_data()

    @staticmethod
    def remove_par(s: str) -> str:
        s = s.replace('(', '')
        s = s.replace(')', '')
        return s

    def get_devices_on_network(self) -> List[Device]:
        devices: List[Device] = []
        devices_str = os.popen('arp -a')
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

    def load_data(self):
        with open(self.persistance_filename, 'rb') as file_stream:
            self.devices_time_online = pickle.load(file_stream)
        logger.info('Previous working data have been loaded from file {}', self.persistance_filename)

    def persist_data(self):
        with open(self.persistance_filename, 'wb') as file_stream:
            pickle.dump(self.devices_time_online, file_stream)
        logger.info('Working data have been saved to file {}', self.persistance_filename)

    def run(self, iterations: int):
        def _logic():
            logger.info('Started getting online devices.')
            start = time.time()
            devices = self.get_devices_on_network()  # TODO: run every second in subprocesses
            end = time.time()
            worked_time = end - start
            logger.info('Devices getting complete in {}', worked_time)
            if worked_time > self.update_time:
                raise RuntimeError('Command "arp -a" works %f - more than update time %d. Kindly increase update time' %
                                   (worked_time, self.update_time))
            time.sleep(self.update_time - worked_time)
            online_time = self.count_online_time(devices, self.update_time)
            self.persist_data()
            logger.info('Devices online: \n{}', online_time)

        if iterations > 0:
            for _ in range(iterations):
                _logic()
        else:
            while True:
                _logic()
