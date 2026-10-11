from flask import Flask, jsonify, request

app = Flask(__name__)
members = []

@app.get("/")
def home():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ACEest Fitness & Gym</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: white;
                padding: 40px 60px;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                text-align: center;
            }
            h1 {
                color: #1f3a5f;
                margin-bottom: 12px;
            }
            p {
                color: #555;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>ACEest Fitness & Gym</h1>
            <p>Application is running successfully.</p>
        </div>
    </body>
    </html>
    """

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