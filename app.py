import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# 🔑 Replace with your Gemini API key
genai.configure(api_key="AIzaSyDlKtgOk6jfjtdSRSWfjTDOTSM4hSVSD1s")

model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# 🤖 Planner Agent
def planner_agent(user_input):
    prompt = f"""
    You are a planner AI.
    Break the following goal into clear step-by-step tasks:

    Goal: {user_input}

    Return numbered steps.
    """
    response = model.generate_content(prompt)
    return response.text

# ⚙️ Executor Agent
def executor_agent(task):
    prompt = f"""
    Explain this step in detail and give actionable guidance:

    Task: {task}
    """
    response = model.generate_content(prompt)
    return response.text

# 🚀 Multi-Agent Flow
def run_agent(user_input):
    plan = planner_agent(user_input)
    steps = [s for s in plan.split("\n") if s.strip() != ""]

    results = []
    for step in steps:
        result = executor_agent(step)
        results.append(f"🔹 {step}\n{result}")

    return "\n\n".join(results)

# 🌐 Routes
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    query = data.get("query")

    output = run_agent(query)

    return jsonify({"result": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)