import asyncio
import logging
import re
from datetime import datetime
from typing import Dict
import numpy as np
import openai
from dotenv import load_dotenv
import google.generativeai as genai
from huggingface_hub import InferenceClient

# Load environment variables (e.g., API keys)
load_dotenv()

class TradingConfig:
    """Configuration class for trading parameters."""
    
    MIN_PROBABILITY_THRESHOLD = 60.0
    MAX_DAILY_LOSS = 0.05
    MAX_LOTS_PER_SYMBOL = 10
    LOT_SIZES = {
        "NIFTY": 50,
        "BANKNIFTY": 15,
        "MIDCAPNIFTY": 75
    }
    ENTRY_CUTOFF = "15:00"  # 3:00 PM
    CONSENSUS_THRESHOLD = 2

class AIAnalyzer:
    """Provides market analysis using various AI models."""

    def __init__(self, config):
        self.config = config
        
        # Initialize AI clients properly
        self.openai_client = None
        self.gemini_model = None
        self.hf_client = None
        
        self.setup_ai_clients()
        self.market_data = MarketDataProvider()

    def setup_ai_clients(self):
        """Initialize all AI clients with proper error handling"""
        try:
            # OpenAI - Updated for v1.0+
            if hasattr(self.config, 'OPENAI_API_KEY'):
                self.openai_client = openai.OpenAI(
                    api_key=self.config.OPENAI_API_KEY
                )
                logging.info("OpenAI client initialized successfully")
            else:
                logging.warning("OpenAI API key not found")
                
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {e}")
            self.openai_client = None

        try:
            # Gemini
            if hasattr(self.config, 'GEMINI_API_KEY'):
                genai.configure(api_key=self.config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logging.info("Gemini client initialized successfully")
            else:
                logging.warning("Gemini API key not found")
                
        except Exception as e:
            logging.error(f"Failed to initialize Gemini client: {e}")
            self.gemini_model = None

        try:
            # HuggingFace
            if hasattr(self.config, 'HUGGINGFACE_API_KEY'):
                self.hf_client = InferenceClient(token=self.config.HUGGINGFACE_API_KEY)
                logging.info("HuggingFace client initialized successfully")
            else:
                logging.warning("HuggingFace API key not found")
                
        except Exception as e:
            logging.error(f"Failed to initialize HuggingFace client: {e}")
            self.hf_client = None

    def generate_market_prompt(self, symbol: str, current_price: float, expiry_date: str) -> str:
        """Generate a detailed market analysis prompt for AI models."""
        return f"""
Analyze the current market sentiment and potential price movement for {symbol} with a current price of ₹{current_price} leading up to the expiry date of {expiry_date}.

Consider factors such as recent news, market volatility, and any relevant technical indicators.

Provide a concise analysis in a single paragraph.

Conclude your analysis with a clear prediction of the future direction (BULLISH, BEARISH, or NEUTRAL) and a probability percentage of that outcome (e.g., "Probability: 75%").

Focus on high-probability trades with 70%+ confidence for weekly options selling strategies.
"""

    async def get_openai_analysis(self, symbol: str, current_price: float, expiry_date: str) -> Dict:
        """Get analysis from OpenAI GPT-4 using updated API"""
        try:
            if not self.openai_client:
                return {"error": "OpenAI client not initialized"}
                
            prompt = self.generate_market_prompt(symbol, current_price, expiry_date)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )

            analysis = response.choices[0].message.content
            probability = self.extract_probability(analysis)

            return {
                "provider": "OpenAI",
                "analysis": analysis,
                "probability": probability,
                "direction": self.extract_direction(analysis)
            }

        except Exception as e:
            logging.error(f"OpenAI analysis error: {e}")
            return {"error": str(e)}

    async def get_gemini_analysis(self, symbol: str, current_price: float, expiry_date: str) -> Dict:
        """Get analysis from Google Gemini"""
        try:
            if not self.gemini_model:
                return {"error": "Gemini client not initialized"}
                
            prompt = self.generate_market_prompt(symbol, current_price, expiry_date)
            
            response = self.gemini_model.generate_content(prompt)
            analysis = response.text

            probability = self.extract_probability(analysis)

            return {
                "provider": "Gemini",
                "analysis": analysis,
                "probability": probability,
                "direction": self.extract_direction(analysis)
            }

        except Exception as e:
            logging.error(f"Gemini analysis error: {e}")
            return {"error": str(e)}

    async def get_huggingface_analysis(self, symbol: str, current_price: float, expiry_date: str) -> Dict:
        """Get analysis from Hugging Face models"""
        try:
            if not self.hf_client:
                return {"error": "HuggingFace client not initialized"}
                
            prompt = self.generate_market_prompt(symbol, current_price, expiry_date)
            
            # Use text generation with proper parameters
            response = self.hf_client.text_generation(
                prompt,
                model="microsoft/DialoGPT-medium",  # Using a more stable model
                max_new_tokens=500,
                temperature=0.3,
                return_full_text=False
            )

            analysis = response if isinstance(response, str) else str(response)
            probability = self.extract_probability(analysis)

            return {
                "provider": "HuggingFace",
                "analysis": analysis,
                "probability": probability,
                "direction": self.extract_direction(analysis)
            }

        except Exception as e:
            logging.error(f"HuggingFace analysis error: {e}")
            return {"error": str(e)}

    def extract_probability(self, text: str) -> float:
        """Extract probability percentage from AI response"""
        if not text:
            return 50.0
            
        # Look for patterns like "75%", "probability: 80%", etc.
        patterns = [
            r'probability.*?(\d+)%',
            r'(\d+)%.*?probability',
            r'confidence.*?(\d+)%',
            r'(\d+)%.*?chance',
            r'(\d+)%'  # Generic percentage
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                prob = float(match.group(1))
                # Ensure probability is within reasonable bounds
                return max(30.0, min(95.0, prob))

        # Default probability if not found
        return 55.0

    def extract_direction(self, text: str) -> str:
        """Extract trading direction from AI response"""
        if not text:
            return "NEUTRAL"
            
        text_lower = text.lower()
        bullish_keywords = ['bullish', 'buy', 'long', 'upward', 'positive', 'above', 'rise', 'up']
        bearish_keywords = ['bearish', 'sell', 'short', 'downward', 'negative', 'below', 'fall', 'down']

        bullish_count = sum(1 for keyword in bullish_keywords if keyword in text_lower)
        bearish_count = sum(1 for keyword in bearish_keywords if keyword in text_lower)

        if bullish_count > bearish_count:
            return "BULLISH"
        elif bearish_count > bullish_count:
            return "BEARISH"
        else:
            return "NEUTRAL"

    async def get_consensus_analysis(self, symbol: str, current_price: float, expiry_date: str) -> Dict:
        """Get consensus analysis from all AI providers with fallback"""
        tasks = []
        
        # Only add tasks for initialized clients
        if self.openai_client:
            tasks.append(self.get_openai_analysis(symbol, current_price, expiry_date))
        if self.gemini_model:
            tasks.append(self.get_gemini_analysis(symbol, current_price, expiry_date))
        if self.hf_client:
            tasks.append(self.get_huggingface_analysis(symbol, current_price, expiry_date))

        if not tasks:
            return {"error": "No AI providers available"}

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = []
            
            for result in results:
                if isinstance(result, dict) and 'error' not in result:
                    valid_results.append(result)
                elif isinstance(result, Exception):
                    logging.error(f"AI analysis exception: {result}")

            # Use fallback if no valid results
            if len(valid_results) == 0:
                return self.get_fallback_analysis(symbol, current_price, expiry_date)

            # Calculate consensus
            avg_probability = np.mean([r['probability'] for r in valid_results])
            directions = [r['direction'] for r in valid_results]
            consensus_direction = max(set(directions), key=directions.count) if directions else "NEUTRAL"

            return {
                "consensus_probability": avg_probability,
                "consensus_direction": consensus_direction,
                "individual_results": valid_results,
                "confidence": len(valid_results) / max(len(tasks), 1)
            }

        except Exception as e:
            logging.error(f"Error in consensus analysis: {e}")
            return self.get_fallback_analysis(symbol, current_price, expiry_date)

    def get_fallback_analysis(self, symbol: str, current_price: float, expiry_date: str) -> Dict:
        """Fallback analysis when AI providers fail"""
        # Simple technical analysis fallback
        current_time = datetime.now()
        
        # Mock analysis based on simple rules
        if current_time.hour < 12:
            direction = "BULLISH"
            probability = 65.0
        elif current_time.hour > 14:
            direction = "BEARISH" 
            probability = 62.0
        else:
            direction = "NEUTRAL"
            probability = 55.0

        return {
            "consensus_probability": probability,
            "consensus_direction": direction,
            "individual_results": [{
                "provider": "Fallback",
                "analysis": f"Fallback analysis for {symbol} at ₹{current_price}",
                "probability": probability,
                "direction": direction
            }],
            "confidence": 0.5
        }

class MarketDataProvider:
    """Handles real-time market data"""

    def __init__(self):
        self.cache = {}
        self.last_update = {}

    def get_current_price(self, symbol: str) -> float:
        """Get current market price for symbol"""
        # This would integrate with your broker's API
        # For demo purposes, returning mock data
        mock_prices = {
            "NIFTY": 24500.0,
            "BANKNIFTY": 52000.0,
            "MIDCAPNIFTY": 15000.0
        }

        # Add some randomness to simulate real market movement
        base_price = mock_prices.get(symbol, 100.0)
        variation = np.random.uniform(-0.01, 0.01)
        return base_price * (1 + variation)

    def get_option_chain(self, symbol: str) -> Dict:
        """Get options chain data"""
        # Mock option chain data
        current_price = self.get_current_price(symbol)
        chain = {
            "symbol": symbol,
            "underlying_price": current_price,
            "calls": {},
            "puts": {}
        }

        # Generate mock strikes around current price
        for i in range(-10, 11):
            strike = current_price + (i * 100)
            strike = round(strike / 50) * 50  # Round to nearest 50

            chain["calls"][strike] = {
                "strike": strike,
                "premium": max(0.1, current_price - strike + np.random.uniform(1, 50)),
                "iv": np.random.uniform(15, 35)
            }

            chain["puts"][strike] = {
                "strike": strike,
                "premium": max(0.1, strike - current_price + np.random.uniform(1, 50)),
                "iv": np.random.uniform(15, 35)
            }

        return chain

class RiskManager:
    """Handles risk management and position sizing"""

    def __init__(self, config):
        self.config = config
        self.daily_pnl = 0.0
        self.active_positions = {}

    def calculate_position_size(self, symbol: str, account_balance: float, risk_per_trade: float) -> int:
        """Calculate optimal position size"""
        max_lots = self.config.MAX_LOTS_PER_SYMBOL
        lot_size = self.config.LOT_SIZES.get(symbol, 50)

        # Risk-based position sizing
        risk_amount = account_balance * risk_per_trade

        # For simplicity, using a basic calculation
        # In reality, you'd factor in option premium, volatility, etc.
        suggested_lots = min(max_lots, max(1, int(risk_amount / 10000)))
        return suggested_lots * lot_size

    def should_take_trade(self, probability: float, daily_pnl: float, account_balance: float) -> bool:
        """Determine if trade should be taken based on risk parameters"""
        # Check minimum probability threshold
        if probability < self.config.MIN_PROBABILITY_THRESHOLD:
            return False

        # Check daily loss limit
        if abs(daily_pnl) > account_balance * self.config.MAX_DAILY_LOSS:
            return False

        # Check if market is within trading hours
        current_time = datetime.now().strftime("%H:%M")
        if current_time > self.config.ENTRY_CUTOFF:
            return False

        return True

    def calculate_stop_loss(self, entry_price: float, direction: str, symbol: str) -> float:
        """Calculate stop loss level"""
        if direction == "BULLISH":  # PUT selling
            return entry_price * 1.5  # 50% loss
        else:  # CALL selling
            return entry_price * 1.5
