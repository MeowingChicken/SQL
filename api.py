from flask import Flask, jsonify

app = Flask(__name__)

# Current robot movement states
movement_state = {
    "forward": False,
    "backward": False,
    "left": False,
    "right": False
}


@app.route("/move/<direction>", methods=["POST"])
def change_direction(direction):
    """
    Toggle a movement direction state.

    Parameters:
        direction (str): The direction to toggle (forward/backward/left/right)

    Returns:
        JSON: Updated state for the requested direction
    """
    if direction in movement_state:
        movement_state[direction] = not movement_state[direction]
        return jsonify({direction: movement_state[direction]})
    return jsonify({"error": "Invalid direction"}), 400


@app.route("/state", methods=["GET"])
def get_state():
    """
    Get the current state of all movement directions.

    Returns:
        JSON: Dictionary of current movement states
    """
    return jsonify(movement_state)

