from .models import ViewingSlot
from datetime import date


def viewing_slots(request):
    """
    Context processor to make viewing slots available across all templates.
    Returns an empty slots list if no property_id is provided in the request.
    """
    property_id = request.GET.get('property_id')
    slots = []

    if property_id:
        try:
            # Get all available slots for the property
            slots = ViewingSlot.objects.filter(
                property_id=property_id,
                is_booked=False,
                date__gte=date.today()
            ).order_by('date', 'start_time')

            # Format slots for template use
            slots = [{
                'id': slot.id,
                'date': slot.date,
                'start_time': slot.start_time,
                'formatted_date': slot.date.strftime('%B %d, %Y'),
                'formatted_time': (
                    f"{slot.start_time.strftime('%I:%M %p')} - "
                    f"{slot.end_time.strftime('%I:%M %p')}"
                ),
            } for slot in slots]

        except (ValueError, TypeError):
            # Handle invalid property_id gracefully
            slots = []

    return {
        'slots': slots
    }
