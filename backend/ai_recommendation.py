import ollama

def get_ai_recommendation(weather_data):
    prompt = f"""
    Given the following weather conditions:
    - Location: {weather_data['location']['name']}, {weather_data['location']['country']}
    - Temperature: {weather_data['current']['temp_c']}°C
    - Condition: {weather_data['current']['condition']['text']}
    - Wind Speed: {weather_data['current']['wind_kph']} kph
    - Humidity: {weather_data['current']['humidity']}%
    
    Provide an assessment of the risks for transport and recommend alternative routes if necessary.
    """
    response = ollama.chat(model="deepseek-r1:14b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
