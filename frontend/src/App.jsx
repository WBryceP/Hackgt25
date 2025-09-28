"use client";
import Layout from "./layout";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CedarCopilot } from "cedar-os";
import { useState } from "react";

import Home from "./routes/Home";
import Video from "./routes/Video";
import Error from "./routes/Error";

function App() {
  const [error, setError] = useState("");
  return (
    <CedarCopilot
      llmProvider={{
        provider: "custom",
        baseURL: "http://localhost:3000/api/llm", // your backend
      }}
    >
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/v/:id" element={<Video setError={setError} />} />
            <Route path="/error" element={<Error />} error={error} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </CedarCopilot>
  );
}

export default App;
