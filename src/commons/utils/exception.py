from rest_framework.views import Response, exception_handler
from commons.utils.response import APIResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            APIResponse.error(message=str(exc), data=response.data),
            status=response.status_code,
        )

    return Response(APIResponse.error(), status=500)