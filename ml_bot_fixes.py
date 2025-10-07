# Complete ML Bot Error Handling and Training Pipeline Functions

# Save this as ml_bot_fixes.py and integrate or replace your existing code in 10.py

import os
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLBotErrorHandler:
    """Complete ML Bot with comprehensive error handling and training pipeline"""
    def __init__(self, model_path="models/enhanced_bot_model.pkl", data_path="data/training_data.csv"):
        self.model_path = model_path
        self.data_path = data_path
        self.model = None
        self.is_trained = False
        self.setup_directories()

    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        try:
            # Create models directory
            Path("models").mkdir(parents=True, exist_ok=True)
            # Create data directory
            Path("data").mkdir(parents=True, exist_ok=True)
            # Create logs directory
            Path("logs").mkdir(parents=True, exist_ok=True)
            logger.info("✅ Directory structure created successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating directories: {e}")
            return False

    def validate_training_data(self, data_path=None):
        """Comprehensive training data validation"""
        if data_path is None:
            data_path = self.data_path
        try:
            if not os.path.exists(data_path):
                logger.error(f"❌ Training data file not found: {data_path}")
                return False, None
            if os.path.getsize(data_path) == 0:
                logger.error("❌ Training data file is empty")
                return False, None
            # Load data
            if data_path.endswith('.csv'):
                data = pd.read_csv(data_path)
            elif data_path.endswith('.json'):
                with open(data_path, 'r') as f:
                    data = pd.DataFrame(json.load(f))
            else:
                logger.error(f"❌ Unsupported file format: {data_path}")
                return False, None
            if data.empty:
                logger.error("❌ No data found in training file")
                return False, None
            logger.info(f"✅ Data loaded: {len(data)} rows, {len(data.columns)} columns")
            # Minimum samples check
            min_samples = 100
            if len(data) < min_samples:
                logger.warning(f"⚠️ Limited data ({len(data)} samples, recommended ≥{min_samples})")
            # Missing values
            missing = data.isnull().sum().sum()
            if missing > 0:
                logger.warning(f"⚠️ {missing} missing values found")
            # Duplicates
            dup = data.duplicated().sum()
            if dup > 0:
                logger.warning(f"⚠️ {dup} duplicate rows found")
            return True, data
        except Exception as e:
            logger.error(f"❌ Data validation failed: {e}")
            return False, None

    def validate_data_quality(self, data):
        """Detailed data quality validation"""
        try:
            report = {
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'missing_values': {},
                'data_types': {},
                'duplicates': int(data.duplicated().sum()),
                'quality_score': 0
            }
            total_cells = len(data) * len(data.columns)
            missing_cells = data.isnull().sum().sum()
            # Per-column missing
            for col in data.columns:
                m = int(data[col].isnull().sum())
                if m:
                    report['missing_values'][col] = m
                report['data_types'][col] = str(data[col].dtype)
            # Quality score
            score = max(0, 100 - (missing_cells/total_cells*100))
            report['quality_score'] = round(score, 2)
            logger.info(f"📊 Data Quality Score: {report['quality_score']}/100")
            if score < 70:
                logger.warning("⚠️ Low data quality detected")
            return report
        except Exception as e:
            logger.error(f"❌ Data quality validation failed: {e}")
            return None

    def save_model_safely(self, model, model_name=None):
        """Robust model saving with backups"""
        if model_name is None:
            model_name = "enhanced_bot_model.pkl"
        try:
            model_dir = Path("models")
            model_dir.mkdir(parents=True, exist_ok=True)
            model_path = model_dir / model_name
            # Backup existing
            if model_path.exists():
                backup = model_dir / f"{model_name}.backup.{int(datetime.now().timestamp())}"
                os.rename(model_path, backup)
                logger.info(f"💾 Backed up existing model to {backup}")
            with open(model_path, 'wb') as f:
                pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
            # Verify load
            with open(model_path, 'rb') as f:
                _ = pickle.load(f)
            logger.info(f"✅ Model saved and verified: {model_path}")
            return str(model_path)
        except Exception as e:
            logger.error(f"❌ Error saving model: {e}")
            # Fallback to joblib
            try:
                import joblib
                joblib_path = model_dir / f"{model_name}.joblib"
                joblib.dump(model, joblib_path)
                logger.info(f"✅ Model saved via joblib fallback: {joblib_path}")
                return str(joblib_path)
            except Exception:
                logger.error("❌ All model saving methods failed")
                return None

    def load_model_safely(self, model_path=None):
        """Robust model loading with fallbacks"""
        if model_path is None:
            model_path = self.model_path
        try:
            if not os.path.exists(model_path):
                # try alternatives
                for alt in [model_path.replace('.pkl', '.joblib'),
                            model_path.replace('.pkl', '.pickle'),
                            model_path + '.backup']:
                    if os.path.exists(alt):
                        logger.info(f"🔄 Found alternative model: {alt}")
                        model_path = alt
                        break
                else:
                    return None
            # Try pickle load
            try:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"✅ Model loaded: {model_path}")
                return model
            except Exception as pe:
                logger.warning(f"⚠️ Pickle load failed: {pe}")
                # Try joblib
                import joblib
                model = joblib.load(model_path)
                logger.info(f"✅ Model loaded via joblib: {model_path}")
                return model
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            return None

    def prepare_training_data(self, data):
        """Prepare data for ML training"""
        try:
            if 'text' in data and 'label' in data:
                X, y = data['text'].values, data['label'].values
            elif 'input' in data and 'output' in data:
                X, y = data['input'].values, data['output'].values
            elif 'question' in data and 'answer' in data:
                X, y = data['question'].values, data['answer'].values
            else:
                logger.warning("⚠️ Using generic prep: first col X, last col y")
                X, y = data.iloc[:,0].values, data.iloc[:,-1].values
            X = [str(x).strip() for x in X if x and str(x).strip()]
            y = [str(v).strip() for v in y if v and str(v).strip()]
            if len(X) != len(y):
                logger.error("❌ Input-target length mismatch")
                return None, None
            logger.info(f"✅ Prepared {len(X)} samples")
            return np.array(X), np.array(y)
        except Exception as e:
            logger.error(f"❌ Error preparing training data: {e}")
            return None, None

    def train_ml_model(self, retrain=False):
        """Full ML model training pipeline"""
        try:
            logger.info("🔄 Starting training pipeline")
            valid, data = self.validate_training_data()
            if not valid:
                logger.error("❌ Data validation failed")
                return False
            report = self.validate_data_quality(data)
            if report and report['quality_score'] < 50:
                logger.error("❌ Data quality too low")
                return False
            X, y = self.prepare_training_data(data)
            if X is None:
                logger.error("❌ Data prep failed")
                return False
            # Example using TF-IDF + Naive Bayes
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.naive_bayes import MultinomialNB
            from sklearn.pipeline import Pipeline
            from sklearn.model_selection import train_test_split
            Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
                ('clf', MultinomialNB())
            ])
            logger.info("🔄 Training model")
            pipeline.fit(Xtr, ytr)
            tra = pipeline.score(Xtr, ytr)
            tes = pipeline.score(Xte, yte)
            logger.info(f"📊 Train accuracy: {tra:.3f}, Test accuracy: {tes:.3f}")
            if tes < 0.5:
                logger.warning("⚠️ Low test accuracy")
            path = self.save_model_safely(pipeline)
            if path:
                self.model = pipeline
                self.is_trained = True
                logger.info("✅ Training completed")
                return True
            else:
                logger.error("❌ Model save failed")
                return False
        except ImportError as ie:
            logger.error(f"❌ Missing libs: {ie}")
            logger.info("💡 pip install scikit-learn")
            return False
        except Exception as e:
            logger.error(f"❌ Training pipeline error: {e}")
            return False

    def predict_with_fallback(self, input_text):
        """Make predictions with error handling"""
        try:
            if self.model is None:
                self.model = self.load_model_safely()
            if self.model is None:
                logger.warning("⚠️ No model, attempting training")
                if not self.train_ml_model():
                    return "❌ No model available"
            try:
                pred = self.model.predict([input_text])[0]
                conf = max(self.model.predict_proba([input_text])[0])
                if conf < 0.3:
                    return f"🤔 Low confidence ({conf:.2f}), guess: {pred}"
                return pred
            except Exception as pe:
                logger.error(f"❌ Prediction error: {pe}")
                return "❌ Prediction failed"
        except Exception as e:
            logger.error(f"❌ Prediction pipeline error: {e}")
            return "❌ Bot unavailable"

    def get_system_status(self):
        """Get comprehensive system status"""
        return {
            'model_loaded': self.model is not None,
            'model_file_exists': os.path.exists(self.model_path),
            'data_file_exists': os.path.exists(self.data_path),
            'is_trained': self.is_trained,
            'dirs_ok': all(os.path.exists(d) for d in ['models','data','logs'])
        }

    def diagnose_errors(self):
        """Comprehensive error diagnosis"""
        logger.info("🔍 Running system diagnosis")
        st = self.get_system_status()
        issues, sol = [], []
        if not st['dirs_ok']:
            issues.append("Missing directories"); sol.append("Call setup_directories()")
        if not st['data_file_exists']:
            issues.append("Data file not found"); sol.append(f"Ensure data at {self.data_path}")
        if not st['model_file_exists']:
            issues.append("Model file not found"); sol.append("Run train_ml_model()")
        if not st['model_loaded']:
            issues.append("Model not loaded"); sol.append("Call load_model_safely() or train")
        if issues:
            logger.warning("⚠️ Issues found:")
            for i,(i_s, s_s) in enumerate(zip(issues,sol),1):
                logger.warning(f" {i}. {i_s}")
                logger.info(f" Solution: {s_s}")
        else:
            logger.info("✅ No issues detected")
        return issues, sol

    def initialize_bot():
        """Initialize the ML bot with error handling"""
        try:
            bot = MLBotErrorHandler()
            issues, solutions = bot.diagnose_errors()
            if issues:
                logger.info("🔧 Attempting automated fixes")
                if not os.path.exists(bot.data_path):
                    logger.info("💡 Creating sample data")
                    create_sample_training_data(bot.data_path)
                if not os.path.exists(bot.model_path):
                    logger.info("🔄 Training new model")
                    bot.train_ml_model()
            return bot
        except Exception as e:
            logger.error(f"❌ Bot initialization failed: {e}")
            return None

    def validate_model(self, model):
        """Validate if the model is usable."""
        if model is None:
            return False
        if not hasattr(model, 'predict') or not hasattr(model, 'predict_proba'):
            return False
        # Add more checks as needed (e.g., test with dummy data)
        return True

    def create_sample_training_data(data_path):
        """Create sample training data if none exists"""
        sample = {
            'input': [
                'hello', 'hi', 'good morning', 'hey there',
                'how are you', "what's up", 'how do you do',
                'goodbye', 'bye', 'see you later', 'farewell',
                'what is your name', 'who are you', 'what can you do',
                'help', 'I need help', 'assist me', 'support'
            ],
            'output': [
                'greeting','greeting','greeting','greeting',
                'status_inquiry','status_inquiry','status_inquiry',
                'farewell','farewell','farewell','farewell',
                'identity','identity','capabilities',
                'help','help','help','help'
            ]
        }
        try:
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            pd.DataFrame(sample).to_csv(data_path, index=False)
            logger.info(f"✅ Sample data created at {data_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed creating sample data: {e}")
            return False

def main():
    """Main function to demonstrate the bot"""
    logger.info("🚀 Starting Enhanced ML Bot")
    bot = MLBotErrorHandler.initialize_bot()
    if not bot:
        logger.error("❌ Bot init failed")
        return
    tests = ["hello there","goodbye","what can you do","help me"]
    for txt in tests:
        logger.info(f"📤 Input: {txt}")
        resp = bot.predict_with_fallback(txt)
        logger.info(f"📥 Response: {resp}")
        print(f"Bot: {resp}")

if __name__ == "__main__":
    main()
