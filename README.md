# Leave Management

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `leave` |
| **Version** | `1.0.0` |
| **Icon** | `calendar-clear-outline` |
| **Dependencies** | None |

## Models

### `LeaveType`

LeaveType(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, days_per_year, is_paid, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=100 |
| `days_per_year` | PositiveIntegerField |  |
| `is_paid` | BooleanField |  |
| `is_active` | BooleanField |  |

### `LeaveRequest`

LeaveRequest(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, employee_id, employee_name, leave_type, start_date, end_date, days_count, status, reason, approved_by)

| Field | Type | Details |
|-------|------|---------|
| `employee_id` | UUIDField | max_length=32 |
| `employee_name` | CharField | max_length=255 |
| `leave_type` | ForeignKey | → `leave.LeaveType`, on_delete=CASCADE |
| `start_date` | DateField |  |
| `end_date` | DateField |  |
| `days_count` | DecimalField |  |
| `status` | CharField | max_length=20, choices: pending, approved, rejected, cancelled |
| `reason` | TextField | optional |
| `approved_by` | UUIDField | max_length=32, optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `LeaveRequest` | `leave_type` | `leave.LeaveType` | CASCADE | No |

## URL Endpoints

Base path: `/m/leave/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `requests/` | `requests` | GET |
| `leave_types/` | `leave_types_list` | GET |
| `leave_types/add/` | `leave_type_add` | GET/POST |
| `leave_types/<uuid:pk>/edit/` | `leave_type_edit` | GET |
| `leave_types/<uuid:pk>/delete/` | `leave_type_delete` | GET/POST |
| `leave_types/<uuid:pk>/toggle/` | `leave_type_toggle_status` | GET |
| `leave_types/bulk/` | `leave_types_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `leave.view_leaverequest` | View Leaverequest |
| `leave.add_leaverequest` | Add Leaverequest |
| `leave.change_leaverequest` | Change Leaverequest |
| `leave.approve_leaverequest` | Approve Leaverequest |
| `leave.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_leaverequest`, `approve_leaverequest`, `change_leaverequest`, `view_leaverequest`
- **employee**: `add_leaverequest`, `view_leaverequest`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Requests | `calendar-clear-outline` | `requests` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_leave_requests`

List leave requests with optional filters by status or employee.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: pending, approved, rejected, cancelled |
| `employee_name` | string | No | Filter by employee name |
| `limit` | integer | No | Max results (default 20) |

### `get_pending_leave_requests`

Get all pending leave requests that need approval.

### `list_leave_types`

List available leave types with annual allowance.

### `create_leave_request`

Create a new leave request for an employee.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `employee_id` | string | No | Employee UUID |
| `employee_name` | string | Yes | Employee name |
| `leave_type_id` | string | Yes | Leave type ID |
| `start_date` | string | Yes | Start date (YYYY-MM-DD) |
| `end_date` | string | Yes | End date (YYYY-MM-DD) |
| `reason` | string | No | Reason for leave |

### `approve_leave_request`

Approve a pending leave request.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | string | Yes | Leave request ID |

### `reject_leave_request`

Reject a pending leave request.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | string | Yes | Leave request ID |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  leave/
    css/
    js/
templates/
  leave/
    pages/
      dashboard.html
      index.html
      leave_type_add.html
      leave_type_edit.html
      leave_types.html
      requests.html
      settings.html
    partials/
      dashboard_content.html
      leave_type_add_content.html
      leave_type_edit_content.html
      leave_types_content.html
      leave_types_list.html
      panel_leave_type_add.html
      panel_leave_type_edit.html
      requests_content.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
