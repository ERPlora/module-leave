"""
Leave Management Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('leave', 'dashboard')
@htmx_view('leave/pages/dashboard.html', 'leave/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('leave', 'requests')
@htmx_view('leave/pages/requests.html', 'leave/partials/requests_content.html')
def requests(request):
    """Requests view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('leave', 'settings')
@htmx_view('leave/pages/settings.html', 'leave/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

