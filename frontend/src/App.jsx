import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [sessionId, setSessionId] = useState(null);

  const [results, setResults] = useState([]);
  const [summary, setSummary] = useState("");
  const [sources, setSources] = useState([]);
  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeReport = async () => {
    if (!file) {
      setError("Please upload a PDF report.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();

    formData.append("file", file);
    formData.append("question", question.trim());

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          Array.isArray(data.error)
            ? data.error.join(", ")
            : data.error || "Unable to analyze the report."
        );
      }

      setSessionId(data.session_id);

      setResults(data.results || []);

      setSummary(data.summary || "");

      setSources(data.sources || []);

      setMessages([
        {
          role: "user",
          content: question.trim(),
        },
        {
          role: "assistant",
          content: data.answer || "",
        },
      ]);

      setQuestion("");
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!question.trim()) {
      return;
    }

    if (!sessionId) {
      return;
    }

    const currentQuestion = question.trim();

    setQuestion("");
    setError("");

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setLoading(true);

    const formData = new FormData();

    formData.append("session_id", sessionId);
    formData.append("question", currentQuestion);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          Array.isArray(data.error)
            ? data.error.join(", ")
            : data.error || "Unable to process the question."
        );
      }

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer || "",
        },
      ]);

      setSources(data.sources || []);
    } catch (err) {
      setError(err.message || "Something went wrong.");

      setMessages((previousMessages) => {
        const updatedMessages = [...previousMessages];

        if (
          updatedMessages.length > 0 &&
          updatedMessages[updatedMessages.length - 1].role === "user"
        ) {
          updatedMessages.pop();
        }

        return updatedMessages;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (loading) {
        return;
      }

      if (sessionId) {
        sendMessage();
      } else {
        analyzeReport();
      }
    }
  };

  const resetChat = () => {
    setFile(null);
    setQuestion("");
    setSessionId(null);

    setResults([]);
    setSummary("");
    setSources([]);
    setMessages([]);

    setLoading(false);
    setError("");
  };

  const getStatusLabel = (status) => {
    if (status === "within_range") {
      return "Within range";
    }

    if (status === "low") {
      return "Low";
    }

    if (status === "high") {
      return "High";
    }

    return "Unknown";
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>MedReport AI</h1>

          <p>
            Understand your laboratory report with AI-powered explanations.
          </p>
        </div>
      </header>

      <main className="container">
        {!sessionId ? (
          <section className="upload-card">
            <div className="card-heading">
              <h2>Analyze your report</h2>

              <p>
                Upload a digital PDF laboratory report and ask a question
                about your results.
              </p>
            </div>

            <label className="file-box">
              <span className="file-icon">📄</span>

              <span>
                {file
                  ? file.name
                  : "Choose a PDF laboratory report"}
              </span>

              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(event) => {
                  const selectedFile =
                    event.target.files?.[0] || null;

                  setFile(selectedFile);
                  setError("");
                }}
              />
            </label>

            <label className="input-label">
              Your question

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Example: What does my fasting blood glucose result mean?"
                rows={4}
              />
            </label>

            {error && (
              <div className="error">
                {error}
              </div>
            )}

            <button
              className="primary-button"
              onClick={analyzeReport}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Report"}
            </button>
          </section>
        ) : (
          <>
            <section className="report-header">
              <div>
                <span className="eyebrow">
                  REPORT ANALYSIS
                </span>

                <h2>
                  {file?.name || "Medical Laboratory Report"}
                </h2>
              </div>

              <button
                className="secondary-button"
                onClick={resetChat}
              >
                New Report
              </button>
            </section>

            <section className="summary-card">
              <h3>Report Summary</h3>

              <p>{summary}</p>
            </section>

            <section className="results-card">
              <h3>Laboratory Results</h3>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Test</th>
                      <th>Result</th>
                      <th>Reference Range</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {results.map((result, index) => (
                      <tr
                        key={`${result.test_name}-${index}`}
                      >
                        <td>
                          {result.test_name}
                        </td>

                        <td>
                          {result.value}{" "}
                          {result.unit || ""}
                        </td>

                        <td>
                          {result.reference_low !== null &&
                          result.reference_high !== null
                            ? `${result.reference_low} - ${result.reference_high}`
                            : "Not available"}
                        </td>

                        <td>
                          <span
                            className={`status ${
                              result.status
                            }`}
                          >
                            {getStatusLabel(
                              result.status
                            )}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            <section className="chat-card">
              <div className="card-heading">
                <h3>
                  Ask about your report
                </h3>

                <p>
                  Ask follow-up questions about
                  the laboratory results.
                </p>
              </div>

              <div className="messages">
                {messages.map(
                  (message, index) => (
                    <div
                      key={index}
                      className={`message ${
                        message.role === "user"
                          ? "user-message"
                          : "assistant-message"
                      }`}
                    >
                      <div className="message-role">
                        {message.role === "user"
                          ? "You"
                          : "MedReport AI"}
                      </div>

                      <div className="message-content">
                        {message.role ===
                        "assistant" ? (
                          <ReactMarkdown>
                            {message.content}
                          </ReactMarkdown>
                        ) : (
                          <p>
                            {message.content}
                          </p>
                        )}
                      </div>
                    </div>
                  )
                )}

                {loading && (
                  <div className="message assistant-message">
                    <div className="message-role">
                      MedReport AI
                    </div>

                    <div className="message-content">
                      <p>
                        Thinking...
                      </p>
                    </div>
                  </div>
                )}
              </div>

              <div className="chat-input">
                <textarea
                  value={question}
                  onChange={(event) =>
                    setQuestion(
                      event.target.value
                    )
                  }
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a follow-up question..."
                  rows={3}
                  disabled={loading}
                />

                <button
                  className="primary-button"
                  onClick={sendMessage}
                  disabled={
                    loading ||
                    !question.trim()
                  }
                >
                  Send
                </button>
              </div>

              {error && (
                <div className="error">
                  {error}
                </div>
              )}
            </section>

            {sources.length > 0 && (
              <section className="sources-card">
                <h3>Knowledge Sources</h3>

                <p className="sources-description">
                  Medical knowledge used to
                  support the explanation.
                </p>

                {sources.map(
                  (source, index) => (
                    <div
                      className="source"
                      key={index}
                    >
                      <div className="source-header">
                        <div className="source-title">
                          {source.metadata?.topic ||
                            "Medical Knowledge"}
                        </div>

                        <span className="relevance">
                          Relevance:{" "}
                          {typeof source.score ===
                          "number"
                            ? source.score.toFixed(
                                3
                              )
                            : "N/A"}
                        </span>
                      </div>
                    </div>
                  )
                )}
              </section>
            )}

            <div className="disclaimer">
              <strong>
                Educational information only.
              </strong>

              <span>
                MedReport AI does not provide
                diagnoses, prescriptions,
                medication instructions, or
                other clinical decisions.
                Consult a qualified healthcare
                professional for medical advice.
              </span>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;