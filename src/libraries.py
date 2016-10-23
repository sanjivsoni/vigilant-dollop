#for system commands
import os

#for Database
import MySQLdb

#Hashing Encryption
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64

#for twilio
from twilio.rest import TwilioRestClient

#for UTC time
import datetime
from datetime import datetime
from dateutil import tz

#to get current user
import getpass
from uuid import getnode as get_mac

#config file
import config

#for gps coordinates
import requests
import json

#for email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#for captcha
from captcha.image import ImageCaptcha
import string
import random

#for threading
from threading import Thread
from time import sleep
import Queue

# For Random generator and other tools
from random import randint
import re
from functools import partial

#for Kivy
from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window


from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
import datetime
