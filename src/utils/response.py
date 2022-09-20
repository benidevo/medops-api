from rest_framework.response import Response as DRFResponse


class Response:
    def __new__(
        cls, status_code, success=None, data=None, message=None, errors=None, **kwargs
    ):
        return DRFResponse(
            {
                "success": success,
                "message": message if not errors else "validation error",
                "data": data,
                "errors": errors,
                **kwargs,
            },
            status=status_code,
        )
