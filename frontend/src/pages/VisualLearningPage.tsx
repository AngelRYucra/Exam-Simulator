import { useEffect, useState } from "react";
// Necesitarás crear esta función en tu examApi.ts (te explico abajo)
import { fetchVisualQuestion } from "../api/examApi"; 
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

// Extendemos tu tipo Question para asegurar que incluye la imagen
interface VisualQuestion extends Question {
  image_url: string; 
}

export default function VisualLearningPage() {
  const [question, setQuestion] = useState<VisualQuestion | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const loadQuestion = async () => {
    try {
      const q = await fetchVisualQuestion();
      setQuestion(q);
      setSelectedId(null);
      setIsSubmitted(false);
    } catch (error) {
      console.error("Error cargando la pregunta visual:", error);
    }
  };

  useEffect(() => {
    loadQuestion();
  }, []);

  if (!question) {
    return <Typography textAlign="center" mt={5}>Cargando señal...</Typography>;
  }

  const selectedAnswer = question.answers.find(a => a.id === selectedId);
  const correctAnswer = question.answers.find(a => a.is_correct);

  const handleCheck = () => {
    setIsSubmitted(true);
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h5" mb={1} fontWeight="bold" textAlign="center" color="primary">
        Entrenamiento Visual
      </Typography>
      <Typography variant="subtitle1" mb={3} textAlign="center" color="text.secondary">
        Identifica la señal sin leer su nombre
      </Typography>

      <Card elevation={4} sx={{ borderRadius: 3, overflow: 'hidden' }}>
        
        {/* CONTENEDOR DE LA IMAGEN (GRANDE Y DESTACADO) */}
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            bgcolor: '#e0e0e0', // Fondo gris claro para hacer resaltar la señal
            py: 4,
            minHeight: '220px'
          }}
        >
          {question.image_url ? (
            <Box
              component="img"
              src={question.image_url}
              alt="Señal de tránsito a identificar"
              sx={{
                maxHeight: 180,
                maxWidth: '90%',
                objectFit: 'contain',
                filter: 'drop-shadow(0px 8px 12px rgba(0,0,0,0.2))' // Efecto de sombra realista
              }}
            />
          ) : (
            <Typography color="error">Imagen no encontrada</Typography>
          )}
        </Box>

        <CardContent>
          {/* REEMPLAZAMOS EL TEXTO ORIGINAL POR UNA PREGUNTA GENÉRICA */}
          <Typography variant="h6" gutterBottom fontWeight="bold" textAlign="center" mb={3}>
            ¿Qué indica esta señal de tránsito?
          </Typography>

          <RadioGroup
            value={selectedId || ""}
            onChange={(e) => setSelectedId(Number(e.target.value))}
          >
            {question.answers?.map((a) => {
              let bgColor = "transparent";
              if (isSubmitted) {
                if (a.is_correct) bgColor = "#e8f5e9"; // Verde si es correcta
                if (selectedId === a.id && !a.is_correct) bgColor = "#ffebee"; // Rojo si te equivocaste
              }

              return (
                <FormControlLabel
                  key={a.id}
                  value={a.id}
                  control={<Radio />}
                  label={
                    <Typography variant="body1" sx={{ py: 0.5 }}>
                      {a.text}
                    </Typography>
                  }
                  disabled={isSubmitted}
                  sx={{
                    mb: 1.5,
                    borderRadius: 2,
                    backgroundColor: bgColor,
                    transition: "all 0.3s ease",
                    width: "100%",
                    mr: 0,
                    px: 1,
                    border: '1px solid',
                    borderColor: isSubmitted && (a.is_correct || selectedId === a.id) ? 'transparent' : '#f0f0f0',
                    '&:hover': {
                      backgroundColor: !isSubmitted ? '#f5f5f5' : bgColor
                    }
                  }}
                />
              );
            })}
          </RadioGroup>

          {/* RETROALIMENTACIÓN */}
          {isSubmitted && selectedAnswer && (
            <Box mt={3} animation="fadeIn 0.5s">
              <Divider sx={{ mb: 2 }} />
              
              <Alert 
                severity={selectedAnswer.is_correct ? "success" : "error"}
                variant="filled"
                sx={{ mb: 2, borderRadius: 2 }}
              >
                {selectedAnswer.is_correct 
                  ? "¡Correcto! Tienes buen ojo." 
                  : "Cuidado, esa no es la respuesta."}
              </Alert>

              {!selectedAnswer.is_correct && correctAnswer && (
                <Typography variant="body2" sx={{ mt: 1, color: '#2e7d32', fontWeight: 'bold' }}>
                  Significado real: {correctAnswer.explanation || correctAnswer.text}
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      <Box mt={4} display="flex" justifyContent="center">
        {!isSubmitted ? (
          <Button
            variant="contained"
            color="primary"
            size="large"
            fullWidth
            onClick={handleCheck}
            disabled={selectedId === null}
            sx={{ py: 1.5, fontSize: '1.1rem', borderRadius: 2 }}
          >
            Comprobar
          </Button>
        ) : (
          <Button
            variant="contained"
            color="secondary"
            size="large"
            fullWidth
            onClick={loadQuestion}
            sx={{ py: 1.5, fontSize: '1.1rem', borderRadius: 2 }}
          >
            Siguiente Señal ➡️
          </Button>
        )}
      </Box>
    </Container>
  );
}