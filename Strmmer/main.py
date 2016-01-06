# main.py
from gevent.wsgi import WSGIServer
from flask import Flask, render_template, stream_with_context, Response

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def feedStream(video,chunksize=1000):
	"""
	feedStream streams chunks of the video
	"""
	with open(video, "rb") as video_file:
		chunky = True
		while chunky:
			chunk = video_file.read(chunksize)
			if chunk:
				yield chunk
			else:
				chunky = False

@app.route('/video_feed')
def video_feed():
	"""
	you could add algorithm above this portion to prevent users
	who shouldn't view the video from viewing it. 
	This could also have algos for managing expired streams.
	"""
	video = "videos/snap-122203822.mp4"
	return Response(stream_with_context(feedStream(video)))

if __name__ == '__main__':
	http_server = WSGIServer(('0.0.0.0', 5001), app)
	http_server.serve_forever()