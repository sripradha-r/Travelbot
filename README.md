Tools:
1. Streamlit - Frontend
2. LangChain - Remembers preference history
3. OpenAI - Chatbot mechanism (need to use your API key)
4. GeoNames - Top attractions in a city/country (need to use your API key)

User prompts:
1. Start Location
2. Destination
3. Budget
4. Trip Duration (days)
5. Purpose
6. Preferences
7. Food Preferences

System prompt:
The user wants a {budget} travel plan for {destination}. 
        - The trip is for {duration} days and focused on {travel_purpose}.
        - They prefer: {preferences}

Steps to use the app:
1. Create virtual environment using Python's venv
python -m venv venv
venv/Scripts/activate
2. Install packages
pip install -r requirements.txt
3. Run your streamlit app
streamlit run app.py
