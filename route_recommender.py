def recommend_route(
    start,
    destination,
    traffic_data,
    passenger_type="Normal"
):

    # Get traffic values for each corridor
    corridors = {
        "North": traffic_data.get("North", 0),
        "South": traffic_data.get("South", 0),
        "East": traffic_data.get("East", 0),
        "West": traffic_data.get("West", 0)
    }

    # Sort corridors from lowest traffic to highest
    sorted_corridors = sorted(
        corridors,
        key=corridors.get
    )

    # Alternative corridors
    alternatives = [
        corridor
        for corridor in sorted_corridors
        if corridor != start and corridor != destination
    ]

    # Choose route
    if alternatives:

        best_alternative = alternatives[0]

        route = f"{start} → {best_alternative} → {destination}"

    else:

        route = f"{start} → {destination}"

    # Passenger priority handling
    if passenger_type == "Emergency":

        priority_message = (
            "EMERGENCY PRIORITY: Select the fastest "
            "available low-traffic route immediately."
        )

    elif passenger_type == "High Priority":

        priority_message = (
            "HIGH PRIORITY: Prefer the route with "
            "the lowest traffic congestion."
        )

    else:

        priority_message = (
            "NORMAL PRIORITY: Standard low-traffic "
            "route recommendation."
        )

    message = (
        f"Recommended route: {route}. "
        f"{priority_message}"
    )

    return {
        "route": route,
        "message": message,
        "passenger_priority": passenger_type,
        "traffic": corridors
    }