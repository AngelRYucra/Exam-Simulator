import { Box, Typography, Button } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import type { ExamResult } from "../types/exam";

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state as ExamResult;

  if (!result) {
    return <Typography>No result available.</Typography>;
  }

  return (
    <Box p={4} textAlign="center">
      <Typography variant="h4" gutterBottom>
        Exam Result
      </Typography>

      <Typography variant="h5">
        Score: {result.score} / {result.total}
      </Typography>

      <Button
        variant="contained"
        sx={{ mt: 3 }}
        onClick={() => navigate("/")}
      >
        Try Again
      </Button>
    </Box>
  );
}
