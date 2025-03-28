from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
import streamlit as st
import requests

openai_api_key = st.secrets["OPENAI_API_KEY"]

memory = ConversationBufferMemory()

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=openai_api_key)

conversation = ConversationChain(llm=llm, memory=memory)

st.title("AI Travel Planner")
st.write("Your personal AI travel guide")

#General preferences (User Prompts)
st.sidebar.header("Tell us about your trip")
start_location = st.sidebar.text_input("Start Location", placeholder="e.g., India")
destination = st.sidebar.text_input("Destination", placeholder="e.g., Tokyo, Japan")
budget = st.sidebar.selectbox("Budget", ["Budget", "Mid-range", "Luxury"])
duration = st.sidebar.slider("Trip Duration (days)", 1, 14, 5)
travel_purpose = st.sidebar.selectbox("Purpose", ["Sightseeing", "Work", "Food", "Adventure", "Relaxation", "Mixed"])
preferences = st.sidebar.text_area("Preferences", placeholder="e.g., Hidden gems, Local experiences")
dietary_preferences = st.sidebar.text_area("Food Preferences", placeholder="e.g., Vegetarian")

#Local attractions using GeoNames API
geonames_username = st.secrets["GEONAMES_USERNAME"]

#Function to Fetch Live Attractions
def fetch_geonames_places(destination):
    """Fetch top places using GeoNames API."""
    url = "http://api.geonames.org/wikipediaSearchJSON"
    params = {
        "q": destination,
        "maxRows": 10,
        "username": geonames_username # GeoNames requires your username as API key
    }
    response = requests.get(url, params=params).json()
    
    if "geonames" in response:
        return [place["title"] for place in response["geonames"]]
    
    return ["No results found."]

#Button to Find Attractions
if st.sidebar.button("Find Attractions"):
    if not destination:
        st.warning("Please enter a destination.")
    else:
        results = fetch_geonames_places(destination)
        st.subheader(f"Top Attractions in {destination}")
        st.write(results)

if st.sidebar.button("Plan My Trip"):
    if not destination:
        st.warning("Please enter a destination.")
    else:
        prompt = f"""
        The user wants a {budget} travel plan for {destination}. 
        - The trip is for {duration} days and focused on {travel_purpose}.
        - They prefer: {preferences}. 
        """

        response = conversation.predict(input=prompt) 

        st.subheader(f"Your {duration}-Day Itinerary for {destination}")
        st.write(response)

st.subheader("Conversation History")
st.text_area("Chat Memory", memory.buffer, height=200)

st.write("Powered by AI | Developed with Streamlit & LangChain")
