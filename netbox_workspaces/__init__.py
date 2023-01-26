from extras.plugins import PluginConfig


class NetBoxWorkspacesConfig(PluginConfig):
    name = 'netbox_workspaces'
    verbose_name = 'NetBox Workspaces'
    description = 'Manage workspaces in NetBox'
    version = '0.1'
    base_url = 'workspaces'


config = NetBoxWorkspacesConfig
