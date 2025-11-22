"""
Transformer-based NLP event classifier
Uses a pretrained model for text classification
"""
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import numpy as np
import os

class EventClassifier(nn.Module):
    def __init__(self, num_classes=4, model_name='distilbert-base-uncased'):
        super(EventClassifier, self).__init__()

        # Use a lightweight pretrained transformer
        self.encoder = AutoModel.from_pretrained(model_name)
        hidden_size = self.encoder.config.hidden_size

        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, input_ids, attention_mask):
        # Get encoder output
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)

        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]

        # Classify
        logits = self.classifier(pooled_output)
        return logits


class EventCategorizer:
    def __init__(self, model_path=None, model_name='distilbert-base-uncased'):
        """
        Initialize event categorizer
        Args:
            model_path: Path to saved model (optional)
            model_name: Pretrained transformer model name
        """
        self.categories = ['Academic', 'Social', 'Sports', 'Cultural']
        self.num_classes = len(self.categories)

        # Tag suggestions for each category
        self.category_tags = {
            'Academic': ['Workshop', 'Lecture', 'Research', 'Career', 'Study', 'Learning'],
            'Social': ['Entertainment', 'Games', 'Movie', 'Party', 'Networking', 'Fun'],
            'Sports': ['Fitness', 'Game', 'Competition', 'Training', 'Recreation', 'Wellness'],
            'Cultural': ['Festival', 'Performance', 'Art', 'Music', 'International', 'Heritage']
        }

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = EventClassifier(num_classes=self.num_classes, model_name=model_name)
            self.is_trained = False

            if model_path and os.path.exists(model_path):
                self.load_model(model_path)
        except Exception as e:
            print(f"Warning: Could not load transformer model: {e}")
            print("Using rule-based classifier instead")
            self.tokenizer = None
            self.model = None
            self.is_trained = False

    def train(self, training_data, epochs=10, lr=2e-5, batch_size=8):
        """
        Train the classifier
        Args:
            training_data: List of (title, description, category) tuples
            epochs: Number of training epochs
            lr: Learning rate
            batch_size: Batch size
        """
        if self.tokenizer is None or self.model is None:
            print("Transformer model not available, skipping training")
            return

        # Prepare data
        texts = [f"{title} {desc}" for title, desc, _ in training_data]
        labels = [self.categories.index(cat) for _, _, cat in training_data]

        # Tokenize
        encodings = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors='pt'
        )

        labels_tensor = torch.LongTensor(labels)

        # Training setup
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr)

        # Training loop
        self.model.train()
        num_batches = (len(texts) + batch_size - 1) // batch_size

        for epoch in range(epochs):
            total_loss = 0
            correct = 0
            total = 0

            for i in range(num_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, len(texts))

                batch_input_ids = encodings['input_ids'][start_idx:end_idx]
                batch_attention_mask = encodings['attention_mask'][start_idx:end_idx]
                batch_labels = labels_tensor[start_idx:end_idx]

                optimizer.zero_grad()
                outputs = self.model(batch_input_ids, batch_attention_mask)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

                # Calculate accuracy
                _, predicted = torch.max(outputs, 1)
                total += batch_labels.size(0)
                correct += (predicted == batch_labels).sum().item()

            avg_loss = total_loss / num_batches
            accuracy = 100 * correct / total

            if (epoch + 1) % 2 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%')

        self.is_trained = True
        print("Training completed!")

    def predict(self, title, description):
        """
        Predict event category
        Args:
            title: Event title
            description: Event description
        Returns:
            Dictionary with category, confidence, and suggested tags
        """
        if self.tokenizer is None or self.model is None or not self.is_trained:
            # Use rule-based classification
            return self._rule_based_classify(title, description)

        self.model.eval()

        # Combine title and description
        text = f"{title} {description}"

        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors='pt'
        )

        # Predict
        with torch.no_grad():
            outputs = self.model(encoding['input_ids'], encoding['attention_mask'])
            probabilities = torch.softmax(outputs, dim=1)
            predicted_idx = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_idx].item()

        predicted_category = self.categories[predicted_idx]

        # Get suggested tags
        suggested_tags = self._extract_tags(title, description, predicted_category)

        return {
            'category': predicted_category,
            'confidence': confidence,
            'all_probabilities': {
                self.categories[i]: probabilities[0][i].item()
                for i in range(self.num_classes)
            },
            'suggested_tags': suggested_tags
        }

    def _rule_based_classify(self, title, description):
        """Simple rule-based classification as fallback"""
        text = f"{title} {description}".lower()

        # Keywords for each category
        keywords = {
            'Academic': ['workshop', 'lecture', 'research', 'study', 'career', 'seminar',
                        'thesis', 'symposium', 'academic', 'learning', 'education'],
            'Social': ['party', 'social', 'night', 'fun', 'entertainment', 'movie',
                      'game', 'casino', 'paint', 'coffee', 'meet', 'friends'],
            'Sports': ['game', 'football', 'basketball', 'run', 'fitness', 'gym',
                      'yoga', 'sports', 'athletic', 'tournament', 'competition'],
            'Cultural': ['festival', 'cultural', 'dance', 'music', 'heritage',
                        'international', 'celebration', 'traditional', 'art']
        }

        scores = {}
        for category, kw_list in keywords.items():
            score = sum(1 for kw in kw_list if kw in text)
            scores[category] = score

        # Get category with highest score
        predicted_category = max(scores, key=scores.get)

        # If no keywords matched, default to Social
        if scores[predicted_category] == 0:
            predicted_category = 'Social'

        suggested_tags = self._extract_tags(title, description, predicted_category)

        return {
            'category': predicted_category,
            'confidence': 0.75,  # Default confidence for rule-based
            'all_probabilities': {cat: scores[cat] / max(sum(scores.values()), 1)
                                 for cat in self.categories},
            'suggested_tags': suggested_tags
        }

    def _extract_tags(self, title, description, category):
        """Extract relevant tags based on category and text"""
        base_tags = self.category_tags.get(category, [])

        # Find tags mentioned in title or description
        text = f"{title} {description}".lower()
        relevant_tags = []

        for tag in base_tags:
            if tag.lower() in text:
                relevant_tags.append(tag)

        # If we didn't find many, add some default category tags
        if len(relevant_tags) < 2:
            relevant_tags = base_tags[:3]

        return relevant_tags[:5]  # Return up to 5 tags

    def save_model(self, path):
        """Save model"""
        if self.model is not None:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'categories': self.categories
            }, path)
            print(f"Model saved to {path}")

    def load_model(self, path):
        """Load model"""
        if self.model is not None:
            checkpoint = torch.load(path, map_location=torch.device('cpu'))
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.categories = checkpoint.get('categories', self.categories)
            self.is_trained = True
            print(f"Model loaded from {path}")
