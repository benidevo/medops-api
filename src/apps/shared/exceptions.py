from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response

from utils.response import Response as CustomResponse


def custom_handler(exc, context):
    """
    custom exception handler
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.NotAuthenticated):
        return CustomResponse(
            message="Authentication credentials were not provided.",
            success=False,
            status_code=401,
        )
    if isinstance(exc, exceptions.APIException):
        if exc.status_code == 401:
            return CustomResponse(
                message="Token is invalid or expired", success=False, status_code=401
            )
        if exc.status_code == 403:
            return CustomResponse(
                message="You do not have permission to perform this action",
                success=False,
                status_code=403,
            )

        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"detail": exc.detail}

        return Response(data, status=exc.status_code, headers=headers)

    return None
