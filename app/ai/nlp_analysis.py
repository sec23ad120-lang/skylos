from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import List


class NLPClassifier:
    def __init__(self, model_name='distilbert-base-uncased'):
        # Transformer tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        # Placeholder for classifier and scaler
        self.scaler = StandardScaler()
        self.classifier = LogisticRegression()

        # Will store cached embeddings and labels for training
        self.train_embeddings = []
        self.train_labels = []

    def embed_text(self, text: str) -> np.ndarray:
        # Tokenize input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        # Use CLS token embedding (first token)
        cls_embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
        return cls_embedding.squeeze(0)

    def add_training_sample(self, text: str, label: int):
        # label: 1 for suspicious, 0 for clean
        emb = self.embed_text(text)
        self.train_embeddings.append(emb)
        self.train_labels.append(label)

    def train(self):
        X = np.vstack(self.train_embeddings)
        y = np.array(self.train_labels)
        X_scaled = self.scaler.fit_transform(X)
        self.classifier.fit(X_scaled, y)

    def predict(self, text: str) -> bool:
        emb = self.embed_text(text).reshape(1, -1)
        emb_scaled = self.scaler.transform(emb)
        pred = self.classifier.predict(emb_scaled)
        return bool(pred[0])
