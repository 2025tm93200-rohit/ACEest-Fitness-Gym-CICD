from flask import Flask, jsonify, request

app = Flask(__name__)
members = []

@app.get("/")
def home():
    return jsonify({"application":"ACEest Fitness & Gym","status":"running"})

@app.get("/health")
def health():
    return jsonify({"status":"healthy"})

@app.get("/members")
def get_members():
    return jsonify(members)

@app.post("/members")
def add_member():
    data=request.get_json(silent=True) or {}
    name, age = data.get("name"), data.get("age")
    if not name or age is None:
        return jsonify({"error":"name and age are required"}),400
    try:
        age=int(age)
    except (TypeError,ValueError):
        return jsonify({"error":"age must be an integer"}),400
    if age <= 0:
        return jsonify({"error":"age must be greater than 0"}),400
    member={"id":len(members)+1,"name":name,"age":age,
            "plan":data.get("plan","monthly")}
    members.append(member)
    return jsonify(member),201

@app.get("/members/<int:member_id>")
def get_member(member_id):
    member=next((m for m in members if m["id"]==member_id),None)
    if member is None:
        return jsonify({"error":"member not found"}),404
    return jsonify(member)

@app.delete("/members/<int:member_id>")
def delete_member(member_id):
    global members
    if not any(m["id"]==member_id for m in members):
        return jsonify({"error":"member not found"}),404
    members=[m for m in members if m["id"]!=member_id]
    return jsonify({"message":"member deleted"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
