"""
DriveIntel Agentic AI Co-pilot — Safety & Financial Assistant
"""

from utils.logging import log_info, log_warn
from data.sample_data import get_trips, get_goals, STRESS_TIPS
from datetime import datetime, timedelta

def run_co_pilot(user_message: str) -> str:
    """
    Process user message and return AI response.
    Analyzes trips, goals, stress patterns, and provides safety/financial advice.
    """
    try:
        message_lower = user_message.lower().strip()
        
        # Get user data
        trips = get_trips()
        goals = get_goals()
        daily_target = goals.get("daily_target", 50000)
        
        # ── Intent Recognition & Response Logic ──
        
        # 1. GREETING
        if any(word in message_lower for word in ["hello", "hi", "hey", "howdy"]):
            return "Hey there! 👋 I'm here to help you stay safe and maximize your earnings. What can I assist you with?"
        
        # 2. STRESS/SAFETY QUERIES
        if any(word in message_lower for word in ["stress", "anxious", "scared", "safe", "safety"]):
            high_stress_trips = [t for t in trips if t.get("stress_level") == "high"]
            if high_stress_trips:
                avg_stress = sum(t.get("stress_score", 0) for t in high_stress_trips) / len(high_stress_trips)
                tip = STRESS_TIPS[0] if STRESS_TIPS else "Take regular breaks and stay hydrated!"
                return f"I see you've had {len(high_stress_trips)} high-stress trips recently (avg score: {avg_stress:.1f}/10). 💡 Here's a tip: {tip}"
            return "Your recent trips look safe! Keep up the defensive driving habits. 🛡️"
        
        # 3. EARNINGS/GOALS
        if any(word in message_lower for word in ["earning", "money", "goal", "target", "income", "fare", "revenue"]):
            if trips:
                total_earned = sum(t.get("fare", 0) for t in trips[-7:])
                trips_count = len(trips[-7:])
                daily_avg = total_earned / 7 if trips_count > 0 else 0
                remainder = max(0, daily_target - daily_avg)
                return f"📊 Last 7 days: ₹{total_earned:.0f} (avg ₹{daily_avg:.0f}/day). Your goal is ₹{daily_target}. Keep {trips_count} trips going! {'You\'re on track! 🎯' if daily_avg >= daily_target else f'Aim for ₹{remainder:.0f} more to reach goal.'}"
            return f"No trips yet! Start driving to reach your ₹{daily_target} daily goal. 🚗"
        
        # 4. TRIP ANALYSIS
        if any(word in message_lower for word in ["trip", "drive", "today", "yesterday", "last"]):
            if trips:
                recent = trips[-1]
                return f"📍 Your last trip: {recent.get('distance_km', 0):.1f}km, ₹{recent.get('fare', 0):.0f}, Stress: {recent.get('stress_level', 'unknown')}. Great work! 💪"
            return "No trips recorded yet. Start your first trip! 🚗"
        
        # 5. BREAKS/REST
        if any(word in message_lower for word in ["break", "rest", "tired", "fatigue", "sleep"]):
            return "Take a 15-20 minute break every 2 hours of driving. Staying fresh keeps you safe and alert! 😴 Your health is priority #1."
        
        # 6. NAVIGATION/ROUTE
        if any(word in message_lower for word in ["navigation", "route", "direction", "where", "location"]):
            return "For route planning, use Google Maps or your preferred navigation app. Safe routes = better stress management! 🗺️"
        
        # 7. VEHICLE/MAINTENANCE
        if any(word in message_lower for word in ["vehicle", "car", "maintenance", "gas", "service", "tire"]):
            return "Regular vehicle maintenance is crucial for safety! Check tires, brakes, and fluids weekly. A well-maintained car = safer trips! 🔧"
        
        # 8. WEATHER/CONDITIONS
        if any(word in message_lower for word in ["weather", "rain", "storm", "fog", "wind", "road"]):
            return "In bad weather, reduce speed and increase following distance. Your safety matters more than reaching a destination fast! 🌧️"
        
        # 9. PASSENGER/COMMUNICATION
        if any(word in message_lower for word in ["passenger", "rating", "feedback", "review", "customer"]):
            return "Maintain professionalism with passengers: keep the car clean, be courteous, and focus on safe driving. Good ratings follow naturally! ⭐"
        
        # 10. GENERAL ADVICE
        if any(word in message_lower for word in ["advice", "help", "tip", "suggest", "recommend"]):
            tip = STRESS_TIPS[0] if STRESS_TIPS else "Drive defensively and take regular breaks!"
            return f"💡 Safety tip: {tip}"
        
        # DEFAULT - INTELLIGENT FALLBACK
        return f"I'm here to help with safety, earnings, trips, and driving tips! Ask me about your goals, stress levels, or safe driving practices. What would you like to know? 🤖"
        
    except Exception as e:
        log_warn(f"Co-pilot error: {str(e)}")
        raise Exception(f"Agent processing failed: {str(e)}")