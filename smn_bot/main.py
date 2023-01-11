# File System imports
import os
import os.path
import json

# Cryptography imports
from cryptography.fernet import Fernet

# GUI imports
import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfile

# Bot imports
from bot import Instagram

def encode_password(password):
    binary_pass = password.encode("ascii")
    cipher_suite = Fernet(hash_key)
    encrypted = cipher_suite.encrypt(binary_pass)
    return encrypted.decode("ascii")

def decode_password(hash):
    # convert to binary
    binary_hash = hash.encode("ascii")
    cipher_suite = Fernet(hash_key)
    decrypted = cipher_suite.decrypt(binary_hash)
    return decrypted.decode("ascii")

def on_client_save():
    save_client_text.set("Saving...") 

    # get username and password
    username = username_text_box.get("1.0", "end-1c")
    password = password_text_box.get()
    settings_location = settings_location_text_box.get("1.0", "end-1c")

    # encrypt password
    encrypted_password = encode_password(password)

    try:
        # start instagram client
        session = Instagram(username, password, settings_location)

        device_settings = session.ig_client.get_settings()
        client_settings = {
            "username": username,
            "password": encrypted_password,
            "device_settings": device_settings
        }

        # serializing json
        client_settings_json = json.dumps(client_settings, indent=4)
        print(client_settings_json)
        if settings_location == "":
            settings_location = "./client_settings.json"
        with open(settings_location, "w") as f:
            f.write(client_settings_json)
    except:
        print("Big Error")

    password_text_box.delete(0, "end")
    save_client_text.set("Save Client")

def on_post():
    # get video location, settings location and thumbnail location
    video_location = video_location_text_box.get("1.0", "end-1c")
    settings_file_location = settings_location_text_box.get("1.0", "end-1c")
    thumbnail_location = thumbnail_location_text_box.get("1.0", "end-1c")
    caption = video_caption_text_box.get("1.0", "end-1c")
    tags = video_tags_text_box.get("1.0", "end-1c")
    video_caption = f'{caption}\n.\n.\n.\n.\n.\n.\n.\n{tags}'

    # get settings from file
    settings_file = open(settings_file_location)
    settings = json.load(settings_file)

    # upload video
    username = settings["username"]
    password = settings["password"]
    
    decrypted_password = decode_password(password)

    print(video_location)
    session = Instagram(username, decrypted_password, settings_file_location)
    if thumbnail_location != "":
        session.ig_client.video_upload(path=video_location, caption=video_caption, thumbnail=thumbnail_location)
    else:
        session.ig_client.video_upload(path=video_location, caption=video_caption)

    print("VIDEO UPLOADED")
    # except:
    #     print("Error trying to Post")

def open_video_location():
    video_browse_text.set("loading....")
    file = askopenfile(parent=root, mode='rb', title="Choose a Video File", filetypes=[('Mp4 file','*.mp4'), ('Mov file', '*.mov')])
    if file:
        video_location_text_box.insert(1.0, file.name)
    video_browse_text.set("Browse")

def open_thumbnail_location():
    thumbnail_browse_text.set("loading....")
    file = askopenfile(parent=root, mode='rb', title="Choose a ThumbnailFile", filetypes=[('JPEG file','*.jpg')])
    if file:
        thumbnail_location_text_box.insert(1.0, file.name)
    thumbnail_browse_text.set("Browse")

def open_settings_location():
    settings_browse_text.set("loading....")
    file = askopenfile(parent=root, mode='rb', title="Choose a JSON File", filetypes=[('JSON file','*.json')])
    if file:
        settings_location_text_box.insert(1.0, file.name)
    settings_browse_text.set("Browse")

