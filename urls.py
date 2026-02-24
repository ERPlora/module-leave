from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # LeaveType
    path('leave_types/', views.leave_types_list, name='leave_types_list'),
    path('leave_types/add/', views.leave_type_add, name='leave_type_add'),
    path('leave_types/<uuid:pk>/edit/', views.leave_type_edit, name='leave_type_edit'),
    path('leave_types/<uuid:pk>/delete/', views.leave_type_delete, name='leave_type_delete'),
    path('leave_types/<uuid:pk>/toggle/', views.leave_type_toggle_status, name='leave_type_toggle_status'),
    path('leave_types/bulk/', views.leave_types_bulk_action, name='leave_types_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
