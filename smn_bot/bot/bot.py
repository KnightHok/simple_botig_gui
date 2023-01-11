import os
import os.path

import json

from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from dotenv import load_dotenv

# UPLOAD IG VIDEO WITH CAPTION & TAGS

class Instagram():
    ig_client = None

    def __init__(self, username, password, settings_file_location):
        self.ig_account_username = username
        self.settings_file_location = settings_file_location
        self.ig_client = self.Login(username, password)

    def Login(self, username, password):
        try:
            # create instagrapi Client object
            client = Client()
            client.challenge_code_handler = self.default_handler
            print("Attempting to Connect to Account")
            if os.path.exists(self.settings_file_location):
                print("settings found")
                # if there is a settings file

                settings_file = open(self.settings_file_location)
                settings = json.load(settings_file)
                print(settings)

                client.set_settings(settings["device_settings"])
                client.login(username, password)
                print("logged in (with settigns)")
            else:
                # login then dump new settings data
                client.login(username, password)
                print("logged in")

                # client.dump_settings("./client_settings.json")
                print("new settings data has been saved")
        except:
            # log the error and send back to user client
            print("Error while logging in to Instagram")
        return client

    def default_handler(self, username, choice):
        if choice == ChallengeChoice.EMAIL:
            return input("Enter email code: ")

    def submitVideo(self, file_path, caption):
        self.ig_client.video_upload(path=file_path, caption=caption)


if __name__ == "__main__":

    load_dotenv("../.env")
    client_settings_location = "../client_settings.json"

    ig_username = os.getenv("IG_USERNAME")
    ig_password = os.getenv("IG_PASSWORD")

    # get video with a users desired caption and tags
    # video_loaction = "./videos/video.mp4"
    # caption = "chip chip chip\n\n\n\n\n\n\n-----------------"
    # tags = "#random"

    # upload_caption = caption + tags

    session = Instagram(ig_username, ig_password, client_settings_location)
    print(session.ig_client.get_settings())

    # set client user agent
    user_agent = "Mozilla/5.0 (Linux; Android 8.0.0; RNE-L21 Build/HUAWEIRNE-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/73.0.3683.90 Mobile Safari/537.36 Instagram 86.0.0.24.87 Android (26/8.0.0; 480dpi; 1080x2040; HUAWEI; RNE-L21; HWRNE; hi6250; ru_RU; 147375143)"

    # client.set_user_agent(user_agent=user_agent)

    # upload video with user caption and tags

    # client.video_upload(path="./videos/video.mp4", caption=upload_caption, thumbnail="./thumbnails/thumbnail.jpg")
