from rest_framework.permissions import BasePermission


def get_role(request):
    """Helper — safely returns the role from the authenticated user's profile."""
    try:
        return request.user.profile.role
    except Exception:
        return None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request) == 'Admin'


class IsAdminOrPhysicianOrNurse(BasePermission):
    """Roles that can register patients and place orders."""
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Physician', 'Nurse')


class IsPhlebotomist(BasePermission):
    """Roles that can collect samples."""
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Phlebotomist')


class IsLabTechnician(BasePermission):
    """Roles that can enter results."""
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'LabTechnician')


class IsClinicalStaff(BasePermission):
    """Roles that can view completed lab reports."""
    def has_permission(self, request, view):
        return get_role(request) in ('Admin', 'Physician', 'Nurse')