# Leave Management Module

Employee leave requests and approvals.

## Features

- Define leave types with annual day allowances and paid/unpaid classification
- Submit leave requests with start date, end date, and reason
- Approval workflow with pending, approved, rejected, and cancelled statuses
- Track which manager approved each request
- Fractional day support (half-days) via decimal day counts
- Employee-linked requests via UUID reference

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Leave Management > Settings**

Configure leave types, annual allowances, and approval rules.

## Usage

Access via: **Menu > Leave Management**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/leave/dashboard/` | Leave overview and summary statistics |
| Requests | `/m/leave/requests/` | View, create, and manage leave requests |
| Settings | `/m/leave/settings/` | Configure leave types and module settings |

## Models

| Model | Description |
|-------|-------------|
| `LeaveType` | Leave category with name, days per year allowance, paid/unpaid flag, and active status |
| `LeaveRequest` | Employee leave request with type, date range, day count, status, reason, and approver reference |

## Permissions

| Permission | Description |
|------------|-------------|
| `leave.view_leaverequest` | View leave requests |
| `leave.add_leaverequest` | Submit new leave requests |
| `leave.change_leaverequest` | Edit leave requests |
| `leave.approve_leaverequest` | Approve or reject leave requests |
| `leave.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
