import { useEffect, useState } from "react";
import { fetchLearningQuestion } from "../api/examApi";
import type { Question } from "../types/exam";
import {
  Button,
  Container,
  Typography,
  Card,
  CardContent,
  RadioGroup,
  FormControlLabel,
  Radio,
  Alert,
  Box,
  Divider
} from "@mui/material";

export default function LearningPage() {
  const [question, setQuestion] = useState<Question | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const loadQuestion = async () => {
    try {
      const q = await fetchLearningQuestion();
      setQuestion(q);
      setSelectedId(null);
      setIsSubmitted(false);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadQuestion();
  }, []);

  if (!question) {
    return <Typography>Cargando simulacro...</Typography>;
  }

  // Encontramos la respuesta que el usuario seleccionó y la correcta
  const selectedAnswer = question.answers.find(a => a.id === selectedId);
  const correctAnswer = question.answers.find(a => a.is_correct);

  const handleCheck = () => {
    setIsSubmitted(true);
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h5" mb={3} fontWeight="bold">
        Modo Aprendizaje
      </Typography>

      <Card elevation={3}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            {question.text}
          </Typography>

          {question.image_url && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3, mt: 2 }}>
              <Box sx={{ textAlign: 'center' }}>
                <img 
                  src={question.image_url} 
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
                  SEÑAL {question.image_url.split('/').pop()?.split('.')[0].toUpperCase()}
                </Typography>
              </Box>
            </Box>
          )}

          <RadioGroup
            value={selectedId || ""}
            onChange={(e) => setSelectedId(Number(e.target.value))}
          >
            {question.answers?.map((a) => {
              // Lógica de colores post-envío
              let bgColor = "transparent";
              if (isSubmitted) {
                if (a.is_correct) bgColor = "#e8f5e9"; // Verde clarito
                if (selectedId === a.id && !a.is_correct) bgColor = "#ffebee"; // Rojo clarito
              }

              return (
                <FormControlLabel
                  key={a.id}
                  value={a.id}
                  control={<Radio />}
                  label={a.text}
                  disabled={isSubmitted}
                  sx={{
                    mb: 1,
                    borderRadius: 1,
                    backgroundColor: bgColor,
                    transition: "0.3s",
                    width: "100%",
                    mr: 0
                  }}
                />
              );
            })}
          </RadioGroup>

          {/* SECCIÓN DE EXPLICACIÓN DINÁMICA */}
          {isSubmitted && selectedAnswer && (
            <Box mt={3}>
              <Divider sx={{ mb: 2 }} />
              
              <Alert 
                severity={selectedAnswer.is_correct ? "success" : "error"}
                variant="filled"
                sx={{ mb: 2 }}
              >
                {selectedAnswer.is_correct 
                  ? "¡Excelente! Has comprendido la norma." 
                  : "Respuesta Incorrecta. Analicemos por qué:"}
              </Alert>

              <Typography variant="body1" sx={{ fontWeight: 'medium', color: '#333' }}>
                <strong>Tu elección:</strong> {selectedAnswer.explanation}
              </Typography>

              {!selectedAnswer.is_correct && correctAnswer && (
                <Typography variant="body2" sx={{ mt: 1, color: 'green', fontStyle: 'italic' }}>
                  <strong>Lógica correcta:</strong> {correctAnswer.explanation}
                </Typography>
              )}
              
              {/* Explicación general de la pregunta (si existe en tu DB) */}
              {question.explanation && (
                <Typography variant="body2" sx={{ mt: 2, p: 1, bgcolor: '#f0f4f8', borderRadius: 1 }}>
                  💡 <strong>Dato adicional:</strong> {question.explanation}
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      <Box mt={3} display="flex" justifyContent="flex-end">
        {!isSubmitted ? (
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={handleCheck}
            disabled={selectedId === null}
          >
            Validar Respuesta
          </Button>
        ) : (
          <Button
            variant="contained"
            color="secondary"
            size="large"
            onClick={loadQuestion}
          >
            Siguiente Pregunta
          </Button>
        )}
      </Box>
    </Container>
  );
}