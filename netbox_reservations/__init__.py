from extras.plugins import PluginConfig


class NetBoxReservationsConfig(PluginConfig):
    name = 'netbox_reservations'
    verbose_name = 'NetBox Reservations'
    description = 'Manage reservations in NetBox'
    author = 'Tim Morgner'
    author_email = 'tim@timmorgner.de'
    version = '1.2.2'
    base_url = 'reservations'
    min_version = '3.4.0'
    max_version = '4.9.99'
    default_settings = {
        'top_level_menu': True,
    }


config = NetBoxReservationsConfig
