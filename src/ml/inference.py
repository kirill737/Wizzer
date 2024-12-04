import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def postprocess_logits(logits  ):
    # Преобразуем числа в классы
    classes = np.where(logits < -0.33, -1, np.where(logits > 0.33, 1, 0))
    return classes


# Загрузка модели и токенизатора
model = AutoModelForSequenceClassification.from_pretrained("rubert_multilabel_model-best")
tokenizer = AutoTokenizer.from_pretrained("rubert_multilabel_model-best")


text = "преимущества: снимки ОГОНЬ!!!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
outputs = model(**inputs)
predictions = outputs.logits.detach().cpu().numpy()
predictions