"""Tests for leave views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('leave:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('leave:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('leave:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestLeaveTypeViews:
    """LeaveType view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('leave:leave_types_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('leave:leave_type_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('leave:leave_type_add')
        data = {
            'name': 'New Name',
            'days_per_year': '5',
            'is_paid': 'on',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, leave_type):
        """Test edit form loads."""
        url = reverse('leave:leave_type_edit', args=[leave_type.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, leave_type):
        """Test editing via POST."""
        url = reverse('leave:leave_type_edit', args=[leave_type.pk])
        data = {
            'name': 'Updated Name',
            'days_per_year': '5',
            'is_paid': '',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, leave_type):
        """Test soft delete via POST."""
        url = reverse('leave:leave_type_delete', args=[leave_type.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        leave_type.refresh_from_db()
        assert leave_type.is_deleted is True

    def test_toggle_status(self, auth_client, leave_type):
        """Test toggle active status."""
        url = reverse('leave:leave_type_toggle_status', args=[leave_type.pk])
        original = leave_type.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        leave_type.refresh_from_db()
        assert leave_type.is_active != original

    def test_bulk_delete(self, auth_client, leave_type):
        """Test bulk delete."""
        url = reverse('leave:leave_types_bulk_action')
        response = auth_client.post(url, {'ids': str(leave_type.pk), 'action': 'delete'})
        assert response.status_code == 200
        leave_type.refresh_from_db()
        assert leave_type.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('leave:leave_types_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('leave:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('leave:settings')
        response = client.get(url)
        assert response.status_code == 302

