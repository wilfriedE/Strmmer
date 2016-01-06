# main.py
from gevent.wsgi import WSGIServer
from flask import Flask, render_template, stream_with_context, Response
from camera import VideoCamera

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def feedStream(camera):
	"""
	feedStream streams camera images (frames)
	"""
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
               b'Content-Type: video/mjpg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	"""
	you could add algorithm above this portion to prevent users
	who shouldn't view the video from viewing it. 
	This could also have algos for managing expired streams.
	"""
	return Response(feedStream(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	http_server = WSGIServer(('0.0.0.0', 5001), app)
	http_server.serve_forever()