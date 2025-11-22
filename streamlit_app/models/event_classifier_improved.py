"""
Improved Transformer-based NLP event classifier with better fine-tuning
Uses DistilBERT with advanced training techniques
"""
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
import numpy as np
import os
from sklearn.model_selection import train_test_split

class EventDataset(Dataset):
    """Custom dataset for event classification"""
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


class ImprovedEventClassifier(nn.Module):
    """Improved classifier with better architecture"""
    def __init__(self, num_classes=4, model_name='distilbert-base-uncased', dropout=0.3):
        super(ImprovedEventClassifier, self).__init__()

        # Load pretrained transformer
        self.encoder = AutoModel.from_pretrained(model_name)
        hidden_size = self.encoder.config.hidden_size

        # Multi-layer classification head with batch normalization
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout * 0.7),  # Lower dropout in middle layer
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5),
            nn.Linear(128, num_classes)
        )

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        """Initialize classifier weights"""
        for module in self.classifier:
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)

    def forward(self, input_ids, attention_mask):
        # Get encoder output
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)

        # Use [CLS] token representation
        pooled_output = outputs.last_hidden_state[:, 0, :]

        # Classify
        logits = self.classifier(pooled_output)
        return logits


class ImprovedEventCategorizer:
    """Improved event categorizer with better training"""
    def __init__(self, model_path=None, model_name='distilbert-base-uncased'):
        self.categories = ['Academic', 'Social', 'Sports', 'Cultural']
        self.num_classes = len(self.categories)
        self.model_name = model_name

        # Tag suggestions for each category
        self.category_tags = {
            'Academic': ['Workshop', 'Lecture', 'Research', 'Career', 'Study', 'Learning', 'Seminar', 'Conference'],
            'Social': ['Entertainment', 'Games', 'Movie', 'Party', 'Networking', 'Fun', 'Social', 'Community'],
            'Sports': ['Fitness', 'Game', 'Competition', 'Training', 'Recreation', 'Wellness', 'Athletic', 'Exercise'],
            'Cultural': ['Festival', 'Performance', 'Art', 'Music', 'International', 'Heritage', 'Dance', 'Cultural']
        }

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = ImprovedEventClassifier(num_classes=self.num_classes, model_name=model_name)
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model = self.model.to(self.device)
            self.is_trained = False

            if model_path and os.path.exists(model_path):
                self.load_model(model_path)
        except Exception as e:
            print(f"Warning: Could not load transformer model: {e}")
            print("Using rule-based classifier instead")
            self.tokenizer = None
            self.model = None
            self.device = None
            self.is_trained = False

    def train(self, training_data, epochs=15, lr=2e-5, batch_size=16, validation_split=0.15):
        """
        Improved training with validation, learning rate scheduling, and early stopping

        Args:
            training_data: List of (title, description, category) tuples
            epochs: Number of training epochs
            lr: Initial learning rate
            batch_size: Batch size
            validation_split: Fraction of data for validation
        """
        if self.tokenizer is None or self.model is None:
            print("Transformer model not available, skipping training")
            return

        print(f"🎓 Starting improved training with {len(training_data)} examples...")

        # Prepare data
        texts = [f"{title} [SEP] {desc}" for title, desc, _ in training_data]
        labels = [self.categories.index(cat) for _, _, cat in training_data]

        # Train/validation split
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, labels, test_size=validation_split, random_state=42, stratify=labels
        )

        print(f"📊 Train: {len(train_texts)} | Validation: {len(val_texts)}")

        # Create datasets
        train_dataset = EventDataset(train_texts, train_labels, self.tokenizer)
        val_dataset = EventDataset(val_texts, val_labels, self.tokenizer)

        # Create dataloaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()

        # Only fine-tune classifier head initially (freeze encoder)
        for param in self.model.encoder.parameters():
            param.requires_grad = False

        optimizer = torch.optim.AdamW(self.model.classifier.parameters(), lr=lr)

        # Learning rate scheduler with warmup
        total_steps = len(train_loader) * epochs
        warmup_steps = total_steps // 10
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )

        # Training loop
        best_val_acc = 0
        patience = 3
        patience_counter = 0

        for epoch in range(epochs):
            # Unfreeze encoder after a few epochs for fine-tuning
            if epoch == 5:
                print("🔓 Unfreezing encoder for fine-tuning...")
                for param in self.model.encoder.parameters():
                    param.requires_grad = True
                optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr * 0.1)  # Lower LR for encoder

            # Training
            self.model.train()
            train_loss = 0
            train_correct = 0
            train_total = 0

            for batch in train_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)

                optimizer.zero_grad()
                outputs = self.model(input_ids, attention_mask)
                loss = criterion(outputs, labels)
                loss.backward()

                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

                optimizer.step()
                scheduler.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                train_total += labels.size(0)
                train_correct += (predicted == labels).sum().item()

            train_acc = 100 * train_correct / train_total
            avg_train_loss = train_loss / len(train_loader)

            # Validation
            self.model.eval()
            val_loss = 0
            val_correct = 0
            val_total = 0

            with torch.no_grad():
                for batch in val_loader:
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['label'].to(self.device)

                    outputs = self.model(input_ids, attention_mask)
                    loss = criterion(outputs, labels)

                    val_loss += loss.item()
                    _, predicted = torch.max(outputs, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()

            val_acc = 100 * val_correct / val_total
            avg_val_loss = val_loss / len(val_loader)

            print(f'Epoch [{epoch+1}/{epochs}] | '
                  f'Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}% | '
                  f'Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.2f}%')

            # Early stopping
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    print(f"⏹️  Early stopping at epoch {epoch+1}")
                    break

        self.is_trained = True
        print(f"✅ Training completed! Best validation accuracy: {best_val_acc:.2f}%")

    def predict(self, title, description):
        """
        Predict event category with improved confidence calibration
        """
        if self.tokenizer is None or self.model is None or not self.is_trained:
            return self._rule_based_classify(title, description)

        self.model.eval()

        # Combine title and description with separator
        text = f"{title} [SEP] {description}"

        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        # Predict
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            # Apply temperature scaling for better calibration
            temperature = 1.5
            probabilities = torch.softmax(outputs / temperature, dim=1)
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
        """Enhanced rule-based classification as fallback"""
        text = f"{title} {description}".lower()

        # Enhanced keywords for each category
        keywords = {
            'Academic': {
                'high': ['thesis', 'dissertation', 'research', 'seminar', 'conference', 'academic', 'graduate', 'phd'],
                'medium': ['workshop', 'lecture', 'study', 'career', 'fair', 'symposium', 'presentation', 'defense'],
                'low': ['learning', 'education', 'training', 'professional', 'development']
            },
            'Social': {
                'high': ['party', 'social', 'gator nights', 'entertainment', 'game night', 'trivia'],
                'medium': ['meet', 'friends', 'gathering', 'community', 'networking', 'mixer'],
                'low': ['fun', 'event', 'activity', 'welcome', 'orientation']
            },
            'Sports': {
                'high': ['game', 'match', 'tournament', 'championship', 'athletic', 'football', 'basketball'],
                'medium': ['fitness', 'workout', 'training', 'competition', 'intramural', 'rec'],
                'low': ['sports', 'exercise', 'gym', 'wellness', 'yoga', 'running']
            },
            'Cultural': {
                'high': ['festival', 'cultural', 'heritage', 'international', 'performance', 'concert'],
                'medium': ['dance', 'music', 'art', 'theater', 'opera', 'exhibition'],
                'low': ['diversity', 'tradition', 'celebration', 'showcase', 'global']
            }
        }

        scores = {cat: 0 for cat in self.categories}

        for category, keyword_dict in keywords.items():
            for weight, kw_list in [('high', keyword_dict['high']),
                                   ('medium', keyword_dict['medium']),
                                   ('low', keyword_dict['low'])]:
                multiplier = 3 if weight == 'high' else (2 if weight == 'medium' else 1)
                for kw in kw_list:
                    if kw in text:
                        scores[category] += multiplier

        # Get category with highest score
        predicted_category = max(scores, key=scores.get)

        # If no keywords matched, use context clues
        if scores[predicted_category] == 0:
            if any(word in text for word in ['attend', 'join', 'rsvp', 'free food']):
                predicted_category = 'Social'
            else:
                predicted_category = 'Academic'

        suggested_tags = self._extract_tags(title, description, predicted_category)

        total_score = sum(scores.values())
        confidence = scores[predicted_category] / max(total_score, 1)

        return {
            'category': predicted_category,
            'confidence': min(confidence, 0.85),  # Cap rule-based confidence
            'all_probabilities': {cat: scores[cat] / max(total_score, 1)
                                 for cat in self.categories},
            'suggested_tags': suggested_tags
        }

    def _extract_tags(self, title, description, category):
        """Extract relevant tags with better matching"""
        base_tags = self.category_tags.get(category, [])
        text = f"{title} {description}".lower()
        relevant_tags = []

        # Find tags mentioned in title or description
        for tag in base_tags:
            if tag.lower() in text or any(word in text for word in tag.lower().split()):
                relevant_tags.append(tag)

        # Extract additional contextual tags
        if 'free' in text:
            relevant_tags.append('Free')
        if 'food' in text:
            relevant_tags.append('Food')
        if 'prize' in text or 'win' in text:
            relevant_tags.append('Prizes')
        if 'beginner' in text or 'all level' in text:
            relevant_tags.append('All Levels')

        # If we didn't find many, add some default category tags
        if len(relevant_tags) < 3:
            for tag in base_tags[:5]:
                if tag not in relevant_tags:
                    relevant_tags.append(tag)
                if len(relevant_tags) >= 3:
                    break

        return relevant_tags[:6]  # Return up to 6 tags

    def save_model(self, path):
        """Save model"""
        if self.model is not None:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'categories': self.categories,
                'model_name': self.model_name
            }, path)
            print(f"✅ Model saved to {path}")

    def load_model(self, path):
        """Load model"""
        if self.model is not None:
            checkpoint = torch.load(path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.categories = checkpoint.get('categories', self.categories)
            self.is_trained = True
            print(f"✅ Model loaded from {path}")

    def evaluate(self, test_data):
        """Evaluate model on test data"""
        if not self.is_trained:
            print("Model not trained yet")
            return

        correct = 0
        total = len(test_data)

        for title, description, true_category in test_data:
            result = self.predict(title, description)
            if result['category'] == true_category:
                correct += 1

        accuracy = 100 * correct / total
        print(f"📊 Accuracy: {accuracy:.2f}% ({correct}/{total})")
        return accuracy