if __name__ == "__main__":
    hash_key = b'I_hMnkZPq0MFXRKIGGMogcD6XR9EnE7SRFU29E-sIXA='
    root = tk.Tk()
    font_name = tk.font.nametofont("TkDefaultFont")  # Get default font value into Font object
    font_name.actual()

    text = tk.Label(root, text="Music Bot")
    text.config(font =("Courier", 30))
    text.grid(column=1, row=0)

    # video location
    video_location_label = tk.Label(root, text="Video Location:")
    video_location_label.grid(column=0, row=1)
    video_location_label.config(font=(font_name, 16))
    video_location_text_box = tk.Text(root, wrap='none', height=1, width=30, padx=2, pady=1)
    video_location_text_box.grid(column=1, row=1)

    # Browse for video location
    video_browse_text = tk.StringVar()
    video_browse_btn = tk.Button(root, textvariable=video_browse_text, command=lambda:open_video_location(), height=2, width=10)
    video_browse_text.set("Browse")
    video_browse_btn.grid(column=3, row=1)

    # Thumbnail location
    thumbnail_location_label = tk.Label(root, text="Thumbnail Location:")
    thumbnail_location_label.grid(column=0, row=2)
    thumbnail_location_label.config(font=(font_name, 16))
    thumbnail_location_text_box = tk.Text(root, wrap='none', height=1, width=30, padx=2, pady=1)
    thumbnail_location_text_box.grid(column=1, row=2)

    # Browse for Thumbnail location
    thumbnail_browse_text = tk.StringVar()
    thumbnail_browse_btn = tk.Button(root, textvariable=thumbnail_browse_text, command=lambda:open_thumbnail_location(), height=2, width=10)
    thumbnail_browse_text.set("Browse")
    thumbnail_browse_btn.grid(column=3, row=2)

    # settings location
    settings_location_label = tk.Label(root, text="Settings Location:")
    settings_location_label.grid(column=0, row=3)
    settings_location_label.config(font=(font_name, 16))
    settings_location_text_box = tk.Text(root, wrap='none', height=1, width=30, padx=2, pady=1)
    settings_location_text_box.grid(column=1, row=3)

    # Browse for settings
    settings_browse_text = tk.StringVar()
    settings_browse_btn = tk.Button(root, textvariable=settings_browse_text, command=lambda:open_settings_location(), height=2, width=10)
    settings_browse_text.set("Browse")
    settings_browse_btn.grid(column=3, row=3)

    # video caption
    video_caption_label = tk.Label(root, text="Video Caption:")
    video_caption_label.grid(column=0, row=4)
    video_caption_label.config(font=(font_name, 16))
    video_caption_text_box = tk.Text(root, height=5, width=30, padx=2, pady=1)
    video_caption_text_box.grid(column=1, row=4)

    # video tags ()
    video_tags_label = tk.Label(root, text="Video Tags:")
    video_tags_label.grid(column=0, row=5)
    video_tags_label.config(font=(font_name, 16))
    video_tags_text_box = tk.Text(root, height=2, width=30, padx=2, pady=1)
    video_tags_text_box.grid(column=1, row=5)

    # username
    username_label = tk.Label(root, text="Username:")
    username_label.grid(column=0, row=6)
    username_label.config(font=(font_name, 16))
    username_text_box = tk.Text(root, height=1, width=30, padx=2, pady=1)
    username_text_box.grid(column=1, row=6)

    # password
    password_txt = tk.StringVar()
    password_label = tk.Label(root, textvariable=password_txt)
    password_txt.set("Password:")
    password_label.grid(column=0, row=7)
    password_label.config(font=(font_name, 16))
    password_text_box = tk.Entry(root, show="*")
    password_text_box.grid(column=1, row=7)

    # Post Button
    post_text = tk.StringVar()
    post_btn = tk.Button(root, textvariable=post_text, command=lambda: on_post(), height=2, width=5)
    post_text.set("Post")
    post_btn.grid(column=1, row=8)

    # Save Client Button
    save_client_text = tk.StringVar()
    save_client_btn = tk.Button(root, textvariable=save_client_text, command=lambda: on_client_save(), height=2, width=5)
    save_client_text.set("Save Client")
    save_client_btn.grid(column=2, row=8)

    # Enter Email Code Button
    email_btn_txt = tk.StringVar()
    email_btn_txt.set("Enter")
    email_code_btn = tk.Button(root, textvariable=save_client_text, command=lambda: email_code_submit(), height=1, width=2)


    canvas = tk.Canvas(root, width=60, height=50)
    canvas.grid(columnspan=3, rowspan=3)

    root.mainloop()