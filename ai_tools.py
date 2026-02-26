"""AI tools for the Leave module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListLeaveRequests(AssistantTool):
    name = "list_leave_requests"
    description = "List leave requests with optional filters by status or employee."
    module_id = "leave"
    required_permission = "leave.view_leaverequest"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Filter: pending, approved, rejected, cancelled"},
            "employee_name": {"type": "string", "description": "Filter by employee name"},
            "limit": {"type": "integer", "description": "Max results (default 20)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from leave.models import LeaveRequest
        qs = LeaveRequest.objects.select_related('leave_type').order_by('-start_date')
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('employee_name'):
            qs = qs.filter(employee_name__icontains=args['employee_name'])
        limit = args.get('limit', 20)
        return {
            "leave_requests": [
                {
                    "id": str(lr.id),
                    "employee_name": lr.employee_name,
                    "leave_type": lr.leave_type.name if lr.leave_type else None,
                    "start_date": str(lr.start_date),
                    "end_date": str(lr.end_date),
                    "days_count": lr.days_count,
                    "status": lr.status,
                    "reason": lr.reason,
                }
                for lr in qs[:limit]
            ],
            "total": qs.count(),
        }


@register_tool
class GetPendingLeaveRequests(AssistantTool):
    name = "get_pending_leave_requests"
    description = "Get all pending leave requests that need approval."
    module_id = "leave"
    required_permission = "leave.view_leaverequest"
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from leave.models import LeaveRequest
        pending = LeaveRequest.objects.filter(status='pending').order_by('start_date')
        return {
            "pending": [
                {
                    "id": str(lr.id),
                    "employee_name": lr.employee_name,
                    "leave_type": lr.leave_type.name if lr.leave_type else None,
                    "start_date": str(lr.start_date),
                    "end_date": str(lr.end_date),
                    "days_count": lr.days_count,
                    "reason": lr.reason,
                }
                for lr in pending
            ],
            "total": pending.count(),
        }
