import os

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


helpers = {
    "plus": "Преимущества", 
    "minus": "Недостатки",
}

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def postprocess_logits(logits):
    # Преобразуем числа в классы
    classes = np.where(logits <= -0.33, -1, np.where(logits >= 0.33, 1, 0))
    return classes


def process_texts(model: AutoModelForSequenceClassification, tokenizer: AutoTokenizer, texts: list, batch_size: int = 128):
    all_logits = []
    for i in range(0, len(texts), batch_size):
        # Токенизация всех текстов
        inputs = tokenizer(texts[i:i+batch_size], return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)

        # Прогон текстов через модель
        with torch.no_grad():
            outputs = model(**inputs)
        
        all_logits.append(outputs.logits.detach().cpu().numpy())

    # Постобработка logits
    if len(all_logits):
        return postprocess_logits(np.vstack(all_logits))
    else:
        return np.array([[0., 0., 0.]])


def process_reviews(model, tokenizer, reviews):
    indexes, all_texts = [0], []
    for review in reviews: 
        texts = [
            helpers.get(review_part, "") + " : " + review[review_part]
            for review_part in ["plus", "minus", "comment"] if len(review[review_part]) > 4
        ]
        indexes.append(indexes[-1] + len(texts))
        all_texts.extend(texts)

    all_marks = process_texts(model, tokenizer, all_texts)
    
    review_marks = []
    for i, j in zip(indexes[:-1], indexes[1:]):
        review_summary = all_marks[i : j].sum(axis=0)
        review_marks.append(np.where(review_summary >= 1, 1, np.where(review_summary <= -1, -1, 0)))

    return np.array(review_marks)


def load_model():
    # Загрузка модели и токенизатора
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model = AutoModelForSequenceClassification.from_pretrained(os.path.join(script_dir, "rubert_multilabel_model-best"))
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(script_dir, "rubert_multilabel_model-best"))

    return model, tokenizer