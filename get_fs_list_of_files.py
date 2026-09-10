#!#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#######
print("::::intention:::: \n\nthis will update poem.csv with image thumb and generate file list for the kilthub hosted files for reference\n\n :)")
#######
from django.template import response
from importlib_metadata import metadata
import requests
import csv    
# make a new token.
headers = {
    'Content-Type': 'application/json',
}
# add yr id and secret.
json_data = {
    'client_id': "",
    'client_secret': "",
    'grant_type': 'client_credentials',
}
token_response = requests.post('https://api.figshare.com/v2/token', headers=headers, json=json_data).json()['token']
print(token_response)
# if you retreive the above and need to run this again you can just paste it in the line below and uncomment. comment out the one above
# save figshare servers some sweat
# token_response = "2f4235b352f92a6c3c31279853acb18a55f5120b7a2e2f306f7b0f84605de8efad93594a93df49d99a8c2163e68f47324995cd42b2fe8a83bd62c17624413718"

params = {
    'access_token': token_response, 
}

#open poem.csv and then loop through each row to get article_id and make the request
#also build another csv.
fieldnames = ""
tmp_file = []
with open('_data/poem.csv', 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        # print(row)
        article_id = row['article_id']
        if article_id == 'article_id' or article_id == '': #if it's the head. or for some reason it's not from fs and does not have article_id
            continue

        #get metadata 
        metadata = requests.get('https://api.figshare.com/v2/articles/'+str(article_id), params=params).json()
        # see what we want to work with
        # print(metadata)
        #update image thumb with the metadata
        row['image_thumb'] = metadata['thumb']
        #after modification add row to tmp.
        tmp_file.append(row)
        # create new csv named after objectid, and within that have the columns: download_url, name, size, mime_type
        with open('_data/fsfiles/'+str(row['objectid'])+'.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['download_url', 'name', 'size', 'mime_type', 'file_id','type'])
            writer.writeheader()
            for file in metadata['files']:
                writer.writerow({'download_url': file['download_url'], 'name': file['name'], 'size': file['size'], 'mime_type': file['mimetype'], 'file_id': file['id'], "type":""}) 

            # writer.writerow({'download_url': metadata['thumb'], 'name': metadata['thumb'], 'size': "", 'mime_type': "", 'file_id': "", "type":"thumbnail"})
            
with open('_data/poem.csv', 'w') as f: #could just overwrite poem.csv but this is slightly safer.
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in tmp_file:
        writer.writerow(row)