from flask import Flask, send_from_directory
from flask import render_template
from flask.ext.socketio import SocketIO, emit
import threading
import time

ui = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
url = "http://localhost:8080"
    
def background_thread():
    while True:
        socketio.sleep(1)
        text = "FIXME: background thread"

        socketio.emit('log',
                      text,
                      namespace='/console')

@socketio.on('connect', namespace='/console')
def connect():
    global thread
    global ui
    while ui is None:
        time.sleep(0.25)

    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
        ui.ready = True

@socketio.on('ping', namespace='/console')
def ping_pong():
    emit('pong')
    
@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('js', filename)

@app.route('/')
def index():
    return render_template('index.html', console = "Initializing...")

class WebUi(object):
    def __init__(self):
        global ui
        import logging
        logging.basicConfig(filename='error.log',level=logging.DEBUG)
        ui = self
        self.ready = False
        t = threading.Thread(target=socketio.run, args=(app, '0.0.0.0', '8080'))
        t.start()

    def clear(self, demo):
        """Clears the console ready for a new section of the script."""
        if demo.is_simulation:
            # demo.current_command = "clear"
            # self.simulate_command(demo)
            raise Exception("Not implemented yet")
        else:        
            self.type_command(demo, "clear")
            raise Exception("Not implemented yet")

    def heading(self, text):
        """Display a heading"""
        # self.display(text, colorama.Fore.CYAN + colorama.Style.BRIGHT, True)
        # print()
        raise Exception("Not implemented yet")

    def description(self, text):
        """Display some descriptive text. Usually this is text from the demo
        document itself.

        """
        # self.display(text, colorama.Fore.CYAN)
        raise Exception("Not implemented yet")

    def next_step(self, index, title):
        """Displays a next step item with an index (the number to be entered
to select it) and a title (to be displayed).
        """
        # self.display(index, colorama.Fore.CYAN)
        # self.display(title, colorama.Fore.CYAN, True)
        raise Exception("Not implemented yet")

    def instruction(self, text):
        """Display an instruction for the user.
        """
        # self.display(text, colorama.Fore.MAGENTA, True)    
        raise Exception("Not implemented yet")
    
    def warning(self, text):
        """Display a warning to the user.
        """
        # self.display(text, colorama.Fore.RED + colorama.Style.BRIGHT, True)
        raise Exception("Not implemented yet")

    def new_para(self):
        """Starts a new paragraph."""
        # self.new_line()
        # self.new_line()
        raise Exception("Not implemented yet")
    
    def new_line(self):
        """Move to the next line"""
        # print()
        raise Exception("Not implemented yet")
    
    def horizontal_rule(self):
        # print("\n\n============================================\n\n")
        raise Exception("Not implemented yet")

    def display(self, text, color, new_line=False):
        """Display some text in a given color. Do not print a new line unless
        new_line is set to True.

        """
        # print(color, end="")
        #print(text, end="", flush=True)
        if new_line:
            # print(colorama.Style.RESET_ALL)
            raise Exception("Not implemented yet")
        else:
            # print(colorama.Style.RESET_ALL, end="")
            raise Exception("Not implemented yet")
            
    def request_input(self, text):
        """ Displays text that is intended to propmt the user for input. """
        socketio.emit('update',
                      text,
                      namespace='/console')

    def get_command(self):
        self.request_input("What mode do you want to run in? (default 'tutorial')")
        mode = ""
        # mode = input()
        if mode == "":
            mode = "tutorial"
        return mode
    



