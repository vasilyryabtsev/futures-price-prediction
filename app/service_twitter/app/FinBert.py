from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np


def preprocessing(X, y=None):
    '''
    Векторизует корпус с помощью finbert модели ProsusAI.
    '''
    X_copy = X.copy()

    name = 'ProsusAI/finbert'
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSequenceClassification.from_pretrained(name)

    # Токенезация
    def tokenize(x: str):
        '''
        Разбивает документ на токены.
        '''
        return tokenizer.encode(x, add_special_tokens=True)

    tokenized = X_copy['text'].apply(tokenize)

    # Паддинг (чтобы все тексты были одинаковой длины)
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])

    # Masking (нужно показать модели, что все нули это пустое место)
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded, dtype=torch.long)
    attention_mask = torch.tensor(attention_mask, dtype=torch.long)

    # Применение модели
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0].numpy()

    return features
