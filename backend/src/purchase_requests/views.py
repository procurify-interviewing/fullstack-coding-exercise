from django.http import JsonResponse


def list_purchase_requests(request):
    """
    GET /api/purchase-requests/

    See backend/EXERCISE.md for the brief. Replace this stub.
    """
    return JsonResponse({"detail": "Not implemented yet."}, status=501)
