import type { ExamSubmission, ExamResult, Question } from "../types/exam";

//const API_URL = "http://localhost:8000";
// Antes: const API_URL = "http://localhost:8000/exam";
const API_URL = "http://192.168.18.39:8000"; // <-- Usa tu IP real
export async function fetchExam(): Promise<Question[]> {
  const response = await fetch(`${API_URL}/exam/`);
  return response.json();
}

export async function fetchLearningQuestion() {
  const res = await fetch("http://localhost:8000/exam/learn");

  if (!res.ok) {
    throw new Error("Failed to fetch learning question");
  }

  return res.json();
}

export async function fetchVisualQuestion(): Promise<Question> {
  // You can change the URL "/exam/visual-learn" to whatever endpoint 
  // you decide to create in your backend for this feature.
  const res = await fetch(`${API_URL}/exam/visual-learn`);

  if (!res.ok) {
    throw new Error("Failed to fetch visual question");
  }

  return res.json();
}

export async function submitExam(
  data: ExamSubmission
): Promise<ExamResult> {
  const response = await fetch(`${API_URL}/exam/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return response.json();
}
