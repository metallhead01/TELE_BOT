from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from lxml import etree
from telebot import types
import telebot
import logging
import requests
import xml.etree.ElementTree as ET
import urllib3
import base64
import re

FORMAT = '%(asctime)s : LOG : %(levelname)s - %(message)s'
logger_my_functions = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


class VersionNumber:
    def __init__(self, filename):
        self.filename = filename
    def get_version_number (self):
        try:
            info = GetFileVersionInfo (self.filename, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
        except:
            return 0,0,0,0

class RequestIdRole:
    def __init__(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word

    def role_id_request(self):
        # Основное тело запроса
        id_list = []
        filename = VersionNumber("C:\\YURA\\r_keeper_7_Delivery\\YURA_DELIVERY_2\\Delivery\\SDispather.exe") # TODO заменить абсолютные пути относительными
        version = ".".join([str(i) for i in filename.get_version_number()])
        logger_my_functions.debug("SDispatcher version " + ".".join([str(i) for i in filename.get_version_number()]))

        if version < "3.1.3.154":
            xml_request_string_ask_GUID = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "LINKEDSYSTEMSTYPES" WithChildItems="2" WithMacroProp="1"  OnlyActive = "1" PropMask="items.(ident,name,GUIDString,RIChildItems.(Ident,Name,GUIDString,AltName))"/></RK7Query>/></RK7Query>'
            ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
            urllib3.disable_warnings()
            response_GUID = requests.get(ip_string, data=xml_request_string_ask_GUID, auth=(self.user_name, self.pass_word), verify=False)
            parsed_element_list_GUID = ET.fromstring(response_GUID.content)
            for item in parsed_element_list_GUID.findall("./RK7Reference/Items/Item/RIChildItems/TLinkedSystemsConf"):
                attr_of_item_node = item.attrib
                plugin_GUID = attr_of_item_node.get('GUIDString')
                plugin_ID = attr_of_item_node.get('Ident')
                plugin_name = attr_of_item_node.get('Name')
            if plugin_GUID and plugin_ID and plugin_name is not None:
                logger_my_functions.debug("GUID, ID and Name values were taken.")
            else:
                logger_my_functions.debug("GUID, ID and Name receiving error.")
            xml_request_string_ask_BLOB = '<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="LINKEDSYSTEMSCONFS" WithBlobsData="1" RefItemGUID="' + plugin_GUID + '"EncodeBase64="1"/></RK7Query>'
            response_BLOB = requests.get(ip_string, data=xml_request_string_ask_BLOB, auth=(self.user_name, self.pass_word), verify=False)
            parsed_element_list_BLOB = ET.fromstring(response_BLOB.content)
            for item in parsed_element_list_BLOB.findall("./RK7Reference/Items/Item/BlobData/CONFIGRAWXML"):
                BLOB = base64.standard_b64decode(item.text)
                parsed_BLOB = ET.fromstring(BLOB)
                for item in parsed_BLOB.findall("./DLVEmployee/ExpeditorRoles/itemSIFR"):
                    expeditor_role_id = item.text
                for item in parsed_BLOB.findall("./DLVEmployee/inExpTakeOut"):
                    in_exp_take_out = item.text
            if expeditor_role_id and in_exp_take_out is not None:
                logger_my_functions.debug("expeditor_role_id and in_exp_take_out values were taken.")
            else:
                logger_my_functions.debug("expeditor_role_id and in_exp_take_out values receiving error.")
        else:
            id_list = []
            with open ("C:\\YURA\\r_keeper_7_Delivery\\YURA_DELIVERY_2\\Delivery\\MSConfig.Ini", 'r', encoding="cp1251") as ini_file:# TODO заменить абсолютные пути относительными
                for line in ini_file:
                    expeditor_role_id = re.findall('inPersonalRole=(.*)', line)
                    if expeditor_role_id: #пустой список по-умолчанию всегда дает false при логической проверке
                        id_list.append(expeditor_role_id)
                    in_exp_take_out = re.findall('stExpRoles=(.*)', line)
                    if in_exp_take_out:
                        id_list.append(in_exp_take_out)
            if id_list:
                logger_my_functions.debug("expeditor_role_id = " + id_list[0][0] + " and in_exp_take_out = " + id_list[1][0] + " values were taken.")
        return id_list[0:2]

class RequestIdExp:
    def __init__(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word

    def id_exp_request(self):
        role_id = RequestIdRole("172.22.3.86", "4545", "Admin_QSR", "190186")
        role_id.role_id_request()
        xml_request_string_ask_IDs_exp = '<RK7Query><RK7CMD CMD="GetRefData" RefName="Restaurants" IgnoreEnums="1" WithChildItems="3" WithMacroProp="1" OnlyActive = "1" PropMask="RIChildItems.(Ident,Name,genRestIP,genprnStation,genDefDlvCurrency,AltName,RIChildItems.TRole(ItemIdent,passdata,Name,AltName,gen*,RIChildItems.(Ident,Name,AltName,gen*)))"/></RK7Query>'
        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        urllib3.disable_warnings()
        response_GUID_IDs_exp = requests.get(ip_string, data=xml_request_string_ask_IDs_exp, auth=(self.user_name, self.pass_word),
                                     verify=False)
        parsed_element_IDs_exp = ET.fromstring(response_GUID_IDs_exp.content)
        #for item in parsed_element_IDs_exp.findall("./RK7Reference/RIChildItems/TRK7Restaurant/RIChildItems/TRole"):
