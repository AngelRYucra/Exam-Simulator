import { useEffect, useState } from "react";
import { fetchExam, submitExam } from "../api/examApi";
import type { Question, ExamResult } from "../types/exam";
import { Button, Container, Typography, Card, CardContent, RadioGroup, FormControlLabel, Radio, Box } from "@mui/material";

export default function ExamPage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: number }>({});
  const [result, setResult] = useState<ExamResult | null>(null);
  const [timeLeft, setTimeLeft] = useState(40 * 60); // 40 minutes in seconds


  useEffect(() => {
    fetchExam().then(setQuestions);
  }, []);

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  const formattedTime = `${minutes}:${seconds
  .toString()
  .padStart(2, "0")}`;


  useEffect(() => {
  if (timeLeft <= 0) {
    handleSubmit();
    return;
  }

  const timer = setInterval(() => {
    setTimeLeft((prev) => prev - 1);
  }, 1000);

  return () => clearInterval(timer);
}, [timeLeft]);


  const currentQuestion = questions[currentIndex];

  const handleSelect = (answerId: number) => {
    setAnswers({
      ...answers,
      [currentQuestion.id]: answerId,
    });
  };

  const handleSubmit = async () => {
  const submission = {
    answers: Object.entries(answers).map(([qId, aId]) => ({
      question_id: Number(qId),
      answer_id: aId,
    })),
  };

  const examResult = await submitExam(submission);
  setResult(examResult);
};


  const handleNext = async () => {
  const isLast = currentIndex === questions.length - 1;

  if (isLast) {
    await handleSubmit();
  } else {
    setCurrentIndex(currentIndex + 1);
  }
};

  if (!questions.length) {
    return <Typography>Loading...</Typography>;
  }

  if (result) {
    return (
      <Container>
        <Typography variant="h4">
          Score: {result.score} / {result.total}
        </Typography>
      </Container>
    );
  }

  return (
  <Container maxWidth="sm">
    {/* Top bar: question number + timer */}
    <Typography variant="h6" sx={{ mb: 1 }}>
      Question {currentIndex + 1} of {questions.length}
    </Typography>

    <Typography
      variant="h6"
      color="error"
      align="right"
      sx={{ mb: 2 }}
    >
      Time left: {formattedTime}
    </Typography>

    <Card>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>
          {currentQuestion.text}
        </Typography>
        {currentQuestion.image_url && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3, mt: 2 }}>
              <Box sx={{ textAlign: 'center' }}>
                <img 
                  src={currentQuestion.image_url} 
                  alt="Señal de tránsito" 
                  style={{ 
                    maxHeight: '180px', 
                    objectFit: 'contain',
                    borderRadius: '8px',
                    border: '1px solid #e0e0e0',
                    padding: '8px',
                    backgroundColor: '#ffffff',
                    display: 'block', // <-- Esto obliga al texto a irse a la línea de abajo
                    margin: '0 auto'  // <-- Centra la imagen
                  }} 
                />
                
                <Typography 
                  variant="subtitle2" 
                  color="textSecondary" 
                  sx={{ 
                    mt: 1, 
                    fontWeight: 'bold', 
                    fontSize: '0.9rem',
                    letterSpacing: '0.5px' // Le da un toque de "etiqueta" oficial
                  }}
                >
                  SEÑAL {currentQuestion.image_url.split('/').pop()?.split('.')[0].toUpperCase()}
                </Typography>
              </Box>
            </Box>
          )}
        <RadioGroup
          value={answers[currentQuestion.id] || ""}
          onChange={(e) => handleSelect(Number(e.target.value))}
        >
          {currentQuestion.answers.map((a) => (
            <FormControlLabel
              key={a.id}
              value={a.id}
              control={<Radio />}
              label={a.text}
            />
          ))}
        </RadioGroup>
      </CardContent>
    </Card>

    <Button
      variant="contained"
      sx={{ mt: 2 }}
      onClick={handleNext}
      disabled={!answers[currentQuestion.id]}
      fullWidth
    >
      {currentIndex === questions.length - 1
        ? "Finish Exam"
        : "Next Question"}
    </Button>
  </Container>
);
}
