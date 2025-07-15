from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app, resources={r"/summarize": {"origins": "http://localhost:3000"}})

@app.route("/summarize", methods=["POST"])
def summarize_article():
    try:
        data = request.get_json()
        url = data.get("url")

        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

        prompt = f"""
        You are a helpful AI assistant for NEWS summarizer. Given the news article, extract the following details:

        Title: (Title of the article)
        Author(s): (List of author names or 'Not mentioned')
        Publication Date: (Mention if available, otherwise 'Not mentioned')
        Summary: (Concise 6-9 line summary with bullet points)
        Sentiment: (Positive, Negative, or Neutral)

        Article link:
        {url}
        """

        response = model.generate_content(
            contents=prompt,
            generation_config={
                "temperature": 0.2,
                "candidate_count": 1,
                "top_p": 0.9,
                "max_output_tokens": 1024,
            }
        )

        markdown = response.text
        lines = markdown.splitlines()

        result = {
            "title": "",
            "authors": "",
            "date": "",
            "summary": [],
            "sentiment": ""
        }

        section = None

        for line in lines:
            line = line.strip()

            if line.startswith("**Title:**"):
                result["title"] = line.replace("**Title:**", "").strip()
            elif line.startswith("**Author(s):**"):
                result["authors"] = line.replace("**Author(s):**", "").strip()
            elif line.startswith("**Publication Date:**"):
                result["date"] = line.replace("**Publication Date:**", "").strip()
            elif line.startswith("**Summary:**"):
                section = "summary"
            elif line.startswith("**Sentiment:**"):
                result["sentiment"] = line.replace("**Sentiment:**", "").strip()
                section = None
            elif section == "summary" and line.startswith("*"):
                result["summary"].append(line.replace("*", "").strip())

        # print("✅ Summary generated successfully:", result)
        return jsonify(result)
        

    except Exception as e:
        print("🔥 Backend Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
