import json
import random
import os
import re
from fastapi import HTTPException
from app.schemas.exam import ExamResult, QuestionResult

# 1. Tu arreglo oficial de señales
SEÑALES_VALIDAS = [
    'I-3B', 'R-27A', 'P-46D', 'P-18B', 'R-20', 'R-58A', 'P-51', 'I-5', 'P-6A', 'P-53', 
    'T-17', 'IC-02', 'T-06', 'R-54', 'P-10B', 'P-15', 'R-30', 'P-58', 'I-8', 'P-2B', 
    'P-34', 'R-31', 'R-62', 'T-01', 'P-29', 'P-49B', 'T-07', 'R-25', 'I-26', 'P-7', 
    'P-36', 'P-50', 'R-64B', 'I-14', 'I-11', 'P-1B', 'I-13', 'I-23', 'R-26', 'R-23', 
    'R-22', 'I-24', 'R-25D', 'P-21', 'R-40', 'P-17A', 'I-3A', 'P-38', 'T-13', 'T-11', 
    'R-11A', 'R-55A', 'PC-03', 'I-1C', 'R-42B', 'P-31A', 'R-8', 'P-17C', 'R-3', 'P-55', 
    'P-56', 'P-35', 'I-18', 'R-50', 'P-10A', 'R-25A', 'R-45A', 'R-28', 'I-22', 'T-20', 
    'R-12', 'I-28', 'P-60', 'I-27', 'R-42C', 'I-20', 'P-28', 'T-05', 'T-10', 'P-5-2B', 
    'R-14', 'P-3B', 'R-58B', 'PC-01', 'P-33A', 'P-48A', 'P-48B', 'R-36', 'P-16B', 'R-5-2', 
    'I-2A', 'I-4B', 'P-29A', 'P-5-1', 'P-16A', 'P-66', 'R-30F', 'P-25', 'P-6B', 'P-45', 
    'R-11', 'I-17', 'P-31', 'IC-05', 'P-39', 'P-5-1A', 'R-30C', 'R-5-3', 'R-17', 'P-6', 
    'T-16', 'P-44A', 'P-46C', 'I-1D', 'R-43', 'R-32', 'P-52', 'R-5', 'R-33', 'R-47', 
    'T-12', 'I-31', 'R-55B', 'T-09', 'T-03', 'R-10', 'P-4B', 'P-25A', 'R-44', 'P-8', 
    'P-5-2A', 'I-25', 'R-48', 'R-53', 'IC-01', 'R-45', 'P-62', 'R-42', 'P-41', 'R-18', 
    'I-33', 'R-14B', 'R-19', 'R-54A', 'R-49', 'R-27', 'R-16', 'IC-04', 'P-49', 'T-02', 
    'I-9', 'P-28A', 'R-64A', 'R-30A', 'I-34', 'P-66A', 'R-1', 'R-30G', 'I-35', 'P-25B', 
    'R-7', 'R-30B', 'P-46A', 'I-2B', 'I-21', 'P-21B', 'R-30E', 'P-43', 'P-49A', 'P-48', 
    'R-56', 'P-9A', 'R-34', 'I-19', 'P-3A', 'IC-03', 'I-1B', 'R-6', 'P-4A', 'I-7', 
    'P-34A', 'P-44B', 'P-44', 'P-18A', 'I-29', 'P-42', 'R-16A', 'I-6', 'P-22C', 'R-11B', 
    'P-21A', 'R-54B', 'I-4A', 'R-21', 'P-33B', 'R-24', 'P-9B', 'R-30D', 'R-2', 'I-1A', 
    'T-18', 'P-59', 'P-46', 'T-19', 'R-29', 'R-22A', 'I-16', 'I-10', 'I-15', 'R-35', 
    'R-25B', 'I-12', 'R-37', 'T-14', 'P-61', 'P-35C', 'I-32', 'P-17B', 'R-9', 'R-4', 
    'PC-02', 'P-2A', 'R-6A', 'R-8A', 'P-46B', 'R-14A', 'T-04', 'R-42A', 'T-15', 'P-1A', 
    'R-5-1', 'T-08', 'R-25C', 'P-46E', 'R-52', 'R-5-4'
]

SEÑALES_VALIDAS.sort(key=len, reverse=True)

