from sklearn.preprocessing import FunctionTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

def preprocessing(X, y=None):
    '''
    Векторизует корпус с помощью finbert модели ProsusAI.
    '''
    X_copy = X.copy()

    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    # Токенезация
    tokenized = X_copy['text'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))

    # Паддинг (чтобы все тексты были одинаковой длины)
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])

    # Masking (нужно показать модели, что все нули это пустое место)
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)

    # Применение модели
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0].numpy()
    
    return features