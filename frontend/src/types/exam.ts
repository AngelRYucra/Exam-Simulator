export interface Answer {
  id: number;
  text: string;
  explanation?: string;
  is_correct?: boolean; // Solo para preguntas de aprendizaje, indica cuál es la respuesta correcta
}

export interface Question {
  id: number;
  text: string;
  explanation?: string;
  image_url?: string | null;
  answers: Answer[];
}

export interface SubmittedAnswer {
  question_id: number;
  answer_id: number;
}

export interface ExamSubmission {
  answers: SubmittedAnswer[];
}

export interface ExamResult {
  score: number;
  total: number;
  results: {
    question_id: number;
    correct: boolean;
    correct_answer_id: number | null;
  }[];
}

