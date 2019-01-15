from project.server import create_app, socketio
#from flask_socketio import SocketIO

app = create_app()

if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=5011, debug=True)
