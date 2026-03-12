import json
from app.database import SessionLocal
from app.models.question import Question
from app.models.answer import Answer

db = SessionLocal()

with open("app/seed/questions.json", "r", encoding="utf-8") as file:
    questions_data = json.load(file)

for q in questions_data:
    question = Question(
        text=q["text"],
        #explanation=q["explanation"]
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    for a in q["answers"]:
        answer = Answer(
            text=a["text"],
            is_correct=a["is_correct"],
            explanation=a.get("explanation"),
            question_id=question.id
        )
        db.add(answer)

    db.commit()

db.close()

print("Questions inserted successfully!")
