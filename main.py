# imports
import streamlit as st
from openai import OpenAI

# Statics


# Functions
# function to takes in a prompt
def input_prompt(client, input_prompt):
  story_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role":
          "system",
          "content":
          "You are bestseller story writer. You will take the user's prompt and generate a 100 words short story for adults age 20 to 30"
      }, {
          "role": "user",
          "content": f"{input_prompt}"
      }],
      max_tokens=400,
      temperature=0.8)

  story = story_response.choices[0].message.content
  return story


def refine_story(client, unrefined_story):
  design_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role":
          "system",
          "content":
          """Based on the story given. You will design a detailed image prompt for this cover image of this story.
            The image prompt should include the theme of the story with releveant color, suitable for adults.
            The output should be within 100 characters.
            """
      }, {
          "role": "user",
          "content": f"{unrefined_story}"
      }],
      max_tokens=400,
      temperature=0.8)
  refined_story = design_response.choices[0].message.content
  return refined_story


def display_image(client, refined_story):
  cover_response = client.images.generate(model="dall-e-2",
                                          prompt=f"{refined_story}",
                                          size="256x256",
                                          quality="standard",
                                          n=1)

  image_url = cover_response.data[0].url
  st.image(image=str(image_url), width=256)

  return image_url


# Main

# Set up OpenAI API credentials
api_key = st.secrets["OPENAI_SECRET"]

client = OpenAI(api_key=api_key)

with st.form("story_form"):
  st.write("This is for user to key in information")
  msg = st.text_input(label="Some keywords to generate a story: ")
  submitted = st.form_submit_button(label="Submit")
  if submitted:
    st.write("You have submitted the following: ", msg)
    unrefined_story = input_prompt(client, msg)
    refined_story = refine_story(client, unrefined_story)
    image_url = display_image(client, refined_story)
    st.write("Cover Image: ", refined_story)
