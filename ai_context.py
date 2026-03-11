"""
AI context for the Leave module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Leave

### Models

**LeaveType**
- name (str), days_per_year (int), is_paid (bool), is_active (bool)
- Examples: Vacation (22 days, paid), Sick Leave (15 days, paid), Unpaid Leave (0 days, unpaid)

**LeaveRequest**
- employee_id (UUID, indexed) — references the employee's UUID
- employee_name (str, cached)
- leave_type (FK → LeaveType)
- start_date, end_date (DateField)
- days_count (Decimal, e.g. 1, 0.5) — must be set by caller
- status: pending | approved | rejected | cancelled
- reason (text, optional)
- approved_by (UUID, optional) — UUID of the approving manager/user

### Key flows

1. **Setup leave types**: Create LeaveType records (Vacation, Sick Leave, Personal, etc.)
2. **Submit leave request**: Create LeaveRequest with employee_id, leave_type, start_date, end_date, days_count, status=pending
3. **Approve request**: Update status → approved, set approved_by (UUID of approver)
4. **Reject request**: Update status → rejected
5. **Cancel request**: Update status → cancelled (employee or manager)

### Notes

- days_count is not auto-calculated from dates — caller must provide it (account for weekends/holidays if needed)
- approved_by stores a UUID, not an FK object
- There is no balance tracking in this module — it only records requests
- To check remaining leave, query LeaveRequest for the employee filtered by year and status=approved, then compare to LeaveType.days_per_year
"""
