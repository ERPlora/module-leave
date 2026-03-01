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


@register_tool
class ListLeaveTypes(AssistantTool):
    name = "list_leave_types"
    description = "List available leave types with annual allowance."
    module_id = "leave"
    required_permission = "leave.view_leaverequest"
    parameters = {"type": "object", "properties": {}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from leave.models import LeaveType
        types = LeaveType.objects.filter(is_active=True)
        return {"leave_types": [{"id": str(t.id), "name": t.name, "days_per_year": t.days_per_year, "is_paid": t.is_paid} for t in types]}


@register_tool
class CreateLeaveRequest(AssistantTool):
    name = "create_leave_request"
    description = "Create a new leave request for an employee."
    module_id = "leave"
    required_permission = "leave.change_leaverequest"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string", "description": "Employee UUID"},
            "employee_name": {"type": "string", "description": "Employee name"},
            "leave_type_id": {"type": "string", "description": "Leave type ID"},
            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "reason": {"type": "string", "description": "Reason for leave"},
        },
        "required": ["employee_name", "leave_type_id", "start_date", "end_date"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from leave.models import LeaveRequest
        lr = LeaveRequest.objects.create(
            employee_id=args.get('employee_id', ''),
            employee_name=args['employee_name'],
            leave_type_id=args['leave_type_id'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            reason=args.get('reason', ''),
            status='pending',
        )
        return {"id": str(lr.id), "employee_name": lr.employee_name, "status": "pending", "created": True}


@register_tool
class ApproveLeaveRequest(AssistantTool):
    name = "approve_leave_request"
    description = "Approve a pending leave request."
    module_id = "leave"
    required_permission = "leave.change_leaverequest"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"request_id": {"type": "string", "description": "Leave request ID"}},
        "required": ["request_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from leave.models import LeaveRequest
        lr = LeaveRequest.objects.get(id=args['request_id'])
        if lr.status != 'pending':
            return {"error": f"Request is already {lr.status}"}
        lr.status = 'approved'
        lr.approved_by = request.session.get('local_user_id')
        lr.save(update_fields=['status', 'approved_by'])
        return {"id": str(lr.id), "employee_name": lr.employee_name, "status": "approved"}


@register_tool
class RejectLeaveRequest(AssistantTool):
    name = "reject_leave_request"
    description = "Reject a pending leave request."
    module_id = "leave"
    required_permission = "leave.change_leaverequest"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"request_id": {"type": "string", "description": "Leave request ID"}},
        "required": ["request_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from leave.models import LeaveRequest
        lr = LeaveRequest.objects.get(id=args['request_id'])
        if lr.status != 'pending':
            return {"error": f"Request is already {lr.status}"}
        lr.status = 'rejected'
        lr.save(update_fields=['status'])
        return {"id": str(lr.id), "employee_name": lr.employee_name, "status": "rejected"}
