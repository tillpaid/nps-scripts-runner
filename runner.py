import os
import json
import curses


class Runner:
    def __init__(self, store):
        os.system('clear')

        self.store = store
        self.npmType = store.getNpmType()

        self.pointer = 2
        self.config = None
        self.scripts = [
            {
                'name': "npm install",
                'command': "{} install".format(self.npmType)
            },
            {
                'name': "npm install with remove",
                'command': "rm -rf node_modules ; {} install".format(self.npmType)
            }
        ]

        self.maxScriptLength = None
        self.outBorder = None
        self.inBorder = None

        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)

    def run(self):
        self.getPackageJson()
        self.parseScripts()
        self.setBorders()

        keys = {
            'up': curses.KEY_UP,
            'down': curses.KEY_DOWN,
            'k': ord('k'),
            'j': ord('j'),
            'q': ord('q'),
            'esc': 27,
            'space': 32,
            'return': 10
        }

        while True:
            self.printScripts()

            char = self.screen.getch()

            if char == keys['q'] or char == keys['esc']:
                self.quitCurses()
                break
            elif char == keys['space'] or char == keys['return']:
                self.runCommand()
            elif char == keys['up'] or char == keys['k']:
                self.minusPointer()
            elif char == keys['down'] or char == keys['j']:
                self.plusPointer()

    def getPackageJson(self):
        currentDir = os.getcwd()
        packageJsonFile = currentDir + '/package.json'

        packageJsonExists = os.path.exists(packageJsonFile)

        if packageJsonExists:
            try:
                file = open(packageJsonFile, 'r')
                config = json.loads(file.read())
                file.close()
                self.config = config
            except json.decoder.JSONDecodeError:
                print('Package.json file is not a json')
                quit()
        else:
            print('Package.json file not exists in current directory')
            quit()

    def parseScripts(self):
        try:
            scriptsLength = len(self.config['scripts'])

            if scriptsLength > 0:
                for key in self.config['scripts']:
                    self.scripts.append({
                        'name': key,
                        'command': self.config['scripts'][key]
                    })
            else:
                print('Section scripts is empty')
                quit()
        except KeyError:
            print('Package.json file does not contain scripts')
            quit()

    def setBorders(self):
        self.maxScriptLength = 0

        for i in range(len(self.scripts)):
            currentScriptLength = len(self.scripts[i]['name'])

            if currentScriptLength > self.maxScriptLength:
                self.maxScriptLength = currentScriptLength

        self.maxScriptLength += 9

        self.inBorder = "+{}+".format('-' * self.maxScriptLength)
        self.outBorder = "+{}+".format('=' * self.maxScriptLength)

    def plusPointer(self):
        self.pointer += 1

        if self.pointer >= len(self.scripts):
            self.pointer = 2

    def minusPointer(self):
        self.pointer -= 1

        if self.pointer < 0:
            self.pointer = len(self.scripts) - 1

    def runCommand(self):
        if self.pointer > 1:
            command = "{} run {}".format(self.npmType, self.scripts[self.pointer]['name'])
        else:
            command = self.scripts[self.pointer]['command']

        self.quitCurses()

        print("Run command: {}".format(command))
        print('---------------')
        os.system(command)
        quit()

    def printScripts(self):
        self.screen.addnstr('', 0)
        self.screen.addstr(0, 0, self.outBorder)

        counter = 1

        for i in range(len(self.scripts)):
            rowActive = self.pointer == i

            name = self.scripts[i]['name']
            arrow = '| ---> | ' if rowActive else '|      | '
            afterName = "{} |".format(" " * (self.maxScriptLength - len(name) - 9))

            if i == 2:
                self.screen.addstr(counter, 0, self.inBorder)
                counter += 1

            self.screen.addstr(counter, 0, arrow)
            self.screen.addstr(name, curses.color_pair(1 if rowActive else 0))
            self.screen.addstr(afterName)

            counter += 1

        self.screen.addstr(counter, 0, self.outBorder)

    def quitCurses(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
