from flask import Flask, Response

app = Flask(__name__)


@app.route("/wav")
def streamwav():
    def generate():
        with open("SampleAudio1.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

if __name__ == "__main__":
    app.run(host="127.0.0.1")