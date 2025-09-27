import Layout from "./layout";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CedarCopilot } from "cedar-os";

import Home from "./routes/Home";
import Video from "./routes/Video";

function App() {
  return (
    <CedarCopilot
      llmProvider={{
        provider: "custom",
        baseURL: "http://localhost:3000/api/llm", // your backend
      }}
    >
      <Layout>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/v/:id" element={<Video />} />
          </Routes>
        </BrowserRouter>
      </Layout>
    </CedarCopilot>
  );
}

export default App;
