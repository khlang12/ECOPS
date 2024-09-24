from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "key"

MAZE = [
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#"],
    ["#", "P", "#", " ", "E", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#"],
]

START_POS = (3, 1)
END_POS = (3, 4)


@app.route("/")
def index():
    if "position" not in session:
        session["position"] = list(START_POS)
    position = session["position"]
    maze_with_player = update_maze_with_player(position)
    return render_template("index.html", maze=maze_with_player)


@app.route("/move", methods=["POST"])
def move():
    direction = request.form["direction"]
    position = session.get("position", list(START_POS))

    new_position = list(position)

    if direction == "up":
        new_position[0] -= 1
    elif direction == "down":
        new_position[0] += 1
    elif direction == "left":
        new_position[1] -= 1
    elif direction == "right":
        new_position[1] += 1

    if MAZE[new_position[0]][new_position[1]] != "#":
        session["position"] = new_position

    if tuple(new_position) == END_POS:
        return redirect(url_for("win"))

    return redirect(url_for("index"))


@app.route("/win")
def win():
    session.pop
    return "탈출에 성공했습니다! <a href='/'>다시하기</a>"


def update_maze_with_player(position):
    maze_copy = [row[:] for row in MAZE]
    maze_copy[position[0]][position[1]] = "P"
    return maze_copy


if __name__ == "__main__":
    app.run()
