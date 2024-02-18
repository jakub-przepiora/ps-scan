#!/usr/bin/python3

import requests
import os
import sys
import re
from datetime import datetime
import xml.etree.ElementTree as ET

class PsScan:
    global target
    adminPanelList = ['/admin', '/iadmin', '/adminpanel', '/admin123']
    installList = ['/install', '/install123', '/install321', '/.install']
    informationFromScan = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")




    def __init__(self, args) -> None:
        print('''

░▒▓███████▓▒░ ░▒▓███████▓▒░             ░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░              ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓███████▓▒░             ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                             
Autor: TheMrEviil                                                                                

''')
        if sys.argv[2]:
            self.target = sys.argv[2]
            self.createFolderForScanInfo()
            if not self.isPresta():
                print("This target don't use Prestashop")
                return None
            
            self.getPrestaInfoFile()
            self.checkInstallDir()
            self.checkAdminDir()
            self.getThemeName()
            self.getModules()
            pass

    def isPresta(self):
        resp = requests.get(self.target)
        
        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            open(self.informationFromScan+'/home.txt', 'w', encoding='utf-8').write(resp.text)
            return True
        resp = requests.get(target+'/INSTALL.txt')
        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            open(self.informationFromScan+'/home.txt', 'w', encoding='utf-8').write(resp.text)
            return True
        return False

    def checkAdminDir(self):
        
        for path in self.adminPanelList:
            resp = requests.get(self.target+path)
            if resp.status_code == 200:
                print(f'[-] Found Admin panel path: {self.target}{path}')

    def checkInstallDir(self):
        
        for path in self.installList:
            resp = requests.get(self.target+path)
            if resp.status_code == 200:
                print(f'[-] Found Installation path: {self.target}{path}')

    def getThemeName(self):
        try:
            with open(self.informationFromScan+'/home.txt', 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()
                match = re.search(r'/themes/([^/]+)/', content)
                if match:
                    themeName = match.group(1)
                    print(f"[+] Found theme: {themeName}")
                    return themeName
                else:
                    print("[-] Theme not found")
                    return None

        except FileNotFoundError:
            print(f"The file 'home.txt' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        

    def getPrestaVersion(self):
        pass

    def getPrestaVersionFromFile(self, file):

        try:
            with open(file, 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()

                match = re.search(r'PrestaShop\s+(\d+(\.\d+)*)', content)

                if match:
                    version_number = match.group(1)
                    print(f"[+] The PrestaShop version found in the file INSTALL is: {version_number}")
                    return version_number
                else:
                    print("[-] PrestaShop version not found in the file.")
                    return None

        except FileNotFoundError:
            print(f"The file '{file}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getPrestaInfoFile(self):
        resp = requests.get(self.target+"/INSTALL.txt")
        if resp.status_code == 200:
            open(self.informationFromScan+'/install.txt', 'w', encoding='utf-8').write(resp.text)
            self.getPrestaVersionFromFile(self.informationFromScan+'/install.txt')

    def getModules(self):
        print("\n============================ Modules =======================================\n")
        try:
            with open(self.informationFromScan+'/home.txt', 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()

                # Use a regular expression to find module names in different patterns
                matches = re.finditer(r'/module/([^/]+)/|/modules/([^/]+)/|/module/([^/]+)/|/modules/([^/]+)/|modules ([^/]+)|module ([^/]+)', content)

                # List to store unique module names
                unique_module_names = []

                for match in matches:
                    moduleName = match.group(1) or match.group(2) or match.group(3) or match.group(4) or match.group(5) or match.group(6)

                    # Check if the module name is not in the list
                    if moduleName and moduleName not in unique_module_names:
                        unique_module_names.append(moduleName)
                        print(f"[+] Module: {moduleName}")

                # Check for the presence of the specific comment and extract "Block Search"
                # comment_match = re.search(r'<!-- Block search module (\w+) -->', content)
                # if comment_match:
                #     comment_text = comment_match.group(1)
                #     print(f"[+] Detected <!-- {comment_text} -->")

        except FileNotFoundError:
            print(f"The file '{self.informationFromScan}/home.txt' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.getModulesVersion(unique_module_names)

    def getModulesVersion(self, moduleList):
        print("\n============================ Try get modules XML =======================================\n")
        for module in moduleList:
            resp = requests.get(self.target+"/modules/"+module+'/config.xml')
            if resp.status_code == 200:
                open(self.informationFromScan+'/'+module+'.xml', 'w', encoding='utf-8').write(resp.text)

                print(f'[+] Found and save '+module+'.xml')
                try:
                    # Parse the XML file
                    tree = ET.parse(self.informationFromScan+'/'+module+'.xml')
                    root = tree.getroot()

                    # Find the version element and extract its text
                    version_element = root.find('.//version')
                    
                    if version_element is not None:
                        version = version_element.text
                        print(f"[!] The module version is: {version}")
                except ET.ParseError as e:
                    print(f"Error parsing XML: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
        pass
        

    def createFolderForScanInfo(self):
        
        fullPath = os.path.join(os.getcwd(), self.informationFromScan)

        if not os.path.exists(fullPath):
            os.mkdir(fullPath)

if __name__ == "__main__":
    if not sys.argv[1]:
        print("You can check flags using: ps-scan.py help")
        pass
    
    if sys.argv[1] == 'help':
        
        helpFlags = ''' 
    -h      Host to scan (https://example.com)
        '''
        print(helpFlags)
    
    if '-h' in sys.argv:
        ans =input("\nDo you have permission to scan this website? [y/n] ")
        if ans == 'y':
            PsScan(sys.argv)
        else:
            pass