class ExamService:
    def __init__(self):
        self._preguntas_cache = []
        self._cargar_datos_en_memoria()

    def _cargar_datos_en_memoria(self):
        try:
            json_path = "/home/hersimmar/Documents/theoric-examen-app/backend/app/seed/data.json"
            
            with open(json_path, "r", encoding="utf-8") as file:
                preguntas_leidas = json.load(file)
                
            for p in preguntas_leidas:
                p["image_url"] = None 
                texto = p["pregunta"]
                
                for senal in SEÑALES_VALIDAS:
                    if re.search(rf'\b{senal}\b', texto, re.IGNORECASE):
                        p["image_url"] = f"/assets/signals/{senal}.png"
                        break
            
            self._preguntas_cache = preguntas_leidas
            print(f"✅ Éxito: Se cargaron {len(self._preguntas_cache)} preguntas y se mapearon sus imágenes.")
        
        except Exception as e:
            print(f"❌ Error al cargar el JSON: {e}")
            self._preguntas_cache = []

    def _transformar_pregunta(self, pregunta_cruda):
        mapped_answers = []
        contador_id = 1
        
        for clave, texto in pregunta_cruda["alternativas"].items():
            es_correcta = (clave == pregunta_cruda["respuesta"])
            explicacion = "¡Excelente!" if es_correcta else f"La respuesta correcta era: {pregunta_cruda['respuesta'].upper()}"
            
            mapped_answers.append({
                "id": contador_id,
                "text": texto,
                "is_correct": es_correcta,
                "explanation": explicacion,
                "_letra_original": clave 
            })
            contador_id += 1

        return {
            "id": pregunta_cruda["id"],
            "text": pregunta_cruda["pregunta"],
            "explanation": f"Tema: {pregunta_cruda['tema']}",
            "image_url": pregunta_cruda.get("image_url"),
            "answers": mapped_answers
        }

    # ==========================================
    # MÉTODOS PARA EL ROUTER
    # ==========================================

    def get_all_questions(self):
        return [self._transformar_pregunta(q) for q in self._preguntas_cache]

    def get_random_questions(self, limit: int):
        if not self._preguntas_cache:
            raise HTTPException(status_code=500, detail="Datos no disponibles")
        seleccion = random.sample(self._preguntas_cache, min(limit, len(self._preguntas_cache)))

        ids_seleccionados = [q["id"] for q in seleccion]
        print(f"🐛 DEBUG [Simulacro]: Generando examen con los IDs: {ids_seleccionados}")

        return [self._transformar_pregunta(q) for q in seleccion]

    def obtener_pregunta_aleatoria(self):
        if not self._preguntas_cache:
            raise HTTPException(status_code=500, detail="Datos no disponibles")
        return self._transformar_pregunta(random.choice(self._preguntas_cache))

    def obtener_pregunta_visual(self):
        if not self._preguntas_cache:
            raise HTTPException(status_code=500, detail="Datos no disponibles")
        
        # Filtra súper rápido las preguntas que SÍ tienen una imagen asignada
        preguntas_visuales = [p for p in self._preguntas_cache if p.get("image_url") is not None]
                
        if not preguntas_visuales:
            raise HTTPException(status_code=404, detail="No se encontraron preguntas visuales.")
            
        return self._transformar_pregunta(random.choice(preguntas_visuales))

    def get_question_by_id(self, question_id: int):
        for q in self._preguntas_cache:
            if q["id"] == question_id:
                return self._transformar_pregunta(q)
        return None

    def evaluate_exam(self, submission):
        score = 0
        results = []

        diccionario_preguntas = {q["id"]: self._transformar_pregunta(q) for q in self._preguntas_cache}

        for item in submission.answers:
            pregunta_formateada = diccionario_preguntas.get(item.question_id)
            if not pregunta_formateada:
                continue

            correct_answer_id = None
            for ans in pregunta_formateada["answers"]:
                if ans["is_correct"]:
                    correct_answer_id = ans["id"]
                    break

            is_correct = (correct_answer_id == item.answer_id)
            if is_correct:
                score += 1

            results.append(
                QuestionResult(
                    question_id=item.question_id,
                    correct=is_correct,
                    correct_answer_id=None if is_correct else correct_answer_id
                )
            )

        return ExamResult(
            score=score,
            total=len(submission.answers),
            results=results
        )

# Instancia global
exam_service = ExamService()