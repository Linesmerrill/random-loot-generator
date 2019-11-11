#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file
import os
import os.path
from os import path
import random
import io
import zipfile
import json
import sys
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',**locals())

@app.route("/return-files/")
def return_files():
    try:
        return send_file("random_loot.zip", as_attachment=True, attachment_filename="random_loot.zip")
    except Exception as e:
        return str(e)

@app.route("/generator")
def generator():
    file_list = []
    remaining = []
    datapack_name = 'random_loot'
    datapack_desc = 'Loot Table Randomizer'
    datapack_filename = datapack_name + '.zip'

    for dirpath, dirnames, filenames in os.walk('loot_tables'):
	    for filename in filenames:
		    file_list.append(os.path.join(dirpath, filename))
		    remaining.append(os.path.join(dirpath, filename))
		
    file_dict = {}

    for file in file_list:
	    i = random.randint(0, len(remaining)-1)
	    file_dict[file] = remaining[i]
	    del remaining[i]
	
    zipbytes = io.BytesIO()
    zip = zipfile.ZipFile(zipbytes, 'w', zipfile.ZIP_DEFLATED, False)

    for from_file in file_dict:
	    with open(from_file) as file:
		    contents = file.read()
		
	    zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

	
    zip.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':datapack_desc}}, indent=4))
    zip.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))
    zip.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Loot table randomizer by SethBling","color":"green"}]')
	
    zip.close()
    with open(datapack_filename, 'wb') as file:
	    file.write(zipbytes.getvalue())
	
    print('Created datapack "{}"'.format(datapack_filename))
    datapack = "Generated Successfully!"
    return render_template('generator.html',**locals())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)