# main.py
from flask import Flask, render_template, stream_with_context, Response
from camera import VideoCamera
import base64

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def feedStream(video,chunksize=10):
	"""
	feedStream streams chunks of the video
	"""
	with open(video, "rb") as video_file:
		while True:
			chunk = video_file.read(chunksize)
			if chunk:
				yield chunk
			else:
				break

@app.route('/video_feed')
def video_feed():
	"""
	you could add algorithm above this portion to prevent users
	who shouldn't view the video from viewing it. 
	This could also have algos for managing expired streams.
	"""
	video = "videos/Snapchat-3166549212292376752.mp4"
	return Response(stream_with_context(feedStream(video)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)