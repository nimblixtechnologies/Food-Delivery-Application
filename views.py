from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeliveryPartner
import json
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


@csrf_exempt
def assign(request):
    if request.method == "POST":
        data = json.loads(request.body)

        lat = float(data["restaurant_lat"])
        lng = float(data["restaurant_lng"])

        partners = DeliveryPartner.objects.filter(is_available=True)

        if not partners.exists():
            return JsonResponse({"error": "No available partners"})

        best_partner = None
        shortest_distance = 999

        for p in partners:
            dist = calculate_distance(lat, lng, p.latitude, p.longitude)

            if dist < shortest_distance:
                shortest_distance = dist
                best_partner = p

        return JsonResponse({
            "assigned_partner": best_partner.name,
            "distance_km": round(shortest_distance, 2)
        })

    return JsonResponse({"error": "POST required"})
