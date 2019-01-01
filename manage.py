from flask import Flask, render_template, request, redirect, url_for
import os
import random
from memory import Memory

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        print(request.form)
        if 'players' and 'level' in request.form.keys():
            players = request.form['players'].split()
            height, width = [int(i) for i in request.form['level'].split()]
            global mem
            mem = Memory(height, width, players)
            global images
            path = "./static/images/sky"
            files = os.listdir(path)
            images = random.sample(files, mem.getMaxIndex())
            return redirect(url_for('memory'))


def indexToImage(field, images):
    for index, image in enumerate(images):
        # print(index+1, image)
        for i, line in enumerate(field):
            for j, label in enumerate(line):
                if label == index+1:
                    field[i][j] = {"label": index+1,
                                   "url": "images/sky/"+image}
                elif label == 0:
                    field[i][j] = {"label": 0, "url": "images/back.png"}
                elif label == -1:
                    field[i][j] = {"label": -1, "url": "images/white.png"}
    return field


@app.route('/memory', methods=["GET", "POST"])
def memory():
    results, messages = "", "ここにメッセージが表示されます"
    if request.method == "GET":
        field = mem.getDisplay()
        field = indexToImage(field, images)
        width = mem.getWidth()
        return render_template('memory.html', field=field, enumerate=enumerate, results=results, message=messages, width=width)

    if request.method == "POST":
        # print(request.form)
        for key, value in request.form.items():
            # print(key, value)
            a, b = int(value[1]), int(value[4])
            field = mem.getDisplay(a, b)
            # print(mem)
            if mem.endFlag:
                results = mem.getResults()
            else:
                results = ""
            if mem.message:
                messages = mem.getMessages()
        field = indexToImage(field, images)
        width = mem.getWidth()
        return render_template('memory.html', field=field, enumerate=enumerate, results=results, message=messages, width=width)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
