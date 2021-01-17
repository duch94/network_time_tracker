import pickle

from jinja2 import Environment, PackageLoader, select_autoescape

from app.device_time_monitor import DeviceTimeMonitor


def get_devices_online() -> str:
    with open(DeviceTimeMonitor.persistance_filename, 'rb') as file_stream:
        devices_online = pickle.load(file_stream)
    env = Environment(
        loader=PackageLoader('web_app', 'views/templates'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    page_template = env.get_template('devices_online.html.j2')
    page = page_template.render(devices_online=devices_online)
    return page
