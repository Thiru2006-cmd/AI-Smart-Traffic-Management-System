from route_recommender import recommend_route


def analyze_passenger_journey(
    start,
    destination,
    passenger_type,
    traffic_data
):
    """
    Analyze passenger journey based on:
    - Start corridor
    - Destination corridor
    - Passenger priority
    - Current traffic conditions
    """

    # Traffic at starting corridor
    start_traffic = traffic_data.get(start, 0)

    # Traffic at destination corridor
    destination_traffic = traffic_data.get(destination, 0)

    # Calculate total traffic
    total_traffic = start_traffic + destination_traffic

    # Journey status and estimated delay
    if total_traffic >= 15:
        journey_status = "HIGH DELAY RISK"
        estimated_delay = "10+ minutes"

    elif total_traffic >= 8:
        journey_status = "MODERATE DELAY RISK"
        estimated_delay = "5 minutes"

    else:
        journey_status = "LOW DELAY RISK"
        estimated_delay = "2 minutes"

    # Passenger priority scores
    priority_scores = {
        "Normal": 1,
        "High Priority": 2,
        "Emergency": 3
    }

    priority_score = priority_scores.get(
        passenger_type,
        1
    )

    # Get route recommendation
    route_result = recommend_route(
        start,
        destination,
        traffic_data,
        passenger_type
    )

    # Return all journey information
    return {
        "start": start,
        "destination": destination,
        "passenger_type": passenger_type,
        "priority_score": priority_score,
        "start_traffic": start_traffic,
        "destination_traffic": destination_traffic,
        "journey_status": journey_status,
        "estimated_delay": estimated_delay,
        "route_result": route_result
    }