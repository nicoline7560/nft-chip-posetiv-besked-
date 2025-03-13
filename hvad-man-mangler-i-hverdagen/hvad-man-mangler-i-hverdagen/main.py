from flask import Flask, render_template
import os
import requests
import time

app = Flask(__name__)

# Hent Together AI API-nøgle fra miljøvariabler
API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

@app.route('/')
def get_message():
    try:
        # Forbedret prompt for kun at få en enkelt kort besked
        unique_prompt = (
            "Generate a short, positive, and uplifting message to make someone smile. "
            "Only return the message itself with no additional context or conversation."
        )

        # Kalder Together AI API
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "prompt": unique_prompt,
                "max_tokens": 50,  # Sikrer kort besked
                "temperature": 1.0,
                "top_p": 0.9,
                "stop": ["User", "\n"]  # Stopper ved ny samtalelinje
            }
        )

        data = response.json()

        # Sikrer at vi får en ren besked
        if "choices" in data and data["choices"]:
            message = data["choices"][0].get("text", "").strip()
        else:
            message = "Du er fantastisk! Husk at smile i dag 😊"

        return render_template("index.html", message=message)

    except Exception as e:
        return render_template("index.html", message="Fejl: Kunne ikke hente besked. Husk, du er fantastisk! 😊")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
