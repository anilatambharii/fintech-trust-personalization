import React, { useState } from "react";

function App() {
  const [userId, setUserId] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    if (!userId.trim()) {
      setError("Please enter a user ID.");
      return;
    }
    setError("");
    setRecommendations([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/recommendations?user_id=${encodeURIComponent(
          userId
        )}`
      );
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Failed to fetch recommendations");
      }
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "Arial" }}>
      <h1>Fintech Personalization Demo</h1>

      <label htmlFor="userId">Enter User ID:</label>
      <input
        id="userId"
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        style={{ marginLeft: 10, padding: 5 }}
      />
      <button
        onClick={fetchRecommendations}
        style={{ marginLeft: 10, padding: "6px 12px" }}
      >
        Get Recommendations
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 20 }}>
          <b>Error:</b> {error}
        </p>
      )}

      {recommendations.length > 0 && (
        <div style={{ marginTop: 30 }}>
          <h2>Recommendations for User {userId}:</h2>
          <ul>
            {recommendations.map((rec, idx) => (
              <li key={idx}>
                <b>{rec.itemId}</b> (score: {rec.score.toFixed(2)})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
