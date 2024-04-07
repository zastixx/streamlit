import streamlit as st
from apify_client import ApifyClient
import pandas as pd

# Function to fetch and display results for a username
def fetch_and_display_results(username):
  client = ApifyClient(st.secrets["apify_api_token"])  # Access API token from Streamlit secrets
  run_input = {"usernames": [username.strip()]}

  run = client.actor("dSCLg0C3YEZ83HzYX").call(run_input=run_input)

  if "defaultDatasetId" in run:
    dataset_results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
      dataset_results.append(item)

    if dataset_results:
      df = pd.DataFrame(dataset_results)
      st.subheader(f"Results for username: {username}")
      st.dataframe(df)
    else:
      st.write(f"No results found for username: {username}")
  else:
    st.write("Actor run did not produce a default dataset.")

# Streamlit App
st.title("INSTAGRAM PROFILE ANALYZER")
st.subheader(
    """Analyze any public profile on Instagram the tool is free
   """
)

# Get usernames from user (using Streamlit text input)
usernames = st.text_input("Enter usernames separated by commas", "")

# Add API token securely using Streamlit secrets
if not st.secrets.get("apify_api_token"):
  st.warning("Please add your API token to Streamlit secrets!")
  st.stop()

# Split usernames
if usernames:
  usernames_list = usernames.split(",")
  for username in usernames_list:
    fetch_and_display_results(username.strip())
