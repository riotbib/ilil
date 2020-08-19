#!/usr/bin/env python3
from bottle import Bottle, run, get, post, request, route, template, response, redirect, view, os, static_file, error 
import time 
from datetime import datetime
from PIL import Image
import toml
import argparse
from bottle import TEMPLATE_PATH
import os
import numpy
import sys

abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
TEMPLATE_PATH.insert(0, abs_views_path )

app = Bottle()

parseArguments = argparse.ArgumentParser(description='ilil')
parseArguments.add_argument('-c', '--config', required=True)
parseArguments.add_argument('-p', '--path', required=True)
arguments = parseArguments.parse_args()

parsedConfig = toml.load(arguments.config)
loadDataToml = arguments.path+"/data.toml"
parsedData = toml.load(loadDataToml)


@app.route('/page/<page>')
def pagination(page):
    loggedIn = request.get_cookie("login", secret='some-secret-key')
    if page.isdigit():

        page = int(page) - 1 
        itemsPerPage = parsedConfig['server']['itemsPerPage'] 
        getDirectory = os.listdir(arguments.path+"/thumbs")
        getDirectory = getDirectory[::-1]
        totalNumberOfImages = len(getDirectory)
        totalNumberOfPages = - ( - int(totalNumberOfImages) // int(itemsPerPage))

        if totalNumberOfImages == 0: 
            return template('error')
        elif page >= totalNumberOfPages:
            redirect("/page/1")
        elif page < 0:
            redirect("/page/1")
        else:
            def divide_chunks(l, n): 
                for i in range(0, len(l), n):  
                    yield l[i:i + n] 
            listOfImages = list(divide_chunks(getDirectory, int(itemsPerPage)))
    
            return template('page', title=parsedConfig['title'], name=parsedConfig['owner']['name'], mail=parsedConfig['owner']['mail'], description=parsedConfig['owner']['description'], page=int(page), totalNumberOfImages=totalNumberOfImages, totalNumberOfPages=totalNumberOfPages, imagesPerPage=listOfImages[page], parsedData=parsedData, loggedIn=loggedIn)

    else:
        return template('error')

@app.route('/')
def start():
   return(pagination("1"))

@app.route('/login') 
def login():
    login = request.get_cookie("login", secret='some-secret-key')
    if login:
        redirect("/")
    else:
        return template('login', loginfailed='')

@app.route('/login', method='POST') 
def do_login():
    password = request.forms.get('password')
    if password == parsedConfig['server']['password'] :
        timestamp = time.time()
        response.set_cookie("login", timestamp, secret='some-secret-key')
        redirect("/add")
    else:
        return template('login', loginfailed='true')

@app.route('/logout')
def logout():
    login = request.get_cookie("login", secret='some-secret-key')
    if login:
        response.delete_cookie("login")
        redirect("/")
    else:
        redirect("/")

@app.route('/add')
def add():
    login = request.get_cookie("login", secret='some-secret-key')
    if login:
        return template('add', title=parsedConfig['title'], name=parsedConfig['owner']['name'], mail=parsedConfig['owner']['mail'], description=parsedConfig['owner']['description'])
    else:
        redirect("/") 

@app.route('/add', method='POST')
def do_add():
    login = request.get_cookie("login", secret='some-secret-key')
    if login:
        description   = request.forms.get('description')
        upload     = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png','.jpg','.jpeg'):
            redirect("/add")

        datetimestamp = datetime.now()
        timestamp = datetimestamp.strftime("%Y%m%d%H%M%S")
        
        save_path = arguments.path+"/originals/{timestamp}{ext}".format(timestamp=timestamp,ext=ext)
        upload.save(save_path) # appends upload.filename automatically

        thumbSize = (300, 300)
        thumb = Image.open(save_path)
        thumb.thumbnail(thumbSize)
        thumbSavePath = arguments.path+"/thumbs/{timestamp}{ext}".format(timestamp=timestamp,ext=ext)
        thumb.save(thumbSavePath)

        picSize = (900, 900)
        pic = Image.open(save_path)
        pic.thumbnail(picSize)
        picSavePath = arguments.path+"/pictures/{timestamp}{ext}".format(timestamp=timestamp,ext=ext)
        pic.save(picSavePath)

        with open(loadDataToml, "a") as dataFile:
            writeToData = '{timestamp} = "{description}"\n'.format(timestamp=timestamp,description=description)
            dataFile.write(writeToData)

        redirect("/")

    else:
        redirect("/")    

@app.route('/id/<timeStamp>')
def id(timeStamp):
    loggedIn = request.get_cookie("login", secret='some-secret-key') # please change, lol
    return template('id', title=parsedConfig['title'], name=parsedConfig['owner']['name'], mail=parsedConfig['owner']['mail'], description=parsedConfig['owner']['description'], timeStamp=timeStamp, arguments=arguments, parsedData=parsedData, loggedIn=loggedIn)

@app.route('/thumbs/<filename>')
def thumb(filename):
    return static_file(filename, root=arguments.path+"/thumbs/")

@app.route('/pictures/<filename>')
def pictures(filename):
    return static_file(filename, root=arguments.path+"/pictures/")

@app.route('/originals/<filename>')
def originals(filename):
    return static_file(filename, root=arguments.path+"/originals/")

@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root=arguments.path+"/static/")

@app.error(404)
def error404(error):
    return template('error')

run(app, host=parsedConfig['server']['host'], port=parsedConfig['server']['port'])
