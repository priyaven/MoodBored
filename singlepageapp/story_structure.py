import openai
from pathlib import Path
import json
import random
import os

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

model_list = ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613'] #, 'gpt-4-0314', 'gpt-4-0613']

BASE_DIR = Path(__file__).resolve().parent
with open(os.path.join(BASE_DIR, "apikey"), "r") as apifile:
    openai.api_key = apifile.read().strip()

class Character:
    name = None
    description = None

class Story:
    story_text = None
    characters = []
    plot_points = []
    settings = []

    art_style = None

    def __init__(self, story_string):
        self.story_text = story_string

    def get_characters_from_story_text(self):
        context = ("Please read the following story and " +
                   "answer questions using the information present here. "
                                  + self.story_text)
        model = random.choice(model_list)

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system",
                       "content": context },
                      {"role": "user", "content": "Pick any 3 characters in the story. ß"
                                                  + "Can you generate a physical description of them I can feed into an image prompt? Make sure to pay attention to race, age, clothes."
                                                  +  "Please return a json string, with fields for character name (CharacterName) and description (Description). Please make sure the json isn't broken."}
            ]
        )
        #answer = response.choices[0].text.strip()
        character_json_string = response.choices[0].message.content
        logger.debug(character_json_string)
        character_json = json.loads(character_json_string)
        if isinstance(character_json, dict):
            keys = list(character_json.keys())
            character_json = character_json[keys[0]]
        for character in character_json:
            c = Character()
            c.name = character['CharacterName']
            c.description = character['Description']
            self.characters.append(c)

        for character in self.characters:
            logger.debug(character.name)
            logger.debug(character.description)
            logger.debug("***")


    def get_art_style(self):
        context = ("Please read the following story and " +
                   "answer questions using the information present here. "
                   + self.story_text)
        art_style_response = openai.ChatCompletion.create(
            model=random.choice(model_list),
            messages=[{"role": "system",
                       "content": context},
                      {"role": "user", "content": "what art style best suits this story? Answer in one phrase."}])
        self.art_style = art_style_response.choices[0].message.content
        logger.debug(self.art_style)

    def get_scenes_from_story(self):
        context = ("Please read the following story and " +
                   "answer questions using the information present here. "
                   + self.story_text)
        model = random.choice(model_list)
        scenes_response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system",
                       "content": context},
                      {"role": "user", "content": "Can you extract 3 vividly visual scenes that represent the story?"
                                                  + "Return them as a json list."}])
        scenes_json_string = scenes_response.choices[0].message.content
        logger.debug(scenes_json_string)
        scenes_json = json.loads(scenes_json_string)
        self.plot_points = scenes_json
        for plot_point in self.plot_points:
            logger.debug(plot_point)
            logger.debug("*******")

    def get_settings_from_story(self):
        context = ("Please read the following story and " +
                   "answer questions using the information present here. "
                   + self.story_text)
        model = random.choice(model_list)
        scenes_response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system",
                       "content": context},
                      {"role": "user", "content": "Can you extract 3 settings in the story? Describe them vividly."
                                                  + "Return them as a json list."}])
        scenes_json_string = scenes_response.choices[0].message.content
        scenes_json = json.loads(scenes_json_string)
        self.settings = scenes_json
        for setting in self.settings:
            logger.debug(setting)


def get_prompts_from_story_text(story_text):
    s = Story(story_text)
    s.get_art_style()
    s.get_characters_from_story_text()
    s.get_scenes_from_story()

    prompts = []
    prefix = "In the style of " + s.art_style + ", draw "
    for character in s.characters:
        prompts.append(prefix + character.description)
    for plot_point in s.plot_points:
        prompts.append(prefix + plot_point)
    for scene in s.settings:
        prompts.append(prefix + scene)
    return prompts

def get_images_from_prompts(prompts):
    images = []
    for prompt in prompts:
        try:
            response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256"
            )
            image_url = response['data'][0]['url']
            images.append(image_url)
        except:
            logger.debug("oopsie fucked up on prompt " + prompt)
            continue
    return images

'''
story_folder = "./shortstories/"
# story_file = "john_redding_goes_to_sea.txt"
story_file = "aerwin.txt"

story_path = Path(__file__).parent / story_folder / story_file
story_txt = None
with open(story_path) as my_file:
    story_txt = my_file.read()

# prompts = get_prompts_from_story_text(story_txt)
# get_images_from_prompts(prompts)
'''



# OPENAI BOILERPLATE
'''
import openai
openai.api_key = "YOUR_API_KEY"

prompt = "Hello, my name is John and I am a software engineer."
model = "text-davinci-003"
response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

generated_text = response.choices[0].text
print(generated_text)
'''