import React, { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();
      setSummaryData(data);
    } catch (error) {
      console.error("Error:", error);
      setSummaryData({ error: "An error occurred while summarizing." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>📰 News Article Summarizer</h1>
      <input
        type="text"
        placeholder="Paste article link here..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={handleSummarize} disabled={loading}>
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {summaryData && summaryData.error && (
        <div className="summary-box error">
          <p>{summaryData.error}</p>
        </div>
      )}

      {summaryData && !summaryData.error && (
        <div className="summary-box">
          <h2>{summaryData.title}</h2>
          <p><strong>Author(s):</strong> {summaryData.authors}</p>
          <p><strong>Published:</strong> {summaryData.date}</p>

          <h3>Summary:</h3>
          <ul>
            {summaryData.summary.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>

          <p><strong>Sentiment:</strong> {summaryData.sentiment}</p>
        </div>
      )}
    </div>
  );
}

export default App;
