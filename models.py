from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

LEAVE_STATUS = [
    ('pending', _('Pending')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
    ('cancelled', _('Cancelled')),
]

class LeaveType(HubBaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    days_per_year = models.PositiveIntegerField(default=0, verbose_name=_('Days Per Year'))
    is_paid = models.BooleanField(default=True, verbose_name=_('Is Paid'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'leave_leavetype'

    def __str__(self):
        return self.name


class LeaveRequest(HubBaseModel):
    employee_id = models.UUIDField(db_index=True, verbose_name=_('Employee Id'))
    employee_name = models.CharField(max_length=255, verbose_name=_('Employee Name'))
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))
    days_count = models.DecimalField(max_digits=5, decimal_places=1, default='1', verbose_name=_('Days Count'))
    status = models.CharField(max_length=20, default='pending', choices=LEAVE_STATUS, verbose_name=_('Status'))
    reason = models.TextField(blank=True, verbose_name=_('Reason'))
    approved_by = models.UUIDField(null=True, blank=True, verbose_name=_('Approved By'))

    class Meta(HubBaseModel.Meta):
        db_table = 'leave_leaverequest'

    def __str__(self):
        return str(self.id)

