from app.device_time_monitor import DeviceTimeMonitor


def main():
    dtm = DeviceTimeMonitor()
    dtm.run(iterations=-1)


if __name__ == '__main__':
    main()
