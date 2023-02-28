from django.conf import settings

from extras.plugins import PluginMenuButton, PluginMenuItem, PluginMenu
from utilities.choices import ButtonColorChoices


reservation_buttons = [
    PluginMenuButton(
        link='plugins:netbox_reservations:reservation_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["netbox_reservations.add_claim"]
    )
]

claim_buttons = [
    PluginMenuButton(
        link='plugins:netbox_reservations:claim_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
        permissions=["netbox_reservations.add_reservation"]
    )
]

_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_reservations:reservation_list',
        link_text='Reservations',
        buttons=reservation_buttons,
        permissions=["netbox_reservations.view_reservation"]
    ),
    PluginMenuItem(
        link='plugins:netbox_reservations:claim_list',
        link_text='Claims',
        buttons=claim_buttons,
        permissions=["netbox_reservations.view_claim"]
    ),
)

_overview_menu_items = (
    PluginMenuItem(
        link='plugins:netbox_reservations:tag_overview_list',
        link_text='Unclaimed Tags',
        permissions=["netbox_reservations.view_claim"]
    ),
    PluginMenuItem(
        link='plugins:netbox_reservations:claim_test',
        link_text='Test',
        permissions=["netbox_reservations.view_claim"])
)

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_reservations', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(
        label="Reservations",
        groups=(("Reservations", _menu_items), ("Overviews", _overview_menu_items)),
        icon_class="mdi mdi-calendar",
    )
else:
    menu_items = _menu_items
