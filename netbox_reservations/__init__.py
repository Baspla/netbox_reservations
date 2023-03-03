from extras.plugins import PluginConfig
from version import __version__


class NetBoxReservationsConfig(PluginConfig):
    name = 'netbox_reservations'
    verbose_name = 'NetBox Reservations'
    description = 'Manage reservations in NetBox'
    author = 'Tim Morgner'
    author_email = 'tim.morgner@telekom.de'
    version = '1.1'
    base_url = 'reservations'
    min_version = '3.4.0'
    max_version = '3.4.99'
    default_settings = {
        'top_level_menu' : True,
    }

config = NetBoxReservationsConfig
