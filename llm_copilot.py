import os
from dotenv import load_dotenv
from google import genai
from knowledge_base.rag_engine import get_rag_context
# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def generate_disruption_explanation(
    north,
    south,
    east,
    west,
    traffic_level,
    green_time
):
    """
    Generates an LLM-based explanation of
    public transport disruption using live traffic data.
    """
    query = f"{traffic_level} traffic disruption affecting North South East West corridors and public transport passengers"

    rag_context = get_rag_context(query)
    print("\n===== RAG RETRIEVED CONTEXT =====")
    print(rag_context)
    print("=================================\n")
    prompt = f"""
    You are TwinFlow Mobility Copilot, an AI assistant for
    public transport disruption management.

LIVE TRAFFIC DATA:
- North corridor: {north} vehicles
- South corridor: {south} vehicles
- East corridor: {east} vehicles
- West corridor: {west} vehicles
- Overall traffic level: {traffic_level}
- ML predicted green signal time: {green_time} seconds
RETRIEVED TRANSPORT KNOWLEDGE (RAG):
{rag_context}

Use the retrieved transport knowledge together with the live traffic data.
Base your recommendations on this information when relevant.

TASK:
Analyze the traffic situation and provide:

1. A short traffic summary.
2. Possible impact on buses and public transport.
3. Which corridor needs attention.
4. A recommended action for commuters or traffic operators.

IMPORTANT:
- Do not claim that you know actual bus schedules.
- Clearly say that disruption impact is an estimate based
  on observed traffic conditions.
- Keep the response concise and easy to understand.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


# Test the file directly
if __name__ == "__main__":

    result = generate_disruption_explanation(
        north=80,
        south=20,
        east=35,
        west=15,
        traffic_level="HIGH",
        green_time=60
    )

    print("\n--- TWINFLOW MOBILITY COPILOT ---\n")
    print(result)