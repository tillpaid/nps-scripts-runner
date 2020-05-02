import os
import json
from pathlib import Path


class Store:
    def __init__(self):
        home = str(Path.home())
        configPath = '.nps'
        settingName = 'settings.json'

        self.settingsDir = "{}/{}".format(home, configPath)
        self.settingsFile = "{}/{}/{}".format(home, configPath, settingName)

        self.defaultConfig = {"type": "npm"}
        self.config = None

    def getNpmType(self):
        if not self.config:
            self.getConfig()

        return self.config['type']

    def changeNpmType(self, type):
        self.config['type'] = type
        self.setConfig(self.config)

    def getConfig(self):
        if not self.checkFile():
            self.setConfig(self.defaultConfig)
            self.config = self.defaultConfig
        else:
            file = open(self.settingsFile, 'r')
            self.config = json.loads(file.read())
            file.close()

    def setConfig(self, config):
        self.checkDir()

        file = open(self.settingsFile, 'w')
        file.write(json.dumps(config))
        file.close()

    def checkDir(self):
        if not os.path.exists(self.settingsDir):
            os.mkdir(self.settingsDir)

    def checkFile(self):
        return os.path.isfile(self.settingsFile)
