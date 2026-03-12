import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ExamPage from "./pages/ExamPage";
import LearningPage from "./pages/LearningPage";
import VisualLearningPage from "./pages/VisualLearningPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/exam" element={<ExamPage />} />
      <Route path="/learn" element={<LearningPage />} />
      <Route path="/visual-learning" element={<VisualLearningPage />} />

    </Routes>
  );
}

export default App;
