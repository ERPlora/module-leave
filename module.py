from django.utils.translation import gettext_lazy as _

MODULE_ID = 'leave'
MODULE_NAME = _('Leave Management')
MODULE_VERSION = '1.0.1'
MODULE_ICON = 'material:event_available'
MODULE_DESCRIPTION = _('Employee leave requests and approvals')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'hr'
HAS_MODELS = True

MENU = {
    'label': _('Leave Management'),
    'icon': 'calendar-clear-outline',
    'order': 41,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Requests'), 'icon': 'calendar-clear-outline', 'id': 'requests'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'leave.view_leaverequest',
'leave.add_leaverequest',
'leave.change_leaverequest',
'leave.approve_leaverequest',
'leave.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_leaverequest",
        "approve_leaverequest",
        "change_leaverequest",
        "view_leaverequest",
    ],
    "employee": [
        "add_leaverequest",
        "view_leaverequest",
    ],
}
