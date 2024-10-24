from rest_framework import permissions
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class IsValidToken(permissions.BasePermission):
    """
    checks token blacklisted or not
    """

    def has_permission(self, request, view):
        is_allowed_user = True
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(" ")[1]
        if not token:
            return False
        try:
            is_blackListed = BlacklistedToken.objects.get(
                token__user=request.user, token__token=token
            )
            if is_blackListed:
                is_allowed_user = False
        except BlacklistedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
