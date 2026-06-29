from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

def get_next_id():
    if not events:
        return 1
    return max(event.id for event in events) + 1

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    title = data.get("title")
    if not title:
        return jsonify({"error": "The 'title' field is required."}), 400

    new_event = Event(get_next_id(), title)
    events.append(new_event)
    return jsonify({
        "message": "Event created successfully.",
        "event": new_event.to_dict()
    }), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found."}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    title = data.get("title")
    if not title:
        return jsonify({"error": "The 'title' field is required."}), 400
    event.title = title
    return jsonify({
        "message": "Event updated successfully.",
        "event": event.to_dict()
    }), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found."}), 404
    events.remove(event)
    return jsonify({
        "message": "Event deleted successfully."
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
