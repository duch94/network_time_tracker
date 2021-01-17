from dataclasses import dataclass


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
