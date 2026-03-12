import {
  Card,
  CardContent,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
} from "@mui/material";
import type { Question } from "../types/exam";

interface Props {
  question: Question;
  selectedAnswer?: number;
  onSelect: (questionId: number, answerId: number) => void;
}

export default function QuestionCard({
  question,
  selectedAnswer,
  onSelect,
}: Props) {
  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {question.text}
        </Typography>

        <RadioGroup
          value={selectedAnswer ?? ""}
          onChange={(e) =>
            onSelect(question.id, Number(e.target.value))
          }
        >
          {question.answers.map((answer) => (
            <FormControlLabel
              key={answer.id}
              value={answer.id}
              control={<Radio />}
              label={answer.text}
            />
          ))}
        </RadioGroup>
      </CardContent>
    </Card>
  );
}
