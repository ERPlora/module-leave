"""Tests for leave models."""
import pytest
from django.utils import timezone

from leave.models import LeaveType


@pytest.mark.django_db
class TestLeaveType:
    """LeaveType model tests."""

    def test_create(self, leave_type):
        """Test LeaveType creation."""
        assert leave_type.pk is not None
        assert leave_type.is_deleted is False

    def test_str(self, leave_type):
        """Test string representation."""
        assert str(leave_type) is not None
        assert len(str(leave_type)) > 0

    def test_soft_delete(self, leave_type):
        """Test soft delete."""
        pk = leave_type.pk
        leave_type.is_deleted = True
        leave_type.deleted_at = timezone.now()
        leave_type.save()
        assert not LeaveType.objects.filter(pk=pk).exists()
        assert LeaveType.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, leave_type):
        """Test default queryset excludes deleted."""
        leave_type.is_deleted = True
        leave_type.deleted_at = timezone.now()
        leave_type.save()
        assert LeaveType.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, leave_type):
        """Test toggling is_active."""
        original = leave_type.is_active
        leave_type.is_active = not original
        leave_type.save()
        leave_type.refresh_from_db()
        assert leave_type.is_active != original


