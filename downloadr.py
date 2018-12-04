import requests
import json
import os
import urllib

blog_name = input("Enter your blog name: ")
tag = urllib.parse.quote(input("Enter a tag to filter by (Leave blank for none): "))
api_key = input("Enter your Tumblr oAuth Consumer Key: ")

input("Will write files to " + os.getcwd() + " Press ENTER to continue or CTRL-C to exit...")
offset = 0

post_type = "photo"
base_uri = "https://api.tumblr.com/v2/blog/" 
if tag != "":

    uri = base_uri + blog_name + ".tumblr.com/posts/" + post_type + "?api_key=" + api_key + "&tag=" + tag + "&offset=" 
else:
    uri = base_uri + blog_name + ".tumblr.com/posts/" + post_type + "?api_key=" + api_key + "&offset="

post_json = requests.get(uri + str(offset)).json()

total_posts = post_json['response']['total_posts']

print("Downloading " + str(total_posts) + " posts.")
post_list = {}
image_num = 0
while offset <= total_posts:
    for post in post_json['response']['posts']:
        id = int(post['id'])
        urls = []
        for x in post['photos']:
            urls.append(x['original_size']['url'])
        post_list[id] = urls

    for id in post_list:
        full_file_name = str(image_num) + '.jpg'  
        img_data = requests.get(post_list[id][0]).content
        with open(full_file_name, 'wb') as handler:
            handler.write(img_data)
        image_num += 1  
    offset += 20
    if offset > total_posts:
        print("Completed!")
    else:
        print("Progress " + str(offset) + " of " + str(total_posts) + ".....................................")
    post_json = requests.get(uri + str(offset)).json()

    total_posts = post_json['response']['total_posts']

print("Images located at:  " + os.getcwd())
