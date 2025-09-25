#!/usr/bin/env python3
# =============================================================================
# GOD BOT PRO: HYBRID EDITION v3.0 - COMPLETE ENHANCED VERSION (NIFTY ONLY FOR TESTING)
# =============================================================================
# Advanced NSE Options Trading Bot with Multi-Timeframe Analysis and AI Learning
# Features: Smart self-analysis, mistake learning, complete data tracking
# Author: Enhanced for ultimate trading intelligence
# =============================================================================
# Import necessary libraries for async operations, data handling, logging, and more
from __future__ import annotations

# =============================================================================
# CLEANED IMPORTS - NO DUPLICATES (FIXED)
# =============================================================================
# Standard library imports (alphabetically organized)
import asyncio
import io
import json
import logging
import math
import os
import random
import sys
import time
import traceback
from collections import deque
from datetime import datetime, time as dt_time, timedelta
from typing import Any, Dict, List, Optional, Tuple

# NEW: Import AgentEngine for AGENTS.md integration
from agent_engine import AgentEngine

# Third-party data handling and web imports
import pickle
import aiohttp
import cloudscraper
import numpy as np  # FIXED: Added missing numpy for MultiTimeframeAnalyzer
import pandas as pd
import requests
import yaml
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Analytics and visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Financial data fallback
import yfinance as yf
# Add these lines after your existing imports:
CANDLE_SYSTEM_ACTIVE = False
candle_system = None

# LOCAL MODULE IMPORTS - signal_engine and 15-min predictor
from signal_engine import process_live_market
from fifteen_min_predictor import FifteenMinPredictor
# Add these imports at the top of your new3.py file (after your existing imports)
def load_config():
    """Load configuration from config.yaml or return default config."""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.info("✅ Configuration loaded from config.yaml")
        return config
    except Exception as e:
        logger.warning(f"⚠️ Could not load config.yaml: {e}. Using default configuration.")
        # Default configuration
        return {
            'symbol': 'NIFTY',
            'model_path': 'enhanced_bot_model.pkl',
            'data_path': 'data/training_data.csv',
            'time_window_analysis': {
                'enabled': True,
                'use_research_probabilities': True,
                'golden_window_focus': True,
                'avoid_lunch_trading': True,
                'minute_level_analysis': True,
                'volume_oi_integration': True
            },
            'ai_integration': {
                'enabled': True,
                'confidence_threshold': 0.7,
                'learning_rate': 0.01
            }
        }
# =============================
# TELEGRAM ALERT SYSTEM
# =============================
TELEGRAM_BOT_TOKEN = "7869031606:AAGiTsf4KoV5aeDHjyppRRFYgc4wm8bc_8M"
TELEGRAM_CHAT_ID = "1598471281"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram(msg: str):
    """Send message to Telegram."""
    try:
        import requests
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
        requests.post(TELEGRAM_URL, data=data, timeout=5)
    except Exception as e:
        logger.error(f"❌ Telegram send failed: {e}")
# =============================================================================
# 🤖 SMART AI CO-PILOT (Embedded, not separate)
# =============================================================================
from typing import Dict, Any

# Simple workflow implementation for AI analysis
class SimpleAIWorkflow:
    """Simple workflow implementation for AI analysis."""
    
    async def ainvoke(self, state, config=None):
        """Simple implementation of ainvoke method."""
        # Extract market data from state
        current_snapshot = state.get("current_snapshot", {})
        market_history = state.get("market_history", [])
        
        # Simple analysis logic
        spot_price = current_snapshot.get('underlying_value', 0)
        ce_oi = current_snapshot.get('CE_OI', 0)
        pe_oi = current_snapshot.get('PE_OI', 0)
        
        # Determine market bias
        oi_bias = ce_oi - pe_oi
        market_bias = "BULLISH" if oi_bias < 0 else "BEARISH" if oi_bias > 0 else "NEUTRAL"
        
        # Generate trade signals
        trade_action = "BUY" if market_bias == "BULLISH" else "SELL" if market_bias == "BEARISH" else "HOLD"
        confidence = min(abs(oi_bias) / max(ce_oi, pe_oi, 1) * 100, 100)
        
        return {
            "strategy_updates": {
                "strategy": f"{market_bias} based on OI bias"
            },
            "risk_assessment": {
                "should_trade": confidence > 50
            },
            "self_reflection": {
                "analysis": f"Market appears {market_bias.lower()} with {confidence:.1f}% confidence"
            },
            "trade_signals": [{
                "action": trade_action,
                "confidence": confidence
            }]
        }

class SmartAITradingBot:
    def __init__(self, symbol: str = "NIFTY"):
        self.symbol = symbol
        self.total_trades = 0
        self.successful_trades = 0
        self.total_pnl = 0.0
        self.error_count = 0
        self.corrections_made = 0
        
        # FIXED: Add workflow attribute
        self.workflow = SimpleAIWorkflow()
        
        logger.info("🤖 Smart AI Co-Pilot initialized inside God Bot PRO")
    
    async def self_correct(self, error_log: list, current_analysis: Dict[str, Any]):
        """Use AI logic to suggest or apply fixes"""
        if not error_log:
            return {"status": "NO_ERROR"}
        
        last_error = error_log[-1]
        error_msg = last_error["error"]
        
        # Apply known fixes
        if "display_15_timeframe_table" in error_msg:
            self._fix_display_table()
            return {"status": "FIXED", "issue": "display_table"}
        elif "EnhancedMarketState" in error_msg:
            self._fix_market_state()
            return {"status": "FIXED", "issue": "market_state"}
        
        return {"status": "UNKNOWN_ERROR"}
    
    def _fix_display_table(self):
        global display_15_timeframe_table
        exec("""
def display_15_timeframe_table(timeframe_analysis):
    print('\\n📊 15-TIMEFRAME ANALYSIS TABLE')
    for key, data in timeframe_analysis.items():
        status = data.get('status', 'PENDING')
        print(f"{key}: {status}")
""")
        # Save to file
        with open("v.py", "r+") as f:
            content = f.read()
            if "def display_15_timeframe_table" not in content:
                f.seek(0, 0)
                f.write("\n\n" + exec.__code__.co_consts[0] + "\n\n" + content)
        logger.info("✅ Auto-fixed: display_15_timeframe_table")
    
    def _fix_market_state(self):
        global EnhancedMarketState
        exec("""
class EnhancedMarketState:
    def __init__(self, symbol, config):
        self.symbol = symbol
        self.config = config
        self.market_history = []
        self.last_spot_price = 0.0
""")
        globals()['EnhancedMarketState'] = EnhancedMarketState
        logger.info("✅ Auto-fixed: EnhancedMarketState")

# Add this import after the existing import
import asyncio

class EnhancedGodBotWithAI:
    """Your existing GodBot enhanced with Smart AI capabilities"""
    
    def __init__(self):
        # Initialize your existing components (keep all your current init code)
        from signal_engine import process_live_market
        self.symbol = "NIFTY"
        self.config = load_config()
        self.market_state = EnhancedMarketState(self.symbol, self.config)
        self.candle_system = CandleIntelligenceSystem()
        self.timeframe_analyzer = MultiTimeframeAnalyzer()
        # ... all your existing initialization ...
        
        # NEW: Add Smart AI Bot as an advisor
        self.smart_ai = SmartAITradingBot(self.symbol)
        self.ai_enabled = True
        
        logger.info("🤖 GodBot enhanced with Smart AI capabilities!")
    
    async def enhanced_analysis_cycle(self, snapshot_data):
        """Enhanced analysis cycle with AI intelligence"""
        
        # 1. Run your EXISTING analysis (keep everything as-is)
        analysis_result = self.run_existing_analysis(snapshot_data)
        
        # 2. Get AI enhancement and recommendations
        if self.ai_enabled:
            try:
                # Let the AI analyze the same data and provide insights
                ai_state = {
                    "current_snapshot": snapshot_data,
                    "market_history": list(self.market_state.market_history)[-50:],
                    "timeframe_analysis": getattr(self, 'last_timeframe_analysis', {}),
                    "candle_analysis": getattr(self, 'last_candle_analysis', {})
                }
                
                # Get AI insights (this runs the smart AI workflow)
                config = {"configurable": {"thread_id": "godbot_ai_thread"}}
                # FIXED: Added error handling for workflow
                try:
                    ai_result = await self.smart_ai.workflow.ainvoke(ai_state, config=config)
                except Exception as workflow_error:
                    logger.error(f"❌ AI workflow error: {workflow_error}")
                    # Provide fallback AI result
                    ai_result = {
                        "strategy_updates": {"strategy": "NEUTRAL"},
                        "risk_assessment": {"should_trade": False},
                        "self_reflection": {"analysis": f"AI workflow failed: {str(workflow_error)}"},
                        "trade_signals": []
                    }
                
                # Combine your analysis with AI insights
                enhanced_result = self.combine_analysis_with_ai(analysis_result, ai_result)
                
                logger.info("🧠 AI Enhancement applied to trading decision")
                return enhanced_result
                
            except Exception as e:
                logger.warning(f"⚠️ AI enhancement failed: {e}, using standard analysis")
                return analysis_result
        
        return analysis_result
    
    def combine_analysis_with_ai(self, your_analysis, ai_analysis):
        """Combine your existing analysis with AI insights"""
        
        # Get AI recommendations
        ai_strategy = ai_analysis.get("strategy_updates", {})
        ai_risk = ai_analysis.get("risk_assessment", {})
        ai_reflection = ai_analysis.get("self_reflection", {})
        
        # Your existing verdict
        your_verdict = your_analysis.get("verdict", "NEUTRAL")
        your_confidence = your_analysis.get("confidence", 0.5)
        
        # AI verdict
        ai_trades = ai_analysis.get("trade_signals", [])
        ai_verdict = "NEUTRAL"
        ai_confidence = 0.5
        
        if ai_trades:
            latest_ai_trade = ai_trades[-1]
            ai_verdict = "BULLISH" if latest_ai_trade.get("action") == "BUY" else "BEARISH"
            ai_confidence = latest_ai_trade.get("confidence", 50) / 100
        
        # Smart combination logic
        if your_verdict == ai_verdict:
            # Both agree - boost confidence
            final_verdict = your_verdict
            final_confidence = min(your_confidence + 0.15, 0.95)  # 15% boost, max 95%
            enhancement_note = f"✅ AI CONFIRMS: {your_verdict} (Confidence boosted)"
            
        elif abs(your_confidence - ai_confidence) < 0.2:
            # Close confidence levels - use your analysis but note AI difference
            final_verdict = your_verdict
            final_confidence = your_confidence
            enhancement_note = f"🤔 AI SUGGESTS: {ai_verdict} (Minor disagreement)"
            
        else:
            # Significant disagreement - be cautious
            final_verdict = "NEUTRAL"
            final_confidence = 0.4
            enhancement_note = f"⚠️ AI CONFLICTS: You={your_verdict}, AI={ai_verdict} (Being cautious)"
        
        # Enhanced result with AI insights
        enhanced_result = your_analysis.copy()
        enhanced_result.update({
            "verdict": final_verdict,
            "confidence": final_confidence,
            "ai_enhancement": enhancement_note,
            "ai_strategy": ai_strategy.get("strategy", "No AI strategy"),
            "ai_reflection": ai_reflection.get("analysis", "No AI reflection"),
            "ai_risk_assessment": ai_risk.get("should_trade", True),
            "combined_reasoning": f"{your_analysis.get('reasoning', '')} + {enhancement_note}"
        })
        
        return enhanced_result
    
    def log_analysis_results(self, analysis_result):
        """Log the analysis results with timeframe details"""
        try:
            verdict = analysis_result.get("verdict", "NEUTRAL")
            confidence = analysis_result.get("confidence", 0.5)
            reasoning = analysis_result.get("reasoning", "No reasoning provided")
            
            logger.info("=" * 80)
            logger.info("📊 COMPREHENSIVE ANALYSIS RESULTS")
            logger.info("=" * 80)
            logger.info(f"🎯 Final Verdict: {verdict}")
            logger.info(f"📈 Confidence: {confidence:.2f}")
            logger.info(f"💡 Reasoning: {reasoning}")
            
            # Log timeframe analysis if available
            timeframe_data = analysis_result.get("detailed_timeframe_data", {})
            if timeframe_data:
                logger.info("\n📊 TIMEFRAME BREAKDOWN:")
                logger.info("-" * 50)
                for interval, data in timeframe_data.items():
                    logger.info(f"⏰ {interval}:")
                    logger.info(f"   Price: {data.get('spot_change_pct', 0):.4f}%")
                    logger.info(f"   Momentum: {data.get('momentum', 'UNKNOWN')}")
                    logger.info(f"   Strength: {data.get('strength_score', 0):.2f}/10")
            
            # Log technical analysis
            tech_analysis = analysis_result.get("technical_analysis", {})
            if tech_analysis:
                logger.info("\n🔧 TECHNICAL INDICATORS:")
                logger.info("-" * 50)
                logger.info(f"   OI Bias: {tech_analysis.get('oi_bias', 0):,}")
                logger.info(f"   OI PCR: {tech_analysis.get('oi_pcr', 0):.4f}")
                logger.info(f"   Volume Bias: {tech_analysis.get('volume_bias', 0):,}")
            
            # Log AI enhancement if available
            if "ai_enhancement" in analysis_result:
                logger.info(f"\n🤖 AI Enhancement: {analysis_result['ai_enhancement']}")
            
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"❌ Error logging analysis results: {e}")
            
    async def execute_trade_logic(self, analysis_result):
        """Execute trade based on analysis result"""
        try:
            verdict = analysis_result.get("verdict", "NEUTRAL")
            confidence = analysis_result.get("confidence", 0.5)
            
            # Only execute if confidence is high enough
            if confidence >= 0.7 and verdict in ["BULLISH", "BEARISH"]:
                action = "BUY" if verdict == "BULLISH" else "SELL"
                
                logger.info(f"🚀 EXECUTING TRADE: {action} with confidence {confidence:.2f}")
                
                # In a real implementation, this would execute the trade
                # For now, we'll just log it
                trade_result = {
                    "action": action,
                    "confidence": confidence,
                    "status": "EXECUTED",
                    "timestamp": datetime.now().isoformat()
                }
                
                return trade_result
            else:
                logger.info(f"⏸️ NO TRADE: Confidence {confidence:.2f} below threshold or neutral verdict")
                return {
                    "action": "NONE",
                    "confidence": confidence,
                    "status": "SKIPPED",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Error executing trade: {e}")
            return {
                "action": "ERROR",
                "confidence": 0,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_existing_analysis(self, snapshot_data):
        """Run your existing analysis logic with conservative trend detection."""
        try:
            # Get current market state
            current_price = snapshot_data.get('underlying_value', 0)
            ce_oi = snapshot_data.get('CE_OI', 0)
            pe_oi = snapshot_data.get('PE_OI', 0)
            oi_pcr = snapshot_data.get('OI_PCR', 1.0)
            
            # Get timeframe analysis with conservative approach
            timeframe_analysis = self.timeframe_analyzer.analyze_timeframe_changes(self.market_state.market_history)
            market_state = timeframe_analysis.get('market_state', 'UNKNOWN')
            
            # NEW: Log timeframe analysis details
            logger.info("=" * 80)
            logger.info("📊 TIMEFRAME ANALYSIS DETAILS")
            logger.info("=" * 80)
            
            for interval, data in timeframe_analysis.get('changes', {}).items():
                logger.info(f"⏰ {interval}:")
                logger.info(f"   Price Change: {data.get('spot_change_pct', 0):.4f}%")
                logger.info(f"   Momentum: {data.get('momentum', 'UNKNOWN')}")
                logger.info(f"   Strength: {data.get('strength_score', 0):.2f}/10")
            
            logger.info("=" * 80)
            
            # Use conservative market state determination
            if market_state == "SIDEWAYS":
                verdict = "NEUTRAL"
                confidence = 0.6
                reasoning = "Market is in sideways consolidation based on multi-timeframe analysis"
            elif market_state == "BEARISH":
                verdict = "BEARISH"
                confidence = 0.7
                reasoning = "Bearish trend detected across multiple timeframes"
            elif market_state == "BULLISH":
                verdict = "BULLISH"
                confidence = 0.7
                reasoning = "Bullish trend detected across multiple timeframes"
            else:
                verdict = "NEUTRAL"
                confidence = 0.5
                reasoning = "Insufficient data to determine market trend"
            
            # Technical indicators
            technical_analysis = {
                "oi_bias": ce_oi - pe_oi,
                "oi_pcr": oi_pcr,
                "volume_bias": snapshot_data.get('PE_VOL', 0) - snapshot_data.get('CE_VOL', 0)
            }
            
            # Timeframe analysis
            timeframe_analysis_result = {
                "trend": market_state,
                "strength": timeframe_analysis.get('analysis_summary', {}).get('avg_strength', 5.0),
                "max_price_change": timeframe_analysis.get('analysis_summary', {}).get('max_price_change', 0.0)
            }
            
            return {
                "verdict": verdict,
                "confidence": confidence,
                "reasoning": reasoning,
                "technical_analysis": technical_analysis,
                "timeframe_analysis": timeframe_analysis_result,
                "detailed_timeframe_data": timeframe_analysis.get('changes', {})
            }
            
        except Exception as e:
            logger.error(f"❌ Error in existing analysis: {e}")
            return {
                "verdict": "NEUTRAL",
                "confidence": 0.5,
                "reasoning": f"Analysis error: {str(e)}",
                "technical_analysis": {},
                "timeframe_analysis": {},
                "detailed_timeframe_data": {}
            }
            
    async def run_enhanced_bot(self):
        """Main loop with AI enhancement"""
        logger.info("🚀 Starting Enhanced GodBot with Smart AI")
        
        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🔄 ENHANCED CYCLE {cycle_count}")
                logger.info(f"{'='*60}")
                
                # 1. Fetch market data (your existing code)
                snapshot_data = await self.fetch_market_data()  # Your existing function
                
                # 2. Run enhanced analysis with AI
                analysis_result = await self.enhanced_analysis_cycle(snapshot_data)
                
                # 3. Execute trades (your existing logic)
                await self.execute_trade_logic(analysis_result)  # Your existing function
                
                # 4. Log results (your existing logging)
                self.log_analysis_results(analysis_result)  # Your existing function
                
                # Wait for next cycle (your existing timing)
                await asyncio.sleep(60)  # Adjust as per your cycle time
                
            except KeyboardInterrupt:
                logger.info("⏹️ Enhanced bot stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Enhanced cycle error: {e}")
                await asyncio.sleep(30)  # Wait on error

# NEW: Import enhanced time window handlers
from enhanced_time_window_handlers import (
    TIME_WINDOWS,
    EnhancedTimeWindowState,
    process_time_window_analysis,
    get_current_time_window,
)

# Import Candle Intelligence System
from candle_intelligence import CandleIntelligenceSystem
 
# Add this method to the appropriate class (likely EnhancedGodBotWithAI)
def get_enhancement_for_main_bot(self, main_analysis):
    """Provide enhancements for main bot analysis."""
    try:
        return {
            'candle_enhancement': True,
            'additional_confidence': 0.1,
            'pattern_support': 'NEUTRAL'
        }
    except Exception as e:
        logger.error(f"❌ Enhancement generation error: {e}")
        return {}
# =============================================================================
# FIXED: EnhancedMarketState class with CANDLE_SYSTEM_ACTIVE fix
# =============================================================================
class EnhancedMarketState:
    """Enhanced market state management with AI features and comprehensive analysis."""

    def __init__(self, symbol: str, config: Dict[str, Any]):
        self.symbol = symbol
        self.config = config
        # Core data structures
        self.market_history = deque(maxlen=150)
        self.delta_history = deque(maxlen=100)
        # State tracking
        self.data_quality_score = 10.0
        self.last_update_time = None
        self.last_spot_price = 0.0
        self.analysis_count = 0
        self.error_count = 0
        # Performance tracking
        self.processing_times = deque(maxlen=50)
        self.data_freshness_scores = deque(maxlen=20)
        # AI and technical analysis attributes
        self.current_analysis = {}
        self.technical_indicators = {}
        # FIXED: Explicitly initialize time window attributes to prevent AttributeError
        try:
            self.time_window_state = EnhancedTimeWindowState()  # Assuming imported
            self.time_window_analysis = {}  # Default empty dict
            self.current_time_window = None
            logger.info(f"🕐 Time window analysis enabled for {self.symbol}")
            # Initialize Candle Intelligence System
            try:
                from candle_intelligence import CandleIntelligenceSystem
                self.candle_system = CandleIntelligenceSystem()
                logger.info("✅ Candle Intelligence System initialized")
                self.CANDLE_SYSTEM_ACTIVE = True
            except Exception as e:
                logger.error(f"❌ Candle Intelligence System init failed: {e}")
                self.candle_system = None
                self.CANDLE_SYSTEM_ACTIVE = False
        except NameError as e:
            logger.error(f"❌ Time window initialization failed: {e} - Using fallback defaults")
            self.time_window_state = None
            self.time_window_analysis = {}  # Fallback
            self.current_time_window = 'unknown'
            logger.error(f"❌ Candle Intelligence System init failed: {e}")
            candle_system = None
            self.CANDLE_SYSTEM_ACTIVE = False  # FIXED: Make this an instance variable
        logger.info(f"🧠 Enhanced Market State initialized for {symbol}")

# =============================================================================
# ENHANCED TIME WINDOW HANDLERS - MISSING FUNCTIONS
# =============================================================================

def process_time_window_analysis(snapshot_data, time_window_state):
    """Process time window analysis."""
    try:
        current_time = datetime.now().time()
        
        # Determine current time window
        if dt_time(9, 15) <= current_time <= dt_time(10, 30):
            phase = 'OPENING_HOUR'
            action = 'HIGH_CONFIDENCE_TRADE'
        elif dt_time(10, 30) <= current_time <= dt_time(11, 30):
            phase = 'MORNING_MOMENTUM'
            action = 'MOMENTUM_TRADE'
        elif dt_time(11, 30) <= current_time <= dt_time(13, 30):
            phase = 'LUNCH_LULL'
            action = 'AVOID_TRADING'
        elif dt_time(13, 30) <= current_time <= dt_time(15, 00):
            phase = 'AFTERNOON_ACTIVITY'
            action = 'MODERATE_TRADE'
        else:
            phase = 'CLOSING_HOUR'
            action = 'MONITOR_ONLY'
        
        return {
            'phase': phase,
            'action': action,
            'trade_signal': 'MODERATE',
            'analysis': {
                'confidence_level': 'MEDIUM',
                'volume_analysis': 'NORMAL',
                'trend_strength': 'MODERATE'
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Time window analysis error: {e}")
        return {
            'phase': 'unknown',
            'action': 'MONITOR',
            'trade_signal': 'NONE',
            'analysis': {}
        }

def get_current_time_window():
    """Get current time window."""
    current_time = datetime.now().time()
    
    if dt_time(9, 15) <= current_time <= dt_time(10, 30):
        return 'OPENING_HOUR'
    elif dt_time(10, 30) <= current_time <= dt_time(11, 30):
        return 'MORNING_MOMENTUM'
    elif dt_time(11, 30) <= current_time <= dt_time(13, 30):
        return 'LUNCH_LULL'
    elif dt_time(13, 30) <= current_time <= dt_time(15, 00):
        return 'AFTERNOON_ACTIVITY'
    else:
        return 'CLOSING_HOUR'

# Add this class too
class EnhancedTimeWindowState:
    """Enhanced Time Window State management."""
    
    def __init__(self):
        self.current_window = 'unknown'
        self.window_start_time = None
        self.analysis_history = []
        
    def update_window(self, new_window):
        self.current_window = new_window
        self.window_start_time = datetime.now()

# Define TIME_WINDOWS dictionary
TIME_WINDOWS = {
    'OPENING_HOUR': {
        'direction_change_probability': 0.75,
        'volatility_expected': 'HIGH',
        'recommended_action': 'ACTIVE_TRADING'
    },
    'MORNING_MOMENTUM': {
        'direction_change_probability': 0.60,
        'volatility_expected': 'MEDIUM',
        'recommended_action': 'FOLLOW_TREND'
    },
    'LUNCH_LULL': {
        'direction_change_probability': 0.45,
        'volatility_expected': 'LOW',
        'recommended_action': 'AVOID_TRADING'
    },
    'AFTERNOON_ACTIVITY': {
        'direction_change_probability': 0.65,
        'volatility_expected': 'MEDIUM',
        'recommended_action': 'MODERATE_TRADING'
    },
    'CLOSING_HOUR': {
        'direction_change_probability': 0.80,
        'volatility_expected': 'HIGH',
        'recommended_action': 'CAREFUL_TRADING'
    },
    'unknown': {
        'direction_change_probability': 0.50,
        'volatility_expected': 'UNKNOWN',
        'recommended_action': 'MONITOR_ONLY'
    }
}

# Local ML error handler import and initialization
from ml_bot_fixes import MLBotErrorHandler
ml_error_handler = MLBotErrorHandler()

# =============================================================================
# COMPLETE WINDOWS COMPATIBILITY FIX (FIXED: Moved to top, added encoding check)
# =============================================================================

# Logging setup (move this BEFORE model loading)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("godbot_complete.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)
# Initialize Candle Intelligence System
candle_system = CandleIntelligenceSystem()
logger.info("✅ Candle Intelligence System initialized")

# =============================================================================
# ML MODEL LOADING WITH ERROR HANDLING (FIXED: Added validation)
# =============================================================================
try:
    # Attempt to load existing model (or train if missing)
    model = ml_error_handler.load_model_safely()
    scaler: Optional[Any] = None
    if model is None:
        raise RuntimeError("Model could not be loaded")
    
    # FIXED: Add model validation after loading
    if not ml_error_handler.validate_model(model):
        raise ValueError("Loaded model failed validation")
    
    logger.info("✅ ML model loaded and validated successfully")
except Exception as e:
    logger.warning(f"⚠️ Model loading failed: {e}")
    # Diagnose and auto-fix issues, then retry
    ml_error_handler.diagnose_errors()
    model = ml_error_handler.load_model_safely()
    scaler = None
    if model is None:
        logger.error("❌ Failed to load or fix ML model - Running without ML capabilities")

# Now load the model again if needed (second attempt)
try:
    # Attempt to load existing model (or train if missing)
    model = ml_error_handler.load_model_safely()
    scaler: Optional[Any] = None
    if model is None:
        raise RuntimeError("Model could not be loaded")
    # FIXED: Add model validation after loading
    if not ml_error_handler.validate_model(model):
        raise ValueError("Loaded model failed validation")
    logger.info("✅ ML model loaded and validated successfully")
except Exception as e:
    logger.warning(f"⚠️ Model loading failed: {e}")
    # Diagnose and auto-fix issues, then retry
    ml_error_handler.diagnose_errors()
    model = ml_error_handler.load_model_safely()
    scaler = None
    if model is None:
        logger.error("❌ Failed to load or fix ML model - Running without ML capabilities")

# ... rest of the script ...

# ... (rest of your script remains the same)
# =============================================================================
# ROBUST ML IMPORTS WITH PROPER ERROR HANDLING (FIXED: Added availability checks)
# =============================================================================

ML_AVAILABLE = True
TF_AVAILABLE = True
RL_AVAILABLE = True

# Scikit-learn (with availability flag)
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    logger.info("✅ Scikit-learn imported successfully")
except Exception as e:
    ML_AVAILABLE = False
    logger.warning(f"⚠️ ML libraries not available ({e}) - using dummy classes")

    class RandomForestClassifier:
        def fit(self, X, y): return self
        def predict(self, X): return [0] * len(X)
        def predict_proba(self, X): return [[0.5, 0.5]] * len(X)

    class StandardScaler:
        def fit(self, X):
            self.mean_ = np.zeros(len(X) if X and len(X) > 0 else 15)
            return self
        def transform(self, X): return np.array(X) if X else np.array([])
        def fit_transform(self, X): return self.fit(X).transform(X)

    def train_test_split(*args, **kwargs):
        if len(args) >= 2:
            return args, args, args[1], args[1]
        return [], [], [], []

# TensorFlow with Windows-specific fixes
try:
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
    os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

    import tensorflow as tf
    from tensorflow.keras.layers import Dense, Dropout, LSTM
    from tensorflow.keras.models import Sequential

    tf.config.set_visible_devices([], "GPU")
    logger.info("✅ TensorFlow imported successfully (CPU mode)")
except Exception as e:
    TF_AVAILABLE = False
    logger.warning(f"⚠️ TensorFlow not available ({e}) - running without deep learning")

# Reinforcement Learning
try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv
    import gymnasium as gym
    from gymnasium import spaces

    logger.info("✅ Reinforcement Learning libraries imported successfully")
except Exception as e:
    RL_AVAILABLE = False
    logger.warning(f"⚠️ RL libraries not available ({e}) - running without RL features")
# =============================================================================
# CONFIGURATION AND ENVIRONMENT SETUP (FIXED: Added time window config)
# =============================================================================

MODEL_PATH = "enhanced_bot_model.pkl"
load_dotenv()

# FIXED: Added time window specific config
config = {
    # Your existing config...
    'time_window_analysis': {
        'enabled': True,
        'use_research_probabilities': True,
        'golden_window_focus': True,
        'avoid_lunch_trading': True,
        'minute_level_analysis': True,
        'volume_oi_integration': True
    }
}

def safe_log(func, msg, *args, **kwargs):
    """Remove problematic characters for Windows logging."""
    try:
        import re
        emoji_pattern = re.compile(r'[\U00010000-\U0010FFFF]')
        safe_msg = emoji_pattern.sub("", str(msg))
        func(safe_msg, *args, **kwargs)
    except Exception:
        func(str(msg), *args, **kwargs)

# Log ML library status
logger.info("🔧 ML Libraries Status:")
logger.info(f"  Scikit-learn: {'✅ Available' if ML_AVAILABLE else '❌ Disabled'}")
logger.info(f"  TensorFlow: {'✅ Available' if TF_AVAILABLE else '❌ Disabled'}")
logger.info(f"  Reinforcement Learning: {'✅ Available' if RL_AVAILABLE else '❌ Disabled'}")

# =============================================================================
# BLACK-SCHOLES GREEKS IMPLEMENTATION (FIXED: Added safe division usage)
# =============================================================================
import math
from scipy.stats import norm

def black_scholes_greeks(S, K, T, sigma, option_type='call', r=0.05, q=0.0):
    """Calculate Black-Scholes Greeks for options."""
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return (0.0, 0.0)
    
    # FIXED: Use safe_division for d1 calculation
    log_term = safe_division(math.log(S / K), 1, default=0)
    rate_term = (r - q + 0.5 * sigma**2) * T
    denom = safe_division(sigma * math.sqrt(T), 1, default=1)
    
    d1 = safe_division(log_term + rate_term, denom, default=0)
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type.lower() == 'call':
        delta = math.exp(-q * T) * norm.cdf(d1)
    else:  # put
        delta = math.exp(-q * T) * (norm.cdf(d1) - 1)
    
    gamma = (math.exp(-q * T) * norm.pdf(d1)) / (S * sigma * math.sqrt(T))
    return (delta, gamma)

# ADD HERE: Missing utility functions
def safe_division(numerator, denominator, default=0):
    """Safe division to prevent zero division errors."""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ValueError):
        return default

def safe_float_conversion(value, default=0.0):
    """Safely convert value to float."""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

# =============================================================================
# CONTINUE WITH YOUR EXISTING CODE FROM HERE...
# =============================================================================

# Now your bot's top section is completely fixed and ready for time window integration!
# Proceed to integrate as per the guide in bot_integration_guide.py


# =============================================================================
# ENHANCED MARKET STATE CLASS - COMPLETE FIXED VERSION
# =============================================================================
# UPDATED EnhancedMarketState CLASS - FIXED ATTRIBUTE ERROR AND ADDED ROBUST HANDLING
class EnhancedMarketState:
    """Enhanced market state management with AI features and comprehensive analysis."""

    def __init__(self, symbol: str, config: Dict[str, Any]):
        self.symbol = symbol
        self.config = config
        # Core data structures
        self.market_history = deque(maxlen=150)
        self.delta_history = deque(maxlen=100)
        # State tracking
        self.data_quality_score = 10.0
        self.last_update_time = None
        self.last_spot_price = 0.0
        self.analysis_count = 0
        self.error_count = 0
        # Performance tracking
        self.processing_times = deque(maxlen=50)
        self.data_freshness_scores = deque(maxlen=20)
        # AI and technical analysis attributes
        self.current_analysis = {}
        self.technical_indicators = {}
        # FIXED: Explicitly initialize time window attributes to prevent AttributeError
        try:
            self.time_window_state = EnhancedTimeWindowState()
            self.time_window_analysis = {}
            self.current_time_window = None
            logger.info(f"🕐 Time window analysis enabled for {self.symbol}")
            
            # FIXED: Make candle_system an instance variable
            self.candle_system = CandleIntelligenceSystem()
            logger.info("✅ Candle Intelligence System initialized")
            self.CANDLE_SYSTEM_ACTIVE = True
        except Exception as e:  # Catch any exception, not just NameError
            logger.error(f"❌ Initialization failed: {e} - Using fallback defaults")
            self.time_window_state = None
            self.time_window_analysis = {}
            self.current_time_window = 'unknown'
            
            # FIXED: Set candle_system to None on error
            self.candle_system = None
            self.CANDLE_SYSTEM_ACTIVE = False
            logger.error(f"❌ Candle Intelligence System init failed: {e}")
    
    def _get_overall_trend(self):
        if len(self.market_history) < 5:
            return "UNKNOWN"
        
        # Get last 5 snapshots
        recent = list(self.market_history)[-5:]
        prices = [s.get('underlying_value', 0) for s in recent]
        
        # Calculate trend
        if prices[-1] > prices[0] * 1.002:  # 0.2% increase
            return "BULLISH"
        elif prices[-1] < prices[0] * 0.998:  # 0.2% decrease
            return "BEARISH"
        else:
            return "SIDEWAYS"
    
    def update(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update market state with new snapshot and return analysis."""
        import time
        start_time = time.time()
        try:
            if 'timestamp' not in snapshot_data:
                snapshot_data['timestamp'] = datetime.now().isoformat()
            # Update current state
            self.last_spot_price = snapshot_data.get('underlying_value', self.last_spot_price)
            self.last_update_time = datetime.now()
            # Add to history
            self.market_history.append(snapshot_data)
            # Calculate and store deltas if we have previous data
            if len(self.market_history) >= 2:
                self._calculate_deltas()
            # FIXED: Integrate time window analysis with robust error handling
            try:
                if self.time_window_state is not None:
                    time_window_result = process_time_window_analysis(snapshot_data, self.time_window_state)
                    self.time_window_analysis = time_window_result or {}  # Set or fallback to empty
                    self.current_time_window = time_window_result.get('phase', 'unknown')
                    # Log time window intelligence
                    window_action = time_window_result.get('action', 'NONE')
                    trade_signal = time_window_result.get('trade_signal', 'NONE')
                    logger.info(f"🕐 Time Window: {self.current_time_window}")
                    logger.info(f"📊 Window Action: {window_action} | Signal: {trade_signal}")
                    # Add time window data to snapshot
                    snapshot_data['time_window_analysis'] = time_window_result
                    snapshot_data['current_time_window'] = self.current_time_window
                else:
                    logger.warning("⚠️ Time window state not available - Skipping time window analysis")
                    self.time_window_analysis = {}  # Ensure set
                    self.current_time_window = 'unknown'
            except Exception as e:
                logger.error(f"❌ Time window analysis failed: {e}")
                self.time_window_analysis = {}  # FIXED: Set default on any error
                self.current_time_window = 'unknown'
            # Update performance metrics
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            # Update analysis count
            self.analysis_count += 1
            # Calculate data quality score
            self._update_data_quality_score(snapshot_data)
            logger.info(f"🔄 Market state updated for {self.symbol}")
            logger.info(f"📊 History: {len(self.market_history)} snapshots, Quality: {self.data_quality_score}/10")
            return snapshot_data
        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ Error updating market state for {self.symbol}: {e}")
            # FIXED: Set default time window on error to prevent AttributeError
            self.time_window_analysis = {}
            return {}
    
    # ... (keep the rest of the class methods as is from your original file)
    #     
    def _calculate_deltas(self) -> None:
        """Calculate deltas between current and previous snapshot."""
        try:
            current = list(self.market_history)[-1]
            previous = list(self.market_history)[-2]
            
            deltas = {}
            
            # Calculate all delta values
            for key in ['CE_OI', 'PE_OI', 'CE_VOL', 'PE_VOL', 'underlying_value', 'OI_PCR', 'VOL_PCR']:
                current_val = current.get(key, 0)
                previous_val = previous.get(key, 0)
                delta = current_val - previous_val
                delta_pct = (delta / previous_val * 100) if previous_val != 0 else 0
                
                deltas[f'delta_{key}'] = delta
                deltas[f'delta_{key}_pct'] = delta_pct
            
            # Add timestamp
            deltas['timestamp'] = datetime.now().isoformat()
            
            # Store in delta history
            self.delta_history.append(deltas)
            
        except Exception as e:
            logger.error(f"❌ Error calculating deltas: {e}")
    
    def _update_data_quality_score(self, snapshot_data: Dict[str, Any]) -> None:
        """Update data quality score based on completeness and freshness."""
        quality_score = 10.0
        
        # Check data completeness
        required_fields = ['underlying_value', 'CE_OI', 'PE_OI', 'CE_VOL', 'PE_VOL', 'OI_PCR']
        missing_fields = [field for field in required_fields if field not in snapshot_data or snapshot_data[field] is None]
        
        if missing_fields:
            quality_score -= len(missing_fields) * 1.5
            
        # Check for zero values (suspicious)
        zero_fields = [field for field in required_fields if snapshot_data.get(field, 0) == 0]
        if zero_fields:
            quality_score -= len(zero_fields) * 0.5
        
        # Check data freshness
        if self.last_update_time:
            time_since_update = (datetime.now() - self.last_update_time).total_seconds()
            if time_since_update > 300:  # More than 5 minutes
                quality_score -= 2.0
        
        self.data_quality_score = max(0.0, quality_score)
        self.data_freshness_scores.append(self.data_quality_score)
    
    def get_ai_features(self) -> Dict[str, float]:
        """Generate EXACTLY 15 AI features for prediction."""
        if len(self.market_history) < 2:
            return {f'feature_{i}': 0.0 for i in range(15)}

        current = list(self.market_history)[-1]
        previous = list(self.market_history)[-2]

        features = {
            'rsi_value': 50.0,
            'oi_acceleration': float(current.get('CE_OI', 0) - current.get('PE_OI', 0)),
            'max_pain_gravity': 0.0,
            'fear_gauge': float(current.get('OI_PCR', 1.0)),
            'historical_trend': float(current.get('underlying_value', 0) - previous.get('underlying_value', 0)),
            'underlying_value': float(current.get('underlying_value', 0)) / 1000,
            'CE_OI': float(current.get('CE_OI', 0)) / 1000000,
            'PE_OI': float(current.get('PE_OI', 0)) / 1000000,
            'OI_PCR': float(current.get('OI_PCR', 0)),
            'VOL_PCR': float(current.get('VOL_PCR', 0)),
            'iv_skew': self._calculate_iv_skew(current),
            'volume_bias': float(current.get('PE_VOL', 0) - current.get('CE_VOL', 0)) / 1000000,
            'price_momentum': float(current.get('underlying_value', 0) - previous.get('underlying_value', 0)),
            'oi_change_ratio': float(current.get('CE_OI', 0) + current.get('PE_OI', 0)) / max(1.0, float(previous.get('CE_OI', 0) + previous.get('PE_OI', 0))),
            'atr_normalized': float(self.get_atr()) / 100
        }
        return features

    def _calculate_iv_skew(self, current: Dict) -> float:
        """Calculate implied volatility skew."""
        try:
            strike_data = current.get('strike_data', {})
            if not strike_data:
                return 0.0
            
            ivs = [data.get('CE_IV', 0) + data.get('PE_IV', 0) for data in strike_data.values()]
            if len(ivs) < 2:
                return 0.0
            
            return (max(ivs) - min(ivs)) / max(max(ivs), 1)
        except Exception:
            return 0.0
    
    def _calculate_momentum_score(self) -> float:
        """Calculate momentum score from recent price changes."""
        if len(self.market_history) < 3:
            return 0.0
        
        recent_prices = [h.get('underlying_value', 0) for h in list(self.market_history)[-3:]]
        changes = [recent_prices[i] - recent_prices[i-1] for i in range(1, len(recent_prices))]
        
        if not changes:
            return 0.0
        
        avg_change = sum(changes) / len(changes)
        return max(-10.0, min(10.0, avg_change))
    
    def get_atr(self) -> float:
        """Calculate Average True Range for volatility."""
        if len(self.market_history) < 2:
            return 20.0  # Default ATR
        
        price_changes = []
        history_list = list(self.market_history)
        
        for i in range(1, min(14, len(history_list))):
            current_price = history_list[-i].get('underlying_value', 0)
            prev_price = history_list[-i-1].get('underlying_value', current_price)
            price_changes.append(abs(current_price - prev_price))
        
        return sum(price_changes) / len(price_changes) if price_changes else 20.0
    
    def safe_get_recent_history(self, count: int) -> List[Dict]:
        """Safely get recent history converting deque to list."""
        try:
            history_list = list(self.market_history)
            return history_list[-count:] if len(history_list) >= count else history_list
        except Exception as e:
            logger.warning(f"⚠️ Error getting recent history: {e}")
            return []
    
    def safe_get_history_slice(self, start_idx: int, end_idx: int = None) -> List[Dict]:
        """Safely get history slice converting deque to list."""
        try:
            history_list = list(self.market_history)
            if end_idx is None:
                return history_list[start_idx:]
            else:
                return history_list[start_idx:end_idx]
        except Exception as e:
            logger.warning(f"⚠️ Error getting history slice: {e}")
            return []
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current market state summary."""
        if not self.market_history:
            return {"error": "No market data available"}
        
        current_snapshot = list(self.market_history)[-1]
        
        return {
            "symbol": self.symbol,
            "current_spot": self.last_spot_price,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "data_quality": self.data_quality_score,
            "total_snapshots": len(self.market_history),
            "total_deltas": len(self.delta_history),
            "analysis_count": self.analysis_count,
            "error_count": self.error_count,
            "current_snapshot": current_snapshot
        }
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive market state status."""
        return {
            "symbol": self.symbol,
            "data_quality": self.data_quality_score,
            "snapshots": len(self.market_history),
            "last_update": self.last_update_time,
            "atr": self.get_atr(),
            "current_spot": self.last_spot_price,
            "health_status": self.self_diagnose()
        }
    
    def self_diagnose(self) -> str:
        """Self-diagnostic check."""
        issues = []
        
        # Check data availability
        if len(self.market_history) == 0:
            issues.append("NO_DATA")
        elif len(self.market_history) < 5:
            issues.append("INSUFFICIENT_DATA")
        
        # Check data quality
        if self.data_quality_score < 7.0:
            issues.append("LOW_QUALITY")
        
        # Check error rate
        if self.error_count > 0 and self.analysis_count > 0:
            error_rate = (self.error_count / self.analysis_count) * 100
            if error_rate > 10:
                issues.append("HIGH_ERROR_RATE")
        
        if not issues:
            return "HEALTHY"
        elif len(issues) == 1:
            return f"WARNING_{issues[0]}"
        else:
            return f"CRITICAL_{'_'.join(issues[:2])}"
    
    def save_enhanced_historical_data(self):
        """Save historical data for session continuity."""
        try:
            data = {
                'market_history': list(self.market_history),
                'delta_history': list(self.delta_history),
                'last_spot_price': self.last_spot_price,
                'data_quality_score': self.data_quality_score,
                'analysis_count': self.analysis_count,
                'technical_indicators': self.technical_indicators,
                'current_analysis': self.current_analysis
            }
            
            filename = f"{self.symbol}_enhanced_historical_data.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
                
            logger.info(f"💾 Enhanced historical data saved for {self.symbol} ({len(self.market_history)} entries)")
            
        except Exception as e:
            logger.error(f"❌ Error saving enhanced historical data: {e}")
    
    # Add this to your EnhancedMarketState class (around line 1200):

    def load_enhanced_historical_data(self):
        """Load historical data from previous session."""
        try:
            filename = f"{self.symbol}_enhanced_historical_data.json"
            if not os.path.exists(filename):
                logger.info(f"📂 No saved data found for {self.symbol}")
                return False

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Restore data structures
            self.market_history = deque(data.get('market_history', []), maxlen=150)
            self.delta_history = deque(data.get('delta_history', []), maxlen=100)
            self.last_spot_price = data.get('last_spot_price', 0.0)
            self.data_quality_score = data.get('data_quality_score', 10.0)
            self.analysis_count = data.get('analysis_count', 0)
            
            # Restore technical indicators if they exist
            if hasattr(self, 'technical_indicators'):
                self.technical_indicators = data.get('technical_indicators', {})
            
            # Restore current analysis if it exists
            if hasattr(self, 'current_analysis'):
                self.current_analysis = data.get('current_analysis', {})

            logger.info(f"📂 Historical data loaded for {self.symbol} ({len(self.market_history)} entries)")
            return True

        except Exception as e:
            logger.error(f"❌ Error loading historical data: {e}")
            return False

    def _ensure_attributes_exist(self):
        """Ensure all required attributes exist with default values."""
        if not hasattr(self, 'technical_indicators'):
            self.technical_indicators = {}
        if not hasattr(self, 'current_analysis'):
            self.current_analysis = {}
        if not hasattr(self, 'last_update_time'):
            self.last_update_time = None
        if not hasattr(self, 'error_count'):
            self.error_count = 0
        if not hasattr(self, 'processing_times'):
            self.processing_times = deque(maxlen=20)
        if not hasattr(self, 'data_freshness_scores'):
            self.data_freshness_scores = deque(maxlen=20)

    # -- Add here --
# =============================================================================
# ENHANCED MULTI-TIMEFRAME ANALYSIS CLASS - COMPLETE FIXED VERSION
# =============================================================================
from collections import deque
from datetime import datetime, time as dt_time
from typing import Dict, Any, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# FIXED: MultiTimeframeAnalyzer class with proper data storage and retrieval
# =============================================================================
class MultiTimeframeAnalyzer:
    """Advanced multi-timeframe analysis for 15 specific intervals: 3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90 minutes.
    Provides deep market insights across different time horizons with progressive analysis."""
    
    def __init__(self, intervals: List[int] = [3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90]):
        self.intervals = intervals  # 15 custom timeframes
        self.analysis_history = deque(maxlen=100)
        self.last_analysis_results = {}  # Store the last analysis results
        logger.info("🔍 Multi-Timeframe Analyzer initialized with 15 intervals: %s", intervals)
    
    def analyze_timeframe_changes(self, market_history: deque) -> Dict[str, Any]:
        """Analyze changes across multiple timeframes."""
        if len(market_history) < 2:
            return {'status': 'INSUFFICIENT_DATA', 'market_state': 'UNKNOWN', 'changes': {}, 'analysis_summary': {}}
        
        # Convert deque to list for easier manipulation
        history_list = list(market_history)
        current_time = datetime.now()
        
        # Initialize results dictionary
        timeframe_data = {}
        
        # Track market state counts
        bearish_count = 0
        bullish_count = 0
        sideways_count = 0
        
        # Track max price change and average strength
        max_price_change = 0.0
        total_strength = 0.0
        valid_timeframes = 0
        
        logger.info(f"📊 Starting 15-Timeframe Progressive Analysis at {current_time.strftime('%H:%M:%S')}")
        logger.info("=" * 80)
        
        # Analyze each timeframe
        for interval in self.intervals:
            # Calculate how many snapshots we need for this interval
            required_snapshots = interval
            
            # Check if we have enough data
            if len(history_list) < required_snapshots:
                logger.info(f"⏰ {interval}-MINUTE ANALYSIS: SKIPPED (insufficient data)")
                # Still add an entry but mark as incomplete
                timeframe_data[interval] = {
                    'spot_change': 0.0,
                    'spot_change_pct': 0.0,
                    'ce_oi_change': 0,
                    'ce_oi_change_pct': 0.0,  # FIXED: Added missing key
                    'pe_oi_change': 0,
                    'pe_oi_change_pct': 0.0,  # FIXED: Added missing key
                    'momentum': 'INSUFFICIENT_DATA',
                    'strength_score': 0.0,
                    'status': 'INSUFFICIENT_DATA'
                }
                continue
            
            # Get the snapshots for this interval
            start_idx = -required_snapshots
            end_idx = -1 if required_snapshots > 1 else None
            interval_snapshots = history_list[start_idx:end_idx]
            
            if not interval_snapshots or len(interval_snapshots) < 2:
                logger.info(f"⏰ {interval}-MINUTE ANALYSIS: SKIPPED (invalid data)")
                timeframe_data[interval] = {
                    'spot_change': 0.0,
                    'spot_change_pct': 0.0,
                    'ce_oi_change': 0,
                    'ce_oi_change_pct': 0.0,  # FIXED: Added missing key
                    'pe_oi_change': 0,
                    'pe_oi_change_pct': 0.0,  # FIXED: Added missing key
                    'momentum': 'INVALID_DATA',
                    'strength_score': 0.0,
                    'status': 'INVALID_DATA'
                }
                continue
            
            # Get start and end snapshots
            start_snapshot = interval_snapshots[0]
            end_snapshot = interval_snapshots[-1]
            
            # Calculate price change
            start_price = start_snapshot.get('underlying_value', 0)
            end_price = end_snapshot.get('underlying_value', 0)
            spot_change = end_price - start_price
            spot_change_pct = (spot_change / start_price * 100) if start_price > 0 else 0
            
            # Calculate OI changes
            start_ce_oi = start_snapshot.get('CE_OI', 0)
            end_ce_oi = end_snapshot.get('CE_OI', 0)
            ce_oi_change = end_ce_oi - start_ce_oi
            # FIXED: Calculate CE OI percentage change
            ce_oi_change_pct = (ce_oi_change / start_ce_oi * 100) if start_ce_oi > 0 else 0
            
            start_pe_oi = start_snapshot.get('PE_OI', 0)
            end_pe_oi = end_snapshot.get('PE_OI', 0)
            pe_oi_change = end_pe_oi - start_pe_oi
            # FIXED: Calculate PE OI percentage change
            pe_oi_change_pct = (pe_oi_change / start_pe_oi * 100) if start_pe_oi > 0 else 0
            
            # Determine momentum based on price and OI changes
            if spot_change_pct > 0.05 and ce_oi_change > pe_oi_change:
                momentum = "BULLISH"
                bullish_count += 1
            elif spot_change_pct < -0.05 and pe_oi_change > ce_oi_change:
                momentum = "BEARISH"
                bearish_count += 1
            else:
                momentum = "SIDEWAYS"
                sideways_count += 1
            
            # Calculate strength score (0-10)
            strength_score = min(10.0, abs(spot_change_pct) * 100)
            
            # Track max price change
            max_price_change = max(max_price_change, abs(spot_change_pct))
            total_strength += strength_score
            valid_timeframes += 1
            
            # Store the analysis results - FIXED: Added percentage changes
            timeframe_data[interval] = {
                'spot_change': spot_change,
                'spot_change_pct': spot_change_pct,
                'ce_oi_change': ce_oi_change,
                'ce_oi_change_pct': ce_oi_change_pct,  # FIXED: Added missing key
                'pe_oi_change': pe_oi_change,
                'pe_oi_change_pct': pe_oi_change_pct,  # FIXED: Added missing key
                'momentum': momentum,
                'strength_score': strength_score,
                'status': 'COMPLETED'
            }
            
            # Log the analysis - FIXED: Added percentage changes to logging
            logger.info(f"⏰ {interval}-MINUTE ANALYSIS:")
            logger.info(f"  💹 Price: ₹{start_price:.2f} → ₹{end_price:.2f} (Change: {spot_change:.2f}, {spot_change_pct:+.4f}%)")
            logger.info(f"  📈 CE OI: {start_ce_oi:,.0f} → {end_ce_oi:,.0f} (Change: {ce_oi_change:,.0f}, {ce_oi_change_pct:+.2f}%)")
            logger.info(f"  📉 PE OI: {start_pe_oi:,.0f} → {end_pe_oi:,.0f} (Change: {pe_oi_change:,.0f}, {pe_oi_change_pct:+.2f}%)")
            logger.info(f"  🚀 Momentum: {momentum} | Strength: {strength_score:.2f}/10")
        
        # Determine overall market state
        if bullish_count > bearish_count and bullish_count > sideways_count:
            market_state = "BULLISH"
        elif bearish_count > bullish_count and bearish_count > sideways_count:
            market_state = "BEARISH"
        else:
            market_state = "SIDEWAYS"
        
        # Calculate average strength
        avg_strength = total_strength / valid_timeframes if valid_timeframes > 0 else 0
        
        # Create analysis summary
        analysis_summary = {
            'bearish_count': bearish_count,
            'bullish_count': bullish_count,
            'sideways_count': sideways_count,
            'avg_strength': avg_strength,
            'max_price_change': max_price_change
        }
        
        logger.info(f"🎯 CONSERVATIVE MARKET STATE: {market_state}")
        logger.info(f"📊 Analysis Summary: Bearish={bearish_count}, Bullish={bullish_count}, Sideways={sideways_count}")
        logger.info(f"📈 Max Price Change: {max_price_change:.4f}%, Avg Strength: {avg_strength:.2f}")
        logger.info("✅ Timeframe analysis completed")
        
        # FIXED: Store the analysis results for later retrieval
        result = {
            'status': 'COMPLETED',
            'market_state': market_state,
            'changes': timeframe_data,  # This is the key fix - storing the data properly
            'analysis_summary': analysis_summary
        }
        
        # Store the last analysis results
        self.last_analysis_results = result
        
        return result
# =============================================================================
# FIXED: display_15_timeframe_table function
# =============================================================================
def display_15_timeframe_table(timeframe_analysis: Dict[str, Any]) -> None:
    """Display the 15-timeframe analysis results in a table format."""
    print("\n📊 15-TIMEFRAME ANALYSIS TABLE")
    print("=" * 120)
    
    # Extract the timeframe data
    timeframe_data = timeframe_analysis.get('changes', {})
    
    # If no changes data, try to get it from the MultiTimeframeAnalyzer
    if not timeframe_data and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
        analyzer = MultiTimeframeAnalyzer()
        if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
            timeframe_data = analyzer.last_analysis_results.get('changes', {})
    
    # Count completed timeframes
    completed_count = sum(1 for data in timeframe_data.values() if data.get('status') == 'COMPLETED')
    
    # Print the table header
    print(f"{'TF':<5} {'Status':<12} {'Price Δ':<9} {'%Δ':<9} {'CE OI Δ':<12} {'PE OI Δ':<12} {'Momentum':<12} {'Strength':<10}")
    print("-" * 120)
    
    # List of all timeframes we want to display
    all_timeframes = [3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90]
    
    for timeframe in all_timeframes:
        # Get the data for this timeframe
        data = timeframe_data.get(timeframe, {})
        
        if data and data.get('status') == 'COMPLETED':
            # Extract values with defaults
            price_delta = data.get('spot_change', 0.0)
            price_pct = data.get('spot_change_pct', 0.0)
            ce_oi_delta = data.get('ce_oi_change', 0)
            pe_oi_delta = data.get('pe_oi_change', 0)
            momentum = data.get('momentum', 'UNKNOWN')
            strength = data.get('strength_score', 0.0)
            
            # Format momentum with icon
            momentum_icon = "🟢" if momentum == "BULLISH" else "🔴" if momentum == "BEARISH" else "🟡"
            
            print(f"{timeframe:<5} ✅ COMPLETED | {price_delta:+6.2f} | {price_pct:+6.3f}% | "
                  f"{ce_oi_delta:+9,} | {pe_oi_delta:+9,} | {momentum_icon} {momentum:<8} | {strength:6.2f}/10")
        else:
            print(f"{timeframe:<5} ⏳ PENDING    | {'--':>7} | {'--':>8} | {'--':>11} | {'--':>11} | --           | --")
    
    print("-" * 120)
    
    # Log summary
    logger.info(f"📊 15-Timeframe Analysis Summary: {completed_count} Completed, {15-completed_count} Pending")
    
    if completed_count == 0:
        logger.warning(f"⚠️  No timeframes completed — waiting for sufficient market data")

# =============================================================================
# FIXED: Enhanced market state update method
# =============================================================================
def update_market_state_with_timeframe(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update market state with new snapshot and return analysis with timeframe data."""
    import time
    start_time = time.time()
    try:
        if 'timestamp' not in snapshot_data:
            snapshot_data['timestamp'] = datetime.now().isoformat()
        
        # Update current state
        self.last_spot_price = snapshot_data.get('underlying_value', self.last_spot_price)
        self.last_update_time = datetime.now()
        
        # Add to history
        self.market_history.append(snapshot_data)
        
        # Calculate and store deltas if we have previous data
        if len(self.market_history) >= 2:
            self._calculate_deltas()
        
        # FIXED: Integrate timeframe analysis with proper data storage
        timeframe_analyzer = MultiTimeframeAnalyzer()
        timeframe_result = timeframe_analyzer.analyze_timeframe_changes(self.market_history)
        
        # Store the timeframe analysis in current_analysis
        if not hasattr(self, 'current_analysis'):
            self.current_analysis = {}
        
        # FIXED: Store the timeframe analysis properly
        self.current_analysis['timeframe_analysis'] = timeframe_result
        
        # Update performance metrics
        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)
        
        # Update analysis count
        self.analysis_count += 1
        
        # Calculate data quality score
        self._update_data_quality_score(snapshot_data)
        
        logger.info(f"🔄 Market state updated for {self.symbol}")
        logger.info(f"📊 History: {len(self.market_history)} snapshots, Quality: {self.data_quality_score}/10")
        
        # Return the updated snapshot with timeframe analysis
        return snapshot_data
        
    except Exception as e:
        self.error_count += 1
        logger.error(f"❌ Error updating market state for {self.symbol}: {e}")
        return {}

# =============================================================================
# FIXED: Function to properly display 15-timeframe data
# =============================================================================
def print_all_15_timeframes_data(market_state: 'EnhancedMarketState') -> None:
    """Print ALL 15 timeframes data in organized format with complete details."""
    
    print("\n" + "="*140)
    print("🕐 COMPLETE 15-TIMEFRAME DATA STORAGE ANALYSIS")
    print("="*140)
    
    # FIXED: Get timeframe data properly
    timeframe_analysis = {}
    
    # Try to get timeframe analysis from current_analysis
    if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
        timeframe_analysis = market_state.current_analysis['timeframe_analysis']
    
    # If still empty, try to get it from the MultiTimeframeAnalyzer
    if not timeframe_analysis and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
        analyzer = MultiTimeframeAnalyzer()
        if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
            timeframe_analysis = analyzer.last_analysis_results
    
    if not timeframe_analysis:
        print("⚠️  Timeframe analysis not available yet.")
        print(f"📊 Current snapshots: {len(market_state.market_history)}")
        print("🔄 Building data foundation...")
        print("="*140)
        return
    
    # Extract the timeframe data
    timeframe_data = timeframe_analysis.get('changes', {})
    
    print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total Snapshots: {len(market_state.market_history)}")
    
    # Count completed timeframes
    completed_count = sum(1 for data in timeframe_data.values() if data.get('status') == 'COMPLETED')
    print(f"🎯 Timeframes Active: {completed_count}/15")
    
    # Define all 15 expected timeframes in order
    all_timeframes = [3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90]
    
    # SECTION 1: COMPREHENSIVE OVERVIEW TABLE
    print(f"\n📋 15-TIMEFRAME OVERVIEW TABLE:")
    print("-" * 140)
    print(f"{'Timeframe':>10} | {'Status':>12} | {'Price Δ':>8} | {'Price %':>8} | {'CE OI Δ':>10} | {'PE OI Δ':>10} | {'Momentum':>15} | {'Strength':>8}")
    print("-" * 140)
    
    for timeframe in all_timeframes:
        # Get the data for this timeframe
        data = timeframe_data.get(timeframe, {})
        
        if data and data.get('status') == 'COMPLETED':
            # Extract values with defaults
            price_delta = data.get('spot_change', 0.0)
            price_pct = data.get('spot_change_pct', 0.0)
            ce_oi = data.get('ce_oi_change', 0)
            pe_oi = data.get('pe_oi_change', 0)
            momentum = data.get('momentum', 'N/A')
            strength = data.get('strength_score', 0)
            status = "✅ COMPLETED"
        else:
            # Default values for pending timeframes
            price_delta = 0.0
            price_pct = 0.0
            ce_oi = 0
            pe_oi = 0
            momentum = 'WAITING'
            strength = 0.0
            status = "⏳ PENDING"
            
        print(f"{str(timeframe)+'min':>10} | {status:>12} | {price_delta:+8.2f} | {price_pct:+7.3f}% | {ce_oi:+10,} | {pe_oi:+10,} | {momentum:>15} | {strength:>6.2f}/10")
    
    print("-" * 140)
    
    # SECTION 2: PENDING TIMEFRAMES
    pending_timeframes = [tf for tf in all_timeframes if tf not in timeframe_data or timeframe_data.get(tf, {}).get('status') != 'COMPLETED']
    
    if pending_timeframes:
        print(f"\n⏳ PENDING TIMEFRAMES ({len(pending_timeframes)}/15):")
        print("─" * 80)
        for tf in pending_timeframes:
            # Calculate how many more snapshots are needed
            snapshots_needed = tf - len(market_state.market_history)
            if snapshots_needed < 0:
                needed_str = "Ready (data available)"
            else:
                needed_str = f"Need +{snapshots_needed} more snapshots"
            print(f"      {tf}min: {needed_str}")
        print("─" * 80)
    
    # SECTION 3: SUMMARY STATISTICS
    print(f"\n📊 ANALYSIS SUMMARY:")
    print("─" * 80)
    print(f"  🎯 Active Timeframes: {completed_count}/15 ({completed_count/15*100:.1f}%)")
    print(f"  📈 Total Snapshots: {len(market_state.market_history)}")
    print(f"  ⏰ Analysis Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  🎯 Data Quality: {market_state.data_quality_score:.1f}/10")
    print("="*140)
    print("✅ 15-TIMEFRAME DATA DISPLAY COMPLETE")
    print("="*140)
# =============================================================================
# 9:30 AM RECOMMENDATION SYSTEM
# =============================================================================

def get_market_recommendation(market_state: 'EnhancedMarketState', cycle_number: int) -> Dict[str, Any]:
    """Generate recommendations based on market opening strategy - First recommendation at 9:30 AM."""
    
    snapshots_count = len(market_state.market_history)
    current_time = datetime.now().time()
    
    # Check if it's market opening period (9:15 - 9:30)
    is_opening_period = dt_time(9, 15) <= current_time <= dt_time(9, 30)
    
    if snapshots_count < 15:  # Before 15 snapshots (9:30 AM target)
        if snapshots_count < 3:
            return {
                "status": "BUILDING_DATA",
                "recommendation": "🔄 Collecting market data for analysis...",
                "confidence": "NONE", 
                "reason": f"Need {3 - snapshots_count} more snapshots for basic analysis",
                "timeframes_ready": 0,
                "next_milestone": "3 snapshots for 3-minute analysis"
            }
        else:
            available_tf = len(market_state.current_analysis.get('timeframe_analysis', {})) if hasattr(market_state, 'current_analysis') else 0
            return {
                "status": "PRE_RECOMMENDATION",
                "recommendation": "⏳ Building foundation for 9:30 AM first recommendation",
                "confidence": "BUILDING",
                "reason": f"Snapshots: {snapshots_count}/15 | Active timeframes: {available_tf}",
                "timeframes_ready": available_tf,
                "next_milestone": "15 snapshots for first recommendation"
            }
    
    # FIRST RECOMMENDATION AT 9:30 AM (15th snapshot)
    elif snapshots_count == 15:
        return generate_first_trading_recommendation(market_state)
    
    # CONTINUOUS TRACKING (Every minute after 9:30)
    else:
        return generate_tracking_recommendation(market_state, cycle_number)

def generate_first_trading_recommendation(market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """Generate the first trading recommendation at 9:30 AM (15th snapshot)."""
    
    tf_analysis = market_state.current_analysis.get('timeframe_analysis', {})
    
    # Analyze available timeframes
    active_timeframes = len(tf_analysis)
    bullish_signals = sum(1 for data in tf_analysis.values() if "BULLISH" in data.get("momentum", ""))
    bearish_signals = sum(1 for data in tf_analysis.values() if "BEARISH" in data.get("momentum", ""))
    strong_signals = sum(1 for data in tf_analysis.values() if "STRONG" in data.get("momentum", ""))
    
    # Calculate average strength
    avg_strength = sum(data.get("strength_score", 0) for data in tf_analysis.values()) / len(tf_analysis) if tf_analysis else 0
    
    # Generate first recommendation
    if bullish_signals > bearish_signals * 1.5:
        recommendation = f"🟢 FIRST RECOMMENDATION (9:30 AM): BULLISH BIAS CONFIRMED"
        confidence = "HIGH" if bullish_signals >= 3 and avg_strength > 6.0 else "MEDIUM"
        action = "LOOK_FOR_LONG_OPPORTUNITIES"
        bias = "BULLISH"
    elif bearish_signals > bullish_signals * 1.5:
        recommendation = f"🔴 FIRST RECOMMENDATION (9:30 AM): BEARISH BIAS CONFIRMED"
        confidence = "HIGH" if bearish_signals >= 3 and avg_strength > 6.0 else "MEDIUM"
        action = "LOOK_FOR_SHORT_OPPORTUNITIES"
        bias = "BEARISH"
    else:
        recommendation = f"🟡 FIRST RECOMMENDATION (9:30 AM): NEUTRAL - WAIT FOR CLARITY"
        confidence = "MEDIUM"
        action = "MONITOR_FOR_BREAKOUT_DIRECTION"
        bias = "NEUTRAL"
    
    return {
        "status": "FIRST_RECOMMENDATION_ISSUED",
        "recommendation": recommendation,
        "confidence": confidence,
        "action": action,
        "bias": bias,
        "timeframes_analyzed": active_timeframes,
        "bullish_signals": bullish_signals,
        "bearish_signals": bearish_signals,
        "strong_signals": strong_signals,
        "average_strength": round(avg_strength, 2),
        "reason": f"15-minute foundation complete at 9:30 AM - {active_timeframes}/15 timeframes active",
        "tracking_mode": "NOW_SWITCHING_TO_1_MINUTE_TRACKING"
    }

def generate_tracking_recommendation(market_state: 'EnhancedMarketState', cycle: int) -> Dict[str, Any]:
    """Generate tracking recommendations every minute after 9:30 AM."""
    
    tf_analysis = market_state.current_analysis.get('timeframe_analysis', {})
    
    # Track changes in active timeframes
    active_count = len(tf_analysis)
    strong_signals = sum(1 for data in tf_analysis.values() if "STRONG" in data.get("momentum", ""))
    bullish_count = sum(1 for data in tf_analysis.values() if "BULLISH" in data.get("momentum", ""))
    bearish_count = sum(1 for data in tf_analysis.values() if "BEARISH" in data.get("momentum", ""))
    
    # Calculate signal strength
    total_strength = sum(data.get("strength_score", 0) for data in tf_analysis.values())
    avg_strength = total_strength / active_count if active_count > 0 else 0
    
    # Generate tracking recommendation
    if strong_signals >= 5 and avg_strength > 7.5:
        return {
            "status": "CRITICAL_SIGNAL_TRACKING",
            "recommendation": f"🚨 CRITICAL SIGNAL: {strong_signals} strong timeframes | Avg strength: {avg_strength:.1f}/10",
            "confidence": "VERY_HIGH",
            "action": "EXECUTE_PREMIUM_TRADE_SIGNAL",
            "signal_quality": "PREMIUM"
        }
    elif strong_signals >= 3 and avg_strength > 6.5:
        return {
            "status": "STRONG_SIGNAL_TRACKING",
            "recommendation": f"🚀 STRONG SIGNAL: {strong_signals} strong timeframes detected",
            "confidence": "HIGH",
            "action": "EXECUTE_TRADE_SIGNAL",
            "signal_quality": "STRONG"
        }
    elif active_count >= 10:
        trend = "BULLISH" if bullish_count > bearish_count else "BEARISH" if bearish_count > bullish_count else "SIDEWAYS"
        return {
            "status": "COMPREHENSIVE_TRACKING",
            "recommendation": f"📊 TRACKING: {active_count}/15 timeframes | Trend: {trend}",
            "confidence": "MEDIUM_HIGH",
            "action": "MONITOR_FOR_CONFLUENCE",
            "signal_quality": "GOOD"
        }
    elif active_count >= 5:
        return {
            "status": "BUILDING_TRACKING",
            "recommendation": f"⏳ BUILDING: {active_count}/15 timeframes active",
            "confidence": "MEDIUM",
            "action": "CONTINUE_BUILDING_ANALYSIS",
            "signal_quality": "DEVELOPING"
        }
    else:
        return {
            "status": "BASIC_TRACKING",
            "recommendation": f"🔄 BASIC: {active_count}/15 timeframes building",
            "confidence": "LOW",
            "action": "WAIT_FOR_MORE_DATA",
            "signal_quality": "INSUFFICIENT"
        }

def print_candle_intelligence_output(result: dict):
    print("\n🕯️ 5-Minute Candle Intelligence Output 🕯️")
    print("="*80)
    if result.get('status') == 'CANDLE_COMPLETED':
        candle_data = result.get('candle_data', {})
        pattern = result.get('pattern_analysis', {})
        trade_rec = result.get('trade_recommendation', {})
        volume_intel = result.get('volume_intelligence', {})
        oi_intel = result.get('oi_intelligence', {})
        
        print(f"✅ CANDLE #{result['candle_number']} COMPLETED at {result['timestamp']}")
        print(f"📊 OHLC: O={candle_data.get('open'):.2f} H={candle_data.get('high'):.2f} L={candle_data.get('low'):.2f} C={candle_data.get('close'):.2f}")
        print(f"🕯️ Pattern: {pattern.get('pattern')} (Confidence: {pattern.get('confidence'):.0%})")
        print(f"📈 Volume: {volume_intel.get('pattern', 'N/A')} - {volume_intel.get('volume_bias', 'N/A')}")
        print(f"🎯 OI Flow: {oi_intel.get('smart_money_direction', 'N/A')}")
        print(f"🚨 TRADE REC: {trade_rec.get('action')} (Confidence: {trade_rec.get('confidence'):.0%})")
        print(f"💡 Reasoning: {trade_rec.get('reasoning', 'N/A')}")
        
    elif result.get('status') == 'BUILDING_CANDLE':
        progress = result.get('candle_progress', 'N/A')
        current_analysis = result.get('current_analysis', {})
        
        print(f"🔄 CANDLE BUILDING: {progress}")
        print(f"💹 Live Price: ₹{current_analysis.get('current_price', 0):.2f}")
        print(f"📊 OHLC: O={current_analysis.get('open_price', 0):.2f} H={current_analysis.get('high_price', 0):.2f} L={current_analysis.get('low_price', 0):.2f}")
        print(f"🕯️ Body: {current_analysis.get('body_size', 0):.2f} | Upper Wick: {current_analysis.get('upper_wick', 0):.2f} | Lower Wick: {current_analysis.get('lower_wick', 0):.2f}")
        print(f"📈 Volume: CE={current_analysis.get('ce_volume', 0):,} PE={current_analysis.get('pe_volume', 0):,} (Bias: {current_analysis.get('volume_bias', 0):+,})")
        print(f"🎯 OI: CE={current_analysis.get('ce_oi', 0):,} PE={current_analysis.get('pe_oi', 0):,} (PCR: {current_analysis.get('oi_pcr', 0):.3f})")
        
    else:
        print(f"❌ Candle Intelligence Status: {result.get('status')}")
        if 'error' in result:
            print(f"Error: {result['error']}")
    print("="*80)

# =============================================================================
# PROGRESSIVE RECOMMENDATION HELPER FUNCTIONS
# =============================================================================

def get_progressive_recommendation_level(snapshot_count: int) -> tuple:
    """Get recommendation level based on available data."""
    if snapshot_count < 3:
        return "BUILDING_DATA", "No analysis possible yet"
    elif snapshot_count < 15:
        return "PRE_RECOMMENDATION", f"Building foundation ({snapshot_count}/15 snapshots)"
    elif snapshot_count == 15:
        return "FIRST_RECOMMENDATION", "9:30 AM first recommendation ready"
    elif snapshot_count < 30:
        return "ENHANCED_TRACKING", "Multi-timeframe tracking active"
    elif snapshot_count < 60:
        return "ADVANCED_TRACKING", "Advanced multi-timeframe analysis"
    else:
        return "PREMIUM_TRACKING", "Full premium analysis with all timeframes"

def detect_stale_data(market_history: deque, threshold: float = 0.001) -> bool:
    """Detect if market data is stagnant."""
    if len(market_history) < 3:
        return False
    
    recent = list(market_history)[-3:]
    price_changes = [abs(recent[i]['underlying_value'] - recent[i-1]['underlying_value']) 
                    for i in range(1, len(recent))]
    
    # If no price movement in last 3 cycles
    return all(change < threshold for change in price_changes)

# =============================================================================
# CORRECTED MarketDataManager CLASS (with real NSE fetching and processing)
# =============================================================================
import cloudscraper
import requests
import random
from datetime import time as dt_time

class MarketDataManager:
    """Manages NSE data fetching with robust retries and processing."""

    def __init__(self):
        self.data = {}

    def fetch_market_data(self):
        # Fetch raw data from NSE
        raw_data, expiry, ts, spot, full_json_data = self.fetch_option_chain_data_from_nse("NIFTY")
        if raw_data is None:
            print("❌ Failed to fetch NIFTY data from NSE.")
            return {}  # Empty dict on failure

        # Process the raw data into a snapshot (as in thanks.py)
        snapshot = self.process_nse_snapshot(raw_data, expiry, ts, spot)
        return snapshot

    def fetch_option_chain_data_from_nse(self, symbol="NIFTY"):
        """Fetches option chain data from NSE with a robust retry mechanism (from thanks.py)."""
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        market_open_dt_time = dt_time(0, 0)  # Assuming MARKET_OPEN_HOUR/MINUTE from config
        market_close_dt_time = dt_time(23, 59)  # Assuming MARKET_CLOSE_HOUR/MINUTE from config
        if not (market_open_dt_time <= current_time <= market_close_dt_time):
            logger.info(f"⏳ Market is closed ({current_time.strftime('%H:%M')}). Skipping NSE fetch.")
            return None, None, None, None, None
        logger.info("🌐 Fetching NSE Option Chain Data...")
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        headers = {
            "User-Agent": scraper.headers["User-Agent"],
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.nseindia.com/option-chain",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.nseindia.com",
            "X-Requested-With": "XMLHttpRequest"
        }
        scraper.headers.update(headers)
        js = None
        last_error = None
        for attempt in range(3):
            r = None
            try:
                # Step 1: Set cookies by visiting home page
                scraper.get("https://www.nseindia.com", timeout=15)
                time.sleep(random.uniform(4.5, 6))  # Slower human delay
                # Step 2: Call option chain API
                url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
                r = scraper.get(url, timeout=15)
                r.raise_for_status()
                js = r.json()
                break  # Success
            except requests.exceptions.HTTPError as http_err:
                status = r.status_code if r else 'N/A'
                last_error = f"HTTP error {status}: {http_err}"
                logger.warning(f"⚠️ Attempt {attempt+1}/3 failed (HTTP): {last_error}")
            except requests.exceptions.RequestException as req_err:
                last_error = f"Request error: {req_err}"
                logger.warning(f"⚠️ Attempt {attempt+1}/3 failed (Request): {last_error}")
            except json.JSONDecodeError as json_err:
                last_error = f"JSON decode error: {json_err}"
                logger.warning(f"⚠️ Attempt {attempt+1}/3 failed (JSON): {json_err}")
            except Exception as e:
                last_error = f"Unexpected error: {e}"
                logger.error(f"❌ Attempt {attempt+1}/3 failed: {last_error}")
            # Retry logic
            if attempt < 2:
                time.sleep(random.uniform(8, 12))  # Wait before retry
            else:
                logger.error(f"*NSE snapshot failed*: All attempts timed out. Error: {last_error}")
                return None, None, None, None, None
        if not js or "records" not in js or not js["records"].get("expiryDates"):
            logger.error("*Snapshot failed* → Invalid or empty data from NSE.")
            return None, None, None, None, None
        return (
            js["records"]["data"],
            js["records"]["expiryDates"][0],
            current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            js["records"]["underlyingValue"],
            js
        )

    def process_nse_snapshot(self, raw_data, expiry, ts, spot):
        """Process raw NSE data into snapshot and print the required format (from thanks.py logic)."""
        # Initialize totals
        ce_oi = ce_vol = pe_oi = pe_vol = 0
        max_ce_oi = max_pe_oi = 0
        max_ce_strike = max_pe_strike = None
        for r in raw_data:
            if r.get("expiryDate") != expiry or "CE" not in r or "PE" not in r:
                continue
            ce, pe = r["CE"], r["PE"]
            ce_oi += ce.get("openInterest", 0)
            ce_vol += ce.get("totalTradedVolume", 0)
            pe_oi += pe.get("openInterest", 0)
            pe_vol += pe.get("totalTradedVolume", 0)
            # Track max OI strikes for support/resistance
            if ce.get("openInterest", 0) > max_ce_oi:
                max_ce_oi = ce.get("openInterest", 0)
                max_ce_strike = r["strikePrice"]
            if pe.get("openInterest", 0) > max_pe_oi:
                max_pe_oi = pe.get("openInterest", 0)
                max_pe_strike = r["strikePrice"]
        # Calculate PCR and Vol Ratio
        pcr = pe_oi / ce_oi if ce_oi > 0 else 0
        vol_ratio = pe_vol / ce_vol if ce_vol > 0 else 0
        # Support/Resistance (from max OI strikes)
        support = max_pe_strike if max_pe_strike else spot - 50  # Fallback
        resistance = max_ce_strike if max_ce_strike else spot + 50  # Fallback
        # Trend (simple placeholder; enhance if needed)
        trend = "UNKNOWN"  # As in thanks.py
        # PRINT THE EXACT REQUIRED SNAPSHOT FORMAT
        print("="*50)
        print(f"📊 Market Snapshot at {ts} 📊")
        print(f"💰 Spot: {spot} | 🔰 Support: {support} | 🚫 Resistance: {resistance}")
        print(f"🗭 Broad Trend: {trend} | PCR: {pcr:.2f} | Vol Ratio (PE/CE): {vol_ratio:.2f}")
        print(f"🟢 CE OI: {int(ce_oi):,} (Vol: {int(ce_vol):,})")
        print(f"🔴 PE OI: {int(pe_oi):,} (Vol: {int(pe_vol):,})")
        print("="*50)
        # Return processed snapshot for further use in the bot
        return {
            "underlying_value": spot,
            "CE_OI": ce_oi,
            "PE_OI": pe_oi,
            "CE_VOL": ce_vol,
            "PE_VOL": pe_vol,
            "OI_PCR": pcr,
            "VOL_PCR": vol_ratio,
            "support": support,
            "resistance": resistance,
            "trend": trend,
            "timestamp": ts
        }

    def validate_trade(self, trade_amount, account_balance):
        # Basic risk check
        risk_pct = (trade_amount / account_balance) * 100
        return risk_pct <= (self.max_risk / account_balance) * 100

# -- Add here --
class TradingBotIntegrator:
    """Main class to coordinate data, risk, and signals."""
    def __init__(self, data_manager, risk_manager, predictor, signal_engine):
        self.data_manager = data_manager
        self.risk_manager = risk_manager
        self.predictor = predictor
        self.signal_engine = signal_engine

    def run_cycle(self):
        data = self.data_manager.fetch_market_data()
        # Example: Run predictor and signals
        prediction = self.predictor.predict(data)
        signals = self.signal_engine.generate_signals(prediction)
        # Validate and execute trades (simplified)
        for signal in signals:
            trade_amount = 100  # Define your logic
            if self.risk_manager.validate_trade(trade_amount, 200000):  # example account balance
                self.execute_trade(signal, trade_amount)

    def execute_trade(self, signal, amount):
        # Placeholder for trade execution logic
        print(f"Executing {signal} for amount {amount}")

#=============================================================================
# PART 1: IMPORTS AND CONFIGURATION
#=============================================================================
from collections import deque
from datetime import datetime
from typing import Dict, Any, List, Tuple
import numpy as np
import logging

logger = logging.getLogger(__name__)

#=============================================================================
# PART 2: CORE CLASS INITIALIZATION AND CONFIGURATION
#=============================================================================
class EnhancedSmartSelfAnalyzer:
    """Advanced AI analyzer that learns from volume-OI patterns, market phases, and trap detection."""

    def __init__(self):
        """Initialize the enhanced smart analyzer with all required components."""
        # SECTION 2.1: Basic Performance Tracking
        self.trade_history = deque(maxlen=500)
        self.mistake_patterns = {}
        self.learning_insights = deque(maxlen=100)
        self.performance_metrics = {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0,
            "avg_profit": 0.0,
            "avg_loss": 0.0,
            "best_trade": 0.0,
            "worst_trade": 0.0
        }

        # SECTION 2.2: Advanced Pattern Learning Databases
        self.volume_oi_patterns = deque(maxlen=200)  # Learn volume-OI relationships
        self.trap_detection_history = deque(maxlen=100)  # Track trap patterns
        self.market_phase_outcomes = {}  # Learn from different market phases
        self.timing_pattern_success = {}  # Learn optimal entry timing
        self.institutional_patterns = deque(maxlen=150)  # Track smart money patterns

        # SECTION 2.3: Advanced Learning Metrics
        self.trap_avoidance_rate = 0.0
        self.breakout_capture_rate = 0.0
        self.volume_pattern_accuracy = 0.0
        self.phase_detection_accuracy = 0.0

        # SECTION 2.4: AI Brain Configuration
        self.ai_brain_weights = {
            'max_pain_gravity': 2.5,
            'fear_gauge': 3.0,
            'oi_acceleration': 2.5,
            'rsi_momentum': 2.0,
            'historical_trend': 1.5,
            'volume_oi_alignment': 4.0,
            'phase_context': 3.5,
            'trap_detection': 5.0
        }

        logger.info("🧠 Enhanced Smart Self-Analyzer initialized with AI intelligence integration")

    # CRITICAL PATCH 1: Add missing get_current_brain_weights method
    def get_current_brain_weights(self) -> Dict[str, float]:
        """Get current AI brain weights for logging."""
        return self.ai_brain_weights.copy()

    # CRITICAL PATCH 2: Add missing analyze_trade_mistake method
    def analyze_trade_mistake(self, trade_outcome: Dict, market_conditions: Dict, timeframe_analysis: Dict) -> str:
        """Backward compatibility method for basic mistake analysis."""
        # Convert to new format and call enhanced method
        ai_analysis = {
            "volume_analysis": {"pattern": "UNKNOWN", "strength": "MEDIUM"},
            "oi_analysis": {"pattern": "UNKNOWN", "strength": "MEDIUM"},
            "market_phase": {"phase": "UNKNOWN", "confidence": 50}
        }

        return self.analyze_trade_with_ai_intelligence(trade_outcome, market_conditions, ai_analysis)

    # CRITICAL PATCH 3: Add missing update_performance_metrics method
    def update_performance_metrics(self, trade_outcome: Dict):
        """Update basic performance tracking metrics."""
        self.performance_metrics["total_trades"] += 1
        pnl = trade_outcome.get("pnl", 0)

        if trade_outcome.get("result", "") == "WIN":
            wins = self.performance_metrics["winning_trades"] + 1
            self.performance_metrics["winning_trades"] = wins

            # Update best trade
            if pnl > self.performance_metrics["best_trade"]:
                self.performance_metrics["best_trade"] = pnl

            # Update average profit (safe division)
            if wins > 1:
                total_profits = self.performance_metrics["avg_profit"] * (wins - 1)
                self.performance_metrics["avg_profit"] = (total_profits + pnl) / wins
            else:
                self.performance_metrics["avg_profit"] = pnl
        else:
            losses = self.performance_metrics["losing_trades"] + 1
            self.performance_metrics["losing_trades"] = losses

            # Update worst trade
            if pnl < self.performance_metrics["worst_trade"]:
                self.performance_metrics["worst_trade"] = pnl

            # Update average loss (safe division)
            if losses > 1:
                total_losses = self.performance_metrics["avg_loss"] * (losses - 1)
                self.performance_metrics["avg_loss"] = (total_losses + pnl) / losses
            else:
                self.performance_metrics["avg_loss"] = pnl

        # Calculate win rate (safe division)
        total = self.performance_metrics["total_trades"]
        wins = self.performance_metrics["winning_trades"]
        self.performance_metrics["win_rate"] = (wins / total) * 100 if total > 0 else 0

        logger.info("📊 PERFORMANCE UPDATE - Win Rate: %.1f%% (%d/%d trades)",
                   self.performance_metrics["win_rate"], wins, total)

    # CRITICAL PATCH 4: Add missing get_learning_summary method
    def get_learning_summary(self) -> Dict[str, Any]:
        """Generate basic learning summary."""
        return {
            "performance": self.performance_metrics,
            "top_mistakes": dict(sorted(self.mistake_patterns.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recent_insights": list(self.learning_insights)[-10:],
            "learning_trend": "IMPROVING" if len(self.trade_history) > 10 and sum(1 for t in list(self.trade_history)[-10:] if t["trade_outcome"].get("result") == "WIN") > 6 else "NEEDS_WORK"
        }

    # CRITICAL PATCH 5: Add missing analyze_trade_with_ai_intelligence method
    def analyze_trade_with_ai_intelligence(self, trade_outcome: Dict, market_data: Dict, ai_analysis: Dict) -> str:
        """Enhanced trade analysis that learns from AI intelligence patterns."""

        # Store comprehensive trade data
        comprehensive_trade_data = {
            "timestamp": datetime.now().isoformat(),
            "trade_outcome": trade_outcome,
            "market_data": market_data,
            "ai_analysis": ai_analysis,
            "volume_analysis": ai_analysis.get("volume_analysis", {}),
            "oi_analysis": ai_analysis.get("oi_analysis", {}),
            "market_phase": ai_analysis.get("market_phase", {}),
            "move_authenticity": ai_analysis.get("move_type", {})
        }

        self.trade_history.append(comprehensive_trade_data)
        self.update_enhanced_performance_metrics(trade_outcome, ai_analysis)

        if trade_outcome.get("result", "") == "LOSS":
            return self._analyze_ai_enhanced_mistake(comprehensive_trade_data)
        else:
            return self._analyze_ai_enhanced_success(comprehensive_trade_data)

    # CRITICAL PATCH 6: Add missing update_enhanced_performance_metrics method
    def update_enhanced_performance_metrics(self, trade_outcome: Dict, ai_analysis: Dict):
        """Update metrics including AI-specific performance indicators."""

        # Update basic metrics first
        self.update_performance_metrics(trade_outcome)

        # Extract AI-specific data
        market_phase = ai_analysis.get("market_phase", {}).get("phase", "")
        move_authenticity = ai_analysis.get("move_type", {}).get("assessment", "")

        # Track AI-specific metrics
        if market_phase == "FAKE_BREAKOUT_TRAP":
            if trade_outcome.get("result", "") != "LOSS":
                self.trap_avoidance_rate += 1

        if market_phase == "GENUINE_BREAKOUT":
            if trade_outcome.get("result", "") == "WIN":
                self.breakout_capture_rate += 1

        volume_pattern = ai_analysis.get("volume_analysis", {}).get("pattern", "")
        if volume_pattern and trade_outcome.get("result", "") == "WIN":
            self.volume_pattern_accuracy += 1

        if market_phase and trade_outcome.get("result", "") == "WIN":
            self.phase_detection_accuracy += 1

    # CRITICAL PATCH 7: Add missing _analyze_ai_enhanced_mistake method
    def _analyze_ai_enhanced_mistake(self, trade_data: Dict) -> str:
        """Advanced mistake analysis using AI intelligence patterns."""

        trade_outcome = trade_data["trade_outcome"]
        ai_analysis = trade_data["ai_analysis"]
        volume_analysis = ai_analysis.get("volume_analysis", {})
        oi_analysis = ai_analysis.get("oi_analysis", {})
        market_phase = ai_analysis.get("market_phase", {})

        # Identify mistake pattern
        mistake_type = self._identify_ai_enhanced_mistake_pattern(
            trade_outcome, volume_analysis, oi_analysis, market_phase
        )

        # Store in mistake patterns
        self.mistake_patterns[mistake_type] = self.mistake_patterns.get(mistake_type, 0) + 1

        # Learn from volume-OI relationship mistakes
        if volume_analysis and oi_analysis:
            volume_oi_lesson = self._learn_from_volume_oi_mistake(
                volume_analysis, oi_analysis, trade_outcome
            )
            self.volume_oi_patterns.append(volume_oi_lesson)

        # Learn from market phase mistakes
        if market_phase:
            phase_lesson = self._learn_from_phase_mistake(market_phase, trade_outcome)
            phase_name = market_phase.get("phase", "UNKNOWN")
            if phase_name not in self.market_phase_outcomes:
                self.market_phase_outcomes[phase_name] = {"wins": 0, "losses": 0}
            self.market_phase_outcomes[phase_name]["losses"] += 1

        # Generate improvement suggestion
        improvement = self._generate_ai_enhanced_improvement(
            mistake_type, volume_analysis, oi_analysis, market_phase
        )

        # Enhanced logging
        self._log_ai_enhanced_mistake_analysis(
            mistake_type, trade_outcome, volume_analysis, oi_analysis, market_phase, improvement
        )

        return f"🧠 AI LEARNED: {mistake_type} → {improvement}"

    # CRITICAL PATCH 8: Add missing _analyze_ai_enhanced_success method
    def _analyze_ai_enhanced_success(self, trade_data: Dict) -> str:
        """Analyze successful trades to identify winning patterns."""

        trade_outcome = trade_data["trade_outcome"]
        ai_analysis = trade_data["ai_analysis"]
        volume_analysis = ai_analysis.get("volume_analysis", {})
        oi_analysis = ai_analysis.get("oi_analysis", {})
        market_phase = ai_analysis.get("market_phase", {})

        # Identify success pattern
        success_type = self._identify_success_pattern(
            trade_outcome, volume_analysis, oi_analysis, market_phase
        )

        # Learn from market phase successes
        if market_phase:
            phase_name = market_phase.get("phase", "UNKNOWN")
            if phase_name not in self.market_phase_outcomes:
                self.market_phase_outcomes[phase_name] = {"wins": 0, "losses": 0}
            self.market_phase_outcomes[phase_name]["wins"] += 1

        # Store successful volume-OI pattern
        if volume_analysis and oi_analysis:
            success_lesson = self._learn_from_volume_oi_success(
                volume_analysis, oi_analysis, trade_outcome
            )
            self.volume_oi_patterns.append(success_lesson)

        # Log success analysis
        logger.info("✅ AI-ENHANCED SUCCESS ANALYSIS")
        logger.info("="*70)
        logger.info("🎯 Success Type: %s", success_type)
        logger.info("💰 PnL Achieved: %.2f%%", trade_outcome.get("pnl", 0))
        logger.info("📊 Volume Pattern: %s", volume_analysis.get("pattern", "Unknown"))
        logger.info("🎯 OI Pattern: %s", oi_analysis.get("pattern", "Unknown"))
        logger.info("🌊 Market Phase: %s", market_phase.get("phase", "Unknown"))
        logger.info("="*70)

        return f"🎯 AI SUCCESS: {success_type} - Pattern stored for replication"

    # CRITICAL PATCH 9: Add all missing helper methods
    def _identify_ai_enhanced_mistake_pattern(self, trade_outcome: Dict, volume_analysis: Dict,
                                           oi_analysis: Dict, market_phase: Dict) -> str:
        """Enhanced mistake pattern identification using AI intelligence."""

        pnl = abs(trade_outcome.get("pnl", 0))
        phase = market_phase.get("phase", "UNKNOWN")
        volume_pattern = volume_analysis.get("pattern", "UNKNOWN")
        oi_pattern = oi_analysis.get("pattern", "UNKNOWN")

        # Volume-OI trap pattern (like -9.65% loss)
        if volume_pattern == "FAKE_SPIKE" and oi_pattern == "FLAT_OI":
            return "VOLUME_OI_TRAP_PATTERN"
        # Fake breakout traps
        elif phase == "FAKE_BREAKOUT_TRAP":
            return "INSTITUTIONAL_TRAP_ENTRY"
        # Entered too early without confirmation
        elif volume_analysis.get("sustainability", 0) < 0.5:
            return "PREMATURE_ENTRY_NO_CONFIRMATION"
        # Ignored market phase context
        elif phase in ["CONSOLIDATION_WITH_ACTIVITY", "SIDEWAYS_ACCUMULATION"]:
            return "IGNORED_CONSOLIDATION_CONTEXT"
        else:
            return "GENERAL_AI_PATTERN_MISS"

    def _identify_success_pattern(self, trade_outcome: Dict, volume_analysis: Dict,
                                oi_analysis: Dict, market_phase: Dict) -> str:
        """Identify successful trading patterns."""

        pnl = trade_outcome.get("pnl", 0)
        phase = market_phase.get("phase", "UNKNOWN")
        volume_pattern = volume_analysis.get("pattern", "UNKNOWN")
        oi_pattern = oi_analysis.get("pattern", "UNKNOWN")

        if pnl > 15 and volume_pattern == "SUSTAINED_INCREASE" and oi_pattern == "STRONG_OI_BUILD":
            return "PERFECT_VOLUME_OI_BREAKOUT"
        elif phase == "GENUINE_BREAKOUT" and pnl > 10:
            return "SUCCESSFUL_BREAKOUT_CAPTURE"
        elif volume_pattern == "GRADUAL_BUILD" and pnl > 8:
            return "PATIENT_ACCUMULATION_SUCCESS"
        else:
            return "GENERAL_SUCCESS_PATTERN"

    def _learn_from_volume_oi_mistake(self, volume_analysis: Dict, oi_analysis: Dict, trade_outcome: Dict) -> Dict:
        """Learn specific lessons from volume-OI relationship mistakes."""

        volume_pattern = volume_analysis.get("pattern", "")
        oi_pattern = oi_analysis.get("pattern", "")
        pnl = trade_outcome.get("pnl", 0)

        lesson = {
            "timestamp": datetime.now().isoformat(),
            "volume_pattern": volume_pattern,
            "oi_pattern": oi_pattern,
            "outcome": "LOSS",
            "pnl_impact": pnl,
            "lesson": self._generate_volume_oi_lesson(volume_pattern, oi_pattern)
        }

        return lesson

    def _learn_from_volume_oi_success(self, volume_analysis: Dict, oi_analysis: Dict, trade_outcome: Dict) -> Dict:
        """Learn from successful volume-OI combinations."""

        volume_pattern = volume_analysis.get("pattern", "")
        oi_pattern = oi_analysis.get("pattern", "")
        pnl = trade_outcome.get("pnl", 0)

        lesson = {
            "timestamp": datetime.now().isoformat(),
            "volume_pattern": volume_pattern,
            "oi_pattern": oi_pattern,
            "outcome": "WIN",
            "pnl_impact": pnl,
            "lesson": self._generate_success_volume_oi_lesson(volume_pattern, oi_pattern)
        }

        return lesson

    def _learn_from_phase_mistake(self, market_phase: Dict, trade_outcome: Dict) -> Dict:
        """Learn specific lessons from market phase mistakes."""

        phase = market_phase.get("phase", "UNKNOWN")
        pnl = trade_outcome.get("pnl", 0)

        phase_lesson = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "outcome": "LOSS",
            "pnl_impact": pnl,
            "lesson": self._generate_phase_lesson(phase, "LOSS"),
            "confidence": market_phase.get("confidence", 0)
        }

        return phase_lesson

    def _generate_volume_oi_lesson(self, volume_pattern: str, oi_pattern: str) -> str:
        """Generate specific lessons from volume-OI combinations."""

        if volume_pattern == "FAKE_SPIKE" and oi_pattern == "FLAT_OI":
            return "NEVER_TRADE_HIGH_VOLUME_FLAT_OI - Classic trap pattern"
        elif volume_pattern == "SUSTAINED_INCREASE" and oi_pattern == "FLAT_OI":
            return "WAIT_FOR_OI_CONFIRMATION - Volume needs OI support"
        else:
            return "ANALYZE_VOLUME_OI_ALIGNMENT - Both must support trade direction"

    def _generate_success_volume_oi_lesson(self, volume_pattern: str, oi_pattern: str) -> str:
        """Generate lessons from successful volume-OI combinations."""

        if volume_pattern == "SUSTAINED_INCREASE" and oi_pattern == "STRONG_OI_BUILD":
            return "REPLICATE_SUSTAINED_VOLUME_STRONG_OI - Perfect breakout pattern"
        elif volume_pattern == "GRADUAL_BUILD" and oi_pattern == "MODERATE_OI_BUILD":
            return "PATIENT_ACCUMULATION_WORKS - Wait for gradual build patterns"
        else:
            return "VOLUME_OI_ALIGNMENT_SUCCESS - Both indicators supported trade"

    def _generate_phase_lesson(self, phase: str, outcome: str) -> str:
        """Generate lessons from market phase outcomes."""

        if outcome == "LOSS":
            phase_lessons = {
                "FAKE_BREAKOUT_TRAP": "AVOID_FAKE_BREAKOUTS - Wait for volume-OI confirmation",
                "CONSOLIDATION_WITH_ACTIVITY": "NO_TRADES_IN_CONSOLIDATION - High trap probability",
                "SIDEWAYS_ACCUMULATION": "WAIT_FOR_BREAKOUT - Don't trade sideways markets",
                "UNCLEAR_PHASE": "REQUIRE_CLEAR_SIGNALS - No trades in unclear markets"
            }
        else:
            phase_lessons = {
                "GENUINE_BREAKOUT": "REPLICATE_BREAKOUT_ENTRIES - High success pattern",
                "PULLBACK_OR_CORRECTION": "BUY_PULLBACKS_IN_TREND - Good entry opportunities",
                "BUILDING_MOMENTUM": "EARLY_MOMENTUM_ENTRIES - Catch trends early"
            }

        return phase_lessons.get(phase, f"LEARN_FROM_{phase}_{outcome}")

    def _generate_ai_enhanced_improvement(self, mistake_type: str, volume_analysis: Dict,
                                        oi_analysis: Dict, market_phase: Dict) -> str:
        """Generate specific improvements based on AI analysis."""

        enhanced_improvements = {
            "VOLUME_OI_TRAP_PATTERN": "IMPLEMENT: Never enter when volume spikes but OI flat - Add mandatory OI confirmation filter",
            "INSTITUTIONAL_TRAP_ENTRY": "IMPLEMENT: 45-minute waiting rule + 2-candle confirmation before any breakout entry",
            "PREMATURE_ENTRY_NO_CONFIRMATION": "IMPLEMENT: Mandatory 15-minute volume sustainability check before entry",
            "IGNORED_CONSOLIDATION_CONTEXT": "IMPLEMENT: No trades during consolidation phases - Wait for clear breakout",
            "GENERAL_AI_PATTERN_MISS": "IMPLEMENT: Improve AI pattern recognition training"
        }

        return enhanced_improvements.get(mistake_type, "Review AI pattern recognition logic")

    def _log_ai_enhanced_mistake_analysis(self, mistake_type: str, trade_outcome: Dict,
                                        volume_analysis: Dict, oi_analysis: Dict,
                                        market_phase: Dict, improvement: str):
        """Enhanced logging with AI intelligence details."""

        logger.error("🔍 AI-ENHANCED TRADE MISTAKE ANALYSIS")
        logger.error("="*70)
        logger.error("❌ AI Mistake Type: %s", mistake_type)
        logger.error("💸 PnL Impact: %.2f%%", trade_outcome.get("pnl", 0))
        logger.error("📊 Volume Pattern: %s", volume_analysis.get("pattern", "Unknown"))
        logger.error("🎯 OI Pattern: %s", oi_analysis.get("pattern", "Unknown"))
        logger.error("🌊 Market Phase: %s", market_phase.get("phase", "Unknown"))
        logger.error("💡 AI Improvement: %s", improvement)
        logger.error("🔄 Pattern Frequency: %d occurrences", self.mistake_patterns.get(mistake_type, 0))
        logger.error("="*70)

from collections import deque
from datetime import datetime, time as dt_time
from typing import Any, Dict, List

import logging

logger = logging.getLogger(__name__)
def analyze_market_progressive(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """Complete implementation of progressive market analysis."""
    try:
        if len(market_state.market_history) < 3:
            return {
                'status': 'insufficient_data',
                'verdict': 'NEUTRAL',
                'score': 0.0,
                'reason': 'Need more data'
            }
        
        # Multi-timeframe analysis
        mtf_analyzer = MultiTimeframeAnalyzer()
        timeframe_changes = mtf_analyzer.analyze_timeframe_changes(market_state.market_history)
        
        # Store in market state
        market_state.current_analysis = {
            'timeframe_analysis': timeframe_changes,
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate verdict based on analysis
        verdict = self._generate_verdict_from_timeframes(timeframe_changes)
        
        return {
            'status': 'success',
            'verdict': verdict['direction'],
            'score': verdict['strength'],
            'reason': verdict['reason'],
            'timeframe_analysis': timeframe_changes
        }
        
    except Exception as e:
        logger.error(f"❌ analyze_market_progressive failed: {e}")
        return {
            'status': 'error',
            'verdict': 'NEUTRAL',
            'score': 0.0,
            'reason': f'Analysis error: {e}'
        }

def _generate_verdict_from_timeframes(self, timeframe_changes: Dict) -> Dict:
    """Generate trading verdict from timeframe analysis."""
    if not timeframe_changes:
        return {'direction': 'NEUTRAL', 'strength': 0.0, 'reason': 'No timeframe data'}
    
    bullish_count = sum(1 for data in timeframe_changes.values() 
                       if 'BULLISH' in data.get('momentum', ''))
    bearish_count = sum(1 for data in timeframe_changes.values() 
                       if 'BEARISH' in data.get('momentum', ''))
    
    if bullish_count > bearish_count:
        return {'direction': 'BULLISH', 'strength': 6.0, 'reason': f'{bullish_count} bullish timeframes'}
    elif bearish_count > bullish_count:
        return {'direction': 'BEARISH', 'strength': -6.0, 'reason': f'{bearish_count} bearish timeframes'}
    else:
        return {'direction': 'NEUTRAL', 'strength': 0.0, 'reason': 'Mixed signals'}

#=============================================================================
# SMART LIVE COMMENTARY BOT - COMPLETE TELEGRAM INTEGRATION
#=============================================================================

import requests
from datetime import datetime, time as dt_time
from collections import deque
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SmartLiveCommentaryBot:
    """AI bot that provides complete live market commentary and sends everything to Telegram."""

    def __init__(self, config):
        self.config = config
        self.last_commentary_time = None
        self.market_context_history = deque(maxlen=50)
        self.pattern_alerts_sent = set()
        
        # Telegram configuration
        self.telegram_token = config.get('telegram', {}).get('token', '')
        self.chat_id = config.get('telegram', {}).get('chat_id', '')
        self.telegram_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"

        logger.info("🎯 Smart Live Commentary Bot initialized for Telegram broadcasting")

    def generate_comprehensive_market_commentary(self, market_state: 'EnhancedMarketState', analysis_data: Dict[str, Any]) -> str:
        """Generate complete live market commentary with all intelligence."""

        if len(market_state.market_history) < 2:
            return "🔄 Building market intelligence... Need more data for comprehensive analysis."

        current = market_state.market_history[-1]
        previous = market_state.market_history[-2]

        # Generate comprehensive commentary
        commentary_parts = []

        # 1. Market Intelligence Header
        commentary_parts.append(self._generate_intelligence_header(current, market_state))

        # 2. Real-time Market Snapshot
        commentary_parts.append(self._generate_market_snapshot(current, previous))

        # 3. Volume Flow Intelligence
        commentary_parts.append(self._generate_volume_intelligence(current, previous))

        # 4. Open Interest Analysis
        commentary_parts.append(self._generate_oi_intelligence(current, previous))

        # 5. Smart Money Interpretation
        commentary_parts.append(self._generate_smart_money_interpretation(current, previous, analysis_data))

        # 6. Support/Resistance Context
        commentary_parts.append(self._generate_support_resistance_context(market_state)[0])

        # 7. AI Decision Reasoning
        commentary_parts.append(self._generate_ai_reasoning(analysis_data))

        # 8. Market Phase Detection
        commentary_parts.append(self._generate_market_phase_analysis(analysis_data))

        # 9. Risk Assessment
        commentary_parts.append(self._generate_risk_assessment(current, market_state))

        # Combine all parts
        full_commentary = "\n".join(commentary_parts)

        # Store for historical context
        self.market_context_history.append({
            "timestamp": datetime.now().isoformat(),
            "commentary": full_commentary,
            "market_data": current
        })

        return full_commentary

    def _generate_support_resistance_context(self, market_state: 'EnhancedMarketState') -> tuple:
        """Generate support/resistance context and return both text + values - FIXED."""
        
        if len(market_state.market_history) < 5:  # Reduced from 10
            current_price = market_state.last_spot_price
            support_levels = [current_price - 15, current_price - 30]
            resistance_levels = [current_price + 15, current_price + 30] 
            
            context_text = f"""
    📈 SUPPORT/RESISTANCE: 
    • Current: ₹{current_price:.2f}
    • Support: ₹{support_levels[0]:.2f} / ₹{support_levels[1]:.2f}
    • Resistance: ₹{resistance_levels[0]:.2f} / ₹{resistance_levels[1]:.2f}"""
            
            return context_text, support_levels, resistance_levels
        
        recent_data = list(market_state.market_history)[-10:]
        prices = [data.get('underlying_value', 0) for data in recent_data]
        current_price = prices[-1]
        
        # Calculate dynamic support and resistance
        support_levels = [min(prices[-5:]), min(prices)]  # Recent low, Overall low
        resistance_levels = [max(prices[-5:]), max(prices)]  # Recent high, Overall high
        
        # Ensure levels are different from current price
        if support_levels[0] >= current_price:
            support_levels[0] = current_price - 10
        if resistance_levels[0] <= current_price:
            resistance_levels[0] = current_price + 10
        
        context_text = f"""
    📈 SUPPORT/RESISTANCE CONTEXT:
    • Current: ₹{current_price:.2f}
    • Immediate Support: ₹{support_levels[0]:.2f}  
    • Key Support: ₹{support_levels[1]:.2f}
    • Immediate Resistance: ₹{resistance_levels[0]:.2f}
    • Key Resistance: ₹{resistance_levels[1]:.2f}"""

        return context_text, support_levels, resistance_levels

    def _generate_intelligence_header(self, current: Dict, market_state: 'EnhancedMarketState') -> str:
        """Generate intelligence header with cycle info."""
        cycle_num = len(market_state.market_history)
        timestamp = datetime.now().strftime('%H:%M:%S')

        return f"""🧠 SMART AI LIVE MARKET ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Cycle #{cycle_num} | ⏰ Time: {timestamp}
🎯 AI Intelligence Level: {market_state.data_quality_score:.1f}/10"""

    def _generate_market_snapshot(self, current: Dict, previous: Dict) -> str:
        """Generate real-time market snapshot."""
        spot_current = current.get('underlying_value', 0)
        spot_previous = previous.get('underlying_value', 0)
        spot_change = spot_current - spot_previous
        spot_change_pct = (spot_change / spot_previous * 100) if spot_previous > 0 else 0

        pcr_current = current.get('oi_pcr', 0)  # Fixed key name
        pcr_change = pcr_current - previous.get('oi_pcr', 0)  # Fixed key name

        market_regime = self._determine_market_regime(spot_change_pct, pcr_current)

        return f"""
📊 REAL-TIME MARKET SNAPSHOT:
• Spot: ₹{spot_current:.2f} ({spot_change:+.2f}, {spot_change_pct:+.3f}%)
• Market Regime: {market_regime}
• OI PCR: {pcr_current:.3f} ({pcr_change:+.3f})
• Volatility State: {self._assess_volatility_state(spot_change_pct)}"""

    def _generate_volume_intelligence(self, current: Dict, previous: Dict) -> str:
        """Generate volume flow intelligence."""
        ce_vol_change = current.get('total_ce_volume', 0) - previous.get('total_ce_volume', 0)  # Fixed key names
        pe_vol_change = current.get('total_pe_volume', 0) - previous.get('total_pe_volume', 0)  # Fixed key names
        total_vol_change = ce_vol_change + pe_vol_change
        volume_bias = pe_vol_change - ce_vol_change

        # Volume pattern analysis
        volume_pattern = self._analyze_volume_pattern(ce_vol_change, pe_vol_change, total_vol_change)
        institutional_activity = self._assess_institutional_activity(total_vol_change, volume_bias)

        return f"""
🌊 VOLUME FLOW INTELLIGENCE:
• CE Volume: {ce_vol_change:+,} | PE Volume: {pe_vol_change:+,}
• Total Volume: {total_vol_change:+,}
• Volume Bias: {volume_bias:+,} ({self._interpret_volume_bias(volume_bias)})
• Pattern: {volume_pattern}
• Institutional Activity: {institutional_activity}"""

    def _generate_oi_intelligence(self, current: Dict, previous: Dict) -> str:
        """Generate open interest intelligence."""
        ce_oi_change = current.get('total_ce_oi', 0) - previous.get('total_ce_oi', 0)  # Fixed key names
        pe_oi_change = current.get('total_pe_oi', 0) - previous.get('total_pe_oi', 0)  # Fixed key names
        total_oi_change = abs(ce_oi_change) + abs(pe_oi_change)

        oi_pattern = self._analyze_oi_pattern(ce_oi_change, pe_oi_change, total_oi_change)
        commitment_level = self._assess_market_commitment(total_oi_change)

        return f"""
🎯 OPEN INTEREST INTELLIGENCE:
• CE OI: {ce_oi_change:+,} | PE OI: {pe_oi_change:+,}
• Total OI Change: {total_oi_change:,}
• OI Pattern: {oi_pattern}
• Market Commitment: {commitment_level}
• New Money Flow: {self._assess_new_money_flow(ce_oi_change, pe_oi_change)}"""

    def _generate_smart_money_interpretation(self, current: Dict, previous: Dict, analysis_data: Dict) -> str:
        """Generate smart money interpretation."""
        spot_change = current.get('underlying_value', 0) - previous.get('underlying_value', 0)
        ce_vol_change = current.get('total_ce_volume', 0) - previous.get('total_ce_volume', 0)
        pe_vol_change = current.get('total_pe_volume', 0) - previous.get('total_pe_volume', 0)
        volume_bias = pe_vol_change - ce_vol_change

        # Detect smart money patterns
        smart_money_activity = self._detect_smart_money_patterns(spot_change, volume_bias, ce_vol_change, pe_vol_change)
        divergence_analysis = self._analyze_price_volume_divergence(spot_change, volume_bias)

        return f"""
🕵️ SMART MONEY INTERPRETATION:
• Activity Level: {smart_money_activity}
• Price-Volume Relationship: {divergence_analysis}
• Institutional Positioning: {self._assess_institutional_positioning(volume_bias, spot_change)}
• Retail vs Smart Money: {self._assess_retail_vs_smart_money(analysis_data)}"""

    def _generate_ai_reasoning(self, analysis_data: Dict) -> str:
        """Generate AI decision reasoning."""
        verdict = analysis_data.get('verdict', 'NEUTRAL')
        score = analysis_data.get('score', 0)
        triggers = analysis_data.get('triggers', [])

        confidence_breakdown = self._calculate_confidence_breakdown(analysis_data)
        decision_factors = self._analyze_decision_factors(triggers)

        return f"""
🤖 AI DECISION REASONING:
• Current Verdict: {verdict} (Score: {score:.2f}/10)
• Decision Confidence: {confidence_breakdown}
• Key Triggers: {len(triggers)} active
• Primary Factors: {decision_factors}
• Algorithm Status: {self._assess_algorithm_agreement(analysis_data)}"""

    def _generate_market_phase_analysis(self, analysis_data: Dict) -> str:
        """Generate market phase analysis."""
        volume_analysis = analysis_data.get('volume_analysis', {})
        pattern_detection = analysis_data.get('pattern_detection', {})

        current_phase = self._determine_current_market_phase(volume_analysis, pattern_detection)
        phase_probability = self._calculate_phase_probability(current_phase)
        next_move_prediction = self._predict_next_move(current_phase, analysis_data)

        return f"""
🌊 MARKET PHASE ANALYSIS:
• Current Phase: {current_phase}
• Phase Confidence: {phase_probability}%
• Next Move Prediction: {next_move_prediction}
• Pattern Alerts: {self._get_active_pattern_alerts(pattern_detection)}"""

    def _generate_risk_assessment(self, current: Dict, market_state: 'EnhancedMarketState') -> str:
        """Generate comprehensive risk assessment."""
        volatility_risk = self._assess_volatility_risk(market_state)
        liquidity_risk = self._assess_liquidity_risk(current)
        time_risk = self._assess_time_of_day_risk()
        overall_risk = self._calculate_overall_risk_score(volatility_risk, liquidity_risk, time_risk, market_state)

        return f"""
⚠️ COMPREHENSIVE RISK ASSESSMENT:
• Volatility Risk: {volatility_risk}
• Liquidity Risk: {liquidity_risk}
• Time-of-Day Risk: {time_risk}
• Overall Risk Score: {overall_risk}/10
• Recommended Action: {self._recommend_risk_action(overall_risk)}"""

    def send_live_commentary(self, commentary: str, priority: str = "INFO") -> bool:
        """Send live commentary to Telegram."""
        try:
            message_data = {
                'chat_id': self.chat_id,
                'text': commentary,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(self.telegram_url, json=message_data, timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ Telegram commentary sent ({priority})")
                return True
            else:
                logger.error(f"❌ Telegram send failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending commentary: {e}")
            return False

    # Helper methods for analysis
    def _determine_market_regime(self, price_change_pct: float, pcr: float) -> str:
        """Determine current market regime."""
        if abs(price_change_pct) < 0.05:
            return "CONSOLIDATION"
        elif price_change_pct > 0.1 and pcr < 0.8:
            return "BULLISH_BREAKOUT"
        elif price_change_pct < -0.1 and pcr > 1.2:
            return "BEARISH_BREAKDOWN"
        else:
            return "TRANSITION_PHASE"

    def _assess_volatility_state(self, price_change_pct: float) -> str:
        """Assess current volatility state."""
        abs_change = abs(price_change_pct)
        if abs_change > 0.5:
            return "HIGH_VOLATILITY"
        elif abs_change > 0.2:
            return "ELEVATED_VOLATILITY"
        elif abs_change > 0.05:
            return "NORMAL_VOLATILITY"
        else:
            return "LOW_VOLATILITY"

    def _analyze_volume_pattern(self, ce_vol: int, pe_vol: int, total_vol: int) -> str:
        """Analyze volume pattern."""
        if total_vol > 2000000:
            return "VOLUME_EXPLOSION"
        elif abs(ce_vol - pe_vol) > 500000:
            return "DIRECTIONAL_VOLUME"
        elif total_vol < 100000:
            return "LOW_VOLUME"
        else:
            return "BALANCED_VOLUME"

    def _interpret_volume_bias(self, volume_bias: int) -> str:
        """Interpret volume bias."""
        if volume_bias > 200000:
            return "STRONG_PE_BIAS"
        elif volume_bias > 50000:
            return "PE_BIAS"
        elif volume_bias < -200000:
            return "STRONG_CE_BIAS"
        elif volume_bias < -50000:
            return "CE_BIAS"
        else:
            return "BALANCED"

    def _detect_smart_money_patterns(self, price_change: float, volume_bias: int, ce_vol: int, pe_vol: int) -> str:
        """Detect smart money activity patterns."""
        # Bearish divergence: Price up but PE volume dominance
        if price_change > 0 and volume_bias > 100000:
            return "BEARISH_DIVERGENCE_DETECTED"
        # Bullish divergence: Price down but CE volume dominance
        elif price_change < 0 and volume_bias < -100000:
            return "BULLISH_DIVERGENCE_DETECTED"
        # High activity
        elif (ce_vol + pe_vol) > 1500000:
            return "HIGH_INSTITUTIONAL_ACTIVITY"
        else:
            return "NORMAL_ACTIVITY"

    def _analyze_price_volume_divergence(self, price_change: float, volume_bias: int) -> str:
        """Analyze price-volume divergence."""
        if price_change > 0 and volume_bias > 0:
            return "BEARISH_DIVERGENCE - Price up, PE volume up"
        elif price_change < 0 and volume_bias < 0:
            return "BULLISH_DIVERGENCE - Price down, CE volume up"
        elif price_change > 0 and volume_bias < 0:
            return "MOMENTUM_CONFIRMATION - Price and CE volume aligned"
        elif price_change < 0 and volume_bias > 0:
            return "MOMENTUM_CONFIRMATION - Price and PE volume aligned"
        else:
            return "NEUTRAL_RELATIONSHIP"

    def _calculate_support_levels(self, prices: List[float], current_price: float) -> List[float]:
        """Calculate support levels."""
        support_levels = []
        sorted_prices = sorted([p for p in prices if p < current_price], reverse=True)

        if len(sorted_prices) >= 2:
            support_levels = sorted_prices[:2]
        else:
            # Estimate support levels
            support_levels = [current_price - 10, current_price - 25]

        return support_levels

    def _calculate_resistance_levels(self, prices: List[float], current_price: float) -> List[float]:
        """Calculate resistance levels."""
        resistance_levels = []
        sorted_prices = sorted([p for p in prices if p > current_price])

        if len(sorted_prices) >= 2:
            resistance_levels = sorted_prices[:2]
        else:
            # Estimate resistance levels
            resistance_levels = [current_price + 10, current_price + 25]

        return resistance_levels

    def _calculate_confidence_breakdown(self, analysis_data: Dict) -> str:
        """Calculate confidence breakdown."""
        score = analysis_data.get('score', 0)
        if abs(score) > 7:
            return "VERY_HIGH"
        elif abs(score) > 5:
            return "HIGH"
        elif abs(score) > 3:
            return "MEDIUM"
        else:
            return "LOW"

    def _determine_current_market_phase(self, volume_analysis: Dict, pattern_detection: Dict) -> str:
        """Determine current market phase."""
        if pattern_detection.get('bearish_divergence'):
            return "BEARISH_TRAP_SETUP"
        elif pattern_detection.get('bullish_divergence'):
            return "BULLISH_OPPORTUNITY"
        elif pattern_detection.get('volume_explosion'):
            return "HIGH_ACTIVITY_PHASE"
        else:
            return "NORMAL_TRADING_PHASE"

    def _calculate_phase_probability(self, phase: str) -> int:
        """Calculate phase probability."""
        phase_probabilities = {
            "BEARISH_TRAP_SETUP": 85,
            "BULLISH_OPPORTUNITY": 85,
            "HIGH_ACTIVITY_PHASE": 75,
            "NORMAL_TRADING_PHASE": 60
        }
        return phase_probabilities.get(phase, 50)

    def _calculate_overall_risk_score(self, volatility_risk, liquidity_risk, time_risk, market_state):
        """Calculate overall risk score for the market."""
        try:
            risk_score = 5  # Base risk score

            # Volatility risk assessment
            if len(market_state.market_history) >= 2:
                current = market_state.market_history[-1]
                previous = market_state.market_history[-2]
                price_change_pct = abs((current.get('underlying_value', 0) - previous.get('underlying_value', 0)) / previous.get('underlying_value', 1)) * 100
                
                if price_change_pct > 1.0:
                    risk_score += 2
                elif price_change_pct > 0.5:
                    risk_score += 1
            
            # Volume risk assessment
            if len(market_state.market_history) >= 1:
                current = market_state.market_history[-1]
                total_vol = current.get('total_ce_volume', 0) + current.get('total_pe_volume', 0)
                
                if total_vol < 500000:  # Low liquidity
                    risk_score += 2
                elif total_vol > 5000000:  # Very high volume
                    risk_score += 1
            
            # Time-based risk
            current_time = datetime.now().time()
            if current_time < dt_time(9, 30) or current_time > dt_time(15, 15):
                risk_score += 1
            
            return min(10, max(1, risk_score))
            
        except Exception as e:
            logger.error(f"❌ Error calculating risk score: {e}")
            return 5

    # Additional helper methods with default implementations
    def _assess_institutional_activity(self, total_vol: int, volume_bias: int) -> str:
        return "HIGH" if total_vol > 1000000 else "MODERATE" if total_vol > 500000 else "LOW"

    def _analyze_oi_pattern(self, ce_oi: int, pe_oi: int, total_oi: int) -> str:
        return "BUILDING" if total_oi > 50000 else "STABLE" if total_oi > -50000 else "DECLINING"

    def _assess_market_commitment(self, total_oi: int) -> str:
        return "HIGH" if total_oi > 100000 else "MODERATE" if total_oi > 25000 else "LOW"

    def _assess_new_money_flow(self, ce_oi: int, pe_oi: int) -> str:
        if ce_oi > 50000 and pe_oi > 50000:
            return "BOTH_SIDES"
        elif ce_oi > 50000:
            return "BULLISH_FLOW"
        elif pe_oi > 50000:
            return "BEARISH_FLOW"
        else:
            return "MINIMAL"

    def _assess_institutional_positioning(self, volume_bias: int, price_change: float) -> str:
        if volume_bias > 100000:
            return "BEARISH_POSITIONING"
        elif volume_bias < -100000:
            return "BULLISH_POSITIONING"
        else:
            return "NEUTRAL_POSITIONING"

    def _assess_retail_vs_smart_money(self, analysis_data: Dict) -> str:
        triggers = analysis_data.get('triggers', [])
        if any('DIVERGENCE' in str(trigger) for trigger in triggers):
            return "SMART_MONEY_DOMINANT"
        else:
            return "BALANCED_PARTICIPATION"

    def _analyze_decision_factors(self, triggers: List[str]) -> str:
        if not triggers:
            return "NO_CLEAR_FACTORS"

        primary_factors = []
        for trigger in triggers[:3]:  # Top 3 factors
            trigger_str = str(trigger)
            if 'VOLUME' in trigger_str:
                primary_factors.append("Volume")
            elif 'DIVERGENCE' in trigger_str:
                primary_factors.append("Divergence")
            elif 'PCR' in trigger_str:
                primary_factors.append("PCR")
            else:
                primary_factors.append("Technical")

        return ", ".join(primary_factors) if primary_factors else "Mixed Signals"

    def _assess_algorithm_agreement(self, analysis_data: Dict) -> str:
        score = abs(analysis_data.get('score', 0))
        if score > 7:
            return "STRONG_CONSENSUS"
        elif score > 4:
            return "MODERATE_AGREEMENT"
        else:
            return "MIXED_SIGNALS"

    def _predict_next_move(self, current_phase: str, analysis_data: Dict) -> str:
        if current_phase == "BEARISH_TRAP_SETUP":
            return "EXPECT_DOWNWARD_MOVE"
        elif current_phase == "BULLISH_OPPORTUNITY":
            return "EXPECT_UPWARD_MOVE"
        else:
            return "CONTINUE_MONITORING"

    def _get_active_pattern_alerts(self, pattern_detection: Dict) -> str:
        alerts = []
        if pattern_detection.get('bearish_divergence'):
            alerts.append("Bearish Divergence")
        if pattern_detection.get('bullish_divergence'):
            alerts.append("Bullish Divergence")
        if pattern_detection.get('volume_explosion'):
            alerts.append("Volume Explosion")

        return ", ".join(alerts) if alerts else "None"

    def _assess_volatility_risk(self, market_state) -> str:
        try:
            atr = market_state.get_atr() if hasattr(market_state, 'get_atr') else 30
            if atr > 80:
                return "HIGH"
            elif atr > 40:
                return "MEDIUM"
            else:
                return "LOW"
        except:
            return "MEDIUM"

    def _assess_liquidity_risk(self, current: Dict) -> str:
        total_vol = current.get('total_ce_volume', 0) + current.get('total_pe_volume', 0)
        if total_vol < 100000:
            return "HIGH"
        elif total_vol < 500000:
            return "MEDIUM"
        else:
            return "LOW"

    def _assess_time_of_day_risk(self) -> str:
        current_time = datetime.now().time()
        # Market open/close times have higher risk
        if dt_time(9, 15) <= current_time <= dt_time(9, 45) or dt_time(15, 00) <= current_time <= dt_time(15, 30):
            return "HIGH"
        elif dt_time(11, 30) <= current_time <= dt_time(13, 00):
            return "MEDIUM"  # Lunch time
        else:
            return "LOW"

    def _recommend_risk_action(self, risk_score: int) -> str:
        if risk_score >= 8:
            return "AVOID_TRADING"
        elif risk_score >= 6:
            return "REDUCE_POSITION_SIZE"
        elif risk_score >= 4:
            return "NORMAL_CAUTION"
        else:
            return "FAVORABLE_CONDITIONS"
#=============================================================================
# PART 3: MAIN ANALYSIS METHODS
#=============================================================================

    def analyze_trade_with_ai_intelligence(self, trade_outcome: Dict, market_data: Dict, ai_analysis: Dict) -> str:
        """Enhanced trade analysis that learns from AI intelligence patterns."""

        # SECTION 3.1: Store Comprehensive Trade Data
        comprehensive_trade_data = {
            "timestamp": datetime.now().isoformat(),
            "trade_outcome": trade_outcome,
            "market_data": market_data,
            "ai_analysis": ai_analysis,
            "volume_analysis": ai_analysis.get("volume_analysis", {}),
            "oi_analysis": ai_analysis.get("oi_analysis", {}),
            "market_phase": ai_analysis.get("market_phase", {}),
            "move_authenticity": ai_analysis.get("move_type", {})
        }

        # SECTION 3.2: Update History and Metrics
        self.trade_history.append(comprehensive_trade_data)
        self.update_enhanced_performance_metrics(trade_outcome, ai_analysis)

        # SECTION 3.3: Route to Appropriate Analysis
        if trade_outcome.get("result", "") == "LOSS":
            return self._analyze_ai_enhanced_mistake(comprehensive_trade_data)
        else:
            return self._analyze_ai_enhanced_success(comprehensive_trade_data)

    def analyze_trade_mistake(self, trade_outcome: Dict, market_conditions: Dict, timeframe_analysis: Dict) -> str:
        """Backward compatibility method for basic mistake analysis."""
        # Convert to new format and call enhanced method
        ai_analysis = {
            "volume_analysis": {"pattern": "UNKNOWN", "strength": "MEDIUM"},
            "oi_analysis": {"pattern": "UNKNOWN", "strength": "MEDIUM"},
            "market_phase": {"phase": "UNKNOWN", "confidence": 50}
        }

        return self.analyze_trade_with_ai_intelligence(trade_outcome, market_conditions, ai_analysis)

#=============================================================================
# PART 4: MISTAKE ANALYSIS SYSTEM
#=============================================================================

    def _analyze_ai_enhanced_mistake(self, trade_data: Dict) -> str:
        """Advanced mistake analysis using AI intelligence patterns."""

        # SECTION 4.1: Extract Analysis Components
        trade_outcome = trade_data["trade_outcome"]
        ai_analysis = trade_data["ai_analysis"]
        volume_analysis = ai_analysis.get("volume_analysis", {})
        oi_analysis = ai_analysis.get("oi_analysis", {})
        market_phase = ai_analysis.get("market_phase", {})

        # SECTION 4.2: Identify Mistake Pattern
        mistake_type = self._identify_ai_enhanced_mistake_pattern(
            trade_outcome, volume_analysis, oi_analysis, market_phase
        )

        # SECTION 4.3: Store Pattern for Learning
        self.mistake_patterns[mistake_type] = self.mistake_patterns.get(mistake_type, 0) + 1

        # SECTION 4.4: Learn from Volume-OI Relationship
        if volume_analysis and oi_analysis:
            volume_oi_lesson = self._learn_from_volume_oi_mistake(
                volume_analysis, oi_analysis, trade_outcome
            )
            self.volume_oi_patterns.append(volume_oi_lesson)

        # SECTION 4.5: Learn from Market Phase
        if market_phase:
            self._learn_from_phase_mistake(market_phase, trade_outcome)
            phase_name = market_phase.get("phase", "UNKNOWN")
            if phase_name not in self.market_phase_outcomes:
                self.market_phase_outcomes[phase_name] = {"wins": 0, "losses": 0}
            self.market_phase_outcomes[phase_name]["losses"] += 1

        # SECTION 4.6: Generate Improvement Plan
        improvement = self._generate_ai_enhanced_improvement(
            mistake_type, volume_analysis, oi_analysis, market_phase
        )

        # SECTION 4.7: Enhanced Logging
        self._log_ai_enhanced_mistake_analysis(
            mistake_type, trade_outcome, volume_analysis, oi_analysis, market_phase, improvement
        )

        return f"🧠 AI LEARNED: {mistake_type} → {improvement}"

    def _identify_ai_enhanced_mistake_pattern(self, trade_outcome: Dict, volume_analysis: Dict,
                                           oi_analysis: Dict, market_phase: Dict) -> str:
        """Enhanced mistake pattern identification using AI intelligence."""

        # SECTION 4.8: Extract Key Metrics
        pnl = abs(trade_outcome.get("pnl", 0))
        phase = market_phase.get("phase", "UNKNOWN")
        volume_pattern = volume_analysis.get("pattern", "UNKNOWN")
        oi_pattern = oi_analysis.get("pattern", "UNKNOWN")

        # SECTION 4.9: AI-Based Pattern Recognition

        # Critical Pattern 1: Volume-OI Trap (Your -9.65% loss pattern)
        if volume_pattern == "FAKE_SPIKE" and oi_pattern == "FLAT_OI":
            return "VOLUME_OI_TRAP_PATTERN"

        # Critical Pattern 2: Institutional Trap
        elif phase == "FAKE_BREAKOUT_TRAP":
            return "INSTITUTIONAL_TRAP_ENTRY"

        # Critical Pattern 3: Premature Entry
        elif volume_analysis.get("sustainability", 0) < 0.5:
            return "PREMATURE_ENTRY_NO_CONFIRMATION"

        # Critical Pattern 4: Ignored Context
        elif phase in ["CONSOLIDATION_WITH_ACTIVITY", "SIDEWAYS_ACCUMULATION"]:
            return "IGNORED_CONSOLIDATION_CONTEXT"

        # Critical Pattern 5: Volume Explosion Trap
        elif volume_analysis.get("peak_volume", 0) > volume_analysis.get("avg_change", 1) * 3:
            return "VOLUME_EXPLOSION_TRAP"

        # Critical Pattern 6: OI Divergence
        elif oi_analysis.get("strength", "") == "LOW" and volume_analysis.get("strength", "") == "HIGH":
            return "OI_VOLUME_DIVERGENCE_IGNORED"

        # Critical Pattern 7: Counter-Trend
        elif "STRONG" in phase and trade_outcome.get("direction", "") == "COUNTER":
            return "COUNTER_TREND_IN_STRONG_PHASE"

        # Critical Pattern 8: High Volatility
        elif trade_outcome.get("market_volatility", 0) > 100:
            return "HIGH_VOLATILITY_MISJUDGMENT"

        else:
            return "GENERAL_AI_PATTERN_MISS"

#=============================================================================
# PART 5: SUCCESS ANALYSIS SYSTEM
#=============================================================================

    def _analyze_ai_enhanced_success(self, trade_data: Dict) -> str:
        """Analyze successful trades to identify winning patterns."""

        # SECTION 5.1: Extract Success Components
        trade_outcome = trade_data["trade_outcome"]
        ai_analysis = trade_data["ai_analysis"]
        volume_analysis = ai_analysis.get("volume_analysis", {})
        oi_analysis = ai_analysis.get("oi_analysis", {})
        market_phase = ai_analysis.get("market_phase", {})

        # SECTION 5.2: Identify Success Pattern
        success_type = self._identify_success_pattern(
            trade_outcome, volume_analysis, oi_analysis, market_phase
        )

        # SECTION 5.3: Learn from Success
        if market_phase:
            phase_name = market_phase.get("phase", "UNKNOWN")
            if phase_name not in self.market_phase_outcomes:
                self.market_phase_outcomes[phase_name] = {"wins": 0, "losses": 0}
            self.market_phase_outcomes[phase_name]["wins"] += 1

        # SECTION 5.4: Store Successful Pattern
        if volume_analysis and oi_analysis:
            success_lesson = self._learn_from_volume_oi_success(
                volume_analysis, oi_analysis, trade_outcome
            )
            self.volume_oi_patterns.append(success_lesson)

        # SECTION 5.5: Log Success Analysis
        self._log_success_analysis(success_type, trade_outcome, volume_analysis, oi_analysis, market_phase)

        return f"🎯 AI SUCCESS: {success_type} - Pattern stored for replication"

    def _identify_success_pattern(self, trade_outcome: Dict, volume_analysis: Dict,
                                oi_analysis: Dict, market_phase: Dict) -> str:
        """Identify successful trading patterns."""

        pnl = trade_outcome.get("pnl", 0)
        phase = market_phase.get("phase", "UNKNOWN")
        volume_pattern = volume_analysis.get("pattern", "UNKNOWN")
        oi_pattern = oi_analysis.get("pattern", "UNKNOWN")

        # SECTION 5.6: Success Pattern Classification
        if pnl > 15 and volume_pattern == "SUSTAINED_INCREASE" and oi_pattern == "STRONG_OI_BUILD":
            return "PERFECT_VOLUME_OI_BREAKOUT"
        elif phase == "GENUINE_BREAKOUT" and pnl > 10:
            return "SUCCESSFUL_BREAKOUT_CAPTURE"
        elif volume_pattern == "GRADUAL_BUILD" and pnl > 8:
            return "PATIENT_ACCUMULATION_SUCCESS"
        elif phase == "PULLBACK_OR_CORRECTION" and pnl > 5:
            return "SUCCESSFUL_PULLBACK_ENTRY"
        else:
            return "GENERAL_SUCCESS_PATTERN"

#=============================================================================
# PART 6: LEARNING SYSTEM - VOLUME-OI PATTERNS
#=============================================================================

    def _learn_from_volume_oi_mistake(self, volume_analysis: Dict, oi_analysis: Dict, trade_outcome: Dict) -> Dict:
        """Learn specific lessons from volume-OI relationship mistakes."""

        volume_pattern = volume_analysis.get("pattern", "")
        oi_pattern = oi_analysis.get("pattern", "")
        pnl = trade_outcome.get("pnl", 0)

        lesson = {
            "timestamp": datetime.now().isoformat(),
            "volume_pattern": volume_pattern,
            "oi_pattern": oi_pattern,
            "combination": f"{volume_pattern}_{oi_pattern}",
            "outcome": "LOSS",
            "pnl_impact": pnl,
            "lesson": self._generate_volume_oi_lesson(volume_pattern, oi_pattern)
        }

        return lesson

    def _learn_from_volume_oi_success(self, volume_analysis: Dict, oi_analysis: Dict, trade_outcome: Dict) -> Dict:
        """Learn from successful volume-OI combinations."""

        volume_pattern = volume_analysis.get("pattern", "")
        oi_pattern = oi_analysis.get("pattern", "")
        pnl = trade_outcome.get("pnl", 0)

        lesson = {
            "timestamp": datetime.now().isoformat(),
            "volume_pattern": volume_pattern,
            "oi_pattern": oi_pattern,
            "combination": f"{volume_pattern}_{oi_pattern}",
            "outcome": "WIN",
            "pnl_impact": pnl,
            "lesson": self._generate_success_volume_oi_lesson(volume_pattern, oi_pattern)
        }

        return lesson

    def _generate_volume_oi_lesson(self, volume_pattern: str, oi_pattern: str) -> str:
        """Generate specific lessons from volume-OI combinations."""

        volume_oi_lessons = {
            ("FAKE_SPIKE", "FLAT_OI"): "NEVER_TRADE_HIGH_VOLUME_FLAT_OI - Classic trap pattern",
            ("SUSTAINED_INCREASE", "FLAT_OI"): "WAIT_FOR_OI_CONFIRMATION - Volume needs OI support",
            ("LOW_VOLUME", "STRONG_OI_BUILD"): "STEALTH_ACCUMULATION - Watch for breakout opportunity"
        }

        return volume_oi_lessons.get((volume_pattern, oi_pattern),
                                   "ANALYZE_VOLUME_OI_ALIGNMENT - Both must support trade direction")

    def _generate_success_volume_oi_lesson(self, volume_pattern: str, oi_pattern: str) -> str:
        """Generate lessons from successful volume-OI combinations."""

        success_lessons = {
            ("SUSTAINED_INCREASE", "STRONG_OI_BUILD"): "REPLICATE_SUSTAINED_VOLUME_STRONG_OI - Perfect breakout pattern",
            ("GRADUAL_BUILD", "MODERATE_OI_BUILD"): "PATIENT_ACCUMULATION_WORKS - Wait for gradual build patterns",
            ("LOW_VOLUME", "STRONG_OI_BUILD"): "STEALTH_ACCUMULATION_SUCCESS - Smart money pattern profitable"
        }

        return success_lessons.get((volume_pattern, oi_pattern),
                                 "VOLUME_OI_ALIGNMENT_SUCCESS - Both indicators supported trade")

#=============================================================================
# PART 7: LEARNING SYSTEM - MARKET PHASES
#=============================================================================

    def _learn_from_phase_mistake(self, market_phase: Dict, trade_outcome: Dict) -> Dict:
        """Learn specific lessons from market phase mistakes."""

        phase = market_phase.get("phase", "UNKNOWN")
        pnl = trade_outcome.get("pnl", 0)

        phase_lesson = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "outcome": "LOSS",
            "pnl_impact": pnl,
            "lesson": self._generate_phase_lesson(phase, "LOSS"),
            "confidence": market_phase.get("confidence", 0)
        }

        return phase_lesson

    def _generate_phase_lesson(self, phase: str, outcome: str) -> str:
        """Generate lessons from market phase outcomes."""

        if outcome == "LOSS":
            phase_lessons = {
                "FAKE_BREAKOUT_TRAP": "AVOID_FAKE_BREAKOUTS - Wait for volume-OI confirmation",
                "CONSOLIDATION_WITH_ACTIVITY": "NO_TRADES_IN_CONSOLIDATION - High trap probability",
                "SIDEWAYS_ACCUMULATION": "WAIT_FOR_BREAKOUT - Don't trade sideways markets",
                "POTENTIAL_REVERSAL": "WAIT_FOR_REVERSAL_CONFIRMATION - Don't catch falling knives",
                "UNCLEAR_PHASE": "REQUIRE_CLEAR_SIGNALS - No trades in unclear markets"
            }
        else:
            phase_lessons = {
                "GENUINE_BREAKOUT": "REPLICATE_BREAKOUT_ENTRIES - High success pattern",
                "PULLBACK_OR_CORRECTION": "BUY_PULLBACKS_IN_TREND - Good entry opportunities",
                "BUILDING_MOMENTUM": "EARLY_MOMENTUM_ENTRIES - Catch trends early",
                "STEALTH_ACCUMULATION": "FOLLOW_SMART_MONEY - Institutional patterns work"
            }

        return phase_lessons.get(phase, f"LEARN_FROM_{phase}_{outcome}")

#=============================================================================
# PART 8: IMPROVEMENT GENERATION SYSTEM
#=============================================================================

    def _generate_ai_enhanced_improvement(self, mistake_type: str, volume_analysis: Dict,
                                        oi_analysis: Dict, market_phase: Dict) -> str:
        """Generate specific improvements based on AI analysis."""

        enhanced_improvements = {
            "VOLUME_OI_TRAP_PATTERN": "IMPLEMENT: Never enter when volume spikes but OI flat - Add mandatory OI confirmation filter",
            "INSTITUTIONAL_TRAP_ENTRY": "IMPLEMENT: 45-minute waiting rule + 2-candle confirmation before any breakout entry",
            "PREMATURE_ENTRY_NO_CONFIRMATION": "IMPLEMENT: Mandatory 15-minute volume sustainability check before entry",
            "IGNORED_CONSOLIDATION_CONTEXT": "IMPLEMENT: No trades during consolidation phases - Wait for clear breakout",
            "VOLUME_EXPLOSION_TRAP": "IMPLEMENT: Volume spike must be sustained for 30+ minutes with OI support",
            "OI_VOLUME_DIVERGENCE_IGNORED": "IMPLEMENT: Both volume AND OI must align - No single-indicator trades",
            "COUNTER_TREND_IN_STRONG_PHASE": "IMPLEMENT: Trend strength filter - No counter-trend in strong phases",
            "HIGH_VOLATILITY_MISJUDGMENT": "IMPLEMENT: ATR filter - Avoid trades when volatility > 80",
            "GENERAL_AI_PATTERN_MISS": "IMPLEMENT: Improve AI pattern recognition training"
        }

        return enhanced_improvements.get(mistake_type, "Review AI pattern recognition logic")

#=============================================================================
# PART 9: PERFORMANCE METRICS SYSTEM
#=============================================================================

    def update_performance_metrics(self, trade_outcome: Dict):
        """Update basic performance tracking metrics."""
        self.performance_metrics["total_trades"] += 1
        pnl = trade_outcome.get("pnl", 0)

        if trade_outcome.get("result", "") == "WIN":
            wins = self.performance_metrics["winning_trades"] + 1
            self.performance_metrics["winning_trades"] = wins

            # Update best trade
            if pnl > self.performance_metrics["best_trade"]:
                self.performance_metrics["best_trade"] = pnl

            # Update average profit (safe division)
            if wins > 1:
                total_profits = self.performance_metrics["avg_profit"] * (wins - 1)
                self.performance_metrics["avg_profit"] = (total_profits + pnl) / wins
            else:
                self.performance_metrics["avg_profit"] = pnl
        else:
            losses = self.performance_metrics["losing_trades"] + 1
            self.performance_metrics["losing_trades"] = losses

            # Update worst trade
            if pnl < self.performance_metrics["worst_trade"]:
                self.performance_metrics["worst_trade"] = pnl

            # Update average loss (safe division)
            if losses > 1:
                total_losses = self.performance_metrics["avg_loss"] * (losses - 1)
                self.performance_metrics["avg_loss"] = (total_losses + pnl) / losses
            else:
                self.performance_metrics["avg_loss"] = pnl

        # Calculate win rate (safe division)
        total = self.performance_metrics["total_trades"]
        wins = self.performance_metrics["winning_trades"]
        self.performance_metrics["win_rate"] = (wins / total) * 100 if total > 0 else 0

        logger.info("📊 PERFORMANCE UPDATE - Win Rate: %.1f%% (%d/%d trades)",
                   self.performance_metrics["win_rate"], wins, total)

    def update_enhanced_performance_metrics(self, trade_outcome: Dict, ai_analysis: Dict):
        """Update metrics including AI-specific performance indicators."""

        # Update basic metrics first
        self.update_performance_metrics(trade_outcome)

        # Extract AI-specific data
        market_phase = ai_analysis.get("market_phase", {}).get("phase", "")
        move_authenticity = ai_analysis.get("move_type", {}).get("assessment", "")

        # Track AI-specific metrics
        if market_phase == "FAKE_BREAKOUT_TRAP":
            if trade_outcome.get("result", "") != "LOSS":
                self.trap_avoidance_rate += 1

        if market_phase == "GENUINE_BREAKOUT":
            if trade_outcome.get("result", "") == "WIN":
                self.breakout_capture_rate += 1

        volume_pattern = ai_analysis.get("volume_analysis", {}).get("pattern", "")
        if volume_pattern and trade_outcome.get("result", "") == "WIN":
            self.volume_pattern_accuracy += 1

        if market_phase and trade_outcome.get("result", "") == "WIN":
            self.phase_detection_accuracy += 1

#=============================================================================
# PART 10: ANALYTICS AND ALIGNMENT SYSTEM
#=============================================================================

    def _check_volume_oi_alignment(self, volume_analysis: Dict, oi_analysis: Dict) -> str:
        """Check if volume and OI are aligned."""

        vol_strength = volume_analysis.get("strength", "")
        oi_strength = oi_analysis.get("strength", "")

        alignment_matrix = {
            ("HIGH", "HIGH"): "ALIGNED_STRONG",
            ("HIGH", "LOW"): "DIVERGED_TRAP_PATTERN",
            ("HIGH", "MEDIUM"): "DIVERGED_TRAP_PATTERN",
            ("LOW", "HIGH"): "STEALTH_ACCUMULATION",
            ("MEDIUM", "HIGH"): "STEALTH_ACCUMULATION"
        }

        return alignment_matrix.get((vol_strength, oi_strength), "MIXED_SIGNALS")

    def should_avoid_trade_based_on_learning(self, ai_analysis: Dict) -> Tuple[bool, str]:
        """Use learning to determine if a trade should be avoided."""

        market_phase = ai_analysis.get("market_phase", {}).get("phase", "")
        volume_pattern = ai_analysis.get("volume_analysis", {}).get("pattern", "")
        oi_pattern = ai_analysis.get("oi_analysis", {}).get("pattern", "")

        # Check critical trap patterns
        if volume_pattern == "FAKE_SPIKE" and oi_pattern == "FLAT_OI":
            return True, "LEARNED: Volume-OI trap pattern detected - avoiding like your -9.65% loss"

        if market_phase == "FAKE_BREAKOUT_TRAP":
            return True, "LEARNED: Institutional trap detected - waiting for confirmation"

        # Check phase success rates
        phase_success_rates = self._calculate_phase_success_rates()
        if market_phase in phase_success_rates and phase_success_rates[market_phase] < 30:
            return True, f"LEARNED: {market_phase} has {phase_success_rates[market_phase]:.1f}% success rate"

        return False, "No learning-based avoidance triggers"

#=============================================================================
# PART 11: LOGGING SYSTEM
#=============================================================================

    def _log_ai_enhanced_mistake_analysis(self, mistake_type: str, trade_outcome: Dict,
                                        volume_analysis: Dict, oi_analysis: Dict,
                                        market_phase: Dict, improvement: str):
        """Enhanced logging with AI intelligence details."""

        logger.error("🔍 AI-ENHANCED TRADE MISTAKE ANALYSIS")
        logger.error("="*70)
        logger.error("❌ AI Mistake Type: %s", mistake_type)
        logger.error("💸 PnL Impact: %.2f%%", trade_outcome.get("pnl", 0))
        logger.error("📊 Volume Pattern: %s", volume_analysis.get("pattern", "Unknown"))
        logger.error("🎯 OI Pattern: %s", oi_analysis.get("pattern", "Unknown"))
        logger.error("🌊 Market Phase: %s", market_phase.get("phase", "Unknown"))
        logger.error("📈 Volume-OI Alignment: %s", self._check_volume_oi_alignment(volume_analysis, oi_analysis))
        logger.error("💡 AI Improvement: %s", improvement)
        logger.error("🔄 Pattern Frequency: %d occurrences", self.mistake_patterns.get(mistake_type, 0))
        logger.error("="*70)

    def _log_success_analysis(self, success_type: str, trade_outcome: Dict,
                            volume_analysis: Dict, oi_analysis: Dict, market_phase: Dict):
        """Log successful trade analysis."""

        logger.info("✅ AI-ENHANCED SUCCESS ANALYSIS")
        logger.info("="*70)
        logger.info("🎯 Success Type: %s", success_type)
        logger.info("💰 PnL Achieved: %.2f%%", trade_outcome.get("pnl", 0))
        logger.info("📊 Volume Pattern: %s", volume_analysis.get("pattern", "Unknown"))
        logger.info("🎯 OI Pattern: %s", oi_analysis.get("pattern", "Unknown"))
        logger.info("🌊 Market Phase: %s", market_phase.get("phase", "Unknown"))
        logger.info("📈 Volume-OI Alignment: %s", self._check_volume_oi_alignment(volume_analysis, oi_analysis))
        logger.info("="*70)

#=============================================================================
# PART 12: SUMMARY AND REPORTING SYSTEM
#=============================================================================

    def get_learning_summary(self) -> Dict[str, Any]:
        """Generate basic learning summary."""
        return {
            "performance": self.performance_metrics,
            "top_mistakes": dict(sorted(self.mistake_patterns.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recent_insights": list(self.learning_insights)[-10:],
            "learning_trend": "IMPROVING" if len(self.trade_history) > 10 and sum(1 for t in list(self.trade_history)[-10:] if t["trade_outcome"].get("result") == "WIN") > 6 else "NEEDS_WORK"
        }

    def get_ai_enhanced_learning_summary(self) -> Dict[str, Any]:
        """Get comprehensive learning summary with AI intelligence insights."""

        base_summary = self.get_learning_summary()

        ai_insights = {
            "volume_oi_lessons": list(self.volume_oi_patterns)[-5:],
            "trap_avoidance_rate": self.trap_avoidance_rate,
            "breakout_capture_rate": self.breakout_capture_rate,
            "phase_success_rates": self._calculate_phase_success_rates(),
            "top_ai_mistakes": self._get_top_ai_mistake_patterns(),
            "volume_oi_accuracy": self.volume_pattern_accuracy,
            "institutional_pattern_detection": len(self.institutional_patterns),
            "phase_detection_accuracy": self.phase_detection_accuracy
        }

        base_summary.update(ai_insights)
        return base_summary

    def _calculate_phase_success_rates(self) -> Dict[str, float]:
        """Calculate success rates for different market phases."""

        success_rates = {}
        for phase, outcomes in self.market_phase_outcomes.items():
            total = outcomes["wins"] + outcomes["losses"]
            success_rates[phase] = (outcomes["wins"] / total) * 100 if total > 0 else 0.0

        return success_rates

    def _get_top_ai_mistake_patterns(self) -> List[Tuple[str, int]]:
        """Get the most common AI-identified mistake patterns."""

        ai_mistakes = {k: v for k, v in self.mistake_patterns.items()
                      if any(pattern in k for pattern in ["VOLUME_OI", "TRAP", "AI", "PHASE"])}

        return sorted(ai_mistakes.items(), key=lambda x: x[1], reverse=True)[:5]

#=============================================================================
# PART 13: UTILITY AND COMPATIBILITY METHODS
#=============================================================================

    def get_current_brain_weights(self) -> Dict[str, float]:
        """Get current AI brain weights for logging."""
        return self.ai_brain_weights.copy()

    def print_learning_summary(self):
        """Print comprehensive learning summary."""
        summary = self.get_ai_enhanced_learning_summary()

        print("\n" + "="*80)
        print("🧠 AI-ENHANCED LEARNING SUMMARY")
        print("="*80)

        # Performance metrics
        perf = summary["performance"]
        print(f"📊 PERFORMANCE METRICS:")
        print(f"   Total Trades: {perf['total_trades']}")
        print(f"   Win Rate: {perf['win_rate']:.1f}%")
        print(f"   Best Trade: {perf['best_trade']:.2f}%")
        print(f"   Worst Trade: {perf['worst_trade']:.2f}%")
        print(f"   Avg Profit: {perf['avg_profit']:.2f}%")
        print(f"   Avg Loss: {perf['avg_loss']:.2f}%")

        # AI-specific metrics
        print(f"\n🤖 AI INTELLIGENCE METRICS:")
        print(f"   Trap Avoidance Rate: {summary['trap_avoidance_rate']}")
        print(f"   Breakout Capture Rate: {summary['breakout_capture_rate']}")
        print(f"   Volume Pattern Accuracy: {summary['volume_oi_accuracy']}")
        print(f"   Phase Detection Accuracy: {summary['phase_detection_accuracy']}")

        # Top mistakes
        if summary['top_ai_mistakes']:
            print(f"\n❌ TOP AI MISTAKE PATTERNS:")
            for mistake, count in summary['top_ai_mistakes']:
                print(f"   {mistake}: {count} occurrences")

        # Phase success rates
        if summary['phase_success_rates']:
            print(f"\n🌊 MARKET PHASE SUCCESS RATES:")
            for phase, rate in summary['phase_success_rates'].items():
                print(f"   {phase}: {rate:.1f}%")

        print("="*80 + "\n")

#=============================================================================
# END OF ENHANCED SMART SELF-ANALYZER CLASS
#=============================================================================
# =============================================================================
# CONFIGURATION MANAGEMENT
# =============================================================================
def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file with comprehensive defaults if file is missing or invalid.
    This ensures the bot always has a complete config to run, even if the file is corrupted."""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        required = {"indices", "weights", "thresholds", "periods", "risk", "market_hours"} # Required keys for config
        if not all(k in config for k in required):
            raise ValueError("Config missing required sections")
        logger.info("✅ Configuration loaded successfully from %s", config_path)
        return config
    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        logger.warning(f"⚠️ Config load failed: {e}. Using enhanced defaults.") # Log warning if config fails
        return {
            "indices": ["NIFTY"], # ONLY NIFTY for testing as per your request
            "weights": {
                "max_pain_gravity": 2.5, "fear_gauge": 3.0, "oi_acceleration": 2.5,
                "rsi_momentum": 2.0, "historical_trend": 1.5
            }, # Default weights for AI predictions
            "thresholds": {
                "model_confidence": 0.75, "predictive_score": 5.0, # Slightly lower for more trades
                "pre_signal_score": 3.0, "confluence_required": 2, "momentum_accel": 2.0,
                "volatility_threshold": 80, # New: Max ATR for trades
                "timeframe_alignment": 0.7 # New: Required timeframe agreement
            }, # Enhanced thresholds for decisions
            "periods": {
                "cycle_duration": 150, "atr": 5, "history_max": 120, # Increased for more data
                "rsi_window": 14, "outlook_snapshots": [60, 50, 30, 18, 6],
                "thirty_min_window": 60, "timeframe_intervals": [3, 9, 15, 25, 30] # New: Multi-timeframe
            }, # Enhanced periods for calculations
            "risk": {
                "sl_percentage": 0.04, "target_percentage": 0.25, # Tighter SL, higher target
                "partial_target_portion": 0.4, "trail_profit_trigger": 8.0,
                "max_position_size": 5, "daily_loss_limit": -500 # New: Enhanced risk controls
            }, # Enhanced risk management
            "market_hours": {"start": "09:15", "end": "15:30"}, # Market open/close times
            "retry": {"max_attempts": 5, "wait_min": 2, "wait_max": 15}, # Enhanced retry settings
            "cooldown": {"cycles_after_trade": 3} # Increased cooldown
        }
def save_config(config: Dict[str, Any], config_path: str = "config.yaml") -> None:
    """Save configuration to YAML file with proper formatting and backup.
    This persists changes like weight adjustments."""
    try:
        # Create backup of existing config
        if os.path.exists(config_path):
            backup_path = f"{config_path}.backup"
            os.rename(config_path, backup_path)
            logger.info("📁 Config backup created: %s", backup_path)
        with open(config_path, "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False) # Save with nice formatting
        logger.info("💾 Configuration saved successfully to %s", config_path)
    except Exception as e:
        logger.error("❌ Failed to save config: %s", e)
# =============================================================================
# ENHANCED SELF-CORRECTION WITH ML INTEGRATION
# =============================================================================
def self_correct(
    trade_outcome: Dict[str, Any],
    features_at_entry: Dict[str, float],
    config: Dict[str, Any],
    learning_rate: float = 0.05
) -> Dict[str, Any]:
    """Advanced AI self-correction that adjusts model weights and retrains ML models.
    This makes the bot continuously self-learning by tweaking based on wins/losses."""
    logger.info("🔧 INITIATING SELF-CORRECTION PROCESS")
    logger.info("=" * 60)

    weights = config["weights"].copy()
    prediction = trade_outcome["prediction"]
    was_correct = (prediction > 0 and trade_outcome["result"] == "WIN") or \
                  (prediction < 0 and trade_outcome["result"] == "WIN")
    logger.info("🎯 Trade Outcome: %s | Prediction: %.2f | Correct: %s",
                trade_outcome["result"], prediction, was_correct)

    # Enhanced adjustment logic based on confidence and PnL
    base_adjustment = 1 + learning_rate if was_correct else 1 - learning_rate
    confidence_factor = trade_outcome.get("confidence", 0.5)
    pnl_factor = min(abs(trade_outcome.get("pnl", 0)) / 100, 0.5)
    adjusted_rate = learning_rate * (1 + confidence_factor + pnl_factor)
    adjustment = 1 + adjusted_rate if was_correct else 1 - adjusted_rate

    logger.info("📊 Adjustment Details:")
    logger.info(" Base Learning Rate: %.4f", learning_rate)
    logger.info(" Confidence Factor: %.4f", confidence_factor)
    logger.info(" PnL Factor: %.4f", pnl_factor)
    logger.info(" Final Adjustment: %.4f", adjustment)

    # Apply adjustments to relevant features
    old_weights = weights.copy()
    for feature, value in features_at_entry.items():
        if value != 0 and feature in weights:
            weights[feature] *= adjustment
            weights[feature] = max(0.1, min(5.0, weights[feature]))  # Bound weights between 0.1 and 5.0

    # Advanced normalization to prevent runaway scaling
    total = sum(weights.values())
    if total > 0:
        for k in weights:
            weights[k] = (weights[k] / total) * len(weights)

    # Log weight changes
    logger.info("⚖️ Weight Adjustments:")
    for feature in weights:
        old_val = old_weights.get(feature, 0)
        new_val = weights[feature]
        change = new_val - old_val
        logger.info(" %s: %.4f → %.4f (Δ%.4f)", feature, old_val, new_val, change)

    config["weights"] = weights
    save_config(config)
    retrain_ml_model()
    logger.info("=" * 60)
    logger.info("✅ Self-correction completed successfully")
    return config
# =============================================================================
# ENHANCED ML TRAINING AND PREDICTION
# =============================================================================
def retrain_ml_model(model_path: str = MODEL_PATH):
    """
    Retrain the ML model on historical_data.json and save to MODEL_PATH.
    """
    if not os.path.exists("historical_data.json"):
        logger.warning("⚠️ No historical data found for ML training")
        return None
    try:
        with open("historical_data.json", "r") as f:
            history_data = json.load(f)
        if len(history_data) < 50:
            logger.warning("⚠️ Insufficient data for ML training (%d samples)", len(history_data))
            return None
        # prepare features & labels...
        # [your existing training code here]
        # after fitting scaler and model:
     # after fitting scaler and model:
        with open(model_path, 'wb') as f:
            pickle.dump({'model': model, 'scaler': scaler}, f)
        logger.info("🤖 Enhanced ML Model saved to: %s", model_path)

        return model
    except Exception as e:
        logger.error("❌ ML model training failed: %s", e)
        return None

def load_ml_model(model_path: str = MODEL_PATH):
    """Load ML model using pickle instead of joblib for Windows compatibility."""
    if not ML_AVAILABLE:
        logger.warning("⚠️ ML not available - returning dummy model")
        return None, None
        
    try:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            logger.info("✅ ML Model loaded successfully from: %s", model_path)
            return model_data.get('model'), model_data.get('scaler')
        else:
            logger.warning("⚠️ No ML model file found at: %s", model_path)
            return None, None
    except Exception as e:
        logger.error("❌ Failed to load ML model: %s", e)
        return None, None
    
# =============================================================================
# LIGHTWEIGHT NSE DATA FETCH (Enhanced with Proxy, 4x Warmup on Retry + Agent Rotation)
# =============================================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
]

ACCEPT_LANGS = ["en-US,en;q=0.9", "en-IN,en;q=0.8", "en-GB,en;q=0.7", "hi-IN,hi;q=0.6", "fr-FR,fr;q=0.5"]

async def fetch_single_chain_with_retry(symbol: str) -> Optional[Dict[str, Any]]:
    """Lightweight fetch with two-stage retry, 4x warmup on 401, agent rotation, and optional proxy.
    Returns parsed JSON dict if successful, otherwise None.
    """
    def do_fetch_stage(stage: str) -> Dict[str, Any]:
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        # Optional Proxy (uncomment and set a free proxy from free-proxy-list.net to change IP)
        # scraper.proxies = {'http': 'http://your_proxy_ip:port', 'https': 'http://your_proxy_ip:port'}
        scraper.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": random.choice(ACCEPT_LANGS),
            "Referer": "https://www.nseindia.com/option-chain",
            "Origin": "https://www.nseindia.com",
            "X-Requested-With": "XMLHttpRequest",
        })
        warmup_rounds = 1 if stage == "initial" else 4  # 4x on retry for stronger session reset
        for _ in range(warmup_rounds):
            scraper.get("https://www.nseindia.com", timeout=15)
        time.sleep(random.uniform(3.0, 5.0))  # Longer random delays
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        resp = scraper.get(url, timeout=15)
        if resp.status_code == 401:
            raise RuntimeError(f"{symbol} fetch failed with HTTP 401")
        if resp.status_code != 200:
            raise RuntimeError(f"{symbol} fetch failed with HTTP {resp.status_code}")
        js = resp.json()
        if not js or "records" not in js or "data" not in js["records"]:
            raise RuntimeError(f"{symbol} fetch returned invalid JSON")
        return js

    for stage in ("initial", "retry"):
        try:
            data = await asyncio.to_thread(do_fetch_stage, stage)
            logger.info(f"✅ Fetched data for {symbol}")
            return data
        except RuntimeError as e:
            if "HTTP 401" in str(e) and stage == "initial":
                logger.warning(f"⚠️ {symbol} initial stage 401 detected, retrying with 4x warmup...")
                await asyncio.sleep(5)  # Extra wait before retry
            else:
                logger.warning(f"⚠️ {symbol} {stage} stage failed: {e}")
            await asyncio.sleep(3)
        except Exception as e:
            logger.warning(f"⚠️ {symbol} {stage} stage failed: {e}")
            await asyncio.sleep(3)
    logger.error(f"❌ Failed to fetch {symbol} after retries")
    return None
# =============================================================================
# MISSING ENHANCED STRATEGY ENGINE CLASS - ADD THIS TO new3.py
# =============================================================================

class EnhancedStrategyEngine:
    """Enhanced Strategy Engine with progressive market analysis."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.progressive_thresholds = {
            'BASIC': {'bullish': 3.0, 'bearish': -3.0},
            'MEDIUM': {'bullish': 4.0, 'bearish': -4.0},
            'HIGH': {'bullish': 5.0, 'bearish': -5.0},
            'EXPERT': {'bullish': 6.0, 'bearish': -6.0}
        }
        self.analysis_history = deque(maxlen=100)
        self.commentary_bot = None  # Initialize as None
        logger.info("🤖 Enhanced Strategy Engine initialized")
    
    def analyze_market_progressive(self, market_state):
        """Enhanced progressive market analysis with 15-timeframe integration."""
        try:
            logger.info("🔄 Starting enhanced progressive market analysis...")
            
            # Initialize analysis result
            analysis_result = {
                'verdict': 'NEUTRAL',
                'score': 0.0,
                'confidence': 'LOW',
                'reasoning': [],
                'timeframe_analysis': {},
                'progressive_signals': {},
                'enhanced_verdict': 'NEUTRAL',
                'timestamp': datetime.now().isoformat()
            }
            
            # Check if we have enough data
            if len(market_state.market_history) < 3:
                analysis_result['reasoning'].append("Insufficient data for progressive analysis")
                return analysis_result
            
            # Get latest snapshot
            latest_snapshot = market_state.market_history[-1]
            
            # **1. BASIC MARKET ANALYSIS**
            basic_analysis = self.analyze_market_snapshot(latest_snapshot)
            if basic_analysis:
                analysis_result['verdict'] = basic_analysis.get('verdict', 'NEUTRAL')
                analysis_result['score'] = basic_analysis.get('score', 0.0)
                analysis_result['reasoning'].extend(basic_analysis.get('reasoning', []))
            
            # **2. TIMEFRAME ANALYSIS INTEGRATION**
            if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
                tf_analysis = market_state.current_analysis['timeframe_analysis']
                analysis_result['timeframe_analysis'] = tf_analysis
                
                # Calculate timeframe-based signals
                tf_signals = self._analyze_timeframe_signals(tf_analysis)
                analysis_result['progressive_signals']['timeframe_signals'] = tf_signals
                
                # Adjust score based on timeframe consensus
                if tf_signals['consensus'] != 'NEUTRAL':
                    consensus_boost = tf_signals['strength'] * 0.3
                    if tf_signals['consensus'] == analysis_result['verdict']:
                        analysis_result['score'] += consensus_boost
                        analysis_result['reasoning'].append(f"Timeframe consensus supports {tf_signals['consensus']}")
                    else:
                        analysis_result['score'] = max(0, analysis_result['score'] - consensus_boost)
                        analysis_result['reasoning'].append(f"Timeframe consensus conflicts: {tf_signals['consensus']} vs {analysis_result['verdict']}")
            
            # **3. MOMENTUM ANALYSIS**
            momentum_analysis = self._calculate_progressive_momentum(market_state.market_history)
            analysis_result['progressive_signals']['momentum'] = momentum_analysis
            
            if momentum_analysis['strength'] > 6.0:
                momentum_boost = (momentum_analysis['strength'] - 5.0) * 0.2
                if momentum_analysis['direction'] == analysis_result['verdict']:
                    analysis_result['score'] += momentum_boost
                    analysis_result['reasoning'].append(f"Strong {momentum_analysis['direction']} momentum detected")
            
            # **4. VOLUME FLOW ANALYSIS**
            volume_flow = self._analyze_volume_flow_progressive(market_state.market_history)
            analysis_result['progressive_signals']['volume_flow'] = volume_flow
            
            if volume_flow['signal_strength'] > 7.0:
                flow_boost = (volume_flow['signal_strength'] - 6.0) * 0.15
                if volume_flow['direction'] == analysis_result['verdict']:
                    analysis_result['score'] += flow_boost
                    analysis_result['reasoning'].append(f"Strong volume flow supports {volume_flow['direction']}")
            
            # **5. OI DIVERGENCE ANALYSIS**
            oi_divergence = self._analyze_oi_divergence_progressive(market_state.market_history)
            analysis_result['progressive_signals']['oi_divergence'] = oi_divergence
            
            if oi_divergence['divergence_strength'] > 6.5:
                div_adjustment = oi_divergence['divergence_strength'] * 0.1
                if oi_divergence['signal'] == 'BULLISH' and analysis_result['verdict'] == 'BULLISH':
                    analysis_result['score'] += div_adjustment
                elif oi_divergence['signal'] == 'BEARISH' and analysis_result['verdict'] == 'BEARISH':
                    analysis_result['score'] += div_adjustment
                else:
                    analysis_result['score'] = max(0, analysis_result['score'] - div_adjustment)
                
                analysis_result['reasoning'].append(f"OI divergence: {oi_divergence['signal']} ({oi_divergence['divergence_strength']:.1f}/10)")
            
            # **6. FINAL VERDICT CALCULATION**
            # Normalize score and determine final verdict
            analysis_result['score'] = min(10.0, max(0.0, analysis_result['score']))
            
            # Enhanced verdict based on progressive analysis
            if analysis_result['score'] >= 7.0:
                analysis_result['enhanced_verdict'] = analysis_result['verdict']
                analysis_result['confidence'] = 'HIGH'
            elif analysis_result['score'] >= 5.0:
                analysis_result['enhanced_verdict'] = analysis_result['verdict']
                analysis_result['confidence'] = 'MEDIUM'
            elif analysis_result['score'] >= 3.0:
                analysis_result['enhanced_verdict'] = 'WEAK_' + analysis_result['verdict']
                analysis_result['confidence'] = 'LOW'
            else:
                analysis_result['enhanced_verdict'] = 'NEUTRAL'
                analysis_result['confidence'] = 'VERY_LOW'
            
            # **7. CANDLE INTELLIGENCE INTEGRATION**
            # Add this check before using candle_system anywhere in the code
            if hasattr(self, 'candle_system') and self.candle_system is not None:
                # Use candle_system
                candle_data = self.candle_system.some_method()
            else:
                logger.warning("⚠️ Candle system is not available")
                candle_data = None
                if candle_data.get('status') == 'CANDLE_COMPLETED':
                    candle_rec = candle_data.get('trade_recommendation', {})
                    candle_confidence = candle_rec.get('confidence', 0)
                    
                    if candle_confidence > 0.7:  # 70% confidence
                        candle_action = candle_rec.get('action', 'WAIT')
                        if candle_action in ['BUY', 'STRONG_BUY'] and analysis_result['verdict'] == 'BULLISH':
                            analysis_result['score'] += 1.0
                            analysis_result['reasoning'].append(f"Candle intelligence supports BULLISH ({candle_confidence:.0%})")
                        elif candle_action in ['SELL', 'STRONG_SELL'] and analysis_result['verdict'] == 'BEARISH':
                            analysis_result['score'] += 1.0
                            analysis_result['reasoning'].append(f"Candle intelligence supports BEARISH ({candle_confidence:.0%})")
            
            # **8. QUALITY METRICS**
            analysis_result['data_quality'] = market_state.data_quality_score
            analysis_result['snapshots_analyzed'] = len(market_state.market_history)
            analysis_result['active_timeframes'] = len(analysis_result['timeframe_analysis'])
            
            logger.info(f"✅ Progressive analysis complete: {analysis_result['enhanced_verdict']} (Score: {analysis_result['score']:.2f})")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Progressive analysis error: {e}")
            logger.error(f"📍 Traceback: {traceback.format_exc()}")
            
            # Return fallback analysis
            return {
                'verdict': 'NEUTRAL',
                'score': 0.0,
                'confidence': 'ERROR',
                'reasoning': [f'Progressive analysis failed: {str(e)[:100]}'],
                'error': True,
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_timeframe_signals(self, timeframe_analysis):
        """Analyze signals from multiple timeframes."""
        try:
            bullish_count = 0
            bearish_count = 0
            total_strength = 0
            
            for tf, data in timeframe_analysis.items():
                if isinstance(data, dict):
                    momentum = data.get('momentum', 'NEUTRAL')
                    strength = data.get('strength_score', 0)
                    
                    if momentum == 'BULLISH':
                        bullish_count += 1
                    elif momentum == 'BEARISH':
                        bearish_count += 1
                        
                    total_strength += strength
            
            total_timeframes = len(timeframe_analysis)
            avg_strength = total_strength / max(1, total_timeframes)
            
            if bullish_count > bearish_count:
                consensus = 'BULLISH'
            elif bearish_count > bullish_count:
                consensus = 'BEARISH'
            else:
                consensus = 'NEUTRAL'
            
            return {
                'consensus': consensus,
                'bullish_count': bullish_count,
                'bearish_count': bearish_count,
                'strength': avg_strength,
                'total_timeframes': total_timeframes
            }
        except Exception as e:
            logger.error(f"Timeframe signals analysis error: {e}")
            return {'consensus': 'NEUTRAL', 'strength': 0, 'error': True}
    
    def _calculate_progressive_momentum(self, market_history):
        """Calculate momentum from recent market data."""
        try:
            if len(market_history) < 3:
                return {'direction': 'NEUTRAL', 'strength': 0}
            
            recent = list(market_history)[-3:]
            price_changes = []
            volume_changes = []
            
            for i in range(1, len(recent)):
                price_change = recent[i]['underlying_value'] - recent[i-1]['underlying_value']
                price_changes.append(price_change)
                
                vol_change = (recent[i]['CE_VOL'] + recent[i]['PE_VOL']) - (recent[i-1]['CE_VOL'] + recent[i-1]['PE_VOL'])
                volume_changes.append(vol_change)
            
            avg_price_change = sum(price_changes) / len(price_changes)
            avg_volume_change = sum(volume_changes) / len(volume_changes)
            
            # Calculate momentum strength (0-10)
            price_momentum = abs(avg_price_change) / (recent[-1]['underlying_value'] * 0.001)  # Normalize
            volume_momentum = abs(avg_volume_change) / max(1, recent[-1]['CE_VOL'] + recent[-1]['PE_VOL']) * 100
            
            strength = min(10, (price_momentum + volume_momentum) * 2)
            direction = 'BULLISH' if avg_price_change > 0 else 'BEARISH' if avg_price_change < 0 else 'NEUTRAL'
            
            return {
                'direction': direction,
                'strength': strength,
                'price_momentum': price_momentum,
                'volume_momentum': volume_momentum
            }
        except Exception as e:
            logger.error(f"Momentum calculation error: {e}")
            return {'direction': 'NEUTRAL', 'strength': 0, 'error': True}
    
    def _analyze_volume_flow_progressive(self, market_history):
        """Analyze volume flow patterns."""
        try:
            if len(market_history) < 3:
                return {'direction': 'NEUTRAL', 'signal_strength': 0}
            
            recent = list(market_history)[-3:]
            ce_flow_trend = []
            pe_flow_trend = []
            
            for i in range(1, len(recent)):
                ce_flow = recent[i]['CE_VOL'] - recent[i-1]['CE_VOL']
                pe_flow = recent[i]['PE_VOL'] - recent[i-1]['PE_VOL']
                ce_flow_trend.append(ce_flow)
                pe_flow_trend.append(pe_flow)
            
            avg_ce_flow = sum(ce_flow_trend) / len(ce_flow_trend)
            avg_pe_flow = sum(pe_flow_trend) / len(pe_flow_trend)
            
            # Calculate flow imbalance
            total_avg_flow = abs(avg_ce_flow) + abs(avg_pe_flow)
            if total_avg_flow > 0:
                ce_dominance = abs(avg_ce_flow) / total_avg_flow
                pe_dominance = abs(avg_pe_flow) / total_avg_flow
            else:
                ce_dominance = pe_dominance = 0.5
            
            # Determine signal strength (0-10)
            imbalance = abs(ce_dominance - pe_dominance)
            signal_strength = min(10, imbalance * 20)
            
            # Determine direction
            if avg_ce_flow > avg_pe_flow * 1.2:
                direction = 'BEARISH'  # More CE volume often indicates bearish sentiment
            elif avg_pe_flow > avg_ce_flow * 1.2:
                direction = 'BULLISH'  # More PE volume often indicates bullish sentiment
            else:
                direction = 'NEUTRAL'
            
            return {
                'direction': direction,
                'signal_strength': signal_strength,
                'ce_flow': avg_ce_flow,
                'pe_flow': avg_pe_flow,
                'imbalance': imbalance
            }
        except Exception as e:
            logger.error(f"Volume flow analysis error: {e}")
            return {'direction': 'NEUTRAL', 'signal_strength': 0, 'error': True}
    
    def _analyze_oi_divergence_progressive(self, market_history):
        """Analyze Open Interest divergence patterns."""
        try:
            if len(market_history) < 3:
                return {'signal': 'NEUTRAL', 'divergence_strength': 0}
            
            recent = list(market_history)[-3:]
            price_trend = []
            oi_ratio_trend = []
            
            for i in range(1, len(recent)):
                price_change = recent[i]['underlying_value'] - recent[i-1]['underlying_value']
                price_trend.append(price_change)
                
                # OI PCR trend
                current_pcr = recent[i]['PE_OI'] / max(1, recent[i]['CE_OI'])
                prev_pcr = recent[i-1]['PE_OI'] / max(1, recent[i-1]['CE_OI'])
                oi_ratio_change = current_pcr - prev_pcr
                oi_ratio_trend.append(oi_ratio_change)
            
            avg_price_change = sum(price_trend) / len(price_trend)
            avg_oi_ratio_change = sum(oi_ratio_trend) / len(oi_ratio_trend)
            
            # Check for divergence
            price_direction = 'UP' if avg_price_change > 0 else 'DOWN'
            oi_direction = 'UP' if avg_oi_ratio_change > 0 else 'DOWN'
            
            # Divergence strength calculation
            price_strength = abs(avg_price_change) / max(1, recent[-1]['underlying_value'] * 0.001)
            oi_strength = abs(avg_oi_ratio_change) * 10
            
            divergence_strength = min(10, (price_strength + oi_strength) / 2)
            
            # Determine signal
            if price_direction != oi_direction and divergence_strength > 3:
                if price_direction == 'UP' and oi_direction == 'DOWN':
                    signal = 'BEARISH'  # Price up but OI PCR down - potential reversal
                elif price_direction == 'DOWN' and oi_direction == 'UP':
                    signal = 'BULLISH'  # Price down but OI PCR up - potential reversal
                else:
                    signal = 'NEUTRAL'
            else:
                signal = 'NEUTRAL'
            
            return {
                'signal': signal,
                'divergence_strength': divergence_strength,
                'price_trend': price_direction,
                'oi_trend': oi_direction,
                'is_divergence': price_direction != oi_direction
            }
        except Exception as e:
            logger.error(f"OI divergence analysis error: {e}")
            return {'signal': 'NEUTRAL', 'divergence_strength': 0, 'error': True}
    
    def analyze_market_snapshot(self, snapshot):
        """Basic market snapshot analysis - fallback method."""
        try:
            analysis = {
                'verdict': 'NEUTRAL',
                'score': 5.0,
                'reasoning': []
            }
            
            # Basic PCR analysis
            oi_pcr = snapshot.get('OI_PCR', 1.0)
            vol_pcr = snapshot.get('VOL_PCR', 1.0)
            
            if oi_pcr > 1.2:
                analysis['verdict'] = 'BULLISH'
                analysis['score'] += 1.0
                analysis['reasoning'].append(f"High OI PCR: {oi_pcr:.3f}")
            elif oi_pcr < 0.8:
                analysis['verdict'] = 'BEARISH'
                analysis['score'] += 1.0
                analysis['reasoning'].append(f"Low OI PCR: {oi_pcr:.3f}")
            
            if vol_pcr > 1.2:
                if analysis['verdict'] == 'BULLISH':
                    analysis['score'] += 0.5
                analysis['reasoning'].append(f"High VOL PCR: {vol_pcr:.3f}")
            elif vol_pcr < 0.8:
                if analysis['verdict'] == 'BEARISH':
                    analysis['score'] += 0.5
                analysis['reasoning'].append(f"Low VOL PCR: {vol_pcr:.3f}")
            
            return analysis
        except Exception as e:
            logger.error(f"Basic snapshot analysis error: {e}")
            return {'verdict': 'NEUTRAL', 'score': 0.0, 'reasoning': ['Analysis failed'], 'error': True}
    
    def generate_progressive_recommendation(self, analysis, market_state, day_profile):
        """Generate progressive trading recommendation."""
        try:
            verdict = analysis.get('enhanced_verdict', 'NEUTRAL')
            confidence = analysis.get('confidence', 'LOW')
            score = analysis.get('score', 0.0)
            
            # Base recommendation
            if confidence == 'HIGH' and score >= 7.0:
                if verdict == 'BULLISH':
                    recommendation = "🟢 [HIGH CONFIDENCE] Strong bullish signals detected - Consider long positions"
                elif verdict == 'BEARISH':
                    recommendation = "🔴 [HIGH CONFIDENCE] Strong bearish signals detected - Consider short positions"
                else:
                    recommendation = "⚪ [NEUTRAL] Mixed signals - Wait for clearer direction"
            elif confidence == 'MEDIUM':
                if verdict == 'BULLISH':
                    recommendation = "🟡 [MODERATE] Moderate bullish bias - Small position sizes recommended"
                elif verdict == 'BEARISH':
                    recommendation = "🟡 [MODERATE] Moderate bearish bias - Small position sizes recommended"
                else:
                    recommendation = "⚪ [NEUTRAL] Sideways market - Range trading opportunities"
            else:
                recommendation = "🔍 [BASIC] No clear signals detected. Continue monitoring."
            
            return recommendation
            
        except Exception as e:
            logger.error(f"❌ Recommendation generation error: {e}")
            return "❌ Unable to generate recommendation"
    
    def manage_active_trade(self, analysis, day_profile, market_state):
        """Manage active trades based on current analysis."""
        try:
            if not hasattr(day_profile, 'active_trade') or not day_profile.active_trade:
                return {'verdict': 'NO_ACTIVE_TRADE'}
            
            # Basic trade management logic
            current_verdict = analysis.get('enhanced_verdict', 'NEUTRAL')
            trade_type = day_profile.active_trade.get('type', 'UNKNOWN')
            
            # Simple exit logic
            if (trade_type == 'LONG' and current_verdict == 'BEARISH') or \
               (trade_type == 'SHORT' and current_verdict == 'BULLISH'):
                return {'verdict': 'CONSIDER_EXIT', 'reason': f'Signal reversal: {current_verdict}'}
            
            return {'verdict': 'MONITORING', 'reason': 'Trade still valid'}
            
        except Exception as e:
            logger.error(f"❌ Trade management error: {e}")
            return {'verdict': 'ERROR', 'reason': str(e)}
    
    def save_snapshot_for_ai_training(self, snapshot, verdict):
        """Save snapshot for AI training."""
        try:
            # Basic implementation - extend as needed
            logger.info(f"💾 Saved snapshot for AI training: {verdict}")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving AI training data: {e}")
            return False
# =============================================================================
# CODE PATCH TO ADD TO CLASS 1 - MISSING METHODS FROM CLASS 2
# =============================================================================
# Add these methods to the end of Class 1 (before the closing of the class)
# Insert before line 884 where Class 2 currently starts

    def analyze_market_progressive(self, market_state):
        """Enhanced progressive market analysis with 15-timeframe integration."""
        try:
            logger.info("🔄 Starting enhanced progressive market analysis...")
            
            # Initialize analysis result
            analysis_result = {
                'verdict': 'NEUTRAL',
                'score': 0.0,
                'confidence': 'LOW',
                'reasoning': [],
                'timeframe_analysis': {},
                'progressive_signals': {},
                'enhanced_verdict': 'NEUTRAL',
                'timestamp': datetime.now().isoformat()
            }
            
            # Check if we have enough data
            if len(market_state.market_history) < 3:
                analysis_result['reasoning'].append("Insufficient data for progressive analysis")
                return analysis_result
            
            # Get latest snapshot
            latest_snapshot = market_state.market_history[-1]
            
            # **1. BASIC MARKET ANALYSIS**
            basic_analysis = self.analyze_market_snapshot(latest_snapshot)
            if basic_analysis:
                analysis_result['verdict'] = basic_analysis.get('verdict', 'NEUTRAL')
                analysis_result['score'] = basic_analysis.get('score', 0.0)
                analysis_result['reasoning'].extend(basic_analysis.get('reasoning', []))
            
            # **2. TIMEFRAME ANALYSIS INTEGRATION**
            if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
                tf_analysis = market_state.current_analysis['timeframe_analysis']
                analysis_result['timeframe_analysis'] = tf_analysis
                
                # Calculate timeframe-based signals
                tf_signals = self._analyze_timeframe_signals(tf_analysis)
                analysis_result['progressive_signals']['timeframe_signals'] = tf_signals
                
                # Adjust score based on timeframe consensus
                if tf_signals['consensus'] != 'NEUTRAL':
                    consensus_boost = tf_signals['strength'] * 0.3
                    if tf_signals['consensus'] == analysis_result['verdict']:
                        analysis_result['score'] += consensus_boost
                        analysis_result['reasoning'].append(f"Timeframe consensus supports {tf_signals['consensus']}")
                    else:
                        analysis_result['score'] = max(0, analysis_result['score'] - consensus_boost)
                        analysis_result['reasoning'].append(f"Timeframe consensus conflicts: {tf_signals['consensus']} vs {analysis_result['verdict']}")
            
            # **3. MOMENTUM ANALYSIS**
            momentum_analysis = self._calculate_progressive_momentum(market_state.market_history)
            analysis_result['progressive_signals']['momentum'] = momentum_analysis
            
            if momentum_analysis['strength'] > 6.0:
                momentum_boost = (momentum_analysis['strength'] - 5.0) * 0.2
                if momentum_analysis['direction'] == analysis_result['verdict']:
                    analysis_result['score'] += momentum_boost
                    analysis_result['reasoning'].append(f"Strong {momentum_analysis['direction']} momentum detected")
            
            # **4. VOLUME FLOW ANALYSIS**
            volume_flow = self._analyze_volume_flow_progressive(market_state.market_history)
            analysis_result['progressive_signals']['volume_flow'] = volume_flow
            
            if volume_flow['signal_strength'] > 7.0:
                flow_boost = (volume_flow['signal_strength'] - 6.0) * 0.15
                if volume_flow['direction'] == analysis_result['verdict']:
                    analysis_result['score'] += flow_boost
                    analysis_result['reasoning'].append(f"Strong volume flow supports {volume_flow['direction']}")
            
            # **5. OI DIVERGENCE ANALYSIS**
            oi_divergence = self._analyze_oi_divergence_progressive(market_state.market_history)
            analysis_result['progressive_signals']['oi_divergence'] = oi_divergence
            
            if oi_divergence['divergence_strength'] > 6.5:
                div_adjustment = oi_divergence['divergence_strength'] * 0.1
                if oi_divergence['signal'] == 'BULLISH' and analysis_result['verdict'] == 'BULLISH':
                    analysis_result['score'] += div_adjustment
                elif oi_divergence['signal'] == 'BEARISH' and analysis_result['verdict'] == 'BEARISH':
                    analysis_result['score'] += div_adjustment
                else:
                    analysis_result['score'] = max(0, analysis_result['score'] - div_adjustment)
                analysis_result['reasoning'].append(f"OI divergence: {oi_divergence['signal']} ({oi_divergence['divergence_strength']:.1f}/10)")
            
            # **6. FINAL VERDICT CALCULATION**
            # Normalize score and determine final verdict
            analysis_result['score'] = min(10.0, max(0.0, analysis_result['score']))
            
            # Enhanced verdict based on progressive analysis
            if analysis_result['score'] >= 7.0:
                analysis_result['enhanced_verdict'] = analysis_result['verdict']
                analysis_result['confidence'] = 'HIGH'
            elif analysis_result['score'] >= 5.0:
                analysis_result['enhanced_verdict'] = analysis_result['verdict']
                analysis_result['confidence'] = 'MEDIUM'
            elif analysis_result['score'] >= 3.0:
                analysis_result['enhanced_verdict'] = 'WEAK_' + analysis_result['verdict']
                analysis_result['confidence'] = 'LOW'
            else:
                analysis_result['enhanced_verdict'] = 'NEUTRAL'
                analysis_result['confidence'] = 'VERY_LOW'
            
            # **7. CANDLE INTELLIGENCE INTEGRATION**
            if hasattr(market_state, 'current_analysis') and 'candle_intelligence' in market_state.current_analysis:
                candle_data = market_state.current_analysis['candle_intelligence']
                # Check if candle_data is None before using it
                if candle_data is not None and candle_data.get('status') == 'CANDLE_COMPLETED':
                    candle_rec = candle_data.get('trade_recommendation', {})
                    candle_confidence = candle_rec.get('confidence', 0)
                    if candle_confidence > 0.7:  # 70% confidence
                        candle_action = candle_rec.get('action', 'WAIT')
                        if candle_action in ['BUY', 'STRONG_BUY'] and analysis_result['verdict'] == 'BULLISH':
                            analysis_result['score'] += 1.0
                            analysis_result['reasoning'].append(f"Candle intelligence supports BULLISH ({candle_confidence:.0%})")
                        elif candle_action in ['SELL', 'STRONG_SELL'] and analysis_result['verdict'] == 'BEARISH':
                            analysis_result['score'] += 1.0
                            analysis_result['reasoning'].append(f"Candle intelligence supports BEARISH ({candle_confidence:.0%})")
            
            # **8. QUALITY METRICS**
            analysis_result['data_quality'] = market_state.data_quality_score
            analysis_result['snapshots_analyzed'] = len(market_state.market_history)
            analysis_result['active_timeframes'] = len(analysis_result['timeframe_analysis'])
            
            logger.info(f"✅ Progressive analysis complete: {analysis_result['enhanced_verdict']} (Score: {analysis_result['score']:.2f})")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Progressive analysis error: {e}")
            logger.error(f"📍 Traceback: {traceback.format_exc()}")
            # Return fallback analysis
            return {
                'verdict': 'NEUTRAL',
                'score': 0.0,
                'confidence': 'ERROR',
                'reasoning': [f'Progressive analysis failed: {str(e)[:100]}'],
                'error': True,
                'timestamp': datetime.now().isoformat()
            }

    def _analyze_timeframe_signals(self, timeframe_analysis):
        """Analyze signals from multiple timeframes."""
        try:
            bullish_count = 0
            bearish_count = 0
            total_strength = 0
            
            for tf, data in timeframe_analysis.items():
                if isinstance(data, dict):
                    momentum = data.get('momentum', 'NEUTRAL')
                    strength = data.get('strength_score', 0)
                    
                    if momentum == 'BULLISH':
                        bullish_count += 1
                    elif momentum == 'BEARISH':
                        bearish_count += 1
                    
                    total_strength += strength
            
            total_timeframes = len(timeframe_analysis)
            avg_strength = total_strength / max(1, total_timeframes)
            
            if bullish_count > bearish_count:
                consensus = 'BULLISH'
            elif bearish_count > bullish_count:
                consensus = 'BEARISH'
            else:
                consensus = 'NEUTRAL'
            
            return {
                'consensus': consensus,
                'bullish_count': bullish_count,
                'bearish_count': bearish_count,
                'strength': avg_strength,
                'total_timeframes': total_timeframes
            }
            
        except Exception as e:
            logger.error(f"Timeframe signals analysis error: {e}")
            return {'consensus': 'NEUTRAL', 'strength': 0, 'error': True}

    def _calculate_progressive_momentum(self, market_history):
        """Calculate momentum from recent market data."""
        try:
            if len(market_history) < 3:
                return {'direction': 'NEUTRAL', 'strength': 0}
            
            recent = list(market_history)[-3:]
            price_changes = []
            volume_changes = []
            
            for i in range(1, len(recent)):
                price_change = recent[i]['underlying_value'] - recent[i-1]['underlying_value']
                price_changes.append(price_change)
                
                vol_change = (recent[i]['CE_VOL'] + recent[i]['PE_VOL']) - (recent[i-1]['CE_VOL'] + recent[i-1]['PE_VOL'])
                volume_changes.append(vol_change)
            
            avg_price_change = sum(price_changes) / len(price_changes)
            avg_volume_change = sum(volume_changes) / len(volume_changes)
            
            # Calculate momentum strength (0-10)
            price_momentum = abs(avg_price_change) / (recent[-1]['underlying_value'] * 0.001)  # Normalize
            volume_momentum = abs(avg_volume_change) / max(1, recent[-1]['CE_VOL'] + recent[-1]['PE_VOL']) * 100
            
            strength = min(10, (price_momentum + volume_momentum) * 2)
            direction = 'BULLISH' if avg_price_change > 0 else 'BEARISH' if avg_price_change < 0 else 'NEUTRAL'
            
            return {
                'direction': direction,
                'strength': strength,
                'price_momentum': price_momentum,
                'volume_momentum': volume_momentum
            }
            
        except Exception as e:
            logger.error(f"Momentum calculation error: {e}")
            return {'direction': 'NEUTRAL', 'strength': 0, 'error': True}

    def _analyze_volume_flow_progressive(self, market_history):
        """Analyze volume flow patterns."""
        try:
            if len(market_history) < 3:
                return {'direction': 'NEUTRAL', 'signal_strength': 0}
            
            recent = list(market_history)[-3:]
            ce_flow_trend = []
            pe_flow_trend = []
            
            for i in range(1, len(recent)):
                ce_flow = recent[i]['CE_VOL'] - recent[i-1]['CE_VOL']
                pe_flow = recent[i]['PE_VOL'] - recent[i-1]['PE_VOL']
                
                ce_flow_trend.append(ce_flow)
                pe_flow_trend.append(pe_flow)
            
            avg_ce_flow = sum(ce_flow_trend) / len(ce_flow_trend)
            avg_pe_flow = sum(pe_flow_trend) / len(pe_flow_trend)
            
            # Calculate flow imbalance
            total_avg_flow = abs(avg_ce_flow) + abs(avg_pe_flow)
            if total_avg_flow > 0:
                ce_dominance = abs(avg_ce_flow) / total_avg_flow
                pe_dominance = abs(avg_pe_flow) / total_avg_flow
            else:
                ce_dominance = pe_dominance = 0.5
            
            # Determine signal strength (0-10)
            imbalance = abs(ce_dominance - pe_dominance)
            signal_strength = min(10, imbalance * 20)
            
            # Determine direction
            if avg_ce_flow > avg_pe_flow * 1.2:
                direction = 'BEARISH'  # More CE volume often indicates bearish sentiment
            elif avg_pe_flow > avg_ce_flow * 1.2:
                direction = 'BULLISH'  # More PE volume often indicates bullish sentiment
            else:
                direction = 'NEUTRAL'
            
            return {
                'direction': direction,
                'signal_strength': signal_strength,
                'ce_flow': avg_ce_flow,
                'pe_flow': avg_pe_flow,
                'imbalance': imbalance
            }
            
        except Exception as e:
            logger.error(f"Volume flow analysis error: {e}")
            return {'direction': 'NEUTRAL', 'signal_strength': 0, 'error': True}

    def _analyze_oi_divergence_progressive(self, market_history):
        """Analyze Open Interest divergence patterns."""
        try:
            if len(market_history) < 3:
                return {'signal': 'NEUTRAL', 'divergence_strength': 0}
            
            recent = list(market_history)[-3:]
            price_trend = []
            oi_ratio_trend = []
            
            for i in range(1, len(recent)):
                price_change = recent[i]['underlying_value'] - recent[i-1]['underlying_value']
                price_trend.append(price_change)
                
                # OI PCR trend
                current_pcr = recent[i]['PE_OI'] / max(1, recent[i]['CE_OI'])
                prev_pcr = recent[i-1]['PE_OI'] / max(1, recent[i-1]['CE_OI'])
                oi_ratio_change = current_pcr - prev_pcr
                oi_ratio_trend.append(oi_ratio_change)
            
            avg_price_change = sum(price_trend) / len(price_trend)
            avg_oi_ratio_change = sum(oi_ratio_trend) / len(oi_ratio_trend)
            
            # Check for divergence
            price_direction = 'UP' if avg_price_change > 0 else 'DOWN'
            oi_direction = 'UP' if avg_oi_ratio_change > 0 else 'DOWN'
            
            # Divergence strength calculation
            price_strength = abs(avg_price_change) / max(1, recent[-1]['underlying_value'] * 0.001)
            oi_strength = abs(avg_oi_ratio_change) * 10
            
            divergence_strength = min(10, (price_strength + oi_strength) / 2)
            
            # Determine signal
            if price_direction != oi_direction and divergence_strength > 3:
                if price_direction == 'UP' and oi_direction == 'DOWN':
                    signal = 'BEARISH'  # Price up but OI PCR down - potential reversal
                elif price_direction == 'DOWN' and oi_direction == 'UP':
                    signal = 'BULLISH'  # Price down but OI PCR up - potential reversal
                else:
                    signal = 'NEUTRAL'
            else:
                signal = 'NEUTRAL'
            
            return {
                'signal': signal,
                'divergence_strength': divergence_strength,
                'price_trend': price_direction,
                'oi_trend': oi_direction,
                'is_divergence': price_direction != oi_direction
            }
            
        except Exception as e:
            logger.error(f"OI divergence analysis error: {e}")
            return {'signal': 'NEUTRAL', 'divergence_strength': 0, 'error': True}

    def generate_progressive_recommendation(self, analysis, market_state, day_profile):
        """Generate progressive trading recommendation."""
        try:
            verdict = analysis.get('enhanced_verdict', 'NEUTRAL')
            confidence = analysis.get('confidence', 'LOW')
            score = analysis.get('score', 0.0)
            
            # Base recommendation
            if confidence == 'HIGH' and score >= 7.0:
                if verdict == 'BULLISH':
                    recommendation = "🟢 [HIGH CONFIDENCE] Strong bullish signals detected - Consider long positions"
                elif verdict == 'BEARISH':
                    recommendation = "🔴 [HIGH CONFIDENCE] Strong bearish signals detected - Consider short positions"
                else:
                    recommendation = "⚪ [NEUTRAL] Mixed signals - Wait for clearer direction"
            elif confidence == 'MEDIUM':
                if verdict == 'BULLISH':
                    recommendation = "🟡 [MODERATE] Moderate bullish bias - Small position sizes recommended"
                elif verdict == 'BEARISH':
                    recommendation = "🟡 [MODERATE] Moderate bearish bias - Small position sizes recommended"
                else:
                    recommendation = "⚪ [NEUTRAL] Sideways market - Range trading opportunities"
            else:
                recommendation = "🔍 [BASIC] No clear signals detected. Continue monitoring."
            
            return recommendation
            
        except Exception as e:
            logger.error(f"❌ Recommendation generation error: {e}")
            return "❌ Unable to generate recommendation"

    # NOTE: analyze_market_snapshot method may already exist in Class 1
    # Check if it exists before adding this one, or merge if needed
    def analyze_market_snapshot_progressive(self, snapshot):
        """Enhanced market snapshot analysis with progressive features."""
        try:
            analysis = {
                'verdict': 'NEUTRAL',
                'score': 5.0,
                'reasoning': []
            }
            
            # Basic PCR analysis
            oi_pcr = snapshot.get('OI_PCR', 1.0)
            vol_pcr = snapshot.get('VOL_PCR', 1.0)
            
            if oi_pcr > 1.2:
                analysis['verdict'] = 'BULLISH'
                analysis['score'] += 1.0
                analysis['reasoning'].append(f"High OI PCR: {oi_pcr:.3f}")
            elif oi_pcr < 0.8:
                analysis['verdict'] = 'BEARISH'
                analysis['score'] += 1.0
                analysis['reasoning'].append(f"Low OI PCR: {oi_pcr:.3f}")
            
            if vol_pcr > 1.2:
                if analysis['verdict'] == 'BULLISH':
                    analysis['score'] += 0.5
                analysis['reasoning'].append(f"High VOL PCR: {vol_pcr:.3f}")
            elif vol_pcr < 0.8:
                if analysis['verdict'] == 'BEARISH':
                    analysis['score'] += 0.5
                analysis['reasoning'].append(f"Low VOL PCR: {vol_pcr:.3f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Progressive snapshot analysis error: {e}")
            return {'verdict': 'NEUTRAL', 'score': 0.0, 'reasoning': ['Analysis failed'], 'error': True}

# =============================================================================
# END OF PATCH
# =============================================================================

# =============================================================================
# ENHANCED FALLBACK DATA FETCHING
# =============================================================================
async def enhanced_fallback_fetch(symbol: str) -> Dict[str, Any]:
    """Enhanced fallback to yfinance with data quality improvements.
    Provides comprehensive market data when NSE scraping fails."""
    logger.info("🔄 Attempting enhanced fallback fetch for %s", symbol)
    
    try:
        # Map symbols to yfinance tickers
        ticker_map = {
            "NIFTY": "^NNIFTY50",
            "NIFTY": "^NSEI",
            "BANKNIFTY": "^NSEBANK",
        }
        ticker = ticker_map.get(symbol, f"^{symbol}.NS")
        logger.info("📊 Fetching data from yfinance ticker: %s", ticker)
        
        # Fetch extended data for better analysis
        data = yf.download(ticker, period="2d", interval="1m", progress=False)
        if data.empty:
            logger.warning("⚠️ No data received from yfinance for %s", symbol)
            return {}
        
        # Get latest values
        latest = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else latest
        
        # Calculate basic metrics (safe for both DataFrameRow and Series)
        spot = float(latest['Close'])
        volume = float(latest.get('Volume', 100000))
        change = spot - float(previous['Close'])
        change_pct = (change / float(previous['Close'])) * 100 if float(previous['Close']) > 0 else 0
        
        # Extract OHLC data
        open_price = float(latest['Open'])
        high_price = float(latest['High'])
        low_price = float(latest['Low'])
        close_price = spot
        
        # Estimate OI and volume data (since yfinance doesn't provide options data)
        estimated_ce_oi = volume * 2.5  # Rough estimation (adjust as needed)
        estimated_pe_oi = volume * 2.8  # Slightly higher for PE
        estimated_ce_vol = volume * 0.6
        estimated_pe_vol = volume * 0.4
        
        fallback_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "underlying_value": spot,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "CE_OI": estimated_ce_oi,
            "PE_OI": estimated_pe_oi,
            "CE_VOL": estimated_ce_vol,
            "PE_VOL": estimated_pe_vol,
            "OI_PCR": (estimated_pe_oi / estimated_ce_oi) if estimated_ce_oi > 0 else 1.0,
            "VOL_PCR": (estimated_pe_vol / estimated_ce_vol) if estimated_ce_vol > 0 else 1.0,
            "data_source": "YFINANCE_FALLBACK"
        }
        
        logger.info("✅ Fallback data generated for %s:", symbol)
        logger.info(" Spot: ₹%.2f (Change: %.2f, %.2f%%)", spot, change, change_pct)
        logger.info(" OHLC: O:%.2f H:%.2f L:%.2f C:%.2f", open_price, high_price, low_price, close_price)
        logger.info(" Estimated OI - CE: %.0f, PE: %.0f", estimated_ce_oi, estimated_pe_oi)
        return fallback_snapshot
        
    except Exception as e:
        logger.error("❌ Fallback fetch failed for %s: %s", symbol, e)
        return {}
## =============================================================================
# ENHANCED TELEGRAM INTEGRATION - COMPLETE TRADE LIFECYCLE TRACKING
# =============================================================================

def format_recommendation_for_telegram(decision: Dict[str, Any], snapshot: Dict[str, Any], strike_data: Dict[str, Any], option_type: str, atm_strike: float, entry_price: float, sl: float, target1: float, target2: float, pos_mult: float) -> str:
    """Format complete recommendation for Telegram with all details."""
    level = decision.get('confidence_level', 'UNKNOWN')
    verdict = decision.get('verdict', 'UNKNOWN')

    # Emoji mapping
    confidence_emoji = {
        "EARLY_SIGNALS": "🟡",
        "MEDIUM_CONFIDENCE": "🟠",
        "HIGH_CONFIDENCE": "🔴",
        "FULL_POWER": "🚨"
    }

    emoji = confidence_emoji.get(level, "🔍")

    telegram_msg = f"""
🎯 NIFTY TRADE ALERT {emoji}
━━━━━━━━━━━━━━━━━━━
📊 CONFIDENCE: {level}
🎯 SIGNAL: {verdict}

📍 ENTRY DETAILS:
• Option: {option_type} {int(atm_strike)}
• Entry Price: ₹{entry_price:.2f}
• Spot: ₹{snapshot['underlying_value']:.2f}

🎯 TARGETS & RISK:
• Target 1: ₹{target1:.2f}
• Target 2: ₹{target2:.2f}
• Stop Loss: ₹{sl:.2f}
• Position Size: {int(pos_mult*100)}%

📊 MARKET DATA:
• CE OI: {int(snapshot.get('CE_OI', 0)):,}
• PE OI: {int(snapshot.get('PE_OI', 0)):,}
• OI PCR: {snapshot.get('OI_PCR', 0):.3f}
• Vol PCR: {snapshot.get('VOL_PCR', 0):.3f}

💡 REASON: {decision['reason'][:150]}...

⭐ ANALYSIS SCORE: {decision['score']:.2f}/10
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
"""
    return telegram_msg.strip()

def format_trade_update_for_telegram(trade: Dict[str, Any], current_ltp: float, pnl: float, cycle_num: int) -> str:
    """Format trade tracking update for Telegram."""
    confidence_level = trade.get('confidence_level', 'UNKNOWN')

    # Calculate progress percentages
    entry = trade['entry']
    target1 = trade['partial_target']
    target2 = trade['target']
    sl = trade['sl']

    if trade['type'] == 'CE':  # Bullish trade
        target1_progress = ((current_ltp - entry) / (target1 - entry)) * 100 if target1 > entry else 0
        target2_progress = ((current_ltp - entry) / (target2 - entry)) * 100 if target2 > entry else 0
    else:  # Bearish trade
        target1_progress = ((entry - current_ltp) / (entry - target1)) * 100 if entry > target1 else 0
        target2_progress = ((entry - current_ltp) / (entry - target2)) * 100 if entry > target2 else 0

    # Determine emoji based on PnL
    pnl_emoji = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"

    telegram_msg = f"""
📊 TRADE UPDATE #{cycle_num}
━━━━━━━━━━━━━━━━━━━
📈 {trade['type']} {int(trade['strike'])} Tracking

💰 CURRENT STATUS:
• LTP: ₹{current_ltp:.2f}
• PnL: {pnl:+.2f}% {pnl_emoji}
• Entry: ₹{entry:.2f}

🎯 TARGET PROGRESS:
• Target 1: {target1_progress:.1f}% (₹{target1:.2f})
• Target 2: {target2_progress:.1f}% (₹{target2:.2f})

🛡️ RISK MANAGEMENT:
• Stop Loss: ₹{sl:.2f}
• Risk: {((sl - entry) / entry * 100):+.1f}%

⏰ Trade Duration: {(datetime.now() - trade['entry_time']).seconds // 60}m
🎯 Confidence: {confidence_level}
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
"""
    return telegram_msg.strip()

def format_target_hit_for_telegram(trade: Dict[str, Any], current_ltp: float, pnl: float, target_num: int) -> str:
    """Format target hit notification for Telegram."""
    confidence_level = trade.get('confidence_level', 'UNKNOWN')
    duration_minutes = (datetime.now() - trade['entry_time']).seconds // 60

    if target_num == 1:
        emoji = "✅"
        action = "Book 50% profits, trail SL"
        target_price = trade['partial_target']
    else:
        emoji = "🎉"
        action = "Full exit - Trade complete!"
        target_price = trade['target']

    telegram_msg = f"""
{emoji} TARGET {target_num} HIT!
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} SUCCESS

💰 PROFIT DETAILS:
• Target Price: ₹{target_price:.2f}
• Current LTP: ₹{current_ltp:.2f}
• Entry Price: ₹{trade['entry']:.2f}
• PnL: +{pnl:.2f}% 💚

📊 TRADE SUMMARY:
• Duration: {duration_minutes}m
• Confidence: {confidence_level}
• Action: {action}

📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
🎊 WELL DONE! 🎊
"""
    return telegram_msg.strip()

def format_sl_hit_for_telegram(trade: Dict[str, Any], current_ltp: float, pnl: float) -> str:
    """Format stop loss hit notification for Telegram."""
    confidence_level = trade.get('confidence_level', 'UNKNOWN')
    duration_minutes = (datetime.now() - trade['entry_time']).seconds // 60

    # Determine if it's a loss or protected profit
    result_emoji = "🛡️" if pnl > 0 else "❌"
    result_text = "PROFIT PROTECTED" if pnl > 0 else "LOSS CONTROLLED"

    telegram_msg = f"""
{result_emoji} STOP LOSS HIT
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} STOPPED

💰 FINAL RESULT:
• SL Price: ₹{trade['sl']:.2f}
• Exit LTP: ₹{current_ltp:.2f}
• Entry Price: ₹{trade['entry']:.2f}
• Final PnL: {pnl:+.2f}%

📊 TRADE SUMMARY:
• Duration: {duration_minutes}m
• Confidence: {confidence_level}
• Result: {result_text}

💡 Risk management worked!
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
"""
    return telegram_msg.strip()
# =============================================================================
# TELEGRAM SENDING FUNCTION - ADD THIS TO YOUR FILE
# =============================================================================
async def send_enhanced_telegram_message(message: str, priority: str = "NORMAL") -> bool:
    """Send message to Telegram with fixed credentials logic."""
    # Use your actual credentials directly
    BOT_TOKEN = "7869031606:AAGiTsf4KoV5aeDHjyppRRFYgc4wm8bc_8M"
    CHAT_ID = "1598471281"
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        priority_emojis = {
            "CRITICAL": "🚨🚨🚨 ",
            "HIGH": "🔥 ",
            "NORMAL": "📊 ",
            "LOW": "ℹ️ "
        }
        
        formatted_message = priority_emojis.get(priority, "📊 ") + message
        
        payload = {
            "chat_id": CHAT_ID,
            "text": formatted_message,
            "parse_mode": "HTML"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info(f"✅ Telegram message sent ({priority})")
                    return True
                else:
                    logger.error(f"❌ Telegram send failed: {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ Telegram error: {e}")
        return False


# =============================================================================
# UPDATE YOUR EXISTING METHODS WITH ENHANCED TELEGRAM INTEGRATION
# =============================================================================

# UPDATE: generate_progressive_recommendation method
def generate_progressive_recommendation(self, decision: Dict[str, Any], market_state: 'EnhancedMarketState', day_profile: 'EnhancedMarketDayProfile') -> str:
    """Generate recommendations with COMPLETE Telegram integration."""
    verdict = decision['verdict']
    level = decision['confidence_level']

    if verdict == "NEUTRAL":
        return f"🔍 [{level}] No clear signals detected. Continue monitoring."

    # Get current market data
    snapshot = market_state.market_history[-1]
    spot = snapshot['underlying_value']
    strikes = sorted(snapshot.get("strike_data", {}).keys())

    if not strikes:
        return "❌ Insufficient strike data for recommendation."

    atm_strike = min(strikes, key=lambda k: abs(k - spot))
    strike_data = snapshot["strike_data"][atm_strike]

    # Determine option type and entry
    is_bullish = "BULLISH" in verdict
    option_type = "CE" if is_bullish else "PE"
    entry_price = strike_data.get(f"{option_type}_LTP", 0)

    if entry_price <= 0:
        return "❌ Invalid option price data."

    # Progressive position sizing and risk
    position_multipliers = {
        "EARLY_SIGNALS": 0.5, "MEDIUM_CONFIDENCE": 0.75,
        "HIGH_CONFIDENCE": 1.0, "FULL_POWER": 1.0
    }
    risk_multipliers = {
        "EARLY_SIGNALS": 0.5, "MEDIUM_CONFIDENCE": 0.75,
        "HIGH_CONFIDENCE": 1.0, "FULL_POWER": 1.0
    }

    pos_mult = position_multipliers.get(level, 0.5)
    risk_mult = risk_multipliers.get(level, 0.5)

    # Calculate targets and SL
    base_sl_pct = self.config["risk"]["sl_percentage"] * risk_mult
    base_target_pct = self.config["risk"]["target_percentage"]

    sl = entry_price * (1 - base_sl_pct) if is_bullish else entry_price * (1 + base_sl_pct)
    target1 = entry_price * (1 + base_target_pct/2) if is_bullish else entry_price * (1 - base_target_pct/2)
    target2 = entry_price * (1 + base_target_pct) if is_bullish else entry_price * (1 - base_target_pct)

    # Create trade for tracking
    if level in ["MEDIUM_CONFIDENCE", "HIGH_CONFIDENCE", "FULL_POWER"]:
        day_profile.active_trade = {
            "type": option_type, "strike": atm_strike, "entry": entry_price,
            "sl": sl, "partial_target": target1, "target": target2,
            "original_sl": sl, "entry_time": datetime.now(),
            "confidence_level": level, "monitored": True
        }

    # Generate COMPLETE Telegram message
    telegram_msg = format_recommendation_for_telegram(
        decision, snapshot, strike_data, option_type,
        atm_strike, entry_price, sl, target1, target2, pos_mult
    )

    # Send to Telegram with HIGH priority
    asyncio.create_task(send_enhanced_telegram_message(telegram_msg, priority="HIGH"))

    logger.info(f"[{level}] Generated recommendation: {verdict}")
    return telegram_msg

# In the SmartLiveCommentaryBot class, replace these methods:

def _generate_support_resistance_context(self, market_state: 'EnhancedMarketState') -> tuple:
    """Generate support/resistance context and return both text + values - FIXED."""
    
    if len(market_state.market_history) < 5:  # Reduced from 10
        current_price = market_state.last_spot_price
        support_levels = [current_price - 15, current_price - 30]
        resistance_levels = [current_price + 15, current_price + 30] 
        
        context_text = f"""
📈 SUPPORT/RESISTANCE: 
• Current: ₹{current_price:.2f}
• Support: ₹{support_levels[0]:.2f} / ₹{support_levels[1]:.2f}
• Resistance: ₹{resistance_levels[0]:.2f} / ₹{resistance_levels[1]:.2f}"""
        
        return context_text, support_levels, resistance_levels
    
    recent_data = list(market_state.market_history)[-10:]
    prices = [data.get('underlying_value', 0) for data in recent_data]
    current_price = prices[-1]
    
    # Calculate dynamic support and resistance
    support_levels = [min(prices[-5:]), min(prices)]  # Recent low, Overall low
    resistance_levels = [max(prices[-5:]), max(prices)]  # Recent high, Overall high
    
    # Ensure levels are different from current price
    if support_levels[0] >= current_price:
        support_levels[0] = current_price - 10
    if resistance_levels[0] <= current_price:
        resistance_levels[0] = current_price + 10
    
    context_text = f"""
📈 SUPPORT/RESISTANCE CONTEXT:
• Current: ₹{current_price:.2f}
• Immediate Support: ₹{support_levels[0]:.2f}  
• Key Support: ₹{support_levels[1]:.2f}
• Immediate Resistance: ₹{resistance_levels[0]:.2f}
• Key Resistance: ₹{resistance_levels[1]:.2f}"""

    return context_text, support_levels, resistance_levels

def _calculate_support_levels(self, prices: List[float], current_price: float) -> List[float]:
    """Calculate support levels."""
    support_levels = []
    sorted_prices = sorted([p for p in prices if p < current_price], reverse=True)
    if len(sorted_prices) >= 2:
        support_levels = sorted_prices[:2]
    else:
        support_levels = [current_price - 10, current_price - 25]
    return support_levels

def _calculate_resistance_levels(self, prices: List[float], current_price: float) -> List[float]:
    """Calculate resistance levels."""
    resistance_levels = []
    sorted_prices = sorted([p for p in prices if p > current_price])
    if len(sorted_prices) >= 2:
        resistance_levels = sorted_prices[:2]
    else:
        resistance_levels = [current_price + 10, current_price + 25]
    return resistance_levels

# UPDATE: manage_active_trade method
def manage_active_trade(
    self,
    analysis: Dict[str, Any],
    day_profile: 'EnhancedMarketDayProfile',
    market_state: 'EnhancedMarketState'
) -> Dict[str, Any]:
    """Enhanced active trade management with predictive exit, Telegram tracking, and comprehensive risk/reward."""
    trade = day_profile.active_trade
    if not trade:
        return {"verdict": "NO_TRADE", "reason": "No active trade to manage."}

    current_snapshot = market_state.market_history[-1]
    strike_data = current_snapshot.get('strike_data', {})
    if trade['strike'] not in strike_data:
        # Telegram: Strike data missing, force exit
        exit_msg = f"❌ Strike {trade['strike']} data unavailable. Force exit."
        asyncio.create_task(send_enhanced_telegram_message(exit_msg))
        return {"verdict": "EXIT_NOW", "reason": "Strike not found", "pnl": 0.0, "score": analysis.get('score', 0)}

    trade_type = trade['type']
    current_ltp = strike_data[trade['strike']].get(f"{trade_type}_LTP", trade['entry'])
    if current_ltp <= 0:
        current_ltp = trade['entry']

    pnl = ((current_ltp - trade['entry']) / trade['entry']) * 100 if trade['entry'] > 0 else 0.0
    is_bullish = (trade_type == "CE")

    # Trailing stop loss logic
    if 'atr_trail' not in trade:
        trade['atr_trail'] = trade['original_sl']

    atr_val = market_state.get_atr()
    trail_dist = 1.4 * atr_val if atr_val > 0 else current_ltp * 0.04

    if is_bullish:
        candidate_sl = current_ltp - trail_dist
        if candidate_sl > trade['atr_trail']:
            trade['atr_trail'] = candidate_sl
            trade['sl'] = candidate_sl
            sl_update_msg = f"🛡️ Trailing SL Updated: ₹{candidate_sl:.2f} (LTP: ₹{current_ltp:.2f})"
            asyncio.create_task(send_enhanced_telegram_message(sl_update_msg))
    else:
        candidate_sl = current_ltp + trail_dist
        if candidate_sl < trade['atr_trail']:
            trade['atr_trail'] = candidate_sl
            trade['sl'] = candidate_sl
            sl_update_msg = f"🛡️ Trailing SL Updated: ₹{candidate_sl:.2f} (LTP: ₹{current_ltp:.2f})"
            asyncio.create_task(send_enhanced_telegram_message(sl_update_msg))

    # Target 1 check
    if not trade.get('target1_hit', False):
        if (is_bullish and current_ltp >= trade['partial_target']) or (not is_bullish and current_ltp <= trade['partial_target']):
            trade['target1_hit'] = True
            target1_msg = format_target_hit_for_telegram(trade, current_ltp, pnl, 1)
            asyncio.create_task(send_enhanced_telegram_message(target1_msg, priority="HIGH"))
            logger.info(f"✅ Target 1 Hit: LTP ₹{current_ltp:.2f}")

    # Target 2 check
    if (is_bullish and current_ltp >= trade['target']) or (not is_bullish and current_ltp <= trade['target']):
        day_profile.active_trade = None
        target2_msg = format_target_hit_for_telegram(trade, current_ltp, pnl, 2)
        asyncio.create_task(send_enhanced_telegram_message(target2_msg, priority="HIGH"))
        return {"verdict": "EXIT_NOW", "reason": "Target 2 hit!", "pnl": pnl, "score": analysis.get('score', 0), "result": "WIN"}

    # Stop loss check
    if (is_bullish and current_ltp <= trade['sl']) or (not is_bullish and current_ltp >= trade['sl']):
        day_profile.active_trade = None
        sl_msg = format_sl_hit_for_telegram(trade, current_ltp, pnl)
        asyncio.create_task(send_enhanced_telegram_message(sl_msg, priority="HIGH"))
        return {"verdict": "EXIT_NOW", "reason": "SL hit.", "pnl": pnl, "score": analysis.get('score', 0), "result": "LOSS"}

    # Periodic tracking updates (every 3rd cycle)
    cycle_count = getattr(trade, 'update_count', 0) + 1
    trade['update_count'] = cycle_count
    if cycle_count % 3 == 0:  # Every 3rd update
        tracking_msg = format_trade_update_for_telegram(trade, current_ltp, pnl, cycle_count // 3)
        asyncio.create_task(send_enhanced_telegram_message(tracking_msg))

    # Log progress
    progress_msg = f"[{trade.get('confidence_level', 'UNKNOWN')}] Tracking: LTP ₹{current_ltp:.2f} (PnL: {pnl:+.2f}%)"
    logger.info(progress_msg)

    return {"verdict": "TREND_HOLDING", "reason": "Trade active", "pnl": pnl, "score": analysis.get('score', 0)}
#=============================================================================
# ENHANCED MULTI-TIMEFRAME ANALYSIS WITH EXTENDED TIMEFRAMES
#=============================================================================
def analyze_market_progressive(self, market_state: 'EnhancedMarketState', analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhanced progressive market analysis with extended timeframes."""

    # Extended timeframe intervals in minutes
    timeframe_intervals = [3, 9, 15, 21, 30, 60, 90]

    timeframe_analysis = {}

    logger.info(f"📊 Starting Multi-Timeframe Analysis at {datetime.now().strftime('%H:%M:%S')}")
    logger.info("="*80)

    for interval in timeframe_intervals:
        try:
            # Calculate how many snapshots we need for this timeframe
            # Assuming 1 minute per snapshot
            snapshots_needed = interval

            if len(market_state.market_history) >= snapshots_needed:
                # Get data for this timeframe
                timeframe_data = market_state.safe_get_recent_history(snapshots_needed)

                if len(timeframe_data) >= 2:
                    current = timeframe_data[-1]
                    baseline = timeframe_data[0]

                    # Calculate changes over this timeframe
                    price_change = current['underlying_value'] - baseline['underlying_value']
                    price_change_pct = (price_change / baseline['underlying_value']) * 100

                    ce_oi_change = current.get('CE_OI', 0) - baseline.get('CE_OI', 0)
                    pe_oi_change = current.get('PE_OI', 0) - baseline.get('PE_OI', 0)
                    ce_oi_change_pct = (ce_oi_change / baseline.get('CE_OI', 1)) * 100
                    pe_oi_change_pct = (pe_oi_change / baseline.get('PE_OI', 1)) * 100

                    ce_vol_change = current.get('CE_VOL', 0) - baseline.get('CE_VOL', 0)
                    pe_vol_change = current.get('PE_VOL', 0) - baseline.get('PE_VOL', 0)

                    pcr_change = current.get('OI_PCR', 1) - baseline.get('OI_PCR', 1)

                    # Determine momentum
                    if abs(price_change_pct) < 0.05:
                        momentum = "SIDEWAYS"
                    elif price_change_pct > 0.05:
                        momentum = "BULLISH"
                    else:
                        momentum = "BEARISH"

                    # Determine OI divergence
                    if ce_oi_change > pe_oi_change * 1.5:
                        oi_divergence = "BULLISH_DIVERGENCE"
                    elif pe_oi_change > ce_oi_change * 1.5:
                        oi_divergence = "BEARISH_DIVERGENCE"
                    else:
                        oi_divergence = "NEUTRAL"

                    # Determine volume pattern
                    total_vol_change = ce_vol_change + pe_vol_change
                    if total_vol_change > 10000000:  # 10M+
                        volume_pattern = "HIGH_VOLUME"
                    elif total_vol_change > 1000000:  # 1M+
                        volume_pattern = "NORMAL_VOLUME"
                    else:
                        volume_pattern = "LOW_VOLUME"

                    # Calculate strength score (0-10)
                    strength_score = 5.0  # Base score

                    # Adjust based on price movement
                    strength_score += min(abs(price_change_pct) * 2, 2.0)

                    # Adjust based on OI changes
                    if oi_divergence != "NEUTRAL":
                        strength_score += 1.0

                    # Adjust based on volume
                    if volume_pattern == "HIGH_VOLUME":
                        strength_score += 1.5
                    elif volume_pattern == "NORMAL_VOLUME":
                        strength_score += 0.5

                    # Adjust based on PCR changes
                    if abs(pcr_change) > 0.05:
                        strength_score += 0.5

                    strength_score = min(strength_score, 10.0)

                    # Store analysis for this timeframe
                    timeframe_analysis[f"{interval}-MINUTE"] = {
                        "price_change": price_change,
                        "price_change_pct": price_change_pct,
                        "ce_oi_change": ce_oi_change,
                        "pe_oi_change": pe_oi_change,
                        "ce_oi_change_pct": ce_oi_change_pct,
                        "pe_oi_change_pct": pe_oi_change_pct,
                        "ce_vol_change": ce_vol_change,
                        "pe_vol_change": pe_vol_change,
                        "pcr_change": pcr_change,
                        "momentum": momentum,
                        "oi_divergence": oi_divergence,
                        "volume_pattern": volume_pattern,
                        "strength_score": strength_score,
                        "baseline_price": baseline['underlying_value'],
                        "current_price": current['underlying_value'],
                        "baseline_pcr": baseline.get('OI_PCR', 1),
                        "current_pcr": current.get('OI_PCR', 1)
                    }

                    # Enhanced logging for each timeframe
                    logger.info(f"⏰ {interval}-MINUTE ANALYSIS:")
                    logger.info(f"  💹 Price: ₹{baseline['underlying_value']:.2f} → ₹{current['underlying_value']:.2f} (Change: {price_change:+.2f}, {price_change_pct:+.4f}%)")
                    logger.info(f"  📈 CE OI: {baseline.get('CE_OI', 0):,} → {current.get('CE_OI', 0):,} (Change: {ce_oi_change:+,}, {ce_oi_change_pct:+.2f}%)")
                    logger.info(f"  📉 PE OI: {baseline.get('PE_OI', 0):,} → {current.get('PE_OI', 0):,} (Change: {pe_oi_change:+,}, {pe_oi_change_pct:+.2f}%)")
                    logger.info(f"  📊 CE Vol: {baseline.get('CE_VOL', 0):,} → {current.get('CE_VOL', 0):,} (Change: {ce_vol_change:+,})")
                    logger.info(f"  📊 PE Vol: {baseline.get('PE_VOL', 0):,} → {current.get('PE_VOL', 0):,} (Change: {pe_vol_change:+,})")
                    logger.info(f"  🎯 PCR: {baseline.get('OI_PCR', 1):.4f} → {current.get('OI_PCR', 1):.4f} (Change: {pcr_change:+.4f})")
                    logger.info(f"  🚀 Momentum: {momentum} | Divergence: {oi_divergence} | Volume: {volume_pattern}")
                    logger.info(f"  ⚡ Strength Score: {strength_score:.2f}/10")
                    logger.info("------------------------------------------------------------")

            else:
                logger.warning(f"⚠️ Insufficient data for {interval}-minute analysis (need {snapshots_needed}, have {len(market_state.market_history)})")

        except Exception as e:
            logger.error(f"❌ Error in {interval}-minute analysis: {e}")

    logger.info("="*80)
    logger.info(f"📊 Multi-Timeframe Analysis Complete - Market State: {self._determine_overall_market_state(timeframe_analysis)}")
    logger.info("="*80)

    # Store analysis in market state for access by other functions
    if not hasattr(market_state, 'current_analysis'):
        market_state.current_analysis = {}
    market_state.current_analysis['timeframe_analysis'] = timeframe_analysis

    return timeframe_analysis


def _determine_overall_market_state(self, timeframe_analysis: Dict[str, Any]) -> str:
    """Determine overall market state from timeframe analysis."""
    if not timeframe_analysis:
        return "INSUFFICIENT_DATA"

    bullish_count = 0
    bearish_count = 0
    sideways_count = 0

    for interval, data in timeframe_analysis.items():
        momentum = data.get('momentum', 'SIDEWAYS')
        if momentum == 'BULLISH':
            bullish_count += 1
        elif momentum == 'BEARISH':
            bearish_count += 1
        else:
            sideways_count += 1

    if bullish_count > bearish_count + sideways_count:
        return "BULLISH"
    elif bearish_count > bullish_count + sideways_count:
        return "BEARISH"
    else:
        return "STABLE"

#=============================================================================
# COMPREHENSIVE DEBUGGING ANALYSIS FUNCTION - COMPLETE UPDATE
#=============================================================================
def print_comprehensive_analysis(market_state: 'EnhancedMarketState') -> None:
    """Print detailed timeframe analysis and historical data for debugging."""
    try:
        print("\n" + "="*100)
        print("🔍 COMPREHENSIVE BOT DATA ANALYSIS")
        print("="*100)

        # Current market snapshot
        if len(market_state.market_history) > 0:
            latest = list(market_state.market_history)[-1]
            print(f"📊 CURRENT MARKET STATE:")
            print(f"   Spot: ₹{latest['underlying_value']:.2f}")
            print(f"   OI PCR: {latest.get('OI_PCR', 0):.4f} | Vol PCR: {latest.get('VOL_PCR', 0):.4f}")
            print(f"   CE OI: {latest.get('CE_OI', 0):,} | PE OI: {latest.get('PE_OI', 0):,}")
            print(f"   CE Vol: {latest.get('CE_VOL', 0):,} | PE Vol: {latest.get('PE_VOL', 0):,}")
            print(f"   Data Quality: {market_state.data_quality_score:.1f}/10")
            print(f"   History Length: {len(market_state.market_history)} snapshots")
            print(f"   Last Update: {market_state.last_update_time}")
        else:
            print(f"📊 CURRENT MARKET STATE: No data available")

        # Enhanced Multi-timeframe analysis with all timeframes
        print(f"\n⏰ MULTI-TIMEFRAME ANALYSIS (3, 9, 15, 21, 30, 60, 90 MINUTES):")
        if hasattr(market_state, 'current_analysis') and market_state.current_analysis and 'timeframe_analysis' in market_state.current_analysis:
            tf_analysis = market_state.current_analysis['timeframe_analysis']

            # Header for timeframe table
            print("   " + "-"*95)
            print("   Timeframe    Price Δ      Momentum       OI Divergence     Volume       Strength")
            print("   " + "-"*95)

            for interval, data in tf_analysis.items():
                price_change = data.get('price_change', 0)
                price_change_pct = data.get('price_change_pct', 0)
                momentum = data.get('momentum', 'N/A')
                oi_divergence = data.get('oi_divergence', 'N/A')
                volume_pattern = data.get('volume_pattern', 'N/A')
                strength = data.get('strength_score', 0)

                print(f"   {interval:>10}: {price_change:+7.2f} ({price_change_pct:+5.2f}%) {momentum:>13} {oi_divergence:>15} {volume_pattern:>12} {strength:>6.2f}/10")

            print("   " + "-"*95)
        else:
            print("   🔄 Multi-timeframe analysis will be available after processing multiple snapshots")
            print("   📊 Currently building historical data foundation")
            print("   ⚠️ Need data for timeframes: 3, 9, 15, 21, 30, 60, 90 minutes")

        # Enhanced Historical price movement (last 15 snapshots)
        print(f"\n📈 DETAILED PRICE MOVEMENT HISTORY (Last 15 Snapshots):")
        if len(market_state.market_history) >= 2:
            print("   #   Time      Spot Price    Change    CE OI        PE OI        OI PCR   CE Vol      PE Vol")
            print("   " + "-"*90)

            history_to_show = min(15, len(market_state.market_history))
            for i, snapshot in enumerate(list(market_state.market_history)[-history_to_show:]):
                snapshot_num = len(market_state.market_history) - history_to_show + i + 1
                timestamp = snapshot.get('timestamp', '00:00:00')[11:19] if 'timestamp' in snapshot else 'N/A'
                spot = snapshot['underlying_value']
                ce_oi = int(snapshot.get('CE_OI', 0))
                pe_oi = int(snapshot.get('PE_OI', 0))
                ce_vol = int(snapshot.get('CE_VOL', 0))
                pe_vol = int(snapshot.get('PE_VOL', 0))
                oi_pcr = snapshot.get('OI_PCR', 0)

                if i > 0:
                    prev_spot = list(market_state.market_history)[-history_to_show+i-1]['underlying_value']
                    change = spot - prev_spot
                    change_str = f"{change:+6.2f}"
                else:
                    change_str = "   N/A"

                print(f"   {snapshot_num:>2}  {timestamp} ₹{spot:>8.2f} {change_str} {ce_oi:>10,} {pe_oi:>10,} {oi_pcr:>7.4f} {ce_vol:>9,} {pe_vol:>9,}")
        else:
            print("   ⚠️ Need at least 2 snapshots for price movement analysis")

        # Enhanced Delta history analysis
        print(f"\n📊 ENHANCED DELTA ANALYSIS (OI/Volume Changes - Last 10 Cycles):")
        if len(market_state.delta_history) >= 1:
            print("   Cycle    Spot Δ    CE OI Δ       PE OI Δ       CE Vol Δ      PE Vol Δ      PCR Δ")
            print("   " + "-"*85)

            delta_to_show = min(10, len(market_state.delta_history))
            for i, delta in enumerate(list(market_state.delta_history)[-delta_to_show:]):
                cycle_num = len(market_state.delta_history) - delta_to_show + i + 1
                spot_delta = delta.get('delta_underlying_value', 0)
                ce_oi_delta = int(delta.get('delta_CE_OI', 0))
                pe_oi_delta = int(delta.get('delta_PE_OI', 0))
                ce_vol_delta = int(delta.get('delta_CE_VOL', 0))
                pe_vol_delta = int(delta.get('delta_PE_VOL', 0))
                pcr_delta = delta.get('delta_OI_PCR', 0)

                print(f"   #{cycle_num:>3}   {spot_delta:+7.2f}  {ce_oi_delta:>11,}  {pe_oi_delta:>11,}  {ce_vol_delta:>11,}  {pe_vol_delta:>11,}  {pcr_delta:+7.4f}")
        else:
            print("   ⚠️ Need at least 1 cycle for delta analysis")

        # Enhanced Technical indicators
        print(f"\n🔧 TECHNICAL INDICATORS:")
        if hasattr(market_state, 'technical_indicators') and market_state.technical_indicators:
            print("   Indicator                    Value      Status")
            print("   " + "-"*45)
            for indicator, value in market_state.technical_indicators.items():
                # Add status interpretation
                if 'rsi' in indicator.lower():
                    status = "Overbought" if value > 70 else "Oversold" if value < 30 else "Neutral"
                elif 'atr' in indicator.lower():
                    status = "High Vol" if value > 50 else "Low Vol" if value < 20 else "Normal"
                else:
                    status = "Normal"
                print(f"   {indicator.replace('_', ' ').title():>25}: {value:>8.2f}   {status}")
        else:
            print("   ⚠️ Technical indicators not calculated yet")
            # Calculate basic indicators
            atr = market_state.get_atr()
            print(f"   {'ATR (Volatility)':>25}: {atr:>8.2f}   {'High' if atr > 50 else 'Normal'}")

        # Enhanced AI Features
        print(f"\n🧠 AI FEATURES GENERATED FOR PREDICTION:")
        ai_features = market_state.get_ai_features()
        if ai_features:
            print("   Feature                         Value      Normalized")
            print("   " + "-"*55)
            for feature, value in ai_features.items():
                # Show normalized values for better understanding
                if 'underlying_value' in feature:
                    normalized = value  # Already normalized by 1000
                elif 'OI' in feature:
                    normalized = value  # Already normalized by 1M
                else:
                    normalized = value
                print(f"   {feature:>30}: {value:>10.4f}   {normalized:>10.4f}")
        else:
            print("   ⚠️ AI features not available yet - need market data")

        # Market State Health Check
        print(f"\n🏥 MARKET STATE HEALTH CHECK:")
        health_status = market_state.self_diagnose()
        print(f"   Overall Health: {health_status}")
        print(f"   Total Analysis: {market_state.analysis_count}")
        print(f"   Error Count: {market_state.error_count}")

        if hasattr(market_state, 'processing_times') and market_state.processing_times:
            avg_time = np.mean(list(market_state.processing_times))
            max_time = np.max(list(market_state.processing_times))
            print(f"   Avg Processing: {avg_time:.3f}s")
            print(f"   Max Processing: {max_time:.3f}s")

        # Data Storage Status
        print(f"\n💾 DATA STORAGE STATUS:")
        print(f"   Market History: {len(market_state.market_history)}/{market_state.market_history.maxlen} snapshots")
        print(f"   Delta History: {len(market_state.delta_history)}/{market_state.delta_history.maxlen} deltas")
        print(f"   Memory Usage: {len(market_state.market_history) * 0.001:.2f} KB (approx)")

        print("="*100 + "\n")

    except Exception as e:
        logger.error(f"❌ Error in comprehensive analysis: {e}")
        print(f"\n📊 BASIC MARKET STATE:")
        if hasattr(market_state, 'last_spot_price'):
            print(f"   Spot: ₹{market_state.last_spot_price:.2f}")
        print(f"   Snapshots: {len(market_state.market_history) if hasattr(market_state, 'market_history') else 0}")
        if hasattr(market_state, 'self_diagnose'):
            print(f"   Status: {market_state.self_diagnose()}")
        print(f"="*100 + "\n")

#=============================================================================
# ENHANCED MARKET STATE UPDATE - ADD MISSING ATTRIBUTES
#=============================================================================
# Add this to your EnhancedMarketState class __init__ method:
def __init__(self, symbol: str, config: Dict[str, Any]):
    # ... existing code ...

    # ADD THESE MISSING ATTRIBUTES:
    self.current_analysis = {}  # For storing timeframe analysis
    self.technical_indicators = {}  # For storing technical indicators

    # ... rest of existing code ...

# =============================================================================
# COMPREHENSIVE DATA PROCESSING WITH ENHANCED LOGGING
# =============================================================================
def process_nse_snapshot_enhanced(raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process raw NSE data into comprehensive structured snapshot with complete validation.
    Calculates totals, ratios, and provides extensive logging of all metrics."""
    logger.info("🔄 Processing NSE snapshot...")
    logger.info("=" * 80)

    # Validate raw data structure
    if not isinstance(raw_data, dict) or "records" not in raw_data:
        logger.error("❌ Invalid raw data structure received")
        return None

    records = raw_data.get("records", {})
    spot = records.get("underlyingValue")
    if not spot:
        logger.warning("⚠️ Spot price missing in NSE response. Skipping processing.")
        return None

    expiry_dates = records.get("expiryDates")
    if not expiry_dates:
        logger.warning("⚠️ Missing expiry dates in NSE data.")
        return None

    nearest_expiry = expiry_dates[0]
    logger.info("📅 Processing data for nearest expiry: %s", nearest_expiry)
    logger.info("💹 Current spot price: ₹%.2f", float(spot))

    # Initialize comprehensive snapshot
    spot_price = float(spot)
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "underlying_value": spot_price,
        "nearest_expiry": nearest_expiry,
        "open": spot_price,
        "high": spot_price,
        "low": spot_price,
        "close": spot_price,
        "CE_OI": 0.0,
        "PE_OI": 0.0,
        "CE_VOL": 0.0,
        "PE_VOL": 0.0,
        "strike_data": {},
        "processing_stats": {
            "total_strikes": 0,
            "valid_ce_strikes": 0,
            "valid_pe_strikes": 0,
            "max_ce_oi_strike": 0,
            "max_pe_oi_strike": 0,
            "max_ce_vol_strike": 0,
            "max_pe_vol_strike": 0,
        }
    }

    # Process each data record with comprehensive tracking
    max_ce_oi = max_pe_oi = max_ce_vol = max_pe_vol = 0
    data_records = records.get("data", [])
    logger.info("📊 Processing %d data records...", len(data_records))
    for rec in data_records:
        if rec.get("expiryDate") != nearest_expiry:
            continue
        try:
            strike = float(rec["strikePrice"])
            ce = rec.get("CE", {})
            pe = rec.get("PE", {})

            # Extract CE data
            ce_oi = float(ce.get("openInterest", 0.0))
            ce_vol = float(ce.get("totalTradedVolume", 0.0))
            ce_ltp = float(ce.get("lastPrice", 0.0))
            ce_iv = float(ce.get("impliedVolatility", 0.0))

            # Extract PE data
            pe_oi = float(pe.get("openInterest", 0.0))
            pe_vol = float(pe.get("totalTradedVolume", 0.0))
            pe_ltp = float(pe.get("lastPrice", 0.0))
            pe_iv = float(pe.get("impliedVolatility", 0.0))

            # Accumulate totals
            snapshot["CE_OI"] += ce_oi
            snapshot["PE_OI"] += pe_oi
            snapshot["CE_VOL"] += ce_vol
            snapshot["PE_VOL"] += pe_vol

            # Track maximums for statistics
            if ce_oi > max_ce_oi:
                max_ce_oi = ce_oi
                snapshot["processing_stats"]["max_ce_oi_strike"] = strike
            if pe_oi > max_pe_oi:
                max_pe_oi = pe_oi
                snapshot["processing_stats"]["max_pe_oi_strike"] = strike
            if ce_vol > max_ce_vol:
                max_ce_vol = ce_vol
                snapshot["processing_stats"]["max_ce_vol_strike"] = strike
            if pe_vol > max_pe_vol:
                max_pe_vol = pe_vol
                snapshot["processing_stats"]["max_pe_vol_strike"] = strike

            # Store comprehensive strike data
            snapshot["strike_data"][strike] = {
                "CE_OI": ce_oi, "PE_OI": pe_oi,
                "CE_LTP": ce_ltp, "PE_LTP": pe_ltp,
                "CE_VOL": ce_vol, "PE_VOL": pe_vol,
                "CE_IV": ce_iv, "PE_IV": pe_iv,
                "total_oi": ce_oi + pe_oi,
                "total_vol": ce_vol + pe_vol,
                "strike_pcr_oi": pe_oi / ce_oi if ce_oi > 0 else 0,
                "strike_pcr_vol": pe_vol / ce_vol if ce_vol > 0 else 0
            }

            # Count valid strikes
            snapshot["processing_stats"]["total_strikes"] += 1
            if ce_oi > 0 or ce_vol > 0:
                snapshot["processing_stats"]["valid_ce_strikes"] += 1
            if pe_oi > 0 or pe_vol > 0:
                snapshot["processing_stats"]["valid_pe_strikes"] += 1
        except (ValueError, TypeError, KeyError) as e:
            logger.warning("⚠️ Error processing strike data: %s", e)
            continue

    # Calculate comprehensive ratios and metrics
    snapshot["OI_PCR"] = snapshot["PE_OI"] / snapshot["CE_OI"] if snapshot["CE_OI"] > 0 else 0.0
    snapshot["VOL_PCR"] = snapshot["PE_VOL"] / snapshot["CE_VOL"] if snapshot["CE_VOL"] > 0 else 0.0

    # Additional calculated metrics
    total_oi = snapshot["CE_OI"] + snapshot["PE_OI"]
    total_vol = snapshot["CE_VOL"] + snapshot["PE_VOL"]
    snapshot["total_market_oi"] = total_oi
    snapshot["total_market_volume"] = total_vol
    snapshot["ce_oi_percentage"] = (snapshot["CE_OI"] / total_oi * 100) if total_oi > 0 else 0
    snapshot["pe_oi_percentage"] = (snapshot["PE_OI"] / total_oi * 100) if total_oi > 0 else 0
    snapshot["ce_vol_percentage"] = (snapshot["CE_VOL"] / total_vol * 100) if total_vol > 0 else 0
    snapshot["pe_vol_percentage"] = (snapshot["PE_VOL"] / total_vol * 100) if total_vol > 0 else 0

    # Enhanced Greeks and volatility smile calculation with error handling
    try:
        # Calculate time to expiry in years (approximate, for Greeks only)
        time_to_exp = 1 / 365  # If precise expiry needed, compute delta from expiry date
        greek_data = {}
        for strike, data in snapshot["strike_data"].items():
            try:
                ce_iv = data.get("CE_IV", 0) / 100
                pe_iv = data.get("PE_IV", 0) / 100
                if ce_iv > 0 and time_to_exp > 0:
                    ce_delta, ce_gamma = black_scholes_greeks(
                        snapshot['underlying_value'], strike, time_to_exp, ce_iv, option_type='call'
                    )
                else:
                    ce_delta, ce_gamma = 0.0, 0.0
                if pe_iv > 0 and time_to_exp > 0:
                    pe_delta, pe_gamma = black_scholes_greeks(
                        snapshot['underlying_value'], strike, time_to_exp, pe_iv, option_type='put'
                    )
                else:
                    pe_delta, pe_gamma = 0.0, 0.0
                greek_data[strike] = {
                    'ce_delta': ce_delta,
                    'ce_gamma': ce_gamma,
                    'pe_delta': pe_delta,
                    'pe_gamma': pe_gamma
                }
            except Exception as e:
                logger.warning("⚠️ Error calculating Greeks for strike %s: %s", strike, e)
                greek_data[strike] = {
                    'ce_delta': 0.0, 'ce_gamma': 0.0, 'pe_delta': 0.0, 'pe_gamma': 0.0
                }
        snapshot["greek_data"] = greek_data

        # Calculate volatility smile (CE OTM minus ITM IV)
        strikes = sorted(snapshot["strike_data"].keys())
        if strikes:
            atm = min(strikes, key=lambda k: abs(k - snapshot['underlying_value']))
            otm_ce_ivs = [data['CE_IV'] for s, data in snapshot["strike_data"].items()
                         if s > atm and data['CE_IV'] > 0]
            itm_ce_ivs = [data['CE_IV'] for s, data in snapshot["strike_data"].items()
                         if s < atm and data['CE_IV'] > 0]
            if otm_ce_ivs and itm_ce_ivs:
                snapshot["vol_smile_ce"] = np.mean(otm_ce_ivs) - np.mean(itm_ce_ivs)
            else:
                snapshot["vol_smile_ce"] = 0.0
        else:
            snapshot["vol_smile_ce"] = 0.0
    except Exception as e:
        logger.warning("⚠️ Error calculating Greeks/vol smile: %s", e)
        snapshot["greek_data"] = {}
        snapshot["vol_smile_ce"] = 0.0

    # Comprehensive logging of all processed data
    logger.info("📊 COMPREHENSIVE DATA PROCESSING COMPLETE")
    logger.info("=" * 80)
    logger.info("💹 SPOT PRICE: ₹%.2f", snapshot["underlying_value"])
    logger.info("-" * 80)
    logger.info("📈 OPEN INTEREST TOTALS:")
    logger.info(" CE Total OI: %s (%.1f%%)", f"{int(snapshot['CE_OI']):,}", snapshot["ce_oi_percentage"])
    logger.info(" PE Total OI: %s (%.1f%%)", f"{int(snapshot['PE_OI']):,}", snapshot["pe_oi_percentage"])
    logger.info(" Total Market OI: %s", f"{int(total_oi):,}")
    logger.info(" OI PCR: %.4f", snapshot["OI_PCR"])
    logger.info("-" * 80)
    logger.info("📊 VOLUME TOTALS:")
    logger.info(" CE Total Volume: %s (%.1f%%)", f"{int(snapshot['CE_VOL']):,}", snapshot["ce_vol_percentage"])
    logger.info(" PE Total Volume: %s (%.1f%%)", f"{int(snapshot['PE_VOL']):,}", snapshot["pe_vol_percentage"])
    logger.info(" Total Market Volume: %s", f"{int(total_vol):,}")
    logger.info(" Volume PCR: %.4f", snapshot["VOL_PCR"])
    logger.info("-" * 80)
    logger.info("🎯 KEY STRIKES:")
    logger.info(" Max CE OI Strike: %.0f (OI: %s)", snapshot["processing_stats"]["max_ce_oi_strike"], f"{int(max_ce_oi):,}")
    logger.info(" Max PE OI Strike: %.0f (OI: %s)", snapshot["processing_stats"]["max_pe_oi_strike"], f"{int(max_pe_oi):,}")
    logger.info(" Max CE Vol Strike: %.0f (Vol: %s)", snapshot["processing_stats"]["max_ce_vol_strike"], f"{int(max_ce_vol):,}")
    logger.info(" Max PE Vol Strike: %.0f (Vol: %s)", snapshot["processing_stats"]["max_pe_vol_strike"], f"{int(max_pe_vol):,}")
    logger.info("-" * 80)
    logger.info("📋 PROCESSING STATISTICS:")
    logger.info(" Total Strikes Processed: %d", snapshot["processing_stats"]["total_strikes"])
    logger.info(" Valid CE Strikes: %d", snapshot["processing_stats"]["valid_ce_strikes"])
    logger.info(" Valid PE Strikes: %d", snapshot["processing_stats"]["valid_pe_strikes"])
    logger.info(" Greeks Calculated: %d strikes", len(snapshot['greek_data']))
    logger.info(" Volatility Smile: %.2f", snapshot.get('vol_smile_ce', 0))
    logger.info(" Data Quality: HIGH (NSE Direct)")
    logger.info("=" * 80)
    return snapshot

#=============================================================================
# MODULE 1: STOP LOSS CALCULATION ENGINE
#=============================================================================
class StopLossCalculator:
    """Dedicated module for stop loss calculations."""

    def __init__(self, config):
        self.config = config

    def calculate_stop_loss(self, entry_price: float, risk_mult: float, is_bullish: bool) -> float:
        """Calculate stop loss with fixed point system."""
        base_sl_points = 2.0 * risk_mult  # ₹2 per risk level

        # Both CE and PE use same SL logic - price goes DOWN from entry
        sl = entry_price - base_sl_points  # Entry 43 -> SL 41

        logger.info(f"🛡️ SL Calculated: Entry ₹{entry_price:.2f} -> SL ₹{sl:.2f} (Risk: ₹{base_sl_points:.2f})")
        return sl

    def validate_stop_loss(self, entry_price: float, sl: float, min_risk: float = 1.0) -> bool:
        """Validate stop loss parameters."""
        risk_amount = abs(entry_price - sl)
        if risk_amount < min_risk:
            logger.warning(f"⚠️ Risk too low: ₹{risk_amount:.2f} < ₹{min_risk:.2f}")
            return False
        return True

#=============================================================================
# CORRECTED PE/CE TARGET CALCULATION - FINAL FIX
#=============================================================================
def calculate_correct_trade_levels(entry_price: float, risk_mult: float, level: str) -> Dict[str, float]:
    base_sl_points = 2.0 * risk_mult  # ₹2 per risk level
    target1_points = 6.0  # ₹6 profit for T1
    target2_points = 20.0 if level == "FULL_POWER" else 16.0  # ₹16-20 for T2
    sl = entry_price - base_sl_points
    target1 = entry_price + target1_points
    target2 = entry_price + target2_points
    risk_amount = entry_price - sl
    reward_t1 = target1 - entry_price
    reward_t2 = target2 - entry_price
    return {
        "entry_price": entry_price,
        "stop_loss": sl,
        "target1": target1,
        "target2": target2,
        "risk_amount": risk_amount,
        "reward_t1": reward_t1,
        "reward_t2": reward_t2,
    }

def generate_progressive_recommendation(decision: Dict[str, Any], market_state, day_profile) -> str:
    verdict = decision['verdict']
    level = decision['confidence_level']
    if verdict == "NEUTRAL":
        return f"🔍 [{level}] No clear signals detected. Continue monitoring."

    snapshot = market_state.market_history[-1]
    spot = snapshot['underlying_value']
    strikes = sorted(snapshot.get("strike_data", {}).keys())
    if not strikes:
        return "❌ Insufficient strike data for recommendation."

    atm_strike = min(strikes, key=lambda k: abs(k - spot))
    strike_data = snapshot["strike_data"][atm_strike]
    is_bullish = "BULLISH" in verdict
    option_type = "CE" if is_bullish else "PE"
    entry_price = strike_data.get(f"{option_type}_LTP", 0)
    if entry_price <= 0:
        return "❌ Invalid option price data."

    position_multipliers = {
        "EARLY_SIGNALS": 0.5,
        "MEDIUM_CONFIDENCE": 0.75,
        "HIGH_CONFIDENCE": 1.0,
        "FULL_POWER": 1.0,
    }
    risk_multipliers = position_multipliers.copy()
    pos_mult = position_multipliers.get(level, 0.5)
    risk_mult = risk_multipliers.get(level, 0.5)

    # Calculate corrected targets & SL
    trade_levels = calculate_correct_trade_levels(entry_price, risk_mult, level)
    sl = trade_levels["stop_loss"]
    target1 = trade_levels["target1"]
    target2 = trade_levels["target2"]

    risk_amount = trade_levels["risk_amount"]
    reward_t1 = trade_levels["reward_t1"]
    reward_t2 = trade_levels["reward_t2"]

    if level in ["MEDIUM_CONFIDENCE", "HIGH_CONFIDENCE", "FULL_POWER"]:
        day_profile.active_trade = {
            "type": option_type,
            "strike": atm_strike,
            "entry": entry_price,
            "sl": sl,
            "partial_target": target1,
            "target": target2,
            "original_sl": sl,
            "entry_time": datetime.now(),
            "confidence_level": level,
            "monitored": True,
            "risk_reward_t1": reward_t1 / risk_amount if risk_amount > 0 else 0,
            "risk_reward_t2": reward_t2 / risk_amount if risk_amount > 0 else 0,
        }

    # Compose Telegram message with enhanced volume pattern analysis (if available in decision)
    # (The detailed Telegram integration code can be included here using your existing format)

    return f"✅ Recommendation generated: {option_type} {atm_strike}, Entry ₹{entry_price:.2f}, SL ₹{sl:.2f}, Targets ₹{target1:.2f} / ₹{target2:.2f}"

#=============================================================================
# MODULE 3: RISK-REWARD VALIDATION ENGINE
#=============================================================================
class RiskRewardValidator:
    """Dedicated module for risk-reward analysis."""

    def __init__(self, config):
        self.config = config
        self.min_rr_ratio = config.get("risk", {}).get("min_rr_ratio", 2.0)

    def validate_risk_reward(self, entry_price: float, sl: float, target1: float, target2: float) -> Dict[str, float]:
        """Validate and log risk-reward ratios."""
        risk_amount = abs(entry_price - sl)
        reward_t1 = abs(target1 - entry_price)
        reward_t2 = abs(target2 - entry_price)

        rr_t1 = reward_t1 / risk_amount if risk_amount > 0 else 0
        rr_t2 = reward_t2 / risk_amount if risk_amount > 0 else 0

        logger.info(f"⚖️ Risk-Reward Analysis:")
        logger.info(f"   Risk: ₹{risk_amount:.2f}")
        logger.info(f"   T1 R:R = 1:{rr_t1:.1f}")
        logger.info(f"   T2 R:R = 1:{rr_t2:.1f}")

        # Validate minimum requirements
        if rr_t1 < self.min_rr_ratio:
            logger.warning(f"⚠️ T1 R:R below minimum: {rr_t1:.1f} < {self.min_rr_ratio}")

        return {
            "risk_amount": risk_amount,
            "reward_t1": reward_t1,
            "reward_t2": reward_t2,
            "rr_ratio_t1": rr_t1,
            "rr_ratio_t2": rr_t2,
            "meets_min_rr": rr_t1 >= self.min_rr_ratio
        }

    def calculate_position_size(self, account_balance: float, risk_amount: float, max_risk_pct: float = 2.0) -> int:
        """Calculate optimal position size based on risk."""
        max_risk_amount = account_balance * (max_risk_pct / 100)
        position_size = int(max_risk_amount / risk_amount)
        return max(1, position_size)  # Minimum 1 lot

#=============================================================================
# MODULE 4: OPTION PRICING LOGIC EXPLAINER
#=============================================================================
class OptionPricingExplainer:
    """Dedicated module for option pricing explanations."""

    @staticmethod
    def log_option_pricing_logic(is_bullish: bool) -> None:
        """Log explanation of option pricing behavior."""
        if is_bullish:
            logger.info(f"📚 CE Option Logic:")
            logger.info(f"   ✅ Market UP = CE price UP (profit on targets)")
            logger.info(f"   ❌ Market DOWN = CE price DOWN (loss to SL)")
        else:
            logger.info(f"📚 PE Option Logic:")
            logger.info(f"   ✅ Market DOWN = PE price UP (profit on targets)")
            logger.info(f"   ❌ Market UP = PE price DOWN (loss to SL)")

        logger.info(f"🎯 Both CE and PE have UPWARD targets (premium increase)")

    @staticmethod
    def explain_trade_setup(entry_price: float, sl: float, target1: float, target2: float, is_bullish: bool) -> str:
        """Generate detailed trade explanation."""
        option_type = "CE (Call)" if is_bullish else "PE (Put)"
        market_direction = "UP" if is_bullish else "DOWN"

        explanation = f"""
📊 TRADE SETUP EXPLANATION:
Option Type: {option_type}
Entry: ₹{entry_price:.2f}
Expected Market Direction: {market_direction}

💡 Why Targets are HIGHER than Entry:
- When market moves in our favor, option premium INCREASES
- We sell at higher premium = profit
- Entry ₹{entry_price:.2f} → T1 ₹{target1:.2f} → T2 ₹{target2:.2f}

🛡️ Why SL is LOWER than Entry:
- When market moves against us, option premium DECREASES
- We exit at lower premium = controlled loss
- Entry ₹{entry_price:.2f} → SL ₹{sl:.2f}
        """
        return explanation.strip()

# =============================================================================
# MODULE 5: TRADE LEVEL ORCHESTRATOR
# =============================================================================
class TargetCalculator:
    """Simple target calculator used by TradeLevelOrchestrator."""
    def __init__(self, config):
        self.config = config

    def calculate_targets(self, entry_price: float, level: str, is_bullish: bool) -> Tuple[float, float]:
        target1_points = 6.0
        target2_points = 20.0 if level == "FULL_POWER" else 16.0
        t1 = entry_price + target1_points
        t2 = entry_price + target2_points
        return t1, t2

    def calculate_dynamic_targets(self, entry_price: float, volatility: float, level: str) -> tuple[float, float]:
        base_t1 = 6.0
        base_t2 = 20.0 if level == "FULL_POWER" else 16.0
        vol_mult = max(0.7, min(1.5, (volatility / 50.0) if volatility else 1.0))
        t1 = entry_price + base_t1 * vol_mult
        t2 = entry_price + base_t2 * vol_mult
        return t1, t2

class TradeLevelOrchestrator:
    """Main orchestrator for all trade level calculations."""

    def __init__(self, config):
        self.config = config
        self.sl_calculator = StopLossCalculator(config)
        self.target_calculator = TargetCalculator(config)
        self.rr_validator = RiskRewardValidator(config)
        self.explainer = OptionPricingExplainer()

    def calculate_complete_trade_levels(self, entry_price: float, risk_mult: float, level: str, is_bullish: bool, volatility: float = 0.0) -> Dict[str, Any]:
        """Complete orchestrator for all trade level calculations."""

        # Log option pricing explanation
        self.explainer.log_option_pricing_logic(is_bullish)

        # Calculate SL
        sl = self.sl_calculator.calculate_stop_loss(entry_price, risk_mult, is_bullish)

        # Validate SL
        if not self.sl_calculator.validate_stop_loss(entry_price, sl):
            logger.warning("⚠️ Stop loss validation failed")

        # Calculate targets (use dynamic if volatility provided)
        if volatility > 0:
            target1, target2 = self.target_calculator.calculate_dynamic_targets(entry_price, volatility, level)
            logger.info("🔄 Using dynamic targets based on volatility")
        else:
            target1, target2 = self.target_calculator.calculate_targets(entry_price, level, is_bullish)

        # Validate risk-reward
        rr_analysis = self.rr_validator.validate_risk_reward(entry_price, sl, target1, target2)

        # Generate explanation
        trade_explanation = self.explainer.explain_trade_setup(entry_price, sl, target1, target2, is_bullish)

        # Final summary log
        logger.info(f"📊 COMPLETE TRADE SETUP:")
        logger.info(f"   Entry: ₹{entry_price:.2f}")
        logger.info(f"   SL: ₹{sl:.2f}")
        logger.info(f"   T1: ₹{target1:.2f}")
        logger.info(f"   T2: ₹{target2:.2f}")
        logger.info(f"   Type: {'CE (Call)' if is_bullish else 'PE (Put)'}")
        logger.info(f"   Risk Level: {risk_mult}x")
        logger.info(f"   Confidence: {level}")

        return {
            "entry_price": entry_price,
            "stop_loss": sl,
            "target1": target1,
            "target2": target2,
            "risk_reward_analysis": rr_analysis,
            "trade_type": "CE" if is_bullish else "PE",
            "risk_multiplier": risk_mult,
            "confidence_level": level,
            "trade_explanation": trade_explanation,
            "meets_requirements": rr_analysis["meets_min_rr"],
            "volatility_adjusted": volatility > 0
        }
#=============================================================================
# ENHANCED MARKET STATE CLASS - COMPLETE DEFINITION
#=============================================================================
from collections import deque
import numpy as np
import time
from datetime import datetime
import json
from typing import Dict, Any, List

class EnhancedMarketState:
    """Enhanced market state management with comprehensive data tracking."""

    def __init__(self, symbol: str, config: Dict[str, Any]):
        self.symbol = symbol
        self.config = config

        # Core data structures
        self.market_history = deque(maxlen=150)  # Store last 150 snapshots
        self.delta_history = deque(maxlen=50)    # Store delta calculations

        # Current state variables
        self.last_spot_price = 0.0
        self.last_update_time = None
        self.data_quality_score = 10.0

        # Analysis tracking
        self.analysis_count = 0
        self.error_count = 0
        self.last_analysis_time = None

        # Performance metrics
        self.processing_times = deque(maxlen=20)
        self.data_freshness_scores = deque(maxlen=20)

        # Technical indicators storage
        self.technical_indicators = {}

        # Initialize logging
        logger.info(f"🚀 Enhanced Market State initialized for {symbol}")
        logger.info(f"📊 Max history: {self.market_history.maxlen} snapshots")

    def update(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update market state with new snapshot and return analysis."""
        start_time = time.time()

        try:
            # Add timestamp if not present
            if 'timestamp' not in snapshot_data:
                snapshot_data['timestamp'] = datetime.now().isoformat()

            # Update current state
            self.last_spot_price = snapshot_data.get('underlying_value', self.last_spot_price)
            self.last_update_time = datetime.now()

            # Add to history
            self.market_history.append(snapshot_data)

            # Calculate and store deltas if we have previous data
            if len(self.market_history) >= 2:
                self._calculate_deltas()

            # Update performance metrics
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)

            # Update analysis count
            self.analysis_count += 1
            self.last_analysis_time = datetime.now()

            # Calculate data quality score
            self._update_data_quality_score(snapshot_data)

            logger.info(f"🔄 Updating market state for {self.symbol}")
            logger.info(f"📊 Market History Updated:")
            logger.info(f"  Current Length: {len(self.market_history)} snapshots")
            logger.info(f"  Data Quality Score: {self.data_quality_score}/10")
            logger.info(f"  Latest Spot: ₹{self.last_spot_price:.2f}")

            return snapshot_data

        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ Error updating market state for {self.symbol}: {e}")
            return {}

    def _calculate_deltas(self) -> None:
        """Calculate deltas between current and previous snapshot."""
        try:
            current = list(self.market_history)[-1]
            previous = list(self.market_history)[-2]

            deltas = {}

            # Calculate all delta values
            for key in ['CE_OI', 'PE_OI', 'CE_VOL', 'PE_VOL', 'underlying_value', 'OI_PCR', 'VOL_PCR']:
                current_val = current.get(key, 0)
                previous_val = previous.get(key, 0)

                delta = current_val - previous_val
                delta_pct = (delta / previous_val * 100) if previous_val != 0 else 0

                deltas[f'delta_{key}'] = delta
                deltas[f'delta_{key}_pct'] = delta_pct

            # Add timestamp
            deltas['timestamp'] = datetime.now().isoformat()

            # Store in delta history
            self.delta_history.append(deltas)

            # Enhanced logging of delta calculations
            logger.info(f"📈 Delta Analysis:")
            for key in ['CE_OI', 'PE_OI', 'CE_VOL', 'PE_VOL', 'underlying_value', 'OI_PCR', 'VOL_PCR']:
                delta_val = deltas.get(f'delta_{key}', 0)
                delta_pct = deltas.get(f'delta_{key}_pct', 0)
                logger.info(f"  delta_{key}: {delta_val:+.2f}")
                logger.info(f"  delta_{key}_pct: {delta_pct:+.2f}")

        except Exception as e:
            logger.error(f"❌ Error calculating deltas: {e}")

    def _update_data_quality_score(self, snapshot_data: Dict[str, Any]) -> None:
        """Update data quality score based on completeness and freshness."""
        quality_score = 10.0

        # Check data completeness
        required_fields = ['underlying_value', 'CE_OI', 'PE_OI', 'CE_VOL', 'PE_VOL', 'OI_PCR']
        missing_fields = [field for field in required_fields if field not in snapshot_data or snapshot_data[field] is None]

        if missing_fields:
            quality_score -= len(missing_fields) * 1.5
            logger.warning(f"⚠️ Missing fields in snapshot: {missing_fields}")

        # Check for zero values (suspicious)
        zero_fields = [field for field in required_fields if snapshot_data.get(field, 0) == 0]
        if zero_fields:
            quality_score -= len(zero_fields) * 0.5

        # Check data freshness
        if self.last_update_time:
            time_since_update = (datetime.now() - self.last_update_time).total_seconds()
            if time_since_update > 300:  # More than 5 minutes
                quality_score -= 2.0

        self.data_quality_score = max(0.0, quality_score)
        self.data_freshness_scores.append(self.data_quality_score)

    def get_current_state(self) -> Dict[str, Any]:
        """Get current market state summary."""
        if not self.market_history:
            return {"error": "No market data available"}

        current_snapshot = list(self.market_history)[-1]

        return {
            "symbol": self.symbol,
            "current_spot": self.last_spot_price,
            "last_update": self.last_update_time.isoformat() if self.last_update_time else None,
            "data_quality": self.data_quality_score,
            "total_snapshots": len(self.market_history),
            "total_deltas": len(self.delta_history),
            "analysis_count": self.analysis_count,
            "error_count": self.error_count,
            "current_snapshot": current_snapshot
        }

    def get_ai_features(self) -> Dict[str, float]:
        """Generate AI features for prediction."""
        if len(self.market_history) < 2:
            return {}

        current = list(self.market_history)[-1]

        return {
            'rsi_value': 50.0,  # Default RSI
            'oi_acceleration': current.get('CE_OI', 0) - current.get('PE_OI', 0),
            'max_pain_gravity': 0.0,
            'fear_gauge': current.get('OI_PCR', 1.0),
            'historical_trend': 0.0,
            'underlying_value': current.get('underlying_value', 0) / 1000,
            'CE_OI': current.get('CE_OI', 0) / 1000000,
            'PE_OI': current.get('PE_OI', 0) / 1000000,
            'OI_PCR': current.get('OI_PCR', 0),
            'VOL_PCR': current.get('VOL_PCR', 0)
        }

    def get_atr(self) -> float:
        """Calculate Average True Range."""
        if len(self.market_history) < 5:
            return 20.0  # Default ATR

        recent_data = list(self.market_history)[-5:]
        price_changes = []

        for i in range(1, len(recent_data)):
            current_price = recent_data[i].get('underlying_value', 0)
            previous_price = recent_data[i-1].get('underlying_value', 0)
            if previous_price > 0:
                change = abs(current_price - previous_price)
                price_changes.append(change)

        return float(np.mean(price_changes)) if price_changes else 20.0

    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive market state status."""
        return {
            "symbol": self.symbol,
            "data_quality": self.data_quality_score,
            "snapshots": len(self.market_history),
            "last_update": self.last_update_time,
            "atr": self.get_atr(),
            "current_spot": self.last_spot_price
        }

    def self_diagnose(self) -> str:
        """Perform self-diagnosis of market state health."""
        issues = []

        # Check data availability
        if len(self.market_history) == 0:
            issues.append("NO_DATA")
        elif len(self.market_history) < 5:
            issues.append("INSUFFICIENT_DATA")

        # Check data quality
        if self.data_quality_score < 7.0:
            issues.append("LOW_QUALITY")

        # Check error rate
        if self.error_count > 0 and self.analysis_count > 0:
            error_rate = (self.error_count / self.analysis_count) * 100
            if error_rate > 10:
                issues.append("HIGH_ERROR_RATE")

        if not issues:
            return "HEALTHY"
        elif len(issues) == 1:
            return f"WARNING_{issues[0]}"
        else:
            return f"CRITICAL_{'_'.join(issues[:2])}"
    def safe_get_recent_history(self, count: int) -> List[Dict]:
        """Safely get recent history converting deque to list."""
        try:
            history_list = list(self.market_history)
            return history_list[-count:] if len(history_list) >= count else history_list
        except Exception as e:
            logger.warning(f"⚠️ Error getting recent history: {e}")
            return []

    def safe_get_history_slice(self, start_idx: int, end_idx: int = None) -> List[Dict]:
        """Safely get history slice converting deque to list."""
        try:
            history_list = list(self.market_history)
            if end_idx is None:
                return history_list[start_idx:]
            else:
                return history_list[start_idx:end_idx]
        except Exception as e:
            logger.warning(f"⚠️ Error getting history slice: {e}")
            return []

    def save_enhanced_historical_data(self):
        """Save historical data for session continuity."""
        try:
            data = {
                'market_history': list(self.market_history),
                'delta_history': list(self.delta_history),
                'last_spot_price': self.last_spot_price,
                'data_quality_score': self.data_quality_score,
                'analysis_count': self.analysis_count
            }

            filename = f"{self.symbol}_enhanced_historical_data.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)

            logger.info(f"💾 Enhanced historical data saved for {self.symbol} ({len(self.market_history)} entries + metadata)")

        except Exception as e:
            logger.error(f"❌ Error saving enhanced historical data: {e}")

#=============================================================================
# MODULE 6: PREDICTIVE EXIT SYSTEM - FIXED VERSION
#=============================================================================
class PredictiveExitAnalyzer:
    """Advanced predictive exit system with modular components."""

    def __init__(self, config):
        self.config = config

    def safe_get_recent_history(self, market_state, count: int) -> List[Dict]:
        """Safely get recent history converting deque to list."""
        try:
            history_list = list(market_state.market_history)
            return history_list[-count:] if len(history_list) >= count else history_list
        except Exception as e:
            logger.warning(f"⚠️ Error getting recent history: {e}")
            return []

    def analyze_momentum_shift(self, market_state, trade, is_bullish: bool) -> tuple:
        """Analyze momentum shift patterns."""
        exit_signals = []
        strength = 0

        if len(market_state.delta_history) >= 3:
            recent_deltas = list(market_state.delta_history)[-3:]

            if is_bullish:
                # For CE trades - look for bearish momentum building
                pe_oi_acceleration = sum([d.get('delta_PE_OI', 0) for d in recent_deltas[-2:]])
                ce_oi_deceleration = sum([d.get('delta_CE_OI', 0) for d in recent_deltas[-2:]])

                if pe_oi_acceleration > 15000 and ce_oi_deceleration < -5000:
                    exit_signals.append("BEARISH_MOMENTUM_BUILDING")
                    strength += 4
            else:
                # For PE trades - look for bullish momentum building
                ce_oi_acceleration = sum([d.get('delta_CE_OI', 0) for d in recent_deltas[-2:]])
                pe_oi_deceleration = sum([d.get('delta_PE_OI', 0) for d in recent_deltas[-2:]])

                if ce_oi_acceleration > 15000 and pe_oi_deceleration < -5000:
                    exit_signals.append("BULLISH_MOMENTUM_BUILDING")
                    strength += 4

        return exit_signals, strength

    def analyze_volume_divergence(self, market_state, is_bullish: bool) -> tuple:
        """Analyze volume divergence patterns."""
        exit_signals = []
        strength = 0

        if len(market_state.market_history) >= 2:
            market_history_list = list(market_state.market_history)
            current = market_history_list[-1]
            previous = market_history_list[-2]

            ce_vol_change = current.get('CE_VOL', 0) - previous.get('CE_VOL', 0)
            pe_vol_change = current.get('PE_VOL', 0) - previous.get('PE_VOL', 0)

            # For bullish trades - watch for PE volume spikes
            if is_bullish and pe_vol_change > 800000 and pe_vol_change > ce_vol_change * 1.5:
                exit_signals.append("HIGH_PE_VOLUME_DIVERGENCE")
                strength += 3

            # For bearish trades - watch for CE volume spikes
            elif not is_bullish and ce_vol_change > 800000 and ce_vol_change > pe_vol_change * 1.5:
                exit_signals.append("HIGH_CE_VOLUME_DIVERGENCE")
                strength += 3

        return exit_signals, strength

    def analyze_pcr_shift(self, market_state, current_snapshot, is_bullish: bool) -> tuple:
        """Analyze PCR shift patterns."""
        exit_signals = []
        strength = 0

        current_pcr = current_snapshot.get('OI_PCR', 1.0)

        if len(market_state.market_history) >= 3:
            market_history_list = list(market_state.market_history)
            pcr_trend = []

            for i in range(-3, 0):
                if len(market_history_list) >= abs(i):
                    pcr_trend.append(market_history_list[i].get('OI_PCR', 1.0))

            if len(pcr_trend) >= 2:
                pcr_change = pcr_trend[-1] - pcr_trend[0]

                # For bullish trades - rising PCR is bearish
                if is_bullish and pcr_change > 0.02 and current_pcr > 0.75:
                    exit_signals.append("PCR_TURNING_BEARISH")
                    strength += 2

                # For bearish trades - falling PCR is bullish
                elif not is_bullish and pcr_change < -0.02 and current_pcr < 1.25:
                    exit_signals.append("PCR_TURNING_BULLISH")
                    strength += 2

        return exit_signals, strength

    def analyze_profit_protection(self, trade, current_pnl: float) -> tuple:
        """Analyze profit protection signals."""
        exit_signals = []
        strength = 0

        if current_pnl > 3.0:  # If we have decent profits
            # Check if we're losing momentum from peak
            peak_pnl = trade.get('peak_pnl', current_pnl)
            if current_pnl > peak_pnl:
                trade['peak_pnl'] = current_pnl
                peak_pnl = current_pnl

            pnl_drawdown = peak_pnl - current_pnl

            # Exit if losing more than 40% of peak gains
            if pnl_drawdown > peak_pnl * 0.4 and pnl_drawdown > 2.0:
                exit_signals.append("PROFIT_EROSION_DETECTED")
                strength += 3

        return exit_signals, strength

    def analyze_spot_momentum_shift(self, market_state, is_bullish: bool) -> tuple:
        """Analyze spot price momentum shifts."""
        exit_signals = []
        strength = 0

        if len(market_state.market_history) >= 4:
            # FIXED: Convert deque to list before slicing
            market_history_list = list(market_state.market_history)
            recent_spots = [m.get('underlying_value', 0) for m in market_history_list[-4:]]

            # Calculate momentum score
            momentum_changes = []
            for i in range(1, len(recent_spots)):
                momentum_changes.append(recent_spots[i] - recent_spots[i-1])

            if len(momentum_changes) > 0:
                avg_momentum = np.mean(momentum_changes)
                latest_momentum = momentum_changes[-1]

                # Detect momentum reversal
                if is_bullish and avg_momentum > 0 and latest_momentum < -10:
                    exit_signals.append("SPOT_MOMENTUM_REVERSAL")
                    strength += 2
                elif not is_bullish and avg_momentum < 0 and latest_momentum > 10:
                    exit_signals.append("SPOT_MOMENTUM_REVERSAL")
                    strength += 2

        return exit_signals, strength

    def analyze_predictive_exit_signals(self, analysis: Dict[str, Any], day_profile, market_state) -> Dict[str, Any]:
        """Complete predictive exit analysis orchestrator."""
        trade = day_profile.active_trade
        if not trade:
            return {"exit_signal": False, "reason": "No active trade"}

        # FIXED: Safe access to market history
        if len(market_state.market_history) == 0:
            return {"exit_signal": False, "reason": "No market history available"}

        current_snapshot = list(market_state.market_history)[-1]
        trade_type = trade['type']
        is_bullish = (trade_type == "CE")

        # Get current LTP and PnL
        strike_data = current_snapshot.get('strike_data', {})
        current_ltp = strike_data.get(trade['strike'], {}).get(f"{trade_type}_LTP", trade['entry'])
        current_pnl = ((current_ltp - trade['entry']) / trade['entry']) * 100

        # Analyze all exit signals
        all_exit_signals = []
        total_exit_strength = 0

        # 1. Momentum shift analysis
        momentum_signals, momentum_strength = self.analyze_momentum_shift(market_state, trade, is_bullish)
        all_exit_signals.extend(momentum_signals)
        total_exit_strength += momentum_strength

        # 2. Volume divergence analysis
        volume_signals, volume_strength = self.analyze_volume_divergence(market_state, is_bullish)
        all_exit_signals.extend(volume_signals)
        total_exit_strength += volume_strength

        # 3. PCR shift analysis
        pcr_signals, pcr_strength = self.analyze_pcr_shift(market_state, current_snapshot, is_bullish)
        all_exit_signals.extend(pcr_signals)
        total_exit_strength += pcr_strength

        # 4. Profit protection analysis
        profit_signals, profit_strength = self.analyze_profit_protection(trade, current_pnl)
        all_exit_signals.extend(profit_signals)
        total_exit_strength += profit_strength

        # 5. Spot momentum analysis
        spot_signals, spot_strength = self.analyze_spot_momentum_shift(market_state, is_bullish)
        all_exit_signals.extend(spot_signals)
        total_exit_strength += spot_strength

        # DECISION LOGIC
        if total_exit_strength >= 6:  # Strong exit signal
            return {
                "exit_signal": True,
                "exit_type": "PREDICTIVE_EXIT",
                "reason": f"Predictive signals detected: {', '.join(all_exit_signals)}",
                "strength": total_exit_strength,
                "current_pnl": current_pnl
            }
        elif total_exit_strength >= 4:  # Warning signal
            return {
                "exit_signal": False,
                "exit_type": "WARNING",
                "reason": f"Exit warning: {', '.join(all_exit_signals)}",
                "strength": total_exit_strength,
                "current_pnl": current_pnl
            }

        return {"exit_signal": False, "reason": "No predictive exit signals", "current_pnl": current_pnl}

#=============================================================================
# MODULE 7: REAL-TIME MOMENTUM CALCULATOR
#=============================================================================
class MomentumCalculator:
    """Real-time momentum calculation system."""

    def __init__(self, config):
        self.config = config

    def calculate_real_time_momentum(self, market_state) -> Dict[str, float]:
        """Calculate real-time momentum for predictive exits."""
        if len(market_state.market_history) < 5:
            return {"momentum_score": 0.0, "momentum_direction": "NEUTRAL"}

        # FIXED: Get recent 5 snapshots safely
        market_history_list = list(market_state.market_history)
        recent_data = market_history_list[-5:]

        # Calculate various momentum indicators
        spot_momentum = []
        oi_momentum = []
        vol_momentum = []

        for i in range(1, len(recent_data)):
            current = recent_data[i]
            previous = recent_data[i-1]

            # Spot momentum
            spot_change = current.get('underlying_value', 0) - previous.get('underlying_value', 0)
            spot_momentum.append(spot_change)

            # OI momentum (CE vs PE)
            ce_oi_change = current.get('CE_OI', 0) - previous.get('CE_OI', 0)
            pe_oi_change = current.get('PE_OI', 0) - previous.get('PE_OI', 0)
            oi_bias = ce_oi_change - pe_oi_change  # Positive = bearish, Negative = bullish
            oi_momentum.append(-oi_bias)  # Invert for bullish positive

            # Volume momentum
            ce_vol_change = current.get('CE_VOL', 0) - previous.get('CE_VOL', 0)
            pe_vol_change = current.get('PE_VOL', 0) - previous.get('PE_VOL', 0)
            vol_bias = ce_vol_change - pe_vol_change
            vol_momentum.append(-vol_bias)  # Invert for bullish positive

        # Calculate weighted momentum (recent data more important)
        weights = [0.1, 0.2, 0.3, 0.4]  # Last data point gets highest weight

        # Ensure we have enough data points
        if len(spot_momentum) >= len(weights):
            weighted_spot = sum(w * m for w, m in zip(weights, spot_momentum[-len(weights):]))
            weighted_oi = sum(w * m for w, m in zip(weights, oi_momentum[-len(weights):])) / 10000  # Scale down
            weighted_vol = sum(w * m for w, m in zip(weights, vol_momentum[-len(weights):])) / 100000  # Scale down
        else:
            # Fallback for insufficient data
            weighted_spot = np.mean(spot_momentum) if spot_momentum else 0
            weighted_oi = np.mean(oi_momentum) / 10000 if oi_momentum else 0
            weighted_vol = np.mean(vol_momentum) / 100000 if vol_momentum else 0

        # Combined momentum score
        momentum_score = (weighted_spot * 0.4) + (weighted_oi * 0.3) + (weighted_vol * 0.3)

        # Determine direction
        if momentum_score > 2.0:
            direction = "STRONG_BULLISH"
        elif momentum_score > 0.5:
            direction = "BULLISH"
        elif momentum_score < -2.0:
            direction = "STRONG_BEARISH"
        elif momentum_score < -0.5:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return {
            "momentum_score": momentum_score,
            "momentum_direction": direction,
            "spot_momentum": weighted_spot,
            "oi_momentum": weighted_oi,
            "vol_momentum": weighted_vol
        }

#=============================================================================
# MODULE 8: ENHANCED MARKET STATE WITH SAFE HISTORY ACCESS
#=============================================================================
class EnhancedMarketStateManager:
    """Enhanced market state with all safe access methods."""

    def __init__(self, config):
        self.config = config

    def safe_get_recent_history(self, market_state, count: int) -> List[Dict]:
        """Safely get recent history converting deque to list."""
        try:
            history_list = list(market_state.market_history)
            return history_list[-count:] if len(history_list) >= count else history_list
        except Exception as e:
            logger.warning(f"⚠️ Error getting recent history: {e}")
            return []

    def safe_get_history_slice(self, market_state, start_idx: int, end_idx: int = None) -> List[Dict]:
        """Safely get history slice converting deque to list."""
        try:
            history_list = list(market_state.market_history)
            if end_idx is None:
                return history_list[start_idx:]
            else:
                return history_list[start_idx:end_idx]
        except Exception as e:
            logger.warning(f"⚠️ Error getting history slice: {e}")
            return []

    def get_market_state_summary(self, market_state) -> Dict[str, Any]:
        """Get comprehensive market state summary."""
        return {
            "total_snapshots": len(market_state.market_history),
            "data_quality": getattr(market_state, 'data_quality_score', 10.0),
            "last_update": getattr(market_state, 'last_update_time', None),
            "current_spot": market_state.last_spot_price if hasattr(market_state, 'last_spot_price') else 0,
            "health_status": market_state.self_diagnose() if hasattr(market_state, 'self_diagnose') else "UNKNOWN"
        }

#=============================================================================
# MODULE 9: TIMING CONTROLLER
#=============================================================================
class TimingController:
    """Centralized timing control for the bot."""

    def __init__(self, config):
        self.config = config
        self.base_sleep_market = 90  # 1.30 minutes (90 seconds) during market hours
        self.base_sleep_off_market = 180  # 3 minutes outside market hours

    def calculate_sleep_time(self, cycle_start_time: float, is_market_hours: bool) -> float:
        """Calculate optimal sleep time for next cycle."""
        elapsed = time.time() - cycle_start_time

        if is_market_hours:
            base_sleep = self.base_sleep_market  # 90 seconds
            random_delay = random.uniform(-5, 5)  # Small randomization
        else:
            base_sleep = self.base_sleep_off_market  # 180 seconds
            random_delay = random.uniform(-30, 30)  # Larger randomization

        sleep_time = max(1, base_sleep - elapsed + random_delay)

        logger.info(f"⏰ Cycle completed in {elapsed:.2f}s. Next cycle in {sleep_time:.1f}s")
        return sleep_time

    def is_market_hours(self) -> bool:
        """Check if current time is within market hours."""
        current_time = datetime.now().time()
        return dt_time(9, 15) <= current_time <= dt_time(15, 30)

#=============================================================================
# MODULE 10: MAIN INTEGRATION MODULE - UPDATED WITH ALL FIXES
#=============================================================================
class TradingBotIntegrator:
    """Main integration class that combines all modules."""

    def __init__(self, config):
        self.config = config
        self.trade_orchestrator = TradeLevelOrchestrator(config)
        self.exit_analyzer = PredictiveExitAnalyzer(config)
        self.momentum_calculator = MomentumCalculator(config)
        self.market_state_manager = EnhancedMarketStateManager(config)
        self.timing_controller = TimingController(config)

    def generate_progressive_recommendation_updated(self, analysis: Dict[str, Any], market_state, day_profile, level: str) -> Optional[Dict[str, Any]]:
        """Updated progressive recommendation with modular components."""

        # Extract analysis data
        spot_price = analysis.get('spot_price', 0)
        entry_price = analysis.get('recommended_entry_price', 45.0)  # Example
        risk_mult = self.get_risk_multiplier(level)
        is_bullish = analysis.get('direction') == 'BULLISH'
        volatility = analysis.get('volatility', 0)

        # Use modular trade level calculation
        trade_levels = self.trade_orchestrator.calculate_complete_trade_levels(
            entry_price=entry_price,
            risk_mult=risk_mult,
            level=level,
            is_bullish=is_bullish,
            volatility=volatility
        )

        # Check if trade meets requirements
        if not trade_levels["meets_requirements"]:
            logger.warning("❌ Trade does not meet minimum R:R requirements")
            return None

        # Extract values for backward compatibility
        sl = trade_levels["stop_loss"]
        target1 = trade_levels["target1"]
        target2 = trade_levels["target2"]

        # Build recommendation
        recommendation = {
            "action": "BUY" if trade_levels["meets_requirements"] else "HOLD",
            "option_type": trade_levels["trade_type"],
            "strike": self.find_optimal_strike(spot_price, is_bullish),
            "entry_price": entry_price,
            "stop_loss": sl,
            "target1": target1,
            "target2": target2,
            "confidence_level": level,
            "risk_reward_analysis": trade_levels["risk_reward_analysis"],
            "trade_explanation": trade_levels["trade_explanation"],
            "position_size": "100%",  # Will be calculated by risk management
            "volatility_adjusted": trade_levels["volatility_adjusted"]
        }

        return recommendation

    def manage_active_trade_updated(self, analysis: Dict[str, Any], day_profile, market_state) -> Dict[str, Any]:
        """Updated active trade management with predictive exits."""

        # Use modular predictive exit analysis
        predictive_analysis = self.exit_analyzer.analyze_predictive_exit_signals(
            analysis, day_profile, market_state
        )

        # Calculate real-time momentum
        momentum_data = self.momentum_calculator.calculate_real_time_momentum(market_state)

        if predictive_analysis["exit_signal"]:
            return {
                "action": "EXIT",
                "reason": predictive_analysis["reason"],
                "exit_type": predictive_analysis["exit_type"],
                "current_pnl": predictive_analysis["current_pnl"],
                "momentum_data": momentum_data
            }
        elif predictive_analysis.get("exit_type") == "WARNING":
            return {
                "action": "MONITOR",
                "reason": predictive_analysis["reason"],
                "strength": predictive_analysis["strength"],
                "current_pnl": predictive_analysis["current_pnl"],
                "momentum_data": momentum_data
            }

        return {
            "action": "HOLD",
            "current_pnl": predictive_analysis.get("current_pnl", 0),
            "momentum_data": momentum_data
        }

    def get_risk_multiplier(self, level: str) -> float:
        """Get risk multiplier based on confidence level."""
        multipliers = {
            "EARLY_SIGNALS": 0.5,
            "MEDIUM_CONFIDENCE": 1.0,
            "HIGH_CONFIDENCE": 1.5,
            "FULL_POWER": 2.0
        }
        return multipliers.get(level, 1.0)

    def find_optimal_strike(self, spot_price: float, is_bullish: bool) -> int:
        """Find optimal strike based on spot price."""
        # Round to nearest 50 for NIFTY
        base_strike = round(spot_price / 50) * 50

        if is_bullish:
            return int(base_strike)  # ATM for calls
        else:
            return int(base_strike)  # ATM for puts

    def get_comprehensive_status(self, market_state) -> Dict[str, Any]:
        """Get comprehensive bot status."""
        return {
            "market_state": self.market_state_manager.get_market_state_summary(market_state),
            "timing": {
                "is_market_hours": self.timing_controller.is_market_hours(),
                "next_cycle_sleep": self.timing_controller.base_sleep_market
            },
            "modules_loaded": {
                "trade_orchestrator": self.trade_orchestrator is not None,
                "exit_analyzer": self.exit_analyzer is not None,
                "momentum_calculator": self.momentum_calculator is not None,
                "market_state_manager": self.market_state_manager is not None,
                "timing_controller": self.timing_controller is not None
            }
        }

#=============================================================================
# MODULE 11: MAIN LOOP INTEGRATION PATCH
#=============================================================================
def enhanced_market_processing(snapshot_data):
    """Run both the main bot and candle intelligence, then merge outputs."""
    # 1) existing logic
    main_analysis = market_state.update(snapshot_data)

    # 2) candle logic (guarded)
    candle_enhancement = {}
    if CANDLE_SYSTEM_ACTIVE and candle_system:
        try:
            candle_analysis = candle_system.process_snapshot(snapshot_data)
            candle_enhancement = candle_analysis
            if main_analysis and 'verdict' in main_analysis:
                extra = candle_system.get_enhancement_for_main_bot(main_analysis)
                candle_enhancement['main_bot_enhancement'] = extra
        except Exception as e:
            logger.error(f"❌ Candle analysis error: {e}")
            candle_enhancement = {'status': 'ERROR', 'error': str(e)}

    # 3) fuse results
    combined = {
        'main_bot_analysis': main_analysis,
        'candle_intelligence': candle_enhancement,
        'combined_recommendation': generate_combined_recommendation(
            main_analysis, candle_enhancement
        ),
    }
    return combined

# REPLACE THIS SECTION IN YOUR MAIN LOOP:
"""
# OLD CODE TO REPLACE IN generate_progressive_recommendation METHOD:
base_sl_pct = self.config["risk"]["sl_percentage"] * risk_mult
base_target_pct = self.config["risk"]["target_percentage"]
sl = entry_price * (1 - base_sl_pct) if is_bullish else entry_price * (1 + base_sl_pct)
target1 = entry_price * (1 + base_target_pct/2) if is_bullish else entry_price * (1 - base_target_pct/2)
target2 = entry_price * (1 + base_target_pct) if is_bullish else entry_price * (1 - base_target_pct)

# REPLACE WITH:
# Initialize the integrator if not already done
if not hasattr(self, 'bot_integrator'):
    self.bot_integrator = TradingBotIntegrator(self.config)

# Use modular calculation
return self.bot_integrator.generate_progressive_recommendation_updated(
    analysis, market_state, day_profile, level
)
"""

# REPLACE THIS SECTION IN YOUR manage_active_trade METHOD:
"""
# OLD CODE TO REPLACE:
predictive_analysis = self.analyze_predictive_exit_signals(analysis, day_profile, market_state)

# REPLACE WITH:
if not hasattr(self, 'bot_integrator'):
    self.bot_integrator = TradingBotIntegrator(self.config)

return self.bot_integrator.manage_active_trade_updated(analysis, day_profile, market_state)
"""

# REPLACE THIS SECTION IN YOUR MAIN LOOP TIMING:
"""
# OLD TIMING CODE TO REPLACE:
base_sleep = 60 # 1 minute during market hours for faster response

# REPLACE WITH:
if not hasattr(self, 'bot_integrator'):
    self.bot_integrator = TradingBotIntegrator(self.config)

sleep_time = self.bot_integrator.timing_controller.calculate_sleep_time(cycle_start_time, is_market_hours)
time.sleep(sleep_time)
"""

#=============================================================================
# MODULE 12: COMPLETE SAFE HISTORY ACCESS PATCHES
#=============================================================================
def safe_get_recent_history(self, count: int) -> List[Dict]:
    """Safely get recent history converting deque to list."""
    try:
        history_list = list(self.market_history)
        return history_list[-count:] if len(history_list) >= count else history_list
    except Exception as e:
        logger.warning(f"⚠️ Error getting recent history: {e}")
        return []

def safe_get_history_slice(self, start_idx: int, end_idx: int = None) -> List[Dict]:
    """Safely get history slice converting deque to list."""
    try:
        history_list = list(self.market_history)
        if end_idx is None:
            return history_list[start_idx:]
        else:
            return history_list[start_idx:end_idx]
    except Exception as e:
        logger.warning(f"⚠️ Error getting history slice: {e}")
        return []

# FIND AND REPLACE ALL INSTANCES OF THESE PATTERNS IN YOUR CODE:
# market_state.market_history[-X:]  ->  market_state.safe_get_recent_history(X)
# market_state.market_history[X:]   ->  market_state.safe_get_history_slice(X)
# list(market_state.market_history)[-X:]  ->  market_state.safe_get_recent_history(X)
# =============================================================================
# PART 1: PROGRESSIVE RECOMMENDATION SYSTEM WITH LIVE COMMENTARY (UPDATED)
# =============================================================================

def get_recommendation_level(self, market_state: 'EnhancedMarketState') -> str:
    """Determine recommendation level - ENHANCED for better trend persistence."""
    snapshots = len(market_state.market_history)
    
    # NEW: Check overall trend before determining level
    overall_trend = self._get_overall_trend(market_state)
    
    if snapshots >= 20:
        return "FULL_POWER"
    elif snapshots >= 10:
        return "HIGH_CONFIDENCE"
    elif snapshots >= 5:
        return "MEDIUM_CONFIDENCE"
    elif snapshots >= 3:  # Increased from 2 for better data
        return "EARLY_SIGNALS"
    else:
        return "INSUFFICIENT"

def analyze_market_progressive(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """ENHANCED VOLUME-PRIORITY Progressive market analysis with Smart Commentary."""
    level = self.get_recommendation_level(market_state)
    reasons = []
    score = 0.0
    triggers = []
    confidence_multiplier = 1.0
    
    logger.info(f"🎯 Analysis Level: {level} (Snapshots: {len(market_state.market_history)})")
    
    # NEW: Get overall trend first
    overall_trend = self._get_overall_trend(market_state)
    logger.info(f"📊 Overall Market Trend: {overall_trend}")
    
    # Initialize enhanced analysis data
    intelligence_report = {
        "timestamp": datetime.now().isoformat(),
        "analysis_level": level,
        "market_snapshots": len(market_state.market_history),
        "volume_analysis": {},
        "oi_analysis": {},
        "pattern_detection": {},
        "smart_money_signals": {},
        "overall_trend": overall_trend
    }
    
    if len(market_state.market_history) < 3:  # Increased from 2
        intelligence_report.update({
            "verdict": "INSUFFICIENT_DATA",
            "score": 0.0,
            "reasons": ["Need more market data for analysis"],
            "confidence_level": "INSUFFICIENT",
            "level": "INSUFFICIENT",
            "triggers": []
        })
        return intelligence_report
    
    # NEW: Enhanced volume analysis with correct bias calculation
    current = market_state.market_history[-1]
    previous = market_state.market_history[-2]
    
    # Fixed volume bias calculation (positive = bullish)
    ce_volume = current.get('CE_VOL', 0)
    pe_volume = current.get('PE_VOL', 0)
    volume_bias = ce_volume - pe_volume  # Corrected: positive bias = bullish
    
    # Fixed PCR interpretation (PCR < 0.7 = bullish)
    oi_pcr = current.get('OI_PCR', 1.0)
    if oi_pcr < 0.7:
        pcr_signal = "BULLISH"
        score += 2.0
        reasons.append("📊 PCR indicates bullish sentiment")
    elif oi_pcr > 1.3:
        pcr_signal = "BEARISH"
        score -= 2.0
        reasons.append("📊 PCR indicates bearish sentiment")
    else:
        pcr_signal = "NEUTRAL"
    
    # Enhanced momentum calculation
    spot_change = current.get('underlying_value', 0) - previous.get('underlying_value', 0)
    spot_change_pct = (spot_change / previous.get('underlying_value', 1)) * 100
    
    # Fixed momentum calculation with volume confirmation
    if spot_change_pct > 0.05 and volume_bias > 0:
        momentum = "BULLISH"
        score += 2.0
        reasons.append("📈 Bullish momentum with volume confirmation")
    elif spot_change_pct < -0.05 and volume_bias < 0:
        momentum = "BEARISH"
        score -= 2.0
        reasons.append("📉 Bearish momentum with volume confirmation")
    else:
        momentum = "SIDEWAYS"
    
    # NEW: Trend persistence logic
    if overall_trend == "BULLISH":
        if momentum == "BULLISH":
            score += 3.0  # Boost score for trend continuation
            reasons.append("🚀 Bullish trend continuation confirmed")
        elif momentum == "SIDEWAYS":
            score += 1.0  # Small boost for consolidation in bullish trend
            reasons.append("⏸️ Bullish trend with consolidation")
        # Don't penalize for bearish momentum in bullish trend
    elif overall_trend == "BEARISH":
        if momentum == "BEARISH":
            score -= 3.0
            reasons.append("📉 Bearish trend continuation confirmed")
        elif momentum == "SIDEWAYS":
            score -= 1.0
    
    # Check for missed move patterns
    missed_move_check = self.detect_missed_moves(market_state)
    if missed_move_check["detected"]:
        logger.info(f"🎯 MISSED MOVE DETECTED: {missed_move_check['patterns']}")
        if "BULLISH" in str(missed_move_check['patterns']):
            score += 3.0
            triggers.append("MISSED_MOVE_PATTERN")
            reasons.append("🔍 MISSED MOVE: Detected bullish pattern similar to your missed trades")
        else:
            score -= 3.0
    
    # Determine verdict based on score and overall trend
    if score >= 5.0:
        verdict = "BULLISH"
        confidence = "HIGH"
    elif score >= 2.0:
        verdict = "BULLISH"
        confidence = "MEDIUM"
    elif score <= -5.0:
        verdict = "BEARISH"
        confidence = "HIGH"
    elif score <= -2.0:
        verdict = "BEARISH"
        confidence = "MEDIUM"
    else:
        verdict = "NEUTRAL"
        confidence = "LOW"
    
    # NEW: Final trend validation
    if overall_trend == "BULLISH" and verdict == "BEARISH":
        # Require stronger evidence to override bullish trend
        if score > -3.0:
            verdict = "NEUTRAL"
            reasons.append("⚠️ Bearish signal overridden by bullish trend")
    
    intelligence_report.update({
        "verdict": verdict,
        "score": score,
        "reasons": reasons,
        "confidence_level": confidence,
        "level": level,
        "triggers": triggers,
        "momentum": momentum,
        "volume_bias": volume_bias,
        "pcr_signal": pcr_signal
    })
    
    return intelligence_report

def analyze_with_time_window_intelligence(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    '''Enhanced analysis that incorporates time window intelligence with trend persistence.'''
    
    # FIXED: Safely get time window analysis with fallback
    time_window_analysis = getattr(market_state, 'time_window_analysis', {})
    current_window = getattr(market_state, 'current_time_window', 'unknown')
    
    # Ensure attributes exist if missing
    if not hasattr(market_state, 'time_window_analysis'):
        market_state.time_window_analysis = {}
        logger.warning("⚠️ time_window_analysis attribute missing - initialized with empty dict")
    if not hasattr(market_state, 'current_time_window'):
        market_state.current_time_window = 'unknown'
        logger.warning("⚠️ current_time_window attribute missing - initialized as 'unknown'")
    
    # Get the normal progressive analysis
    base_analysis = self.analyze_market_progressive(market_state)
    
    # FIXED: Check if base_analysis is None and provide fallback
    if base_analysis is None:
        logger.error("❌ analyze_market_progressive returned None - using fallback analysis")
        base_analysis = {
            'verdict': 'NEUTRAL',
            'score': 0.0,
            'level': 'BASIC',
            'reasons': ['⚠️ Fallback analysis - progressive analysis failed'],
            'confidence': 'LOW'
        }
    
    # Enhance with time window intelligence
    window_config = TIME_WINDOWS.get(current_window, {})
    direction_change_prob = window_config.get('direction_change_probability', 0.5)
    
    # Adjust score based on time window
    window_action = time_window_analysis.get('action', 'MONITOR')
    trade_signal = time_window_analysis.get('trade_signal', 'NONE')
    
    # Time window score adjustments
    time_window_score_adjustment = 0
    
    # FIXED: Safe access to base_analysis with null checks
    base_score = base_analysis.get('score', 0.0) if base_analysis else 0.0
    base_verdict = base_analysis.get('verdict', 'NEUTRAL')
    
    # NEW: Trend persistence in time windows
    if base_verdict == "BULLISH":
        if window_action in ['HIGH_CONFIDENCE_TRADE', 'MOMENTUM_TRADE']:
            time_window_score_adjustment = +2.0
        elif window_action == 'AVOID_TRADING':
            time_window_score_adjustment = -1.0  # Less penalty for bullish signals
    elif base_verdict == "BEARISH":
        if window_action in ['HIGH_CONFIDENCE_TRADE', 'MOMENTUM_TRADE']:
            time_window_score_adjustment = -2.0
        elif window_action == 'AVOID_TRADING':
            time_window_score_adjustment = +1.0  # Less penalty for bearish signals
    
    # Apply time window adjustment
    adjusted_score = base_score + time_window_score_adjustment
    
    # Update verdict based on adjusted score and time window
    if window_action == 'AVOID_TRADING':
        final_verdict = 'NEUTRAL'
    else:
        # FIXED: Safe access to progressive_thresholds with fallback
        analysis_level = base_analysis.get('level', 'BASIC') if base_analysis else 'BASIC'
        thresholds = self.progressive_thresholds.get(analysis_level, {'bullish': 5.0, 'bearish': -5.0})
        
        # NEW: Trend persistence logic
        if base_verdict == "BULLISH" and adjusted_score < thresholds['bullish']:
            # Don't easily switch from bullish to neutral/bearish
            if adjusted_score > thresholds['bullish'] * 0.7:  # 70% of threshold
                final_verdict = 'BULLISH'
            else:
                final_verdict = 'NEUTRAL'
        elif base_verdict == "BEARISH" and adjusted_score > thresholds['bearish']:
            # Don't easily switch from bearish to neutral/bullish
            if adjusted_score < thresholds['bearish'] * 0.7:  # 70% of threshold
                final_verdict = 'BEARISH'
            else:
                final_verdict = 'NEUTRAL'
        else:
            if adjusted_score >= thresholds['bullish']:
                final_verdict = 'BULLISH'
            elif adjusted_score <= thresholds['bearish']:
                final_verdict = 'BEARISH'
            else:
                final_verdict = 'NEUTRAL'
    
    # Enhanced analysis result
    base_reasons = base_analysis.get('reasons', []) if base_analysis else []
    enhanced_analysis = {
        'verdict': final_verdict,
        'score': adjusted_score,
        'base_score': base_score,
        'time_window_adjustment': time_window_score_adjustment,
        'current_time_window': current_window,
        'window_action': window_action,
        'window_confidence': time_window_analysis.get('analysis', {}).get('confidence_level', 'MEDIUM'),
        'direction_change_probability': direction_change_prob,
        'reasons': base_reasons + [f"🕐 Time Window: {current_window} ({window_action})"],
        'triggers': base_analysis.get('triggers', []),
        'level': base_analysis.get('level', 'BASIC') if base_analysis else 'BASIC',
        'confidence': base_analysis.get('confidence', 'MEDIUM') if base_analysis else 'LOW',
        'time_window_intelligence': time_window_analysis,
        'base_verdict': base_verdict  # NEW: Track original verdict
    }
    
    logger.info(f"🧠 Enhanced Analysis: {final_verdict} (Base: {base_score:.2f}, Adjusted: {adjusted_score:.2f})")
    logger.info(f"🕐 Window: {current_window} | Action: {window_action} | Prob: {direction_change_prob:.0%}")
    
    return enhanced_analysis

# NEW: Helper method to get overall trend
def _get_overall_trend(self, market_state: 'EnhancedMarketState') -> str:
    """Calculate overall market trend from recent data."""
    if len(market_state.market_history) < 5:
        return "UNKNOWN"
    
    # Get last 5 snapshots
    recent = list(market_state.market_history)[-5:]
    prices = [s.get('underlying_value', 0) for s in recent]
    
    # Calculate trend
    if prices[-1] > prices[0] * 1.002:  # 0.2% increase
        return "BULLISH"
    elif prices[-1] < prices[0] * 0.998:  # 0.2% decrease
        return "BEARISH"
    else:
        return "SIDEWAYS"

        # =========================================================================
        # PRIORITY 1: ENHANCED VOLUME-PRICE RELATIONSHIP ANALYSIS
        # =========================================================================
        current = market_state.market_history[-1]
        previous = market_state.market_history[-2]

        # Get volume and price changes
        ce_vol_change = current.get("CE_VOL", 0) - previous.get("CE_VOL", 0)
        pe_vol_change = current.get("PE_VOL", 0) - previous.get("PE_VOL", 0)
        total_vol_change = ce_vol_change + pe_vol_change
        price_change = current.get("underlying_value", 0) - previous.get("underlying_value", 0)
        volume_bias = pe_vol_change - ce_vol_change

        # Store volume analysis for commentary
        intelligence_report["volume_analysis"] = {
            "ce_vol_change": ce_vol_change,
            "pe_vol_change": pe_vol_change,
            "total_vol_change": total_vol_change,
            "volume_bias": volume_bias,
            "price_change": price_change,
            "pattern": self._detect_volume_pattern(ce_vol_change, pe_vol_change, total_vol_change)
        }

        # Enhanced pattern detection
        pattern_detection = self._detect_enhanced_patterns(
            price_change, volume_bias, ce_vol_change, pe_vol_change, total_vol_change
        )
        intelligence_report["pattern_detection"] = pattern_detection

        # CRITICAL PATTERN 1: Bearish Divergence (Your successful trade pattern)
        # CRITICAL PATTERN 1: Bearish Divergence (Your successful trade pattern)
        if price_change > 0 and volume_bias > 15000: # FIXED: Lowered to catch real moves
            score -= 6.0
            triggers.append("BEARISH_DIVERGENCE")
            reasons.append(f"BEARISH DIVERGENCE: Price up ₹{price_change:+.2f} but PE volume dominance {volume_bias:+,}")
            pattern_detection["bearish_divergence"] = True
            logger.warning(f"🔴 BEARISH DIVERGENCE: Price +₹{price_change:.2f}, PE bias +{volume_bias:,}")

        # CRITICAL PATTERN 2: Bullish Divergence
        elif price_change < 0 and volume_bias < -15000: # FIXED: Price down, CE volume dominance
            score += 6.0  # Strong bullish signal
            triggers.append("BULLISH_DIVERGENCE")
            reasons.append(f"BULLISH DIVERGENCE: Price down ₹{price_change:+.2f} but CE volume dominance {abs(volume_bias):+,}")
            pattern_detection["bullish_divergence"] = True
            logger.info(f"🟢 BULLISH DIVERGENCE: Price {price_change:.2f}, CE bias {abs(volume_bias):,}")

        # CRITICAL PATTERN 3: Volume Explosion Analysis
        if total_vol_change > 400000: # FIXED: High volume activity (realistic threshold)
            if abs(volume_bias) > 500000:  # Directional bias
                bias_direction = "PE" if volume_bias > 0 else "CE"
                score += 3.0 if volume_bias < 0 else -3.0  # CE bias = bullish, PE bias = bearish
                triggers.append("VOLUME_EXPLOSION_DIRECTIONAL")
                reasons.append(f"VOLUME EXPLOSION: {total_vol_change:+,} with {bias_direction} bias {abs(volume_bias):+,}")
                pattern_detection["volume_explosion"] = True
            else:
                triggers.append("HIGH_VOLUME_BALANCED")
                reasons.append(f"HIGH VOLUME: {total_vol_change:+,} total volume but balanced flow")

        # =========================================================================
        # PRIORITY 2: ENHANCED OI ANALYSIS
        # =========================================================================
        ce_oi_change = current.get("CE_OI", 0) - previous.get("CE_OI", 0)
        pe_oi_change = current.get("PE_OI", 0) - previous.get("PE_OI", 0)
        total_oi_change = abs(ce_oi_change) + abs(pe_oi_change)
        pcr_current = current.get('OI_PCR', 1.0)

        # Store OI analysis for commentary
        intelligence_report["oi_analysis"] = {
            "ce_oi_change": ce_oi_change,
            "pe_oi_change": pe_oi_change,
            "total_oi_change": total_oi_change,
            "pcr_current": pcr_current,
            "pattern": self._detect_oi_pattern(ce_oi_change, pe_oi_change, total_oi_change)
        }

        # Smart PCR analysis with context
        if price_change < -10:  # During decline
            if pcr_current < 0.7:  # Low PCR during decline
                score += 1.0  # Mild bullish (short covering)
                triggers.append("SHORT_COVERING_PCR")
                reasons.append(f"Mild bullish: Low PCR ({pcr_current:.3f}) during decline - Short covering")
            elif pcr_current > 1.2:  # High PCR during decline
                score -= 2.0  # Bearish (more decline expected)
                triggers.append("BEARISH_PCR_DECLINE")
                reasons.append(f"BEARISH: High PCR ({pcr_current:.3f}) during decline - More selling expected")

        elif price_change > 10:  # During rise
            if pcr_current < 0.7:  # Low PCR during rise
                score += 2.0  # Strong bullish
                triggers.append("BULLISH_PCR_RALLY")
                reasons.append(f"BULLISH: Low PCR ({pcr_current:.3f}) during rally - Strong buying")
            elif pcr_current > 1.2:  # High PCR during rise
                score -= 1.0  # Weak rally warning
                triggers.append("WEAK_RALLY_PCR")
                reasons.append(f"WARNING: High PCR ({pcr_current:.3f}) during rally - Weak buying")

        # =========================================================================
        # PRIORITY 3: SMART MONEY DETECTION
        # =========================================================================
        smart_money_signals = self._detect_smart_money_activity(
            current, previous, price_change, volume_bias, total_vol_change
        )
        intelligence_report["smart_money_signals"] = smart_money_signals

        if smart_money_signals.get("institutional_accumulation"):
            score += 2.0
            triggers.append("INSTITUTIONAL_ACCUMULATION")
            reasons.append("BULLISH: Institutional accumulation detected")

        if smart_money_signals.get("institutional_distribution"):
            score -= 2.0
            triggers.append("INSTITUTIONAL_DISTRIBUTION")
            reasons.append("BEARISH: Institutional distribution detected")

        # =========================================================================
        # ENHANCED CONFIDENCE LEVELS WITH LIVE COMMENTARY
        # =========================================================================
        if level in ["HIGH_CONFIDENCE", "FULL_POWER"]:
            confidence_multiplier *= 1.2

        # Determine final verdict with LOWERED THRESHOLDS
        verdict = self.determine_progressive_verdict(score, triggers, level, confidence_multiplier)
        final_score = round(score * confidence_multiplier, 2)
        
        # DEBUG: Log scoring details for troubleshooting
        logger.info(f"🔍 SCORING DEBUG: Raw score: {score:.2f}, Final: {final_score:.2f}, Triggers: {len(triggers)}")
        logger.info(f"🎯 VERDICT LOGIC: Score threshold check - Bullish: {final_score} > 1.5? Bearish: {final_score} < -1.5?")

        # Complete intelligence report
        intelligence_report.update({
            "verdict": verdict,
            "score": final_score,
            "triggers": triggers,
            "reasons": reasons if reasons else ["Neutral market conditions"],
            "confidence_level": level,
            "level": level,
            "raw_score": round(score, 2), 
            "confidence_multiplier": confidence_multiplier,
            "analysis_timestamp": datetime.now().isoformat()
        })

        # =========================================================================
        # GENERATE AND SEND LIVE COMMENTARY TO TELEGRAM
        # =========================================================================
        if self.smart_commentary_enabled:
            try:
                self.generate_live_commentary_and_send_telegram(market_state, intelligence_report)
            except Exception as e:
                logger.error(f"❌ Error generating live commentary: {e}")

        # Enhanced logging with volume patterns
        # Enhanced logging to track missed moves
        logger.info(f"📊 Volume Analysis - CE: {ce_vol_change:+,}, PE: {pe_vol_change:+,}, Price: {price_change:+.2f}")
        logger.info(f"🔍 MISSED MOVE CHECK - Volume Bias: {volume_bias:+,}, Total Volume: {total_vol_change:+,}")

        # Special check for your exact missed patterns  
        if abs(volume_bias) > 5000 or abs(price_change) > 3 or total_vol_change > 150000:
            logger.warning(f"🎯 POTENTIAL MISSED MOVE: Price {price_change:+.2f}, Bias {volume_bias:+,}, Volume {total_vol_change:+,}")
        logger.info(f"🎯 Final Verdict: {verdict} (Score: {final_score:.2f})")

        return intelligence_report

    def detect_missed_moves(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
        """Special detection system for moves like the ones you missed."""
        
        if len(market_state.market_history) < 2:
            return {"detected": False, "reason": "Insufficient data"}
        
        current = market_state.market_history[-1]
        previous = market_state.market_history[-2]
        
        # Extract the exact patterns from your missed moves
        ce_vol_change = current.get("CE_VOL", 0) - previous.get("CE_VOL", 0)
        pe_vol_change = current.get("PE_VOL", 0) - previous.get("PE_VOL", 0) 
        price_change = current.get("underlying_value", 0) - previous.get("underlying_value", 0)
        volume_bias = pe_vol_change - ce_vol_change
        total_vol_change = ce_vol_change + pe_vol_change
        
        detected_moves = []
        
        # Pattern 1: Your Cycle 11 pattern (Price +8.10, CE bias -6,611)
        if 3 < price_change < 15 and -50000 < volume_bias < -3000:
            detected_moves.append("BULLISH_BREAKOUT_PATTERN")
        
        # Pattern 2: Your Cycle 12 pattern (Price -1.40, PE bias +36,644)  
        if -5 < price_change < 2 and 15000 < volume_bias < 100000:
            detected_moves.append("BEARISH_DIVERGENCE_PATTERN")
        
        # Pattern 3: Your Cycle 13 pattern (Price +6.20, CE bias -34,465)
        if 3 < price_change < 10 and -80000 < volume_bias < -10000:
            detected_moves.append("BULLISH_RECOVERY_PATTERN")
        
        # Pattern 4: Your Cycle 15 pattern (Price +4.85, CE bias -22,501)
        if 2 < price_change < 8 and -50000 < volume_bias < -8000:
            detected_moves.append("MOMENTUM_CONTINUATION_PATTERN")
        
        # High volume activity (like your 400K+ volumes)
        if total_vol_change > 200000:
            detected_moves.append("HIGH_VOLUME_ACTIVITY")
        
        return {
            "detected": len(detected_moves) > 0,
            "patterns": detected_moves,
            "price_change": price_change,
            "volume_bias": volume_bias,
            "total_volume": total_vol_change,
            "recommendation": "STRONG_SIGNAL" if len(detected_moves) >= 2 else "MONITOR"
        }

    def _detect_volume_pattern(self, ce_vol: int, pe_vol: int, total_vol: int) -> str:
        """Detect volume patterns for commentary."""
        if total_vol > 2000000:
            return "VOLUME_EXPLOSION"
        elif abs(ce_vol - pe_vol) > 500000:
            return "DIRECTIONAL_VOLUME"
        elif total_vol < 100000:
            return "LOW_VOLUME"
        else:
            return "BALANCED_VOLUME"

    def _detect_oi_pattern(self, ce_oi: int, pe_oi: int, total_oi: int) -> str:
        """Detect OI patterns for commentary."""
        if total_oi > 100000:
            return "STRONG_OI_BUILD"
        elif total_oi > 25000:
            return "MODERATE_OI_BUILD"
        elif total_oi < -50000:
            return "OI_DECLINE"
        else:
            return "FLAT_OI"

    def _detect_enhanced_patterns(self, price_change: float, volume_bias: int,
                                ce_vol: int, pe_vol: int, total_vol: int) -> Dict[str, bool]:
        """Detect enhanced market patterns."""
        patterns = {
            "bearish_divergence": False,
            "bullish_divergence": False,
            "volume_explosion": False,
            "stealth_accumulation": False,
            "institutional_activity": False
        }

        # Bearish divergence: Price up + PE volume dominance
        if price_change > 0 and volume_bias > 100000:
            patterns["bearish_divergence"] = True

        # Bullish divergence: Price down + CE volume dominance
        if price_change < 0 and volume_bias < -100000:
            patterns["bullish_divergence"] = True

        # Volume explosion
        if total_vol > 1500000:
            patterns["volume_explosion"] = True

        # High institutional activity
        if total_vol > 1000000:
            patterns["institutional_activity"] = True

        # Stealth accumulation (moderate OI with low volume)
        if 200000 < total_vol < 800000:
            patterns["stealth_accumulation"] = True

        return patterns

    def _detect_smart_money_activity(self, current: Dict, previous: Dict,
                                   price_change: float, volume_bias: int, total_vol: int) -> Dict[str, bool]:
        """Detect smart money activity patterns."""
        smart_money = {
            "institutional_accumulation": False,
            "institutional_distribution": False,
            "smart_money_bullish": False,
            "smart_money_bearish": False
        }

        # Institutional accumulation: Large OI build with controlled volume
        ce_oi_change = current.get("CE_OI", 0) - previous.get("CE_OI", 0)
        pe_oi_change = current.get("PE_OI", 0) - previous.get("PE_OI", 0)

        if pe_oi_change > 50000 and price_change > 5 and total_vol < 1000000:
            smart_money["institutional_accumulation"] = True
            smart_money["smart_money_bullish"] = True

        # Institutional distribution: Large volume with minimal OI increase
        if total_vol > 1500000 and abs(ce_oi_change) + abs(pe_oi_change) < 25000:
            smart_money["institutional_distribution"] = True
            smart_money["smart_money_bearish"] = True

        return smart_money

#=============================================================================
#PART 3: SMART LIVE COMMENTARY INTEGRATION
#=============================================================================

    def generate_live_commentary_and_send_telegram(self, market_state: 'EnhancedMarketState', analysis: Dict[str, Any]) -> None:
        """Generate comprehensive live commentary and send to Telegram."""

        try:
            # Generate comprehensive market commentary
            live_commentary = self.commentary_bot.generate_comprehensive_market_commentary(market_state, analysis)

            # Send to Telegram with appropriate priority
            verdict = analysis.get("verdict", "NEUTRAL")
            priority = "HIGH" if verdict != "NEUTRAL" else "INFO"

            asyncio.create_task(send_enhanced_telegram_message(live_commentary, priority=priority))

            logger.info(f"📱 Live market commentary sent to Telegram (Priority: {priority})")

        except Exception as e:
            logger.error(f"❌ Error sending live commentary: {e}")
#PART 4: ENHANCED RECOMMENDATION GENERATION WITH COMMENTARY
#=============================================================================

    def generate_progressive_recommendation(self, decision: Dict[str, Any], market_state: 'EnhancedMarketState', day_profile: 'EnhancedMarketDayProfile') -> str:
        """Generate recommendations with ENHANCED Telegram integration and live commentary."""
        verdict = decision.get('verdict', 'NEUTRAL')
        level = decision.get('confidence_level', decision.get('level', 'BASIC'))

        if verdict == "NEUTRAL":
            neutral_msg = f"🔍 [{level}] No clear signals detected. Continue monitoring."

            # Send live commentary even for neutral signals
            if self.smart_commentary_enabled:
                try:
                    commentary = self.commentary_bot.generate_comprehensive_market_commentary(market_state, decision)
                    full_msg = f"{neutral_msg}\n\n{commentary}"
                    asyncio.create_task(send_enhanced_telegram_message(full_msg, priority="INFO"))
                except Exception as e:
                    logger.error(f"❌ Error sending neutral commentary: {e}")
                    asyncio.create_task(send_enhanced_telegram_message(neutral_msg, priority="INFO"))

            return neutral_msg

        # Get current market data
        snapshot = market_state.market_history[-1]
        spot = snapshot['underlying_value']
        strikes = sorted(snapshot.get("strike_data", {}).keys())

        if not strikes:
            return "❌ Insufficient strike data for recommendation."

        atm_strike = min(strikes, key=lambda k: abs(k - spot))
        strike_data = snapshot["strike_data"][atm_strike]

        # Determine option type and entry
        is_bullish = "BULLISH" in verdict
        option_type = "CE" if is_bullish else "PE"
        entry_price = strike_data.get(f"{option_type}_LTP", 0)

        if entry_price <= 0:
            return "❌ Invalid option price data."

        # Progressive position sizing and risk
        position_multipliers = {
            "EARLY_SIGNALS": 0.5, "MEDIUM_CONFIDENCE": 0.75,
            "HIGH_CONFIDENCE": 1.0, "FULL_POWER": 1.0
        }

        pos_mult = position_multipliers.get(level, 0.5)

        # CORRECTED PE/CE TARGET CALCULATION
        base_sl_points = 2.0  # ₹2 stop loss
        target1_points = 6.0  # ₹6 profit for T1
        target2_points = 20.0 if level == "FULL_POWER" else 16.0  # ₹16-20 for T2

        # CORRECT LOGIC: Targets are HIGHER than entry for both PE and CE
        sl = entry_price - base_sl_points
        target1 = entry_price + target1_points
        target2 = entry_price + target2_points

        # Risk-Reward calculation
        risk_amount = base_sl_points
        reward_t1 = target1_points
        reward_t2 = target2_points

        # Create trade for tracking
        if level in ["MEDIUM_CONFIDENCE", "HIGH_CONFIDENCE", "FULL_POWER"]:
            day_profile.active_trade = {
                "type": option_type, "strike": atm_strike, "entry": entry_price,
                "sl": sl, "partial_target": target1, "target": target2,
                "original_sl": sl, "entry_time": datetime.now(),
                "confidence_level": level, "monitored": True,
                "risk_reward_t1": reward_t1/risk_amount,
                "risk_reward_t2": reward_t2/risk_amount
            }

        # Determine signal priority
        volume_analysis = decision.get('volume_analysis', {})
        pattern_detection = decision.get('pattern_detection', {})

        signal_priority = "HIGH PRIORITY"
        if pattern_detection.get('bearish_divergence') or pattern_detection.get('bullish_divergence'):
            signal_priority = "🚨 CRITICAL PRIORITY"
        elif pattern_detection.get('volume_explosion'):
            signal_priority = "⚡ HIGH PRIORITY"

        # Generate confidence emoji
        confidence_emoji = {
            "EARLY_SIGNALS": "🟡", "MEDIUM_CONFIDENCE": "🟠",
            "HIGH_CONFIDENCE": "🔴", "FULL_POWER": "🚨"
        }

        emoji = confidence_emoji.get(level, "🔍")
        signal_type = verdict.replace("_", " ").title()

        # Enhanced volume pattern description
        volume_bias = volume_analysis.get('volume_bias', 0)
        if volume_bias > 100000:
            volume_pattern = f"📉 PE Bias (+{volume_bias:,})"
        elif volume_bias < -100000:
            volume_pattern = f"📈 CE Bias (+{abs(volume_bias):,})"
        else:
            volume_pattern = "⚖️ Balanced Flow"

        # Generate enhanced Telegram message
        telegram_msg = f"""{signal_priority}
🎯 NIFTY TRADE ALERT
━━━━━━━━━━━━━━━━━━━
📊 CONFIDENCE: {level}
🎯 SIGNAL: {signal_type}

📍 ENTRY DETAILS:
• Option: {option_type} {int(atm_strike)}
• Entry Price: ₹{entry_price:.2f}
• Spot: ₹{spot:.2f}

🎯 TARGETS & RISK:
• Target 1: ₹{target1:.2f}
• Target 2: ₹{target2:.2f}
• Stop Loss: ₹{sl:.2f}
• Position Size: {int(pos_mult*100)}%

📊 MARKET DATA:
• CE OI: {int(snapshot.get('CE_OI', 0)):,}
• PE OI: {int(snapshot.get('PE_OI', 0)):,}
• OI PCR: {snapshot.get('OI_PCR', 0):.3f}

📊 VOLUME ANALYSIS:
• CE Volume: {volume_analysis.get('ce_vol_change', 0):+.0f}
• PE Volume: {volume_analysis.get('pe_vol_change', 0):+.0f}
• Total Volume: {volume_analysis.get('total_vol_change', 0):+.0f}
• Price Change: ₹{volume_analysis.get('price_change', 0):+.2f}
• Pattern: {volume_pattern}

💡 REASON: {decision['reason'][:120]}...

⚖️ RISK:REWARD:
• T1 R:R = 1:{reward_t1/risk_amount:.1f}
• T2 R:R = 1:{reward_t2/risk_amount:.1f}

⭐ ANALYSIS SCORE: {decision['score']:.2f}/10
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━"""

        # Add pattern alerts
        pattern_alerts = []
        if pattern_detection.get('bearish_divergence'):
            pattern_alerts.append("🔴 BEARISH DIVERGENCE: Price up but PE volume dominance")
        if pattern_detection.get('bullish_divergence'):
            pattern_alerts.append("🟢 BULLISH DIVERGENCE: Price down but CE volume dominance")
        if pattern_detection.get('volume_explosion'):
            pattern_alerts.append("💥 VOLUME EXPLOSION: Institutional activity detected")

        if pattern_alerts:
            telegram_msg += f"\n\n🚨 PATTERN ALERTS:\n" + "\n".join([f"• {alert}" for alert in pattern_alerts])

        # Add volume interpretation
        telegram_msg += f"\n\n💡 VOLUME INTERPRETATION:"
        if volume_bias > 200000:
            telegram_msg += f"\n📉 Strong bearish volume shift - More traders buying PUTs"
        elif volume_bias < -200000:
            telegram_msg += f"\n📈 Strong bullish volume shift - More traders buying CALLs"
        elif volume_analysis.get('total_vol_change', 0) > 1000000:
            telegram_msg += f"\n⚡ High volume activity - Major institutional moves"
        else:
            telegram_msg += f"\n⚖️ Balanced volume flow - Normal market conditions"

        # Add target logic explanation
        telegram_msg += f"\n\n📚 TARGET LOGIC:"
        if option_type == "PE":
            telegram_msg += f"\n• Market DOWN → PE premium UP → Sell at HIGHER prices"
        else:
            telegram_msg += f"\n• Market UP → CE premium UP → Sell at HIGHER prices"
        telegram_msg += f"\n• Entry ₹{entry_price:.2f} → T1 ₹{target1:.2f} → T2 ₹{target2:.2f}"

        # =========================================================================
        # ENHANCED TELEGRAM INTEGRATION WITH LIVE COMMENTARY
        # =========================================================================

        try:
            if self.smart_commentary_enabled:
                # Generate comprehensive market commentary
                market_commentary = self.commentary_bot.generate_comprehensive_market_commentary(market_state, decision)

                # Combine recommendation with live commentary
                comprehensive_msg = f"""{telegram_msg}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{market_commentary}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                # Send enhanced message with live commentary
                priority = "CRITICAL" if "CRITICAL" in signal_priority else "HIGH"
                asyncio.create_task(send_enhanced_telegram_message(comprehensive_msg, priority=priority))

                logger.info(f"📱 Enhanced recommendation with live commentary sent (Priority: {priority})")
            else:
                # Send original recommendation only
                priority = "CRITICAL" if "CRITICAL" in signal_priority else "HIGH"
                asyncio.create_task(send_enhanced_telegram_message(telegram_msg, priority=priority))

                logger.info(f"📱 Standard recommendation sent (Priority: {priority})")

        except Exception as e:
            logger.error(f"❌ Error sending enhanced recommendation: {e}")
            # Fallback to basic message
            asyncio.create_task(send_enhanced_telegram_message(telegram_msg, priority="HIGH"))

        return telegram_msg
    def log_timeframe_data_safely(timeframe_data):
        """Log timeframe data with safe key access"""
        for interval, data in timeframe_data.items():
            try:
                # Safe access with defaults
                spot_change = data.get('spot_change', 0)
                spot_change_pct = data.get('spot_change_pct', 0.0)
                ce_oi_change = data.get('ce_oi_change', 0)
                ce_oi_change_pct = data.get('ce_oi_change_pct', 0.0)
                pe_oi_change = data.get('pe_oi_change', 0)
                pe_oi_change_pct = data.get('pe_oi_change_pct', 0.0)
                momentum = data.get('momentum', 'UNKNOWN')
                strength = data.get('strength_score', 0)
                
                logger.info(f"⏰ {interval.upper()} TIMEFRAME DATA:")
                logger.info(f"   Spot Change: {spot_change:+} ({spot_change_pct:+.4f}%)")
                logger.info(f"   CE OI Change: {ce_oi_change:+,} ({ce_oi_change_pct:+.2f}%)")
                logger.info(f"   PE OI Change: {pe_oi_change:+,} ({pe_oi_change_pct:+.2f}%)")
                logger.info(f"   Momentum: {momentum} | Strength: {strength:.2f}/10")
                
            except Exception as e:
                logger.error(f"❌ Error logging timeframe data for {interval}: {e}")
#=============================================================================
#PART 5: VERDICT DETERMINATION & UTILITY METHODS
#=============================================================================

    def determine_progressive_verdict(self, score: float, triggers: List[str], level: str, confidence_multiplier: float) -> str:
        """Determine verdict with ULTRA-LOW thresholds to catch missed moves."""
        final_score = score * confidence_multiplier

        # ULTRA-LOW thresholds to catch your missed moves
        if level == "FULL_POWER":
            bullish_threshold = 1.0 # FIXED: Further reduced
            bearish_threshold = -1.0
        elif level == "HIGH_CONFIDENCE":
            bullish_threshold = 0.8 # FIXED: Further reduced
            bearish_threshold = -0.8
        elif level == "MEDIUM_CONFIDENCE":
            bullish_threshold = 0.6 # FIXED: Further reduced  
            bearish_threshold = -0.6
        else: # EARLY_SIGNALS
            bullish_threshold = 0.4 # FIXED: Further reduced
            bearish_threshold = -0.4
        
        if final_score >= bullish_threshold:
            if level == "FULL_POWER":
                return "HIGH_CONVICTION_BULLISH"
            elif level in ["HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE"]:
                return "STRONG_BULLISH"
            else:
                return "BULLISH"
        elif final_score <= bearish_threshold:
            if level == "FULL_POWER":
                return "HIGH_CONVICTION_BEARISH" 
            elif level in ["HIGH_CONFIDENCE", "MEDIUM_CONFIDENCE"]:
                return "STRONG_BEARISH"
            else:
                return "BEARISH"
        else:
            return "NEUTRAL"


    def toggle_smart_commentary(self, enabled: bool = None) -> bool:
        """Toggle smart commentary on/off."""
        if enabled is not None:
            self.smart_commentary_enabled = enabled
        else:
            self.smart_commentary_enabled = not self.smart_commentary_enabled

        status = "ENABLED" if self.smart_commentary_enabled else "DISABLED"
        logger.info(f"🎤 Smart Live Commentary: {status}")
        return self.smart_commentary_enabled

    def get_strategy_status(self) -> Dict[str, Any]:
        """Get current strategy engine status."""
        return {
            "ml_model_loaded": self.ml_model is not None,
            "scaler_loaded": self.scaler is not None,
            "smart_commentary_enabled": self.smart_commentary_enabled,
            "pattern_detection_enabled": self.pattern_detection_enabled,
            "volume_intelligence_enabled": self.volume_intelligence_enabled,
            "progressive_thresholds": self.progressive_thresholds
        }

    def generate_support_resistance_context(self, market_state: 'EnhancedMarketState'):
        """Generate support/resistance context and return both text + values."""
        if len(market_state.market_history) < 10:
            return "\n📈 SUPPORT/RESISTANCE: Building historical context...", None, None

        recent_data = list(market_state.market_history)[-10:]
        prices = [data.get('underlying_value', 0) for data in recent_data]
        current_price = prices[-1]

        resistance_levels = self.calculate_resistance_levels(prices, current_price)
        support_levels = self.calculate_support_levels(prices, current_price)

       # Assuming resistance_levels and support_levels are lists
        immediate_support = support_levels[0] if isinstance(support_levels, list) and len(support_levels) > 0 else current_price - 10
        key_support = support_levels[1] if isinstance(support_levels, list) and len(support_levels) > 1 else current_price - 25
        immediate_resistance = resistance_levels[0] if isinstance(resistance_levels, list) and len(resistance_levels) > 0 else current_price + 10
        key_resistance = resistance_levels[1] if isinstance(resistance_levels, list) and len(resistance_levels) > 1 else current_price + 25

        context_text = f"""
    📈 SUPPORT/RESISTANCE CONTEXT:
    • Current: ₹{current_price:.2f}
    • Immediate Support: ₹{immediate_support:.2f}
    • Key Support: ₹{key_support:.2f}
    • Immediate Resistance: ₹{immediate_resistance:.2f}
    • Key Resistance: ₹{key_resistance:.2f}"""

        return context_text, support_levels, resistance_levels

    def calculate_support_levels(self, prices: List[float], current_price: float) -> List[float]:
        """Calculate support levels."""
        support_levels = []
        sorted_prices = sorted([p for p in prices if p < current_price], reverse=True)
        if len(sorted_prices) >= 2:
            support_levels = sorted_prices[:2]
        else:
            support_levels = [current_price - 10, current_price - 25]
        return support_levels

    def calculate_resistance_levels(self, prices: List[float], current_price: float) -> List[float]:
        """Calculate resistance levels."""
        resistance_levels = []
        sorted_prices = sorted([p for p in prices if p > current_price])
        
        if len(sorted_prices) >= 2:
            resistance_levels = sorted_prices[:2]
        else:
            # Estimate resistance levels
            resistance_levels = [current_price + 10, current_price + 25]
        
        return resistance_levels


    def predict_with_model(self, features: Dict[str, float], weights: Dict[str, float], atr: float):
        """Enhanced prediction using ML model with weighted fallback and confidence adjustment."""
        try:
            if self.ml_model is not None and self.scaler is not None:
                # Prepare features for ML model
                feature_values = [
                    features.get('spot_price', 0),             # 1
                    features.get('ce_oi', 0),                  # 2
                    features.get('pe_oi', 0),                  # 3
                    features.get('ce_vol', 0),                 # 4
                    features.get('pe_vol', 0),                 # 5
                    features.get('oi_pcr', 1.0),               # 6
                    features.get('vol_pcr', 1.0),              # 7
                    features.get('price_change', 0),           # 8
                    features.get('volume_bias', 0),            # 9
                    features.get('atr', atr),                  # 10
                    features.get('rsi_value', 50.0),           # 11
                    features.get('oi_acceleration', 0.0),      # 12
                    features.get('max_pain_gravity', 0.0),     # 13
                    features.get('fear_gauge', 0.0),           # 14
                    features.get('historical_trend', 0.0)      # 15
                ]
                scaled_features = self.scaler.transform([feature_values])

                # Get ML prediction
                ml_prediction = self.ml_model.predict(scaled_features)[0]
                ml_confidence = max(self.ml_model.predict_proba(scaled_features)[0])
                
                logger.info(f"🤖 ML Model Prediction: {ml_prediction} (Confidence: {ml_confidence:.2f})")
                
                return {
                    "prediction": ml_prediction,
                    "confidence": ml_confidence,
                    "method": "ML_MODEL"
                }
            else:
                # Fallback to weighted analysis
                weighted_score = sum(features.get(key, 0) * weight for key, weight in weights.items())
                
                # Normalize score
                prediction = 1 if weighted_score > 0 else 0
                confidence = min(abs(weighted_score) / 100, 1.0)
                
                logger.info(f"📊 Weighted Fallback Prediction: {prediction} (Confidence: {confidence:.2f})")
                
                return {
                    "prediction": prediction,
                    "confidence": confidence,
                    "method": "WEIGHTED_FALLBACK"
                }
                
        except Exception as e:
            logger.error(f"❌ Error in predict_with_model: {e}")
            return {
                "prediction": 0,
                "confidence": 0.1,
                "method": "ERROR_FALLBACK"
            }

#=============================================================================
# END OF ENHANCED STRATEGY ENGINE WITH SMART LIVE COMMENTARY
#=============================================================================
#=============================================================================
# PART 2: PROGRESSIVE RECOMMENDATION SYSTEM - COMPLETELY UPDATED VERSION
#=============================================================================
def get_recommendation_level(self, market_state: 'EnhancedMarketState') -> str:
    """Determine recommendation level - Adjusted to start after exactly 5 cycles."""
    snapshots = len(market_state.market_history)
    if snapshots >= 20:
        return "FULL_POWER"
    elif snapshots >= 10:
        return "HIGH_CONFIDENCE"
    elif snapshots >= 5:  # FIXED: Start recommendations after exactly 5 cycles
        return "MEDIUM_CONFIDENCE"
    else:
        return "INSUFFICIENT"  # No recommendations before 5 cycles

def analyze_market_progressive(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """ENHANCED VOLUME-PRIORITY Progressive market analysis with Volume Shift Detection."""
    level = self.get_recommendation_level(market_state)
    reasons = []
    score = 0.0
    triggers = []
    confidence_multiplier = 1.0

    # Initialize volume analysis data
    decision_volume_analysis = {
        "ce_vol_change": 0,
        "pe_vol_change": 0,
        "total_vol_change": 0,
        "volume_bias": 0,
        "bias_intensity": 0,
        "price_change": 0.0
    }

    logger.info(f"🎯 Analysis Level: {level} (Snapshots: {len(market_state.market_history)})")

    # =========================================================================
    # PRIORITY 1: ENHANCED VOLUME SHIFT ANALYSIS WITH RECOMMENDATIONS
    # =========================================================================
    if len(market_state.market_history) >= 2:
        current = market_state.market_history[-1]
        previous = market_state.market_history[-2]

        # Get volume and price changes with safety checks
        ce_vol_change = current.get("CE_VOL", 0) - previous.get("CE_VOL", 0)
        pe_vol_change = current.get("PE_VOL", 0) - previous.get("PE_VOL", 0)
        total_vol_change = ce_vol_change + pe_vol_change
        price_change = current.get("underlying_value", 0) - previous.get("underlying_value", 0)

        # Volume bias calculation (Positive = PE bias, Negative = CE bias)
        volume_bias = pe_vol_change - ce_vol_change

        # SAFE BIAS INTENSITY CALCULATION - ZERO DIVISION PROTECTION
        if total_vol_change != 0:
            bias_intensity = abs(volume_bias) / total_vol_change * 100
        else:
            bias_intensity = 0
            logger.info("📊 Market quiet - No volume activity for bias calculation")

        # Store volume analysis data
        decision_volume_analysis = {
            "ce_vol_change": ce_vol_change,
            "pe_vol_change": pe_vol_change,
            "total_vol_change": total_vol_change,
            "volume_bias": volume_bias,
            "bias_intensity": bias_intensity,
            "price_change": price_change
        }

        # CRITICAL PATTERN 1: BEARISH DIVERGENCE (Price up, PE volume dominance)
        if price_change > 0 and volume_bias > 15000:  # FIXED: lowered threshold
            score -= 6.0
            triggers.append("BEARISH_DIVERGENCE_DETECTED")
            reasons.append(f"🔴 BEARISH DIVERGENCE: Price up ₹{price_change:+.2f} but PE volume dominance +{volume_bias:,}")
            logger.warning(f"🚨 BEARISH DIVERGENCE: Price +{price_change:.2f}, PE volume dominance +{volume_bias:,}")
            if volume_bias > 500000:
                score -= 2.0
                triggers.append("STRONG_BEARISH_DIVERGENCE")
                reasons.append(f"🚨 STRONG BEARISH DIVERGENCE: Massive PE volume bias +{volume_bias:,}")

        # CRITICAL PATTERN 2: BULLISH DIVERGENCE (Price down, CE volume dominance)
        elif price_change < 0 and volume_bias < -15000:  # FIXED: lowered threshold
            score += 6.0
            triggers.append("BULLISH_DIVERGENCE_DETECTED")
            reasons.append(f"🟢 BULLISH DIVERGENCE: Price down ₹{price_change:+.2f} but CE volume dominance +{abs(volume_bias):,}")
            logger.info(f"✅ BULLISH DIVERGENCE: Price {price_change:.2f}, CE volume dominance +{abs(volume_bias):,}")
            if abs(volume_bias) > 500000:
                score += 2.0
                triggers.append("STRONG_BULLISH_DIVERGENCE")
                reasons.append(f"🚀 STRONG BULLISH DIVERGENCE: Massive CE volume bias +{abs(volume_bias):,}")

        # NEW PATTERN: Price Movement with Lower Volume Bias
        elif abs(price_change) > 3.0 and abs(volume_bias) > 8000:
            if price_change > 0 and volume_bias < 0:
                score += 2.5
                triggers.append("PRICE_MOMENTUM_BULLISH")
                reasons.append(f"🚀 BULLISH MOMENTUM: Price +₹{price_change:.2f} with CE bias {abs(volume_bias):,}")
            elif price_change < 0 and volume_bias > 0:
                score -= 2.5
                triggers.append("PRICE_MOMENTUM_BEARISH")
                reasons.append(f"🔴 BEARISH MOMENTUM: Price ₹{price_change:.2f} with PE bias {volume_bias:,}")

        # ORIGINAL CRITICAL PATTERN 3: MOMENTUM CONFIRMATION (Price & volume in same direction)
        elif price_change > 12 and volume_bias < -200000:
            score += 5.0
            triggers.append("BULLISH_MOMENTUM_CONFIRMATION")
            reasons.append(f"🚀 BULLISH MOMENTUM CONFIRMATION: Price +{price_change:.2f}, CE volume support")

        # CRITICAL PATTERN 4: VOLUME EXPLOSION (High total volume with directional bias)
        if total_vol_change > 400000:  # FIXED: lowered threshold
            triggers.append("VOLUME_EXPLOSION")
            if bias_intensity > 60:
                if volume_bias > 0:
                    score -= 4.0
                    triggers.append("PE_VOLUME_EXPLOSION")
                    reasons.append(f"💥 PE VOLUME EXPLOSION: {total_vol_change:,} total, {bias_intensity:.1f}% PE bias")
                    logger.warning(f"🚨 PE VOLUME EXPLOSION: {bias_intensity:.1f}% PE bias in {total_vol_change:,}")
                else:
                    score += 4.0
                    triggers.append("CE_VOLUME_EXPLOSION")
                    reasons.append(f"💥 CE VOLUME EXPLOSION: {total_vol_change:,} total, {bias_intensity:.1f}% CE bias")
                    logger.info(f"✅ CE VOLUME EXPLOSION: {bias_intensity:.1f}% CE bias in {total_vol_change:,}")
            else:
                reasons.append(f"📊 HIGH VOLUME: {total_vol_change:,} but balanced flow")

        # PATTERN 5: LOW VOLUME RALLY/DECLINE
        elif price_change > 10 and total_vol_change < 300000:
            score -= 2.0
            triggers.append("LOW_VOLUME_RALLY")
            reasons.append(f"⚠️ LOW VOLUME RALLY: Price +{price_change:.2f} with {total_vol_change:,} volume")

        elif price_change < -10 and total_vol_change < 300000:
            score += 1.0
            triggers.append("LOW_VOLUME_DECLINE")
            reasons.append(f"📊 LOW VOLUME DECLINE: Weak selling with {total_vol_change:,} volume")

        # PATTERN 6: CLASSIC VOLUME PATTERNS
        elif total_vol_change > 800000 and price_change < -10:
            score -= 6.0
            triggers.append("HIGH_VOLUME_SELLOFF")
            reasons.append(f"🚨 HIGH VOLUME SELLOFF: {total_vol_change:,} vol, price {price_change:.2f}")

        elif pe_vol_change > 700000 and price_change < -8:
            score -= 5.0
            triggers.append("PANIC_PUT_BUYING")
            reasons.append(f"🚨 PANIC PUT BUYING: PE vol {pe_vol_change:,}")

        elif ce_vol_change > 600000 and price_change > 12:
            score += 4.0
            triggers.append("STRONG_CALL_BUYING")
            reasons.append(f"✅ STRONG CALL BUYING: CE vol {ce_vol_change:,}, price +{price_change:.2f}")

        elif abs(ce_vol_change - pe_vol_change) < 200000 and price_change > 8 and total_vol_change > 400000:
            score += 2.5
            triggers.append("HEALTHY_VOLUME_RALLY")
            reasons.append("✅ HEALTHY VOLUME RALLY")

        # Enhanced logging
        logger.info("📊 Enhanced Volume Shift Analysis:")
        if total_vol_change != 0:
            ce_pc = ce_vol_change/total_vol_change*100
            pe_pc = pe_vol_change/total_vol_change*100
            logger.info(f"   CE Vol: {ce_vol_change:+,} ({ce_pc:.1f}%), PE Vol: {pe_vol_change:+,} ({pe_pc:.1f}%)")
        else:
            logger.info(f"   CE Vol: {ce_vol_change:+,}, PE Vol: {pe_vol_change:+,}, Market quiet")
        logger.info(f"   Volume Bias: {volume_bias:+,} ({bias_intensity:.1f}%), Price Change: ₹{price_change:+.2f}")

        # Handle zero volume
        if total_vol_change == 0:
            reasons.append("📊 Market quiet")
            confidence_multiplier *= 0.7

    else:
        logger.info("📊 Insufficient history for volume analysis")
        reasons.append("📊 Insufficient data")
        confidence_multiplier *= 0.3

    # =========================================================================
    # PRIORITY 2: STEALTH ACCUMULATION DETECTION (Multi-cycle)
    # =========================================================================
    if len(market_state.market_history) >= 4:
        recent = list(market_state.market_history)[-4:]
        biases = []
        for i in range(1,4):
            b = (recent[i].get('PE_VOL',0)-recent[i-1].get('PE_VOL',0)) - (recent[i].get('CE_VOL',0)-recent[i-1].get('CE_VOL',0))
            biases.append(b)
        logger.info(f"🔍 Stealth Accumulation: biases {biases}")
        if all(b>8000 for b in biases):
            score -= 3.0; triggers.append("STEALTH_BEARISH_ACC"); reasons.append("🕵 STEALTH BEARISH ACCUM")
        elif all(b<-8000 for b in biases):
            score += 3.0; triggers.append("STEALTH_BULLISH_ACC"); reasons.append("🕵 STEALTH BULLISH ACC")
        elif any(b>0 for b in biases) and any(b<0 for b in biases):
            score *= 0.8; triggers.append("MIXED_VOLUME_SIGNALS"); reasons.append("⚠ Mixed volume signals")

    # =========================================================================
    # PRIORITY 3: SMART PCR ANALYSIS
    # =========================================================================
    if len(market_state.market_history) >= 2:
        curr = market_state.market_history[-1]
        prev = market_state.market_history[-2]
        pcr_c = curr.get('OI_PCR',1.0)
        pcr_p = prev.get('OI_PCR',1.0)
        d = curr.get('underlying_value',0)-prev.get('underlying_value',0)
        dp = pcr_c-pcr_p
        logger.info(f"📊 PCR: {pcr_p:.3f}->{pcr_c:.3f} Δ{dp:+.3f}, Price Δ{d:+.2f}")
        if d< -10:
            if pcr_c<0.7: score+=0.5; triggers.append("SHORT_COVER"); reasons.append("📈 Short covering PCR")
            if pcr_c>1.2: score-=2.0; triggers.append("BEAR_PCR"); reasons.append("🔴 Bearish PCR")
            if dp>0.02: score-=1.5; triggers.append("RISING_FEAR"); reasons.append("🔴 Rising fear PCR")
        elif d>10:
            if pcr_c<0.7: score+=2.0; triggers.append("BULL_PCR"); reasons.append("✅ Bullish PCR")
            if pcr_c>1.2: score-=1.0; triggers.append("WEAK_RALLY_PCR"); reasons.append("⚠ Weak rally PCR")
            if dp< -0.05: score+=1.0; triggers.append("BUILD_CONFIDENCE"); reasons.append("✅ Building confidence PCR")
        else:
            if pcr_c<0.65: score+=1.0; triggers.append("LOW_PCR_NEUTRAL"); reasons.append("📈 Mild bull PCR")
            if pcr_c>1.35: score-=1.0; triggers.append("HIGH_PCR_NEUTRAL"); reasons.append("📉 Mild bear PCR")
        if pcr_c<0.5: score+=1.5; triggers.append("EXTREMELY_LOW_PCR"); reasons.append("🚀 Extreme bull PCR")
        if pcr_c>2.0: score-=1.5; triggers.append("EXTREMELY_HIGH_PCR"); reasons.append("💥 Extreme bear PCR")

    # =========================================================================
    # PRIORITY 4: OI ANALYSIS
    # =========================================================================
    if len(market_state.market_history) >= 2:
        curr = market_state.market_history[-1]
        prev = market_state.market_history[-2]
        pe_oi = curr.get("PE_OI",0)-prev.get("PE_OI",0)
        ce_oi = curr.get("CE_OI",0)-prev.get("CE_OI",0)
        d = curr.get('underlying_value',0)-prev.get('underlying_value',0)
        logger.info(f"📊 OI: PE Δ{pe_oi:+,}, CE Δ{ce_oi:+,}, Price Δ{d:+.2f}")
        if d< -10:
            if pe_oi>8000: score-=1.5; triggers.append("PE_OI_DECLINE"); reasons.append("🔴 PE OI build on decline")
            if ce_oi< -15000: score-=1.0; triggers.append("CE_OI_UNWIND"); reasons.append("🔴 CE unwind")
        elif d>10:
            if ce_oi>8000: score-=1.5; triggers.append("CE_OI_RALLY"); reasons.append("⚠ CE resistance build")
            if pe_oi>8000: score+=2.0; triggers.append("PE_OI_RALLY"); reasons.append("✅ PE support build")
            if pe_oi< -15000: score-=1.0; triggers.append("PE_OI_UNWIND_R"); reasons.append("⚠ PE unwind")
        if abs(pe_oi)>50000: confidence_multiplier*=1.1; triggers.append("MASSIVE_PE_OI")
        if abs(ce_oi)>50000: confidence_multiplier*=1.1; triggers.append("MASSIVE_CE_OI")

    # =========================================================================
    # PRIORITY 5: REGIME & MOMENTUM ANALYSIS
    # =========================================================================
    if len(market_state.market_history)>=5:
        prices = [m.get('underlying_value',0) for m in list(market_state.market_history)[-5:]]
        vols   = [(m.get('CE_VOL',0)+m.get('PE_VOL',0)) for m in list(market_state.market_history)[-4:]]
        slope = (prices[-1]-prices[0])/4
        vol_avg = sum(vols[i]-vols[i-1] for i in range(1,4))/3
        logger.info(f"📊 Regime: Price slope {slope:+.2f}, Vol trend {vol_avg:+,.0f}")
        if slope < -3 and vol_avg>300000:
            s = min(abs(slope)/5+vol_avg/500000,3.0)
            score -=3.0*s; triggers.append("BEAR_REGIME"); reasons.append(f"🚨 Bear regime ({s:.1f})"); confidence_multiplier*=1.3
        elif slope>3 and vol_avg>300000:
            s = min(slope/5+vol_avg/500000,2.5)
            score +=2.5*s; triggers.append("BULL_REGIME"); reasons.append(f"✅ Bull regime ({s:.1f})"); confidence_multiplier*=1.2
        elif abs(slope)>8:
            vf = min(abs(slope)/10,1.0)
            score *= (1-vf*0.3); triggers.append("HIGH_VOL"); reasons.append("⚠ High volatility"); confidence_multiplier*=0.8
        elif abs(slope)<1 and vol_avg<100000:
            triggers.append("CONSOLIDATION_REGIME"); reasons.append("📊 Consolidation"); confidence_multiplier*=0.9
        # regime change
        if len(market_state.market_history)>=8:
            old = [m.get('underlying_value',0) for m in list(market_state.market_history)[-8:-4]]
            os = (old[-1]-old[0])/3
            if (os>2 and slope<-2) or (os<-2 and slope>2):
                triggers.append("REGIME_CHANGE"); reasons.append(f"🔄 Regime change {os:+.2f}->{slope:+.2f}"); confidence_multiplier*=1.1

    # =========================================================================
    # ADJUST CONFIDENCE
    # =========================================================================
    if level in ["HIGH_CONFIDENCE","FULL_POWER"]:
        confidence_multiplier *=1.2
        logger.info(f"🎯 {level} x1.2 confidence")
    vc = decision_volume_analysis["total_vol_change"]
    if vc>2000000: confidence_multiplier*=1.3; logger.info("🔥 Massive volume boost")
    elif vc<100000: confidence_multiplier*=0.6; logger.info("⚠ Low volume penalty")

    # =========================================================================
    # FINAL VERDICT
    # =========================================================================
    verdict = self.determine_progressive_verdict(score,triggers,level,confidence_multiplier)
    return {
        "verdict": verdict,
        "score": round(score*confidence_multiplier,2),
        "triggers": triggers,
        "reason": " | ".join(reasons) if reasons else "Neutral",
        "confidence_level": level,
        "raw_score": round(score,2),
        "confidence_multiplier": confidence_multiplier,
        "volume_analysis": decision_volume_analysis
    }

#=============================================================================
#PART 3: PREDICTIVE EXIT SYSTEM (NEW) - FULLY FIXED VERSION
#=============================================================================
def analyze_predictive_exit_signals(self, analysis: Dict[str, Any], day_profile:        'EnhancedMarketDayProfile', market_state: 'EnhancedMarketState') -> Dict[str, Any]:
        """Advanced predictive exit system - Exit BEFORE losses occur."""
        trade = day_profile.active_trade
        if not trade:
            return {"exit_signal": False, "reason": "No active trade"}

        # FIXED: Safe access to market history
        if len(market_state.market_history) == 0:
            return {"exit_signal": False, "reason": "No market history available"}

        current_snapshot = list(market_state.market_history)[-1]
        trade_type = trade['type']
        is_bullish = (trade_type == "CE")

        # Get current LTP and PnL
        strike_data = current_snapshot.get('strike_data', {})
        current_ltp = strike_data.get(trade['strike'], {}).get(f"{trade_type}_LTP", trade['entry'])
        current_pnl = ((current_ltp - trade['entry']) / trade['entry']) * 100

        exit_signals = []
        exit_strength = 0

        # 1. MOMENTUM SHIFT DETECTION (Most Important)
        if len(market_state.delta_history) >= 3:
            recent_deltas = list(market_state.delta_history)[-3:]

            # Check for momentum reversal patterns
            if is_bullish:
                # For CE trades - look for bearish momentum building
                pe_oi_acceleration = sum([d.get('delta_PE_OI', 0) for d in recent_deltas[-2:]])
                ce_oi_deceleration = sum([d.get('delta_CE_OI', 0) for d in recent_deltas[-2:]])

                if pe_oi_acceleration > 15000 and ce_oi_deceleration < -5000:
                    exit_signals.append("BEARISH_MOMENTUM_BUILDING")
                    exit_strength += 4

            else:
                # For PE trades - look for bullish momentum building
                ce_oi_acceleration = sum([d.get('delta_CE_OI', 0) for d in recent_deltas[-2:]])
                pe_oi_deceleration = sum([d.get('delta_PE_OI', 0) for d in recent_deltas[-2:]])

                if ce_oi_acceleration > 15000 and pe_oi_deceleration < -5000:
                    exit_signals.append("BULLISH_MOMENTUM_BUILDING")
                    exit_strength += 4

        # 2. VOLUME DIVERGENCE - Early Warning
        if len(market_state.market_history) >= 2:
            # FIXED: Safe access to market history
            market_history_list = list(market_state.market_history)
            current = market_history_list[-1]
            previous = market_history_list[-2]

            ce_vol_change = current.get('CE_VOL', 0) - previous.get('CE_VOL', 0)
            pe_vol_change = current.get('PE_VOL', 0) - previous.get('PE_VOL', 0)

            # For bullish trades - watch for PE volume spikes
            if is_bullish and pe_vol_change > 800000 and pe_vol_change > ce_vol_change * 1.5:
                exit_signals.append("HIGH_PE_VOLUME_DIVERGENCE")
                exit_strength += 3

            # For bearish trades - watch for CE volume spikes
            elif not is_bullish and ce_vol_change > 800000 and ce_vol_change > pe_vol_change * 1.5:
                exit_signals.append("HIGH_CE_VOLUME_DIVERGENCE")
                exit_strength += 3

        # 3. PCR SHIFT PREDICTION
        current_pcr = current_snapshot.get('OI_PCR', 1.0)
        if len(market_state.market_history) >= 3:
            # FIXED: Safe access to market history with slicing
            market_history_list = list(market_state.market_history)
            pcr_trend = []
            for i in range(-3, 0):
                if len(market_history_list) >= abs(i):
                    pcr_trend.append(market_history_list[i].get('OI_PCR', 1.0))

            if len(pcr_trend) >= 2:
                pcr_change = pcr_trend[-1] - pcr_trend[0]

                # For bullish trades - rising PCR is bearish
                if is_bullish and pcr_change > 0.02 and current_pcr > 0.75:
                    exit_signals.append("PCR_TURNING_BEARISH")
                    exit_strength += 2

                # For bearish trades - falling PCR is bullish
                elif not is_bullish and pcr_change < -0.02 and current_pcr < 1.25:
                    exit_signals.append("PCR_TURNING_BULLISH")
                    exit_strength += 2

        # 4. PROFIT PROTECTION - Exit if gains start eroding
        if current_pnl > 3.0:  # If we have decent profits
            # Check if we're losing momentum from peak
            peak_pnl = trade.get('peak_pnl', current_pnl)
            if current_pnl > peak_pnl:
                trade['peak_pnl'] = current_pnl
                peak_pnl = current_pnl

            pnl_drawdown = peak_pnl - current_pnl

            # Exit if losing more than 40% of peak gains
            if pnl_drawdown > peak_pnl * 0.4 and pnl_drawdown > 2.0:
                exit_signals.append("PROFIT_EROSION_DETECTED")
                exit_strength += 3

        # 5. SPOT PRICE MOMENTUM SHIFT - COMPLETELY FIXED
        if len(market_state.market_history) >= 4:
            # FIXED: Convert deque to list before slicing
            market_history_list = list(market_state.market_history)
            recent_spots = [m.get('underlying_value', 0) for m in market_history_list[-4:]]
            recent_volumes = [(m.get('CE_VOL', 0) + m.get('PE_VOL', 0)) for m in market_history_list[-4:]]

            # Calculate momentum score
            momentum_changes = []
            for i in range(1, len(recent_spots)):
                momentum_changes.append(recent_spots[i] - recent_spots[i-1])

            if len(momentum_changes) > 0:
                avg_momentum = np.mean(momentum_changes)
                latest_momentum = momentum_changes[-1]

                # Detect momentum reversal
                if is_bullish and avg_momentum > 0 and latest_momentum < -10:
                    exit_signals.append("SPOT_MOMENTUM_REVERSAL")
                    exit_strength += 2
                elif not is_bullish and avg_momentum < 0 and latest_momentum > 10:
                    exit_signals.append("SPOT_MOMENTUM_REVERSAL")
                    exit_strength += 2

        # DECISION LOGIC
        if exit_strength >= 6:  # Strong exit signal
            return {
                "exit_signal": True,
                "exit_type": "PREDICTIVE_EXIT",
                "reason": f"Predictive signals detected: {', '.join(exit_signals)}",
                "strength": exit_strength,
                "current_pnl": current_pnl
            }
        elif exit_strength >= 4:  # Warning signal
            return {
                "exit_signal": False,
                "exit_type": "WARNING",
                "reason": f"Exit warning: {', '.join(exit_signals)}",
                "strength": exit_strength,
                "current_pnl": current_pnl
            }

        return {"exit_signal": False, "reason": "No predictive exit signals", "current_pnl": current_pnl}

def calculate_real_time_momentum(self, market_state: 'EnhancedMarketState') -> Dict[str, float]:
        """Calculate real-time momentum for predictive exits."""
        if len(market_state.market_history) < 5:
            return {"momentum_score": 0.0, "momentum_direction": "NEUTRAL"}

        # FIXED: Get recent 5 snapshots safely
        market_history_list = list(market_state.market_history)
        recent_data = market_history_list[-5:]

        # Calculate various momentum indicators
        spot_momentum = []
        oi_momentum = []
        vol_momentum = []

        for i in range(1, len(recent_data)):
            current = recent_data[i]
            previous = recent_data[i-1]

            # Spot momentum
            spot_change = current.get('underlying_value', 0) - previous.get('underlying_value', 0)
            spot_momentum.append(spot_change)

            # OI momentum (CE vs PE)
            ce_oi_change = current.get('CE_OI', 0) - previous.get('CE_OI', 0)
            pe_oi_change = current.get('PE_OI', 0) - previous.get('PE_OI', 0)
            oi_bias = ce_oi_change - pe_oi_change  # Positive = bearish, Negative = bullish
            oi_momentum.append(-oi_bias)  # Invert for bullish positive

            # Volume momentum
            ce_vol_change = current.get('CE_VOL', 0) - previous.get('CE_VOL', 0)
            pe_vol_change = current.get('PE_VOL', 0) - previous.get('PE_VOL', 0)
            vol_bias = ce_vol_change - pe_vol_change
            vol_momentum.append(-vol_bias)  # Invert for bullish positive

        # Calculate weighted momentum (recent data more important)
        weights = [0.1, 0.2, 0.3, 0.4]  # Last data point gets highest weight

        # Ensure we have enough data points
        if len(spot_momentum) >= len(weights):
            weighted_spot = sum(w * m for w, m in zip(weights, spot_momentum[-len(weights):]))
            weighted_oi = sum(w * m for w, m in zip(weights, oi_momentum[-len(weights):])) / 10000  # Scale down
            weighted_vol = sum(w * m for w, m in zip(weights, vol_momentum[-len(weights):])) / 100000  # Scale down
        else:
            # Fallback for insufficient data
            weighted_spot = np.mean(spot_momentum) if spot_momentum else 0
            weighted_oi = np.mean(oi_momentum) / 10000 if oi_momentum else 0
            weighted_vol = np.mean(vol_momentum) / 100000 if vol_momentum else 0

        # Combined momentum score
        momentum_score = (weighted_spot * 0.4) + (weighted_oi * 0.3) + (weighted_vol * 0.3)

        # Determine direction
        if momentum_score > 2.0:
            direction = "STRONG_BULLISH"
        elif momentum_score > 0.5:
            direction = "BULLISH"
        elif momentum_score < -2.0:
            direction = "STRONG_BEARISH"
        elif momentum_score < -0.5:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return {
            "momentum_score": momentum_score,
            "momentum_direction": direction,
            "spot_momentum": weighted_spot,
            "oi_momentum": weighted_oi,
            "vol_momentum": weighted_vol
        }

def safe_get_recent_history(self, market_state: 'EnhancedMarketState', count: int) -> List[Dict]:
        """Safely get recent history converting deque to list."""
        try:
            history_list = list(market_state.market_history)
            return history_list[-count:] if len(history_list) >= count else history_list
        except Exception as e:
            logger.warning(f"⚠️ Error getting recent history: {e}")
            return []
#=============================================================================
#PART 4: TRADE DECISION & MANAGEMENT ENGINE
#=============================================================================
def generate_trade_decision(self, market_state: 'EnhancedMarketState', day_profile: 'EnhancedMarketDayProfile'):
    """Generate progressive trade decisions with predictive capabilities and confidence scoring."""
    try:
        # 1️⃣ Support/Resistance context + levels
        sr_text, support_level, resistance_level = self._generate_support_resistance_context(market_state)


        # 2️⃣ Prepare last 20 volumes and OI
        volumes_20 = [s.get('CE_VOL', 0) + s.get('PE_VOL', 0) for s in market_state.safe_get_recent_history(20)]
        oi_20 = [s.get('CE_OI', 0) + s.get('PE_OI', 0) for s in market_state.safe_get_recent_history(20)]

        # 3️⃣ Get latest OHLC
        if not market_state.market_history:
            return {"verdict": "NEUTRAL", "score": 0, "reason": "No market data", "confidence_level": "LOW"}

        latest = market_state.market_history[-1]
        ohlc_data = (
            latest.get('open', latest.get('underlying_value', 0)),
            latest.get('high', latest.get('underlying_value', 0)),
            latest.get('low', latest.get('underlying_value', 0)),
            latest.get('close', latest.get('underlying_value', 0))
        )

        # 4️⃣ Higher timeframe trend match (placeholder - set your logic)
        higher_tf_alignment = True

        # 5️⃣ Call our signal engine
        from signal_engine import process_live_market
        signal_result = process_live_market(
            o=open_price,
            h=high_price,
            l=low_price,
            c=close_price,
            sr_levels=[support, resistance],
            volumes=volumes,
            oi_values=oi_values,
            higher_tf_alignment=higher_tf_alignment
        )



        # --- Existing Progressive AI Analysis ---
        analysis = self.analyze_market_progressive(market_state)
        logger.info(f"DEBUG: Analysis Verdict: {analysis['verdict']} | Score: {analysis['score']}")
        logger.info(f"DEBUG: Signal Engine Verdict: {signal_result}")

        # Merge Both Systems: Require BOTH to be trade-worthy
        if analysis['verdict'] != "NEUTRAL" and signal_result['action'] == "trade":
            rec = self.generate_progressive_recommendation(analysis, market_state, day_profile)
            logger.info(f"DEBUG: Generated Recommendation: {rec}")
            return {**analysis, "engine_signal": signal_result}
        else:
            logger.info("DEBUG: No high-confidence trade setup.")
            return {
                "verdict": "NEUTRAL",
                "score": 0,
                "reason": "No agreement between AI analysis and Signal Engine",
                "confidence_level": "LOW"
            }

    except Exception as e:
        logger.error(f"❌ Error in generate_trade_decision: {e}")
        return {
            "verdict": "NEUTRAL", 
            "score": 0,
            "reason": f"Error in analysis: {str(e)}",
            "confidence_level": "LOW"
        }

def manage_active_trade(self, analysis: Dict[str, Any], day_profile: 'EnhancedMarketDayProfile', market_state: 'EnhancedMarketState') -> Dict[str, Any]:
        """PREDICTIVE trade management - Exit BEFORE losses occur."""
        trade = day_profile.active_trade
        if not trade:
            return {"verdict": "NO_TRADE", "reason": "No active trade to manage."}

        # FIRST - Check predictive exit signals
        predictive_analysis = self.analyze_predictive_exit_signals(analysis, day_profile, market_state)

        if predictive_analysis.get("exit_signal", False):
            day_profile.active_trade = None
            current_pnl = predictive_analysis.get("current_pnl", 0)
            exit_reason = predictive_analysis.get("reason", "Predictive exit")

            # Send PREDICTIVE EXIT to Telegram
            confidence_level = trade.get('confidence_level', 'UNKNOWN')
            predictive_exit_msg = f"""
🧠 PREDICTIVE EXIT TRIGGERED!
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} - SMART EXIT

💡 REASON: {exit_reason}
💰 Final PnL: {current_pnl:+.2f}%
⚡ Exit Type: {predictive_analysis.get('exit_type', 'PREDICTIVE')}
🎯 Confidence: [{confidence_level}]

🧠 Bot predicted reversal BEFORE SL hit!
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
✅ CAPITAL PROTECTED!
"""
            asyncio.create_task(send_enhanced_telegram_message(predictive_exit_msg.strip(), priority="HIGH"))

            return {
                "verdict": "EXIT_NOW",
                "reason": f"Predictive exit: {exit_reason}",
                "pnl": current_pnl,
                "score": analysis['score'],
                "result": "SMART_EXIT"
            }

        # Check for warning signals
        elif predictive_analysis.get("exit_type") == "WARNING":
            warning_msg = f"⚠️ [{trade.get('confidence_level', 'UNKNOWN')}] EXIT WARNING: {predictive_analysis.get('reason', 'Unknown')} | Current PnL: {predictive_analysis.get('current_pnl', 0):+.2f}%"
            asyncio.create_task(send_enhanced_telegram_message(warning_msg))

        # Continue with regular trade management (targets, SL, etc.)
        trade_type = trade['type']
        s_now = market_state.market_history[-1]
        is_bullish = (trade_type == "CE")
        strike_data = s_now.get('strike_data', {})

        if trade['strike'] not in strike_data:
            return {"verdict": "EXIT_NOW", "reason": "Strike not found, exiting.", "pnl": 0.0, "score": analysis['score']}

        current_ltp = strike_data.get(trade['strike'], {}).get(f"{trade_type}_LTP", trade['entry'])
        if current_ltp <= 0:
            current_ltp = trade['entry']

        pnl = ((current_ltp - trade['entry']) / trade['entry']) * 100 if trade['entry'] > 0 else 0.0

        # Dynamic trailing SL (enhanced)
        if 'atr_trail' not in trade:
            trade['atr_trail'] = trade['original_sl']

        atr_val = market_state.get_atr()
        trail_dist = 1.2 * atr_val if atr_val > 0 else current_ltp * 0.03  # Tighter trailing

        if is_bullish:
            candidate_sl = current_ltp - trail_dist
            if candidate_sl > trade['atr_trail']:
                trade['atr_trail'] = candidate_sl
                trade['sl'] = candidate_sl
                # Send SL update to Telegram
                sl_update_msg = f"🛡️ Trailing SL Updated: ₹{candidate_sl:.2f} (LTP: ₹{current_ltp:.2f})"
                asyncio.create_task(send_enhanced_telegram_message(sl_update_msg))
        else:
            candidate_sl = current_ltp + trail_dist
            if candidate_sl < trade['atr_trail']:
                trade['atr_trail'] = candidate_sl
                trade['sl'] = candidate_sl
                # Send SL update to Telegram
                sl_update_msg = f"🛡️ Trailing SL Updated: ₹{candidate_sl:.2f} (LTP: ₹{current_ltp:.2f})"
                asyncio.create_task(send_enhanced_telegram_message(sl_update_msg))

        # Check targets first (before SL)
        if not trade.get('target1_hit', False):
            target1 = trade['partial_target']
            if (is_bullish and current_ltp >= target1) or (not is_bullish and current_ltp <= target1):
                trade['target1_hit'] = True
                target1_msg = f"""
✅ TARGET 1 HIT!
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} SUCCESS

💰 PROFIT DETAILS:
• Target Price: ₹{target1:.2f}
• Current LTP: ₹{current_ltp:.2f}
• Entry Price: ₹{trade['entry']:.2f}
• PnL: +{pnl:.2f}% 💚

📊 TRADE SUMMARY:
• Duration: {(datetime.now() - trade['entry_time']).seconds // 60}m
• Confidence: {trade.get('confidence_level', 'UNKNOWN')}
• Action: Book 50% profits, trail SL

📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
🎊 WELL DONE! 🎊
"""
                asyncio.create_task(send_enhanced_telegram_message(target1_msg.strip(), priority="HIGH"))
                logger.info(f"✅ [{trade.get('confidence_level', 'UNKNOWN')}] Target 1 Hit: LTP ₹{current_ltp:.2f}")

        if (is_bullish and current_ltp >= trade['target']) or (not is_bullish and current_ltp <= trade['target']):
            day_profile.active_trade = None
            target2_msg = f"""
🎉 TARGET 2 HIT!
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} COMPLETE SUCCESS

💰 FINAL PROFIT:
• Target Price: ₹{trade['target']:.2f}
• Exit LTP: ₹{current_ltp:.2f}
• Entry Price: ₹{trade['entry']:.2f}
• Final PnL: +{pnl:.2f}% 💚

📊 TRADE SUMMARY:
• Duration: {(datetime.now() - trade['entry_time']).seconds // 60}m
• Confidence: {trade.get('confidence_level', 'UNKNOWN')}
• Result: FULL TARGET ACHIEVED

📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
🎊 EXCELLENT TRADE! 🎊
"""
            asyncio.create_task(send_enhanced_telegram_message(target2_msg.strip(), priority="HIGH"))
            return {"verdict": "EXIT_NOW", "reason": "Target 2 hit! Recommendation successful.", "pnl": pnl, "score": analysis['score'], "result": "WIN"}

        # Traditional SL as last resort (should rarely hit now)
        if (is_bullish and current_ltp <= trade['sl']) or (not is_bullish and current_ltp >= trade['sl']):
            day_profile.active_trade = None
            confidence_level = trade.get('confidence_level', 'UNKNOWN')
            duration_minutes = (datetime.now() - trade['entry_time']).seconds // 60

            # Determine if it's a loss or protected profit
            result_emoji = "🛡️" if pnl > 0 else "❌"
            result_text = "PROFIT PROTECTED" if pnl > 0 else "LOSS CONTROLLED"

            sl_msg = f"""
{result_emoji} STOP LOSS HIT
━━━━━━━━━━━━━━━━━━━
🎯 {trade['type']} {int(trade['strike'])} STOPPED

💰 FINAL RESULT:
• SL Price: ₹{trade['sl']:.2f}
• Exit LTP: ₹{current_ltp:.2f}
• Entry Price: ₹{trade['entry']:.2f}
• Final PnL: {pnl:+.2f}%

📊 TRADE SUMMARY:
• Duration: {duration_minutes}m
• Confidence: {confidence_level}
• Result: {result_text}

💡 Risk management worked!
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
"""
            asyncio.create_task(send_enhanced_telegram_message(sl_msg.strip(), priority="HIGH"))
            return {"verdict": "EXIT_NOW", "reason": "Emergency SL hit.", "pnl": pnl, "score": analysis['score'], "result": "EMERGENCY_EXIT"}

        # Send periodic tracking updates (every 3rd cycle)
        cycle_count = getattr(trade, 'update_count', 0) + 1
        trade['update_count'] = cycle_count

        if cycle_count % 3 == 0:  # Every 3rd update
            tracking_msg = f"""
📊 TRADE UPDATE #{cycle_count // 3}
━━━━━━━━━━━━━━━━━━━
📈 {trade['type']} {int(trade['strike'])} Tracking

💰 CURRENT STATUS:
• LTP: ₹{current_ltp:.2f}
• PnL: {pnl:+.2f}% {"🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"}
• Entry: ₹{trade['entry']:.2f}

🎯 TARGET PROGRESS:
• Target 1: {((current_ltp - trade['entry']) / (trade['partial_target'] - trade['entry']) * 100) if is_bullish else ((trade['entry'] - current_ltp) / (trade['entry'] - trade['partial_target']) * 100):.1f}% (₹{trade['partial_target']:.2f})
• Target 2: {((current_ltp - trade['entry']) / (trade['target'] - trade['entry']) * 100) if is_bullish else ((trade['entry'] - current_ltp) / (trade['entry'] - trade['target']) * 100):.1f}% (₹{trade['target']:.2f})

🛡️ RISK MANAGEMENT:
• Stop Loss: ₹{trade['sl']:.2f}
• Risk: {((trade['sl'] - trade['entry']) / trade['entry'] * 100):+.1f}%

⏰ Trade Duration: {(datetime.now() - trade['entry_time']).seconds // 60}m
🎯 Confidence: {trade.get('confidence_level', 'UNKNOWN')}
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
"""
            asyncio.create_task(send_enhanced_telegram_message(tracking_msg.strip()))

        # Progress tracking
        progress_msg = f"[{trade.get('confidence_level', 'UNKNOWN')}] Predictive Tracking: LTP ₹{current_ltp:.2f} (PnL: {pnl:+.2f}%)"
        logger.info(progress_msg)

        return {"verdict": "TREND_HOLDING", "reason": "Predictive monitoring active", "pnl": pnl, "score": analysis['score']}
#=============================================================================
#PART 5: RECOMMENDATION GENERATION & TELEGRAM INTEGRATION - COMPLETE UPDATED VERSION
#=============================================================================
def generate_progressive_recommendation(self, decision: Dict[str, Any], market_state: 'EnhancedMarketState', day_profile: 'EnhancedMarketDayProfile') -> str:
        """Generate recommendations with CORRECTED PE/CE targets and ENHANCED volume analysis integration."""
        verdict = decision['verdict']
        level = decision['confidence_level']

        if verdict == "NEUTRAL":
            return f"🔍 [{level}] No clear signals detected. Continue monitoring."

        # Get current market data
        snapshot = market_state.market_history[-1]
        spot = snapshot['underlying_value']
        strikes = sorted(snapshot.get("strike_data", {}).keys())

        if not strikes:
            return "❌ Insufficient strike data for recommendation."

        atm_strike = min(strikes, key=lambda k: abs(k - spot))
        strike_data = snapshot["strike_data"][atm_strike]

        # Determine option type and entry
        is_bullish = "BULLISH" in verdict
        option_type = "CE" if is_bullish else "PE"
        entry_price = strike_data.get(f"{option_type}_LTP", 0)

        if entry_price <= 0:
            return "❌ Invalid option price data."

        # Progressive position sizing and risk
        position_multipliers = {
            "EARLY_SIGNALS": 0.5, "MEDIUM_CONFIDENCE": 0.75,
            "HIGH_CONFIDENCE": 1.0, "FULL_POWER": 1.0
        }
        risk_multipliers = {
            "EARLY_SIGNALS": 0.5, "MEDIUM_CONFIDENCE": 0.75,
            "HIGH_CONFIDENCE": 1.0, "FULL_POWER": 1.0
        }

        pos_mult = position_multipliers.get(level, 0.5)
        risk_mult = risk_multipliers.get(level, 0.5)

        # CORRECTED PE/CE TARGET CALCULATION - FIXED LOGIC
        base_sl_points = 2.0 * risk_mult  # ₹2 per risk level
        target1_points = 6.0  # ₹6 profit for T1
        target2_points = 20.0 if level == "FULL_POWER" else 16.0  # ₹16-20 for T2

        # 📚 CORRECT OPTION LOGIC FOR BOTH PE AND CE:
        # - When option moves in our favor, premium INCREASES
        # - Targets should be HIGHER than entry (sell at higher premium)
        # - Stop loss should be LOWER than entry (exit at lower premium)
        #
        # PE Example: Market falls → PE premium rises → Sell at higher price (T1: 42, T2: 56)
        # CE Example: Market rises → CE premium rises → Sell at higher price (T1: 42, T2: 56)

        # CORRECTED CALCULATION (SAME FOR BOTH PE AND CE):
        sl = entry_price - base_sl_points         # Entry 36 → SL 34 (LOSS)
        target1 = entry_price + target1_points    # Entry 36 → T1 42 (PROFIT)
        target2 = entry_price + target2_points    # Entry 36 → T2 56 (BIGGER PROFIT)

        # Risk-Reward validation
        risk_amount = entry_price - sl  # 36 - 34 = 2
        reward_t1 = target1 - entry_price  # 42 - 36 = 6
        reward_t2 = target2 - entry_price  # 56 - 36 = 20

        logger.info(f"📊 CORRECTED {option_type} Targets:")
        logger.info(f" Entry: ₹{entry_price:.2f}")
        logger.info(f" Target 1: ₹{target1:.2f} (+₹{reward_t1:.2f})")
        logger.info(f" Target 2: ₹{target2:.2f} (+₹{reward_t2:.2f})")
        logger.info(f" Stop Loss: ₹{sl:.2f} (-₹{risk_amount:.2f})")
        logger.info(f" Risk:Reward = 1:{reward_t1/risk_amount:.1f} | 1:{reward_t2/risk_amount:.1f}")

        # Create trade for tracking
        if level in ["MEDIUM_CONFIDENCE", "HIGH_CONFIDENCE", "FULL_POWER"]:
            day_profile.active_trade = {
                "type": option_type, "strike": atm_strike, "entry": entry_price,
                "sl": sl, "partial_target": target1, "target": target2,
                "original_sl": sl, "entry_time": datetime.now(),
                "confidence_level": level, "monitored": True,
                "corrected_targets": True,  # Flag to indicate corrected logic
                "risk_reward_t1": reward_t1/risk_amount if risk_amount > 0 else 0,
                "risk_reward_t2": reward_t2/risk_amount if risk_amount > 0 else 0
            }

        # Extract volume analysis data for enhanced Telegram message
        volume_analysis = decision.get('volume_analysis', {})
        ce_vol_change = volume_analysis.get('ce_vol_change', 0)
        pe_vol_change = volume_analysis.get('pe_vol_change', 0)
        total_vol_change = volume_analysis.get('total_vol_change', 0)
        volume_bias = volume_analysis.get('volume_bias', 0)
        price_change = volume_analysis.get('price_change', 0.0)

        # Determine volume shift pattern for display
        if volume_bias > 100000:
            volume_pattern = f"PE Bias (+{volume_bias:,})"
            volume_emoji = "📉"
        elif volume_bias < -100000:
            volume_pattern = f"CE Bias (+{abs(volume_bias):,})"
            volume_emoji = "📈"
        else:
            volume_pattern = "Balanced Flow"
            volume_emoji = "⚖️"

        # Determine signal priority based on volume patterns
        pattern_detection = decision.get('pattern_detection', {})
        signal_priority = "HIGH PRIORITY"

        if pattern_detection.get('bearish_divergence') or pattern_detection.get('bullish_divergence'):
            signal_priority = "🚨 CRITICAL PRIORITY"
        elif pattern_detection.get('volume_explosion'):
            signal_priority = "⚡ HIGH PRIORITY"
        elif pattern_detection.get('stealth_accumulation'):
            signal_priority = "🔍 HIGH PRIORITY"

        # Generate confidence emoji and description
        confidence_emoji = {
            "EARLY_SIGNALS": "🟡", "MEDIUM_CONFIDENCE": "🟠",
            "HIGH_CONFIDENCE": "🔴", "FULL_POWER": "🚨"
        }

        confidence_desc = {
            "EARLY_SIGNALS": "EARLY_SIGNALS", "MEDIUM_CONFIDENCE": "MEDIUM_CONFIDENCE",
            "HIGH_CONFIDENCE": "HIGH_CONFIDENCE", "FULL_POWER": "FULL_POWER"
        }

        emoji = confidence_emoji.get(level, "🔍")
        conf_desc = confidence_desc.get(level, level)

        # Determine signal type based on verdict
        signal_type = verdict.replace("_", " ").title()

        # Generate ENHANCED Telegram message with corrected targets and volume analysis
        telegram_msg = f"""{signal_priority}
🎯 NIFTY TRADE ALERT
━━━━━━━━━━━━━━━━━━━
📊 CONFIDENCE: {conf_desc}
🎯 SIGNAL: {signal_type}

📍 ENTRY DETAILS:
• Option: {option_type} {int(atm_strike)}
• Entry Price: ₹{entry_price:.2f}
• Spot: ₹{spot:.2f}

🎯 TARGETS & RISK:
• Target 1: ₹{target1:.2f}
• Target 2: ₹{target2:.2f}
• Stop Loss: ₹{sl:.2f}
• Position Size: {int(pos_mult*100)}%

📊 MARKET DATA:
• CE OI: {int(snapshot.get('CE_OI', 0)):,}
• PE OI: {int(snapshot.get('PE_OI', 0)):,}
• OI PCR: {snapshot.get('OI_PCR', 0):.3f}

📊 VOLUME ANALYSIS:
• CE Volume: {ce_vol_change:+,}
• PE Volume: {pe_vol_change:+,}
• Total Volume: {total_vol_change:+,}
• Price Change: ₹{price_change:+.2f}
• Pattern: {volume_emoji} {volume_pattern}

💡 REASON: {decision['reason'][:120]}...

⚖️ RISK:REWARD:
• T1 R:R = 1:{reward_t1/risk_amount:.1f}
• T2 R:R = 1:{reward_t2/risk_amount:.1f}

⭐ ANALYSIS SCORE: {decision['score']:.2f}/10
📅 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━"""

        # Add pattern-specific alerts
        pattern_alerts = []
        if pattern_detection.get('bearish_divergence'):
            pattern_alerts.append("🔴 BEARISH DIVERGENCE: Price up but PE volume dominance")
        if pattern_detection.get('bullish_divergence'):
            pattern_alerts.append("🟢 BULLISH DIVERGENCE: Price down but CE volume dominance")
        if pattern_detection.get('volume_explosion'):
            pattern_alerts.append("💥 VOLUME EXPLOSION: Institutional activity detected")
        if pattern_detection.get('stealth_accumulation'):
            pattern_alerts.append("🕵️ STEALTH ACCUMULATION: Smart money positioning")

        if pattern_alerts:
            telegram_msg += f"\n\n🚨 PATTERN ALERTS:\n" + "\n".join([f"• {alert}" for alert in pattern_alerts])

        # Add volume shift interpretation
        telegram_msg += f"\n\n💡 VOLUME INTERPRETATION:"
        if volume_bias > 200000:
            telegram_msg += f"\n📉 Strong bearish volume shift - More traders buying PUTs"
        elif volume_bias < -200000:
            telegram_msg += f"\n📈 Strong bullish volume shift - More traders buying CALLs"
        elif total_vol_change > 1000000:
            telegram_msg += f"\n⚡ High volume activity - Major institutional moves"
        else:
            telegram_msg += f"\n⚖️ Balanced volume flow - Normal market conditions"

        # Add corrected target explanation
        telegram_msg += f"\n\n📚 TARGET LOGIC:"
        if option_type == "PE":
            telegram_msg += f"\n• Market DOWN → PE premium UP → Sell at HIGHER prices"
            telegram_msg += f"\n• Entry ₹{entry_price:.2f} → T1 ₹{target1:.2f} → T2 ₹{target2:.2f}"
        else:
            telegram_msg += f"\n• Market UP → CE premium UP → Sell at HIGHER prices"
            telegram_msg += f"\n• Entry ₹{entry_price:.2f} → T1 ₹{target1:.2f} → T2 ₹{target2:.2f}"

        # Send to Telegram with appropriate priority
        priority = "CRITICAL" if "CRITICAL" in signal_priority else "HIGH"
        asyncio.create_task(send_enhanced_telegram_message(telegram_msg, priority=priority))

        # Enhanced logging with volume patterns
        logger.info(f"[{level}] Generated recommendation: {verdict}")
        logger.info(f"📊 Entry: ₹{entry_price:.2f} | T1: ₹{target1:.2f} | T2: ₹{target2:.2f} | SL: ₹{sl:.2f}")
        logger.info(f"📊 Volume Pattern: {volume_pattern} | Price Change: ₹{price_change:+.2f}")

        if pattern_alerts:
            for alert in pattern_alerts:
                logger.warning(f"🚨 {alert}")

        return telegram_msg
#=============================================================================
#PART 6: AI MODEL & LEGACY SUPPORT METHODS
#============================================================================
def predict_with_model(self, features: Dict[str, float], weights: Dict[str, float], atr: float) -> Dict[str, Any]:
        """Enhanced prediction using ML model with weighted fallback and confidence adjustment."""
        if not features:
            return {"prediction": 0.0, "confidence": 0.0, "features": {}, "source": "NONE"}

        # First, try ML model if available
        if self.ml_model is not None and self.scaler is not None:
            try:
                feature_names = list(features.keys())
                feature_vector = [features.get(name, 0.0) for name in feature_names]
                if len(feature_vector) > 0:
                    scaled_features = self.scaler.transform([feature_vector])
                    ml_prediction = self.ml_model.predict(scaled_features)[0]
                    ml_confidence = max(self.ml_model.predict_proba(scaled_features)[0])
                    logger.info("🤖 ML Prediction: %s (Confidence: %.2f%%)", "UP" if ml_prediction > 0 else "DOWN", ml_confidence * 100)
                    return {"prediction": ml_prediction, "confidence": ml_confidence, "features": features, "source": "ML"}
            except Exception as e:
                logger.warning("⚠️ ML prediction failed: %s", e)

        # Fallback to weighted model
        total_score = sum(features.get(k, 0.0) * v for k, v in weights.items())
        max_score = sum(abs(v) for v in weights.values())
        base_confidence = min(abs(total_score) / max_score if max_score > 0 else 0.0, 1.0)

        # Adjust confidence based on volatility (ATR)
        volatility_adjustment = max(0.5, min(1.0, 1.0 - atr / 50.0)) if atr > 0 else 1.0
        confidence = base_confidence * volatility_adjustment

        logger.info("⚖️ Weighted Prediction: %.2f (Confidence: %.2f%%)", total_score, confidence * 100)
        return {"prediction": total_score, "confidence": confidence, "features": features, "source": "WEIGHTED"}

def analyze_market_predictive(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
        """Enhanced predictive market analysis with comprehensive signal detection (Legacy Support)."""
        if len(market_state.market_history) < 2:
            return {"verdict": "INSUFFICIENT_DATA", "score": 0.0, "reason": "Need at least 2 market snapshots"}

        # Get current and previous snapshots
        current = market_state.market_history[-1]
        previous = market_state.market_history[-2]

        # Initialize analysis
        score = 0.0
        reasons = []
        signals = []

        # 1. OI Analysis (Strong Signals)
        pe_oi_change = current.get("PE_OI", 0) - previous.get("PE_OI", 0)
        ce_oi_change = current.get("CE_OI", 0) - previous.get("CE_OI", 0)

        if pe_oi_change > 15000:  # Strong PE OI building
            score += 3.0
            signals.append("PE_OI_BUILD_STRONG")
            reasons.append(f"Strong PE OI building (+{int(pe_oi_change):,})")
        elif pe_oi_change > 5000:  # Moderate PE OI building
            score += 1.5
            signals.append("PE_OI_BUILD")
            reasons.append(f"PE OI building (+{int(pe_oi_change):,})")

        if ce_oi_change > 8000:  # Strong CE OI building
            score -= 3.0
            signals.append("CE_OI_BUILD_STRONG")
            reasons.append(f"Strong CE OI building (+{int(ce_oi_change):,})")
        elif ce_oi_change > 5000:  # Moderate CE OI building
            score -= 1.5
            signals.append("CE_OI_BUILD")
            reasons.append(f"CE OI building (+{int(ce_oi_change):,})")

        # 2. PCR Analysis
        current_pcr = current.get('OI_PCR', 1.0)
        if current_pcr < 0.7:  # Bullish PCR
            score += 2.0
            signals.append("PCR_BULLISH")
            reasons.append(f"Bullish PCR ({current_pcr:.3f})")
        elif current_pcr > 1.3:  # Bearish PCR
            score -= 2.0
            signals.append("PCR_BEARISH")
            reasons.append(f"Bearish PCR ({current_pcr:.3f})")

        # 3. Volume Analysis
        pe_vol_change = current.get("PE_VOL", 0) - previous.get("PE_VOL", 0)
        ce_vol_change = current.get("CE_VOL", 0) - previous.get("CE_VOL", 0)

        if pe_vol_change > 1000000:  # High PE volume
            score += 1.0
            signals.append("PE_VOL_HIGH")
            reasons.append(f"High PE volume (+{int(pe_vol_change):,})")

        if ce_vol_change > 1000000:  # High CE volume
            score -= 1.0
            signals.append("CE_VOL_HIGH")
            reasons.append(f"High CE volume (+{int(ce_vol_change):,})")

        # 4. Price Movement
        price_change = current.get("underlying_value", 0) - previous.get("underlying_value", 0)
        price_change_pct = (price_change / previous.get("underlying_value", 1)) * 100

        if abs(price_change_pct) > 0.5:  # Significant price movement
            if price_change > 0:
                score += 1.0
                signals.append("PRICE_MOMENTUM_UP")
                reasons.append(f"Strong upward momentum (+{price_change:.2f})")
            else:
                score -= 1.0
                signals.append("PRICE_MOMENTUM_DOWN")
                reasons.append(f"Strong downward momentum ({price_change:.2f})")

        # 5. Determine verdict based on score
        if score >= 5.0:
            verdict = "HIGH_CONVICTION_BULLISH"
        elif score <= -5.0:
            verdict = "HIGH_CONVICTION_BEARISH"
        elif score >= 3.0:
            verdict = "PRE_SIGNAL"
            reasons.append("High-confidence bullish signal building")
        elif score <= -3.0:
            verdict = "PRE_SIGNAL"
            reasons.append("High-confidence bearish signal building")
        else:
            verdict = "NEUTRAL"
            reasons.append("No clear directional signals")

        return {
            "verdict": verdict,
            "score": round(score, 2),
            "signals": signals,
            "reason": " | ".join(reasons) if reasons else "Neutral market conditions",
            "current_pcr": current_pcr,
            "price_change": price_change,
            "pe_oi_change": pe_oi_change,
            "ce_oi_change": ce_oi_change
        }

def generate_trade_recommendation(self, decision: Dict[str, Any], market_state: 'EnhancedMarketState', day_profile: 'EnhancedMarketDayProfile') -> str:
        """Generate detailed trade recommendation with entry, targets, SL, and start tracking (Legacy Support)."""
        if decision['verdict'] not in ["NEW_BULLISH_TRADE", "NEW_BEARISH_TRADE"]:
            return "No new trade recommended."

        # Get current spot and ATM strike
        snapshot = market_state.market_history[-1]
        spot = snapshot['underlying_value']
        strikes = sorted(snapshot.get("strike_data", {}).keys())
        if not strikes:
            return "Insufficient data for recommendation."

        atm_strike = min(strikes, key=lambda k: abs(k - spot))
        strike_data = snapshot["strike_data"][atm_strike]

        # Determine type: CE for bullish, PE for bearish
        option_type = "CE" if decision['verdict'] == "NEW_BULLISH_TRADE" else "PE"
        entry_price = strike_data.get(f"{option_type}_LTP", 0)

        if entry_price <= 0:
            return "Invalid entry price."

        # Calculate targets and SL (based on config risk percentages)
        sl_pct = self.config["risk"]["sl_percentage"]  # e.g., 0.04 -> 4%
        target1_pct = self.config["risk"]["target_percentage"] / 2  # e.g., 0.125
        target2_pct = self.config["risk"]["target_percentage"]  # e.g., 0.25

        atr = market_state.get_atr()  # Adjust for volatility
        sl_adjust = entry_price * sl_pct + atr * 0.5  # Risk-adjusted SL

        sl = entry_price - sl_adjust if option_type == "CE" else entry_price + sl_adjust
        target1 = entry_price + (entry_price * target1_pct) if option_type == "CE" else entry_price - (entry_price * target1_pct)
        target2 = entry_price + (entry_price * target2_pct) if option_type == "CE" else entry_price - (entry_price * target2_pct)

        # Create active trade for tracking
        day_profile.active_trade = {
            "type": option_type,
            "strike": atm_strike,
            "entry": entry_price,
            "sl": sl,
            "partial_target": target1,
            "target": target2,
            "original_sl": sl,  # For trailing
            "entry_time": datetime.now(),
            "monitored": True  # Flag for tracking
        }

        rec = f"{decision['verdict']} Recommendation: Buy {option_type} at ₹{entry_price:.2f} (Spot: ₹{spot:.2f}, Strike: {atm_strike}). Targets: ₹{target1:.2f} / ₹{target2:.2f}. SL: ₹{sl:.2f}. Reason: {decision['reason']}"

        logger.info(rec)
        asyncio.create_task(send_enhanced_telegram_message(rec, priority="HIGH"))  # Alert

        return rec
# =============================================================================
# ENHANCED MARKET DAY PROFILE WITH ADVANCED TRADE TRACKING
# =============================================================================
class EnhancedMarketDayProfile:
    """Enhanced daily trading profile with comprehensive trade tracking and performance analytics."""
    def __init__(self, index_name: str, config: Dict[str, Any]):
        self.index_name = index_name
        self.config = config
        # Enhanced trading state tracking
        self.dominant_force = "NEUTRAL"
        self.active_trade = None
        self.trade_history = deque(maxlen=50)
        self.reversal_warning_count = 0
        self.cooldown_cycles = 0
        self.pre_signal_flag = False
        # Advanced AI integration
        self.last_ai_prediction = None
        self.last_ai_features = None
        self.prediction_history = deque(maxlen=100)
        # Performance tracking
        self.daily_stats = {
            "trades_taken": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0,
            "best_trade": 0.0,
            "worst_trade": 0.0,
            "avg_hold_time": 0.0,
            "max_drawdown": 0.0
        }
        # Risk management
        self.risk_metrics = {
            "current_exposure": 0.0,
            "daily_loss": 0.0,
            "max_daily_loss": config.get("risk", {}).get("daily_loss_limit", -500),
            "consecutive_losses": 0,
            "last_trade_time": None
        }
        logger.info("📈 Enhanced Market Day Profile initialized for %s", index_name)
    def update_trade_performance(self, trade_result: Dict[str, Any]):
        """Update comprehensive trade performance metrics after each trade completion."""
        pnl = trade_result.get("pnl", 0.0)
        self.daily_stats["trades_taken"] += 1
        self.daily_stats["total_pnl"] += pnl
        if trade_result.get("result") == "WIN":
            self.daily_stats["winning_trades"] += 1
            self.risk_metrics["consecutive_losses"] = 0
            if pnl > self.daily_stats["best_trade"]:
                self.daily_stats["best_trade"] = pnl
        else:
            self.daily_stats["losing_trades"] += 1
            self.risk_metrics["consecutive_losses"] += 1
            self.risk_metrics["daily_loss"] += abs(pnl)
            if pnl < self.daily_stats["worst_trade"]:
                self.daily_stats["worst_trade"] = pnl
        # Update risk metrics
        self.risk_metrics["current_exposure"] = 0.0 if not self.active_trade else pnl
        self.risk_metrics["last_trade_time"] = datetime.now()
        total = self.daily_stats["trades_taken"]
        wins = self.daily_stats["winning_trades"]
        self.daily_stats["win_rate"] = (wins / total) * 100 if total > 0 else 0
        self.daily_stats["avg_pnl"] = self.daily_stats["total_pnl"] / total if total > 0 else 0
        logger.info("📊 Updated Performance - Win Rate: %.1f%% (%d/%d trades)", self.daily_stats["win_rate"], wins, total)
    def check_risk_limits(self) -> bool:
        """Check if current risk metrics are within acceptable limits."""
        if self.risk_metrics["daily_loss"] >= abs(self.risk_metrics["max_daily_loss"]):
            logger.warning("🚨 Daily loss limit reached: %.2f", self.risk_metrics["daily_loss"])
            return False
        if self.risk_metrics["consecutive_losses"] >= 5:
            logger.warning("🚨 Too many consecutive losses: %d", self.risk_metrics["consecutive_losses"])
            return False
        return True
    
    class FuturePredictionEngine:
        """AI system that predicts market movements 15-20 minutes ahead."""
        
        def __init__(self, config):
            self.config = config
            self.prediction_models = {}
            self.historical_accuracy = {}
            self.pattern_memory = deque(maxlen=200)
            
        def predict_next_15_minutes(self, market_state, current_analysis) -> Dict[str, Any]:
            """Predict market movement for next 15-20 minutes with high accuracy."""
            
            if len(market_state.market_history) < 10:
                return {"prediction": "INSUFFICIENT_DATA", "confidence": 0}
                
            # Extract current market intelligence
            current_data = self._extract_prediction_features(market_state)
            
            # Pattern recognition for future movement
            pattern_prediction = self._analyze_historical_patterns(market_state)
            
            # Volume momentum prediction
            volume_momentum = self._predict_volume_continuation(market_state)
            
            # OI structure analysis for direction
            oi_direction = self._analyze_oi_future_impact(market_state)
            
            # Institutional flow prediction
            smart_money_direction = self._predict_institutional_moves(market_state)
            
            # Combine all predictions
            final_prediction = self._combine_predictions(
                pattern_prediction, volume_momentum, oi_direction, smart_money_direction
            )
            
            # Generate specific targets and timing
            future_targets = self._calculate_future_targets(final_prediction, market_state)
            
            prediction_result = {
                "direction": final_prediction["direction"],
                "confidence": final_prediction["confidence"],
                "time_horizon": "15-20 minutes",
                "expected_move": future_targets["expected_move"],
                "key_levels": future_targets["key_levels"],
                "reasoning": final_prediction["reasoning"],
                "accuracy_track_record": self._get_recent_accuracy()
            }
            
            # Send prediction to Telegram
            self._send_prediction_to_telegram(prediction_result, market_state)
            
            return prediction_result
        
        def _extract_prediction_features(self, market_state) -> Dict:
            """Extract advanced features for prediction."""
            recent_data = list(market_state.market_history)[-10:]
            
            # Price momentum analysis
            price_momentum = self._calculate_momentum_strength(recent_data)
            
            # Volume acceleration patterns
            volume_acceleration = self._calculate_volume_acceleration(recent_data)
            
            # OI building vs unwinding
            oi_flow_pattern = self._analyze_oi_flow_patterns(recent_data)
            
            # Market microstructure
            microstructure = self._analyze_market_microstructure(recent_data)
            
            return {
                "price_momentum": price_momentum,
                "volume_acceleration": volume_acceleration,
                "oi_flow": oi_flow_pattern,
                "microstructure": microstructure
            }
        
        def _analyze_historical_patterns(self, market_state) -> Dict:
            """Find similar historical patterns and their outcomes."""
            current_pattern = self._encode_current_pattern(market_state)
            
            similar_patterns = []
            for historical_pattern in self.pattern_memory:
                similarity = self._calculate_pattern_similarity(current_pattern, historical_pattern)
                if similarity > 0.8:  # 80% similarity threshold
                    similar_patterns.append(historical_pattern)
            
            if similar_patterns:
                # Analyze outcomes of similar patterns
                outcomes = [p["actual_outcome"] for p in similar_patterns]
                bullish_outcomes = sum(1 for o in outcomes if o > 0)
                success_rate = bullish_outcomes / len(outcomes)
                
                return {
                    "prediction": "BULLISH" if success_rate > 0.6 else "BEARISH",
                    "confidence": abs(success_rate - 0.5) * 2,  # Convert to 0-1 scale
                    "similar_patterns_found": len(similar_patterns)
                }
            
            return {"prediction": "NEUTRAL", "confidence": 0, "similar_patterns_found": 0}
        
        def _predict_volume_continuation(self, market_state) -> Dict:
            """Predict if current volume patterns will continue."""
            recent_data = list(market_state.market_history)[-5:]
            
            if len(recent_data) < 3:
                return {"prediction": "NEUTRAL", "confidence": 0}
            
            # Calculate volume momentum over last 5 cycles
            volume_trend = []
            for i in range(1, len(recent_data)):
                current_vol = recent_data[i].get('CE_VOL', 0) + recent_data[i].get('PE_VOL', 0)
                prev_vol = recent_data[i-1].get('CE_VOL', 0) + recent_data[i-1].get('PE_VOL', 0)
                volume_trend.append(current_vol - prev_vol)
            
            # Check for acceleration
            if len(volume_trend) >= 2:
                recent_acceleration = volume_trend[-1] - volume_trend[-2]
                trend_direction = "INCREASING" if sum(volume_trend) > 0 else "DECREASING"
                
                # High volume usually continues for 15-20 minutes
                if abs(recent_acceleration) > 500000:
                    return {
                        "prediction": trend_direction,
                        "confidence": 0.8,
                        "acceleration": recent_acceleration
                    }
            
            return {"prediction": "STABLE", "confidence": 0.5}
        
        def _send_prediction_to_telegram(self, prediction: Dict, market_state) -> None:
            """Send future prediction to Telegram."""
            current_spot = market_state.market_history[-1].get('underlying_value', 0)
            
            prediction_msg = f"""🔮 FUTURE MARKET PREDICTION

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ⏰ PREDICTION HORIZON: Next 15-20 minutes
    📊 Current Spot: ₹{current_spot:.2f}

    🎯 PREDICTED DIRECTION: {prediction['direction']}
    📈 Expected Move: {prediction.get('expected_move', 'TBD')}
    🎯 Confidence: {prediction['confidence']*100:.1f}%

    🔍 REASONING:
    {prediction.get('reasoning', 'Pattern-based analysis')}

    🎯 KEY LEVELS TO WATCH:
    {chr(10).join([f"• {level}" for level in prediction.get('key_levels', [])])}

    📊 RECENT ACCURACY: {prediction.get('accuracy_track_record', 0)*100:.1f}%
    📅 Time: {datetime.now().strftime('%H:%M:%S')}

    💡 STRATEGY: Position accordingly for next 15-20 min move
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

            asyncio.create_task(send_enhanced_telegram_message(prediction_msg, priority="HIGH"))
    
    def analyze_market_with_future_prediction(self, market_state: 'EnhancedMarketState') -> Dict[str, Any]:
        """Enhanced analysis with future prediction capabilities."""
        
        # Initialize future prediction engine if not exists
        if not hasattr(self, 'prediction_engine'):
            self.prediction_engine = FuturePredictionEngine(self.config)
        
        # Get current analysis
        current_analysis = self.analyze_market_progressive(market_state)
        
        # Generate future predictions
        future_prediction = self.prediction_engine.predict_next_15_minutes(market_state, current_analysis)
        
        # Combine current analysis with future prediction
        enhanced_analysis = current_analysis.copy()
        enhanced_analysis['future_prediction'] = future_prediction
        
        # Adjust current signals based on future prediction
        if future_prediction['confidence'] > 0.7:
            # High confidence future prediction - adjust current recommendation
            if future_prediction['direction'] == 'BULLISH' and enhanced_analysis['verdict'] == 'NEUTRAL':
                enhanced_analysis['verdict'] = 'EARLY_BULLISH'
                enhanced_analysis['reason'] += f" | FUTURE: {future_prediction['reasoning']}"
            elif future_prediction['direction'] == 'BEARISH' and enhanced_analysis['verdict'] == 'NEUTRAL':
                enhanced_analysis['verdict'] = 'EARLY_BEARISH'
                enhanced_analysis['reason'] += f" | FUTURE: {future_prediction['reasoning']}"
        
        return enhanced_analysis
    
    def detect_smart_money_future_moves(self, market_state) -> Dict[str, Any]:
        """Detect institutional positioning for future moves."""
        
        if len(market_state.market_history) < 5:
            return {"signal": "INSUFFICIENT_DATA"}
        
        recent_data = list(market_state.market_history)[-5:]
        
        # Look for stealth accumulation patterns
        stealth_patterns = self._detect_stealth_accumulation(recent_data)
        
        # Detect option buildup patterns
        buildup_patterns = self._detect_option_buildup(recent_data)
        
        # Analyze unusual activity
        unusual_activity = self._detect_unusual_activity(recent_data)
        
        smart_money_signal = {
            "stealth_accumulation": stealth_patterns,
            "option_buildup": buildup_patterns,
            "unusual_activity": unusual_activity,
            "predicted_direction": self._predict_smart_money_direction(stealth_patterns, buildup_patterns),
            "time_horizon": "15-30 minutes"
        }
        
        return smart_money_signal

# =============================================================================
# COMPLETE ENHANCED MAIN LOOP WITH PROGRESSIVE RECOMMENDATIONS & FUTURE PREDICTION
# UPDATED VERSION WITH ALL PATCHES AND IMPROVEMENTS (Firebase Disabled)
# =============================================================================
async def main(config_path: str = "config.yaml") -> None:
    """Main loop for God Bot PRO with progressive recommendations, session continuity,
    future prediction system, and comprehensive debugging analysis."""

    # Initialize all components
    config = load_config(config_path)
    # initialize_firebase()  # COMMENTED OUT - Firebase disabled
    market_state = EnhancedMarketState("NIFTY", config)  # Only NIFTY with enhanced persistence
    day_profile = EnhancedMarketDayProfile("NIFTY", config)  # 🔧 FIX: Added required arguments
    engine = EnhancedStrategyEngine(config)  # Progressive recommendation engine
    self_analyzer = EnhancedSmartSelfAnalyzer()  # Global self-analyzer for mistake learning

    logger.info("🚀 God Bot PRO: Hybrid Edition v3.0 - Initialized for NIFTY with Progressive Recommendations & Session Continuity")
    logger.info("📊 Features: Volume-Priority Analysis, Predictive Exits, Future Prediction, Session Continuity")

    # Track session statistics
    session_start_time = datetime.now()
    total_cycles = 0
    successful_cycles = 0
    failed_cycles = 0

    # Send startup notification
    startup_msg = f"""🚀 GOD BOT PRO v3.0 STARTED
━━━━━━━━━━━━━━━━━━━
🎯 Target: NIFTY Only (Testing Mode)
📊 Features Active:
• Volume-Priority Analysis ✅
• Predictive Exit System ✅
• Progressive Recommendations ✅
• Future Prediction System ✅
• Session Continuity ✅

🧠 AI Components:
• Multi-timeframe Analysis ✅
• Greeks & Vol Smile ✅
• Self-Learning System ✅
• Smart Trade Management ✅
• Future Market Prediction ✅

📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━
🎯 Ready for intelligent trading!"""
    
    await send_enhanced_telegram_message(startup_msg.strip(), priority="HIGH")

    try:
        while True:
            try:
                cycle_start_time = time.time()
                total_cycles += 1

                logger.info("⏰ Starting cycle #%d at %s", total_cycles, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                # Check market hours
                current_time = datetime.now().time()
                market_start = dt_time(9, 15)  # 9:15 AM
                market_end = dt_time(15, 30)   # 3:30 PM
                is_market_hours = market_start <= current_time <= market_end

                if not is_market_hours:
                    logger.info("⏰ Outside market hours (%s). Reduced frequency mode.", current_time.strftime('%H:%M:%S'))

                # Log current weights for transparency
                weights = config.get("weights", {})
                logger.info("🧠 Current AI Brain Weights: %s", weights)

                # Self-diagnose before fetching
                diagnosis = market_state.self_diagnose()
                if "HEALTHY" not in diagnosis:
                    logger.warning("⚠️ Diagnosis for NIFTY: %s. Attempting recovery in fetch.", diagnosis)

                # Fetch ONLY NIFTY with enhanced retry
                nifty_raw = await fetch_single_chain_with_retry("NIFTY")
                nifty_snapshot = None

                if not nifty_raw:
                    logger.warning("⚠️ NIFTY fetch failed, using yfinance fallback")
                    nifty_snapshot = await enhanced_fallback_fetch("NIFTY")
                    if nifty_snapshot:
                        nifty_snapshot["data_quality"] = "ESTIMATED"
                        nifty_snapshot["data_source"] = "YFINANCE_FALLBACK"
                else:
                    nifty_snapshot = process_nse_snapshot_enhanced(nifty_raw)
                    if nifty_snapshot:
                        nifty_snapshot["data_quality"] = "RELIABLE"
                        nifty_snapshot["data_source"] = "NSE_DIRECT"

                # Process and update NIFTY state
                if nifty_snapshot:
                    logger.info("✅ Fetched data for NIFTY")
                    
                    # Save to Firebase first (before processing) - COMMENTED OUT
                    # if firebase_admin._apps:
                    #     save_market_data_to_firebase(nifty_snapshot, "NIFTY")

                    # Update market state
                    latest_analysis = market_state.update(nifty_snapshot)
                    # --- Prepare last 20 volumes and OI ---
                    volumes_20 = [
                        s.get('CE_VOL', 0) + s.get('PE_VOL', 0)
                        for s in market_state.safe_get_recent_history(20)
                    ]
                    oi_20 = [
                        s.get('CE_OI', 0) + s.get('PE_OI', 0)
                        for s in market_state.safe_get_recent_history(20)
                    ]

                    # --- Get Support/Resistance levels from your existing SR function ---
 
                    # --- Call our Signal Engine ---
                    # --- Get Support/Resistance levels FIRST ---
                    # --- Get Support/Resistance levels FIRST ---
                    sr_text, support_level, resistance_level = engine.generate_support_resistance_context(market_state)

                    # --- Call our Signal Engine ---
                    from signal_engine import process_live_market

                    result = process_live_market(
                        ohlc_data=(
                            nifty_snapshot['open'],
                            nifty_snapshot['high'],
                            nifty_snapshot['low'],
                            nifty_snapshot['close']
                        ),
                        sr_levels=[support_level, resistance_level],  # ✅ Now these are defined
                        volumes=volumes_20,
                        oi_values=oi_20,
                        
                        higher_tf_alignment=True
                    )


                    # --- If high-confidence signal, act on it ---
                    if result['action'] == 'trade':
                        logger.info(f"🚀 High Confidence Trade: {result}")
                        # You can place your trade execution code or Telegram alert here

                    if latest_analysis:
                        successful_cycles += 1

                        # Generate AI features and predictions
                        ai_features = market_state.get_ai_features()
                        if ai_features:
                            atr = market_state.get_atr()
                            ai_model_output = engine.predict_with_model(ai_features, weights, atr)
                            # Store AI predictions for analysis
                            setattr(day_profile, 'last_ai_prediction', ai_model_output)
                            setattr(day_profile, 'last_ai_features', ai_features)

                        # 🔮 ENHANCED ANALYSIS WITH FUTURE PREDICTION (INTEGRATED PATCH)
                        analysis_result = engine.analyze_market_with_future_prediction(market_state)

                        # Check for future-based recommendations
                        if 'future_prediction' in analysis_result:
                            future_pred = analysis_result['future_prediction']
                            if future_pred['confidence'] > 0.8:  # Very high confidence
                                logger.info(f"🔮 HIGH CONFIDENCE FUTURE PREDICTION: {future_pred['direction']} in next 15-20 min")
                                
                                # Send future prediction alert to Telegram
                                future_alert = f"""🔮 HIGH CONFIDENCE FUTURE PREDICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Next 15-20 Minutes
📊 Direction: {future_pred['direction']}
🎯 Confidence: {future_pred['confidence']*100:.1f}%
💡 Expected Move: {future_pred.get('expected_move', 'TBD')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                                
                                await send_enhanced_telegram_message(future_alert, priority="CRITICAL")

                        # Use analysis_result instead of decision for compatibility
                        decision = analysis_result

                        # Save significant decisions to Firebase - COMMENTED OUT
                        # if decision.get("verdict") != "NEUTRAL" and firebase_admin._apps:
                        #     save_analysis_data_to_firebase(decision, "NIFTY")

                        # Log comprehensive market intelligence
                        logger.info("[NIFTY] Market Intelligence - Spot: ₹%.2f | OI: CE %s, PE %s | VOL: CE %s, PE %s | PCRs: OI %.4f, Vol %.4f",
                                    latest_analysis.get('underlying_value', 0.0),
                                    f"{int(latest_analysis.get('CE_OI', 0)):,}",
                                    f"{int(latest_analysis.get('PE_OI', 0)):,}",
                                    f"{int(latest_analysis.get('CE_VOL', 0)):,}",
                                    f"{int(latest_analysis.get('PE_VOL', 0)):,}",
                                    latest_analysis.get('OI_PCR', 0.0),
                                    latest_analysis.get('VOL_PCR', 0.0))

                        # 🔥 HANDLE PROGRESSIVE RECOMMENDATIONS (ENHANCED SYSTEM WITH FUTURE PREDICTION)
                        if decision.get('verdict') in ["EARLY_BULLISH", "EARLY_BEARISH", "STRONG_BULLISH",
                                                       "STRONG_BEARISH", "HIGH_CONVICTION_BULLISH", "HIGH_CONVICTION_BEARISH"]:
                            
                            # Generate and send progressive recommendation
                            rec_message = engine.generate_progressive_recommendation(decision, market_state, day_profile)
                            logger.info(f"🎯 [NIFTY] Generated {decision.get('confidence_level', 'UNKNOWN')} recommendation")
                            
                            # Send live commentary if enabled
                            if hasattr(engine, 'commentary_bot') and engine.commentary_bot:
                                commentary = engine.commentary_bot.generate_comprehensive_market_commentary(market_state, decision)
                                if commentary and len(commentary.strip()) > 50:  # Only send if meaningful commentary
                                    await send_enhanced_telegram_message(f"🧠 LIVE MARKET ANALYSIS:\n{commentary}", priority="NORMAL")

                        # Handle legacy recommendations (backward compatibility)
                        elif decision.get('verdict') in ["NEW_BULLISH_TRADE", "NEW_BEARISH_TRADE"]:
                            rec_message = engine.generate_trade_recommendation(decision, market_state, day_profile)
                            logger.info("[NIFTY] Generated legacy trade recommendation")

                        # 🎯 MANAGE ACTIVE TRADES (ENHANCED MONITORING)
                        if day_profile.active_trade:
                            trade_result = engine.manage_active_trade(decision, day_profile, market_state)
                            
                            if trade_result.get('verdict') == 'EXIT_NOW':
                                # Save trade data to Firebase - COMMENTED OUT
                                # if firebase_admin._apps:
                                #     trade_data = {
                                #         **day_profile.active_trade,
                                #         "pnl": trade_result.get("pnl", 0),
                                #         "result": trade_result.get("result", "UNKNOWN"),
                                #         "exit_reason": trade_result.get("reason", "Unknown"),
                                #         "duration_minutes": (datetime.now() - day_profile.active_trade.get('entry_time', datetime.now())).seconds // 60
                                #     }
                                #    save_trade_data_to_firebase(trade_data, "NIFTY")

                                                        # Self-correction and learning
                                if 'trade_outcome' in trade_result:
                                    config = self_correct(trade_result['trade_outcome'], trade_result.get('features_at_entry', {}), config)

                                    # Enhanced self-analysis
                                    if hasattr(market_state, 'timeframe_analyzer'):
                                        tf_analysis = market_state.timeframe_analyzer.analyze_timeframe_changes(market_state.market_history)
                                    else:
                                        tf_analysis = {}

                                    self_analyzer.analyze_trade_mistake(
                                        trade_result['trade_outcome'],
                                        market_state.get_comprehensive_status(),
                                        tf_analysis
                                    )

                                # Update day profile
                                day_profile.update_trade_performance(trade_result)

                        # Handle trade exits with detailed analysis
                        if decision.get('verdict') == "EXIT_NOW":
                            # Post-trade evaluation and learning
                            if 'result' in decision:
                                pnl = decision.get('pnl', 0.0)
                                was_correct = decision['result'] == "WIN" or pnl > 0
                                confidence_level = decision.get('confidence_level', 'UNKNOWN')

                                eval_msg = f"[{confidence_level}] Trade Evaluation: Recommendation was {'✅ CORRECT' if was_correct else '❌ INCORRECT'}. Actual PnL: {pnl:+.2f}%."
                                logger.info(eval_msg)

                                # Send evaluation to Telegram
                                asyncio.create_task(send_enhanced_telegram_message(eval_msg))

                # Enhanced NIFTY summary with comprehensive debugging analysis
                if nifty_snapshot:
                    # Console output for monitoring
                    print(f"\n📊 NIFTY CYCLE #{total_cycles} SUMMARY:")
                    print("=" * 80)
                    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')} | 💹 Spot: ₹{nifty_snapshot.get('underlying_value', 0):.2f}")
                    print(f"🟢 CE: OI {int(nifty_snapshot.get('CE_OI', 0)):,} | Vol {int(nifty_snapshot.get('CE_VOL', 0)):,}")
                    print(f"🔴 PE: OI {int(nifty_snapshot.get('PE_OI', 0)):,} | Vol {int(nifty_snapshot.get('PE_VOL', 0)):,}")
                    print(f"📊 PCR: OI {nifty_snapshot.get('OI_PCR', 0):.4f} | Vol {nifty_snapshot.get('VOL_PCR', 0):.4f}")
                    print(f"📈 Source: {nifty_snapshot.get('data_source', 'Unknown')} | Quality: {nifty_snapshot.get('data_quality', 'Unknown')}")

                    # 🔮 DISPLAY FUTURE PREDICTION STATUS
                    if 'future_prediction' in analysis_result:
                        future_pred = analysis_result['future_prediction']
                        print(f"\n🔮 FUTURE PREDICTION (Next 15-20 min):")
                        print(f"    Direction: {future_pred['direction']}")
                        print(f"    Confidence: {future_pred['confidence']*100:.1f}%")
                        print(f"    Expected Move: {future_pred.get('expected_move', 'TBD')}")
                        print(f"    Accuracy Track Record: {future_pred.get('accuracy_track_record', 0)*100:.1f}%")

                    # Enhanced debugging analysis
                    print_comprehensive_analysis(market_state)
                    # Print complete timeframe data storage
                    print_complete_timeframe_data_storage(market_state)

                    # Also print the quick summary
                    print_timeframe_data_summary(market_state)
                    # Print PROGRESSIVE recommendation status
                    recommendation_level = engine.get_recommendation_level(market_state)
                    snapshots_count = len(market_state.market_history)

                    status_map = {
                        "INSUFFICIENT": f"🔴 Need {2 - snapshots_count} more snapshots for early signals",
                        "EARLY_SIGNALS": f"🟡 Early signals ready | {5 - snapshots_count} until medium confidence",
                        "MEDIUM_CONFIDENCE": f"🟠 Medium confidence | {10 - snapshots_count} until high confidence", 
                        "HIGH_CONFIDENCE": f"🔵 High confidence | {20 - snapshots_count} until full power",
                        "FULL_POWER": f"🚨 FULL AI POWER ACTIVE - Maximum accuracy mode"
                    }

                    print(f"\n🎯 RECOMMENDATION SYSTEM STATUS:")
                    print(f"    Level: {recommendation_level} ({snapshots_count} snapshots)")
                    print(f"    Status: {status_map.get(recommendation_level, 'Unknown')}")

                    # Volume analysis from the latest decision
                    if 'volume_analysis' in decision:
                        vol_data = decision['volume_analysis']
                        print(f"\n📊 VOLUME ANALYSIS (Last Cycle):")
                        print(f"    CE Volume Change: {vol_data.get('ce_vol_change', 0):+,}")
                        print(f"    PE Volume Change: {vol_data.get('pe_vol_change', 0):+,}")
                        print(f"    Price Change: ₹{vol_data.get('price_change', 0):+.2f}")
                        print(f"    Total Volume Change: {vol_data.get('total_vol_change', 0):+,}")

                    # Print current trade status if any
                    if day_profile.active_trade:
                        trade = day_profile.active_trade
                        confidence_level = trade.get('confidence_level', 'UNKNOWN')
                        duration = datetime.now() - trade['entry_time']
                        duration_str = f"{duration.seconds // 60}m {duration.seconds % 60}s"

                        print(f"\n🔥 ACTIVE TRADE MONITORING [{confidence_level}]:")
                        print(f"    {trade['type']} {int(trade['strike'])} | Entry: ₹{trade['entry']:.2f} | Duration: {duration_str}")
                        print(f"    🎯 Targets: ₹{trade['partial_target']:.2f} / ₹{trade['target']:.2f}")
                        print(f"    🛡️ Stop Loss: ₹{trade['sl']:.2f}")

                        # Calculate current PnL if possible
                        if 'strike_data' in nifty_snapshot and trade['strike'] in nifty_snapshot['strike_data']:
                            current_ltp = nifty_snapshot['strike_data'][trade['strike']].get(f"{trade['type']}_LTP", 0)
                            if current_ltp > 0:
                                current_pnl = ((current_ltp - trade['entry']) / trade['entry']) * 100
                                pnl_emoji = "🟢" if current_pnl > 0 else "🔴" if current_pnl < 0 else "⚪"
                                print(f"    💰 Current: ₹{current_ltp:.2f} | PnL: {current_pnl:+.2f}% {pnl_emoji}")

                                # Show target progress
                                target1_progress = ((current_ltp - trade['entry']) / (trade['partial_target'] - trade['entry'])) * 100 if trade['partial_target'] != trade['entry'] else 0
                                target2_progress = ((current_ltp - trade['entry']) / (trade['target'] - trade['entry'])) * 100 if trade['target'] != trade['entry'] else 0
                                
                                print(f"    📈 Progress: T1 {target1_progress:.1f}% | T2 {target2_progress:.1f}%")

                    # Print AI decision status with progressive details
                    print(f"\n🤖 AI DECISION STATUS:")
                    print(f"    Latest Verdict: {decision.get('verdict', 'UNKNOWN')}")
                    print(f"    Confidence Level: {decision.get('confidence_level', 'N/A')}")
                    print(f"    Analysis Score: {decision.get('score', 0):.2f}")
                    if decision.get('raw_score'):
                        print(f"    Raw Score: {decision.get('raw_score', 0):.2f} × {decision.get('confidence_multiplier', 1.0):.2f}")
                    if decision.get('triggers'):
                        print(f"    Triggers: {', '.join(decision.get('triggers', [])[:3])}...")  # Show first 3 triggers
                    if decision.get('reason'):
                        print(f"    Reason: {decision['reason'][:100]}...")

                    # Print performance stats
                    performance = day_profile.get_performance_summary()
                    if performance['trades'] > 0:
                        print(f"\n📊 TODAY'S PERFORMANCE:")
                        print(f"    Trades: {performance['trades']} | Win Rate: {performance['win_rate']:.1f}%")
                        print(f"    Total PnL: {performance['daily_pnl']:+.2f}%")
                        print(f"    Best: {performance['best_trade']:+.2f}% | Worst: {performance['worst_trade']:+.2f}%")
                        print(f"    Risk Level: {performance['risk_level']}")

                        # Show consecutive stats
                        if performance['consecutive_wins'] > 0:
                            print(f"    🔥 Consecutive Wins: {performance['consecutive_wins']}")
                        elif performance['consecutive_losses'] > 0:
                            print(f"    ❄️ Consecutive Losses: {performance['consecutive_losses']}")

                    # Session statistics
                    uptime = datetime.now() - session_start_time
                    success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0
                    print(f"\n⏱️ SESSION STATISTICS:")
                    print(f"    Uptime: {str(uptime).split('.')[0]} | Cycles: {total_cycles} (Success: {success_rate:.1f}%)")
                    print(f"    Data Quality: {market_state.data_quality_score:.1f}/10")
                    #print(f"    Firebase: ❌ Disabled")  # Updated status
                    print(f"    Last Update: {market_state.last_update_time.strftime('%H:%M:%S') if market_state.last_update_time else 'Never'}")

                else:
                    failed_cycles += 1
                    logger.error("❌ NIFTY data not available this cycle")
                    print("❌ NIFTY data not available this cycle")

                # Dynamic sleep timing based on market hours and performance
                elapsed = time.time() - cycle_start_time

                if is_market_hours:
                    base_sleep = 100  # 1.67 minutes during market hours for faster response
                    random_delay = random.uniform(-10, 10)  # Smaller randomization
                else:
                    base_sleep = 180  # 3 minutes outside market hours
                    random_delay = random.uniform(-30, 30)  # Larger randomization

                # Adjust sleep based on success rate
                success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 100
                if success_rate < 80:
                    base_sleep *= 1.5  # Sleep longer if having issues
                    logger.warning("⚠️ Reduced success rate detected, increasing cycle interval")

                sleep_time = max(10, base_sleep + random_delay - elapsed)  # Minimum 10 seconds

                print(f"\n⏰ Cycle #{total_cycles} completed in {elapsed:.1f}s.")
                print(f"💤 Sleeping for {sleep_time:.1f}s until next cycle...")
                print("=" * 100)

                # Send periodic status updates to Telegram
                if total_cycles % 30 == 0 and is_market_hours:  # Every 30 cycles during market hours
                    status_msg = f"""📊 CYCLE #{total_cycles} STATUS
⏰ Time: {datetime.now().strftime('%H:%M:%S')}
💹 Spot: ₹{nifty_snapshot.get('underlying_value', 0) if nifty_snapshot else 0:.2f}
📊 Success Rate: {success_rate:.1f}%
🎯 Level: {recommendation_level}
📈 Data Quality: {market_state.data_quality_score:.1f}/10
🔮 Future Prediction: {'Active' if 'future_prediction' in analysis_result else 'Inactive'}"""
                    
                    await send_enhanced_telegram_message(status_msg.strip(), priority="NORMAL")

                # Sleep until next cycle with proper Ctrl+C handling
                try:
                    await asyncio.sleep(sleep_time)
                except asyncio.CancelledError:
                    logger.info("🛑 Sleep cancelled by shutdown signal - exiting immediately")
                    break  # Exit the main loop immediately on Ctrl+C

            except Exception as e:
                failed_cycles += 1
                logger.error("❌ Error occurred in cycle #%d: %s", total_cycles, str(e))
                logger.error("Full traceback: %s", traceback.format_exc())

                # Send error notification to Telegram
                error_msg = f"❌ Error occurred in cycle #{total_cycles}: {str(e)}\n🔄 Continuing in 30 seconds..."
                await send_enhanced_telegram_message(error_msg, priority="HIGH")

                print(f"❌ Error occurred in cycle #{total_cycles}: {str(e)}")
                print("🔄 Continuing in 30 seconds...")
                
                # Handle Ctrl+C during error sleep as well
                try:
                    await asyncio.sleep(30)  # Longer sleep on error
                except asyncio.CancelledError:
                    logger.info("🛑 Error sleep cancelled by shutdown signal")
                    break  # Exit main loop even during error recovery

    except KeyboardInterrupt:
        logger.info("🛑 Received shutdown signal. Cleaning up...")
        
        # Calculate final stats
        uptime = datetime.now() - session_start_time
        success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0
        performance = day_profile.get_performance_summary() if hasattr(day_profile, 'get_performance_summary') else {'trades': 0, 'daily_pnl': 0}
        
        # Final status message
        final_msg = f"""🛑 GOD BOT PRO SHUTDOWN
━━━━━━━━━━━━━━━━━━━
📊 Session Summary:
• Total Cycles: {total_cycles}
• Successful: {successful_cycles} ({success_rate:.1f}%)
• Failed: {failed_cycles}
• Uptime: {str(uptime).split('.')[0]}

💰 Performance:
• Trades: {performance.get('trades', 0)}
• Session PnL: {performance.get('daily_pnl', 0):+.2f}%
• Level Achieved: {engine.get_recommendation_level(market_state)}
• Data Quality: {market_state.data_quality_score:.1f}/10

🎯 Thank you for using God Bot PRO!
━━━━━━━━━━━━━━━━━━━"""
        
        await send_enhanced_telegram_message(final_msg.strip(), priority="HIGH")

    except Exception as e:
        logger.critical("💥 Critical error in main loop: %s", e)
        logger.critical("Full traceback: %s", traceback.format_exc())

        # Critical error notification
        critical_msg = f"""💥 CRITICAL ERROR - BOT STOPPED
━━━━━━━━━━━━━━━━━━━
❌ Error: {str(e)}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Cycles Completed: {total_cycles}

Please check logs and restart manually.
━━━━━━━━━━━━━━━━━━━"""
        
        await send_enhanced_telegram_message(critical_msg.strip(), priority="CRITICAL")
        raise
    
    finally:
        # Graceful shutdown with comprehensive data saving
        logger.info("💾 Initiating graceful shutdown...")
        print("\n💾 Saving session data for continuity...")

        try:
            # Save enhanced market state data
            market_state.save_enhanced_historical_data()
            logger.info("✅ Market state data saved")

            # Save active trade if exists
            if day_profile.active_trade:
                trade_data = {
                    'active_trade': day_profile.active_trade,
                    'trades_today': getattr(day_profile, 'trades_today', []),
                    'daily_pnl': getattr(day_profile, 'daily_pnl', 0),
                    'session_end_time': datetime.now().isoformat(),
                    'risk_level': getattr(day_profile, 'risk_level', 'NORMAL')
                }

                with open(f"NIFTY_active_trades.json", 'w') as f:
                    json.dump(trade_data, f, indent=2, default=str)

                logger.info("💼 Active trade data saved for restoration")
                print(f"💼 Active {day_profile.active_trade['type']} trade saved - will resume on restart")

            # Save final session summary
            session_summary = {
                'session_start': session_start_time.isoformat(),
                'session_end': datetime.now().isoformat(),
                'total_cycles': total_cycles,
                'successful_cycles': successful_cycles,
                'success_rate': (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0,
                'final_data_quality': market_state.data_quality_score,
                'snapshots_collected': len(market_state.market_history),
                'recommendation_level_achieved': engine.get_recommendation_level(market_state),
                'trades_taken': len(getattr(day_profile, 'trades_today', [])),
                'final_pnl': getattr(day_profile, 'daily_pnl', 0),
                'config_weights': config.get('weights', {}),
                #'firebase_enabled': False,  # Updated to False
                'self_analyzer_insights': len(getattr(self_analyzer, 'learning_insights', []))
            }

            with open("session_summary.json", 'w') as f:
                json.dump(session_summary, f, indent=2)

            # Send comprehensive shutdown notification
            uptime = datetime.now() - session_start_time
            success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0
            
            shutdown_msg = f"""🛑 GOD BOT PRO SHUTDOWN
━━━━━━━━━━━━━━━━━━━
⏰ Duration: {str(uptime).split('.')[0]}
🔄 Cycles: {total_cycles} ({successful_cycles} successful)
📊 Success Rate: {success_rate:.1f}%
📈 Snapshots: {len(market_state.market_history)}
🎯 Level: {engine.get_recommendation_level(market_state)}

💰 Performance:
• Trades: {len(getattr(day_profile, 'trades_today', []))}
• Session PnL: {getattr(day_profile, 'daily_pnl', 0):+.2f}%
• Data Quality: {market_state.data_quality_score:.1f}/10

💾 All data saved for next session
#🔥 Firebase: Disabled (Local Storage Only)
━━━━━━━━━━━━━━━━━━━
✅ Ready for restart anytime!"""
            
            await send_enhanced_telegram_message(shutdown_msg.strip(), priority="HIGH")

            print("✅ Session data saved successfully.")
            print("📊 Session Summary:")
            print(f"    Duration: {str(uptime).split('.')[0]}")
            print(f"    Cycles: {total_cycles} ({successful_cycles} successful)")
            print(f"    Snapshots: {len(market_state.market_history)}")
            print(f"    Level Achieved: {engine.get_recommendation_level(market_state)}")
            #print(f"    Firebase: ❌ Disabled")
            if len(getattr(day_profile, 'trades_today', [])) > 0:
                print(f"    Trades: {len(day_profile.trades_today)} (PnL: {day_profile.daily_pnl:+.2f}%)")

        except Exception as e:
            logger.error("❌ Error during shutdown: %s", e)
            print(f"⚠️ Error saving session data: {e}")

        logger.info("✅ Graceful shutdown complete")
        print("\n🛑 God Bot PRO stopped gracefully. All data preserved for next session.")


# =============================================================================
# ENHANCED MARKET DAY PROFILE CLASS (WITH REQUIRED INIT ARGUMENTS)
# =============================================================================
class EnhancedMarketDayProfile:
    """Enhanced daily market profile with advanced trade tracking and performance analytics."""

    def __init__(self, index_name: str, config: Dict[str, Any]):
        """Initialize with required index_name and config arguments."""
        self.index_name = index_name
        self.config = config

        self.active_trade = None
        self.trades_today = []
        self.cooldown_cycles = 0
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.consecutive_wins = 0
        self.last_trade_time = None
        self.risk_level = "NORMAL"  # NORMAL, REDUCED, HIGH

        # Enhanced tracking
        self.session_start = datetime.now()
        self.total_signals_generated = 0
        self.signals_accuracy = {"correct": 0, "incorrect": 0}
        self.hourly_performance = {}

        logger.info("📊 Enhanced Market Day Profile initialized for %s", index_name)

    def update(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        '''Update market state with new snapshot and return analysis INCLUDING time window intelligence.'''
        import time
        start_time = time.time()
        
        try:
            # Add timestamp if not present (existing)
            if 'timestamp' not in snapshot_data:
                snapshot_data['timestamp'] = datetime.now().isoformat()
            
            # Update current state (existing)
            self.last_spot_price = snapshot_data.get('underlying_value', self.last_spot_price)
            self.last_update_time = datetime.now()
            
            # Add to history (existing)
            self.market_history.append(snapshot_data)
            
            # Calculate deltas (existing)
            if len(self.market_history) >= 2:
                self._calculate_deltas()
            
            # NEW: Time window analysis integration
            time_window_result = process_time_window_analysis(snapshot_data, self.time_window_state)
            self.time_window_analysis = time_window_result
            self.current_time_window = time_window_result.get('phase', 'unknown')
            
            # Log time window intelligence
            window_action = time_window_result.get('action', 'NONE')
            trade_signal = time_window_result.get('trade_signal', 'NONE')
            
            logger.info(f"🕐 Current Time Window: {self.current_time_window}")
            logger.info(f"📊 Window Analysis: {json.dumps(self.time_window_analysis, indent=2)}")
            
            # Print detailed time window intelligence
            logger.info(f"🕐 Time Window: {self.current_time_window}")
            logger.info(f"📊 Window Action: {window_action} | Signal: {trade_signal}")
            
            # ADDED: Print 3-9 minute timeframe data storage
            try:
                if hasattr(market_state, 'market_history') and len(market_state.market_history) > 0:
                    recent_data = list(market_state.market_history)[-10:]  # Last 10 snapshots
                    logger.info("📈 3-9 Minute Timeframe Data Storage:")
                    for i, snapshot in enumerate(recent_data):
                        timestamp = snapshot.get('timestamp', 'N/A')
                        underlying = snapshot.get('underlying_value', 0)
                        oi_pcr = snapshot.get('OI_PCR', 0)
                        vol_pcr = snapshot.get('VOL_PCR', 0)
                        logger.info(f"  [{i+1}] {timestamp} | Underlying: {underlying} | OI_PCR: {oi_pcr:.3f} | VOL_PCR: {vol_pcr:.3f}")
                        
                    # Print time window specific data if available
                    if self.time_window_analysis:
                        window_data = self.time_window_analysis.get('analysis', {})
                        if window_data:
                            logger.info(f"🔍 Time Window Specific Analysis: {json.dumps(window_data, indent=2)}")
                else:
                    logger.info("📈 3-9 Minute Timeframe Data: No historical data available yet")
            except Exception as e:
                logger.error(f"❌ Error printing timeframe data: {e}")
            
            # Add time window data to snapshot
            snapshot_data['time_window_analysis'] = time_window_result
            snapshot_data['current_time_window'] = self.current_time_window
            
            # Update performance metrics (existing)
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            self.analysis_count += 1
            
            # Calculate data quality score (existing)
            self._update_data_quality_score(snapshot_data)
            
            logger.info(f"🔄 Market state updated for {self.symbol}")
            logger.info(f"📊 History: {len(self.market_history)} snapshots, Quality: {self.data_quality_score}/10")
            
            return snapshot_data
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ Error updating market state for {self.symbol}: {e}")
            return {}

    def get_win_rate(self) -> float:
        """Calculate current win rate."""
        if not self.trades_today:
            return 0.0

        wins = sum(1 for trade in self.trades_today if trade.get("pnl", 0) > 0)
        return (wins / len(self.trades_today)) * 100

    def get_performance_summary(self) -> Dict[str, Any]:
        """Generate comprehensive performance summary."""
        if not self.trades_today:
            return {
                "trades": 0, "win_rate": 0.0, "daily_pnl": 0.0,
                "best_trade": 0.0, "worst_trade": 0.0,
                "avg_win": 0.0, "avg_loss": 0.0,
                "consecutive_wins": self.consecutive_wins,
                "consecutive_losses": self.consecutive_losses,
                "risk_level": self.risk_level
            }

        wins = [t["pnl"] for t in self.trades_today if t.get("pnl", 0) > 0]
        losses = [t["pnl"] for t in self.trades_today if t.get("pnl", 0) <= 0]

        return {
            "trades": len(self.trades_today),
            "win_rate": self.get_win_rate(),
            "daily_pnl": self.daily_pnl,
            "best_trade": max(wins) if wins else 0.0,
            "worst_trade": min(losses) if losses else 0.0,
            "avg_win": np.mean(wins) if wins else 0.0,
            "avg_loss": np.mean(losses) if losses else 0.0,
            "consecutive_wins": self.consecutive_wins,
            "consecutive_losses": self.consecutive_losses,
            "risk_level": self.risk_level
        }
        
    def main():
        print("Starting AI Trading Bot with agents integration...")
        # Initialize AgentEngine after class definitions
        engine = AgentEngine("AGENTS.md")
        print("Successfully loaded AGENTS.md configuration")
        
        # Initialize other components AFTER class definitions
        time_window = EnhancedTimeWindowState()
        tf_analyzer = MultiTimeframeAnalyzer()
        candle_sys = CandleIntelligenceSystem()
        self_analyzer = EnhancedSmartSelfAnalyzer()
        commentary_bot = SmartLiveCommentaryBot(config={"telegram": {}})
        
        # Proceed with your main logic
        # e.g., call your trading functions, start loops, etc.
        # ...
        print("All components initialized successfully!")
    # Add this function before the run_bot() function

# =============================================================================
# FIXED: display_15_timeframe_table function
# =============================================================================
def display_15_timeframe_table(timeframe_analysis: Dict[str, Any]) -> None:
    """Display the 15-timeframe analysis results in a table format."""
    print("\n📊 15-TIMEFRAME ANALYSIS TABLE")
    print("=" * 120)
    
    # Extract the timeframe data
    timeframe_data = timeframe_analysis.get('changes', {})
    
    # If no changes data, try to get it from the MultiTimeframeAnalyzer
    if not timeframe_data and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
        analyzer = MultiTimeframeAnalyzer()
        if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
            timeframe_data = analyzer.last_analysis_results.get('changes', {})
    
    # Count completed timeframes
    completed_count = sum(1 for data in timeframe_data.values() if data.get('status') == 'COMPLETED')
    
    # Print the table header
    print(f"{'TF':<5} {'Status':<12} {'Price Δ':<9} {'%Δ':<9} {'CE OI Δ':<12} {'PE OI Δ':<12} {'Momentum':<12} {'Strength':<10}")
    print("-" * 120)
    
    # List of all timeframes we want to display
    all_timeframes = [3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90]
    
    for timeframe in all_timeframes:
        # Get the data for this timeframe
        data = timeframe_data.get(timeframe, {})
        
        if data and data.get('status') == 'COMPLETED':
            # Extract values with defaults
            price_delta = data.get('spot_change', 0.0)
            price_pct = data.get('spot_change_pct', 0.0)
            ce_oi_delta = data.get('ce_oi_change', 0)
            pe_oi_delta = data.get('pe_oi_change', 0)
            momentum = data.get('momentum', 'UNKNOWN')
            strength = data.get('strength_score', 0.0)
            
            # Format momentum with icon
            momentum_icon = "🟢" if momentum == "BULLISH" else "🔴" if momentum == "BEARISH" else "🟡"
            
            print(f"{timeframe:<5} ✅ COMPLETED | {price_delta:+6.2f} | {price_pct:+6.3f}% | "
                  f"{ce_oi_delta:+9,} | {pe_oi_delta:+9,} | {momentum_icon} {momentum:<8} | {strength:6.2f}/10")
        else:
            print(f"{timeframe:<5} ⏳ PENDING    | {'--':>7} | {'--':>8} | {'--':>11} | {'--':>11} | --           | --")
    
    print("-" * 120)
    
    # Log summary
    logger.info(f"📊 15-Timeframe Analysis Summary: {completed_count} Completed, {15-completed_count} Pending")
    
    if completed_count == 0:
        logger.warning(f"⚠️  No timeframes completed — waiting for sufficient market data")
# ============================================================================= 
# SAFETY WRAPPER FOR TIMEFRAME TABLE CALL (to prevent NameError crashes)
# ============================================================================= 
def safe_display_15_timeframe_table(timeframe_analysis):
    """
    Safe wrapper to avoid NameError or runtime crashes.
    """
    try:
        if 'display_15_timeframe_table' in globals():
            display_15_timeframe_table(timeframe_analysis)
        else:
            logger.warning("⚠️ display_15_timeframe_table function not found in global scope")
    except Exception as e:
        logger.error(f"⚠️ Safe display wrapper failed: {e}")
# =============================================================================
# 🔔 5-MINUTE CANDLE COMPLETED INTELLIGENCE REPORT
# =============================================================================
from collections import deque
from typing import Dict, Any

# Store last N five-minute candles
five_minute_candles: deque[Dict[str, Any]] = deque(maxlen=100)

class FiveMinuteCandle:
    def __init__(self, start_time, open_price):
        self.start_time = start_time
        self.open = open_price
        self.high = open_price
        self.low = open_price
        self.close = open_price
        self.ce_oi_start = None
        self.pe_oi_start = None
        self.ce_vol_start = None
        self.pe_vol_start = None

    def update(self, snapshot: Dict[str, Any]):
        price = snapshot['underlying_value']
        self.high = max(self.high, price)
        self.low = min(self.low, price)
        self.close = price

        # Initialize OI/vol at candle start
        if self.ce_oi_start is None:
            self.ce_oi_start = snapshot['CE_OI']
            self.pe_oi_start = snapshot['PE_OI']
            self.ce_vol_start = snapshot['CE_VOL']
            self.pe_vol_start = snapshot['PE_VOL']

    def finalize(self, snapshot: Dict[str, Any]):
        return {
            'start_time': self.start_time,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'delta_CE_OI': snapshot['CE_OI'] - self.ce_oi_start,
            'delta_PE_OI': snapshot['PE_OI'] - self.pe_oi_start,
            'delta_CE_VOL': snapshot['CE_VOL'] - self.ce_vol_start,
            'delta_PE_VOL': snapshot['PE_VOL'] - self.pe_vol_start,
        }

    def print_candle_completed_intel(candle_result: dict, snapshot_data: dict, prev_snapshot: dict):
        """
        ✅ Prints a rich intelligence report when a 5-minute candle completes.
        Shows OI/Vol changes, pattern, support/resistance, and reasoning.
        """
        if candle_result.get('status') != 'CANDLE_COMPLETED':
            return

        c = candle_result['candle_data']
        pattern = candle_result['pattern_analysis']
        trade = candle_result['trade_recommendation']

        open_price = c['open']
        close_price = c['close']
        high_price = c['high']
        low_price = c['low']
        body = abs(close_price - open_price)
        change_pct = (close_price - open_price) / open_price * 100 if open_price else 0

        # OI & Vol Changes
        ce_oi_now = snapshot_data['CE_OI']
        ce_oi_prev = prev_snapshot['CE_OI']
        pe_oi_now = snapshot_data['PE_OI']
        pe_oi_prev = prev_snapshot['PE_OI']
        ce_vol_now = snapshot_data['CE_VOL']
        ce_vol_prev = prev_snapshot['CE_VOL']
        pe_vol_now = snapshot_data['PE_VOL']
        pe_vol_prev = prev_snapshot['PE_VOL']

        ce_oi_change = ce_oi_now - ce_oi_prev
        pe_oi_change = pe_oi_now - pe_oi_prev
        ce_vol_change = ce_vol_now - ce_vol_prev
        pe_vol_change = pe_vol_now - pe_vol_prev

        # Support/Resistance (adjust as needed)
        support = 24550
        resistance = 24600
        spot = close_price
        near_support = abs(spot - support) < 30
        near_resistance = abs(spot - resistance) < 30

        # Candle Type
        total_range = high_price - low_price + 1e-9
        if body / total_range > 0.7:
            candle_type = "🟢 BULLISH_MARUBOZU" if close_price > open_price else "🔴 BEARISH_MARUBOZU"
        elif body < 10:
            candle_type = "🟡 DOJI"
        else:
            candle_type = "🟢 BULLISH_CANDLE" if close_price > open_price else "🔴 BEARISH_CANDLE"

        # Reasons
        reasons = []
        if ce_oi_change > 5000 and ce_vol_change > 100000:
            reasons.append("🚀 CE OI & Volume Surge → Institutional Buying")
        if pe_oi_change > 5000 and pe_vol_change > 100000:
            reasons.append("🛡️ PE OI & Volume Surge → Hedging/Protection")
        if ce_oi_change < -5000 and ce_vol_change > 50000:
            reasons.append("💥 CE Unwinding + High Volume → Longs Exiting")
        if pe_oi_change < -5000 and pe_vol_change > 50000:
            reasons.append("📉 PE Unwinding + High Volume → Shorts Covering")

        # Final Verdict
        verdict = ""
        if "Institutional Buying" in "".join(reasons) and near_support:
            verdict = "✅ STRONG BULLISH SIGNAL: Demand at Support"
        elif "Hedging/Protection" in "".join(reasons) and near_resistance:
            verdict = "✅ STRONG BEARISH SIGNAL: Supply at Resistance"
        elif close_price > open_price:
            verdict = "📈 Bullish: Price Up Despite No Clear Signal"
        else:
            verdict = "📉 Bearish: Weakness Detected"

        # Print Report
        print("\n" + "🔥" * 60)
        print("🕯️ 5-MINUTE CANDLE COMPLETED – INTELLIGENCE REPORT")
        print("🔥" * 60)
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💹 Price: ₹{open_price:.2f} → ₹{close_price:.2f} ({change_pct:+.3f}%)")
        print(f"📊 OHLC: O={open_price:.2f} H={high_price:.2f} L={low_price:.2f} C={close_price:.2f}")
        print(f"🕯️  Body: {body:.2f} | Upper Wick: {high_price - max(open_price, close_price):.2f} | Lower Wick: {min(open_price, close_price) - low_price:.2f}")
        print(f"📈 Volume: CE Δ{ce_vol_change:+,} | PE Δ{pe_vol_change:+,}")
        print(f"🎯 OI: CE Δ{ce_oi_change:+,} | PE Δ{pe_oi_change:+,}")
        level_context = ("🟢 Near Support (₹{support})" if near_support else
                        "🔴 Near Resistance (₹{resistance})" if near_resistance else
                        "⚪ Mid-Zone")
        print(f"📍 Level Context: {level_context}")
        print(f"🕯️  Candle Type: {candle_type}")
        print(f"🔍 Pattern: {pattern.get('pattern', 'None')} ({pattern.get('confidence', 0):.0%} confidence)")
        print("💡 Key Reasons:")
        for reason in reasons:
            print(f"   → {reason}")
        print(f"🎯 Final Verdict: {verdict}")
        print("🔥" * 60)
    def print_5min_candle_data_summary(market_state: 'EnhancedMarketState') -> None:
        """Print comprehensive 5-minute candle data with volume and OI information."""
        
        print("\n" + "="*140)
        print("✅ 5-MINUTES TIMEFRAME DATA DISPLAY COMPLETE CANDLES")
        print("="*140)

        # Get current snapshot data for display
        current_snapshot = market_state.market_history[-1] if market_state.market_history else {}
        current_time = datetime.now()
        
        # Define 5-minute timeframes (15 intervals of 5 minutes each)
        timeframes = ["5min", "10min", "15min", "20min", "25min", "30min", "35min", "40min", 
                    "45min", "50min", "55min", "60min", "65min", "70min", "75min"]
        
        print(f"\n📊 5-MINUTE CANDLE INTELLIGENCE SUMMARY:")
        print("─" * 140)
        print(f"{'Time':>8} | {'Status':>12} | {'Candle':>20} | {'CE OI':>12} | {'CE Vol':>12} | {'PE OI':>12} | {'PE Vol':>12} | {'Strength':>10}")
        print("─" * 140)
        
        # Get candle system data if available
        candle_count = 0
        building_candle = None
        completed_candles = []
        
        if CANDLE_SYSTEM_ACTIVE and candle_system is not None:
            if hasattr(candle_system, 'completed_candles'):
                completed_candles = list(candle_system.completed_candles)
                candle_count = len(completed_candles)
            if hasattr(candle_system, 'building_candle'):
                building_candle = candle_system.building_candle
        
        # Display each timeframe
        for i, timeframe in enumerate(timeframes):
            if i < candle_count:
                # Completed candle
                candle = completed_candles[i]
                status = "✅ COMPLETED"
                candle_type = getattr(candle, 'pattern_type', 'NONE')
                ce_oi = f"{getattr(candle, 'ce_oi', 0):,}"
                ce_vol = f"{getattr(candle, 'ce_volume', 0):,}"
                pe_oi = f"{getattr(candle, 'pe_oi', 0):,}"
                pe_vol = f"{getattr(candle, 'pe_volume', 0):,}"
                strength = f"{getattr(candle, 'pattern_strength', 0):.2f}/10"
                
            elif i == candle_count and building_candle:
                # Currently building candle
                status = "🔄 BUILDING"
                candle_type = "FORMING"
                ce_oi = f"{getattr(building_candle, 'ce_oi', current_snapshot.get('CE_OI', 0)):,}"
                ce_vol = f"{getattr(building_candle, 'ce_volume', current_snapshot.get('CE_VOL', 0)):,}"
                pe_oi = f"{getattr(building_candle, 'pe_oi', current_snapshot.get('PE_OI', 0)):,}"
                pe_vol = f"{getattr(building_candle, 'pe_volume', current_snapshot.get('PE_VOL', 0)):,}"
                strength = "Building..."
                
            else:
                # Pending candle
                status = "⏳ PENDING"
                candle_type = "WAITING"
                ce_oi = "0"
                ce_vol = "0"
                pe_oi = "0"
                pe_vol = "0"
                strength = "0.00/10"
            
            print(f"{timeframe:>8} | {status:>12} | {candle_type:>20} | {ce_oi:>12} | {ce_vol:>12} | {pe_oi:>12} | {pe_vol:>12} | {strength:>10}")
            
        print("─" * 140)
        
        # Summary information
        candle_status = "UNKNOWN"
        if hasattr(market_state, 'current_analysis') and market_state.current_analysis:
            candle_intelligence = market_state.current_analysis.get('candle_intelligence', {})
            if candle_intelligence:
                candle_status = candle_intelligence.get('status', 'UNKNOWN')
        
        print(f"\n📊 CANDLE ANALYSIS SUMMARY:")
        print("─" * 80)
        print(f" 🕯️ Completed Candles: {candle_count}/15")
        print(f" 📊 Current Status: {candle_status}")
        print(f" ⏰ Analysis Time: {current_time.strftime('%H:%M:%S')}")
        print(f" 🎯 System Active: {'✅ YES' if CANDLE_SYSTEM_ACTIVE else '❌ NO'}")
        print(f" 💹 Current Spot: ₹{current_snapshot.get('underlying_value', 0):.2f}")
        print("="*140)
        print("✅ 5-MINUTES TIMEFRAME DATA DISPLAY COMPLETE")
        print("="*140)

# =============================================================================
# SCRIPT ENTRY POINT - COMPLETE FIXED VERSION WITH 15-TIMEFRAME INTEGRATION + CANDLE INTELLIGENCE
# =============================================================================

# Define global variables at module level (outside any function)
session_start_time = datetime.now()
total_cycles = 0
successful_cycles = 0
failed_cycles = 0

if __name__ == "__main__":
    import sys
    import asyncio
    import signal
    import traceback
    from datetime import datetime, time as dt_time
    from fifteen_min_predictor import FifteenMinPredictor
    # Enhanced import for telegram messaging
# =============================================================================
# 🤖 SELF-HEALING MONITOR
# =============================================================================
class SelfHealingMonitor:
    def __init__(self):
        self.error_log = []
    async def handle_error(self, error_msg: str, cycle: int):
        known_fixes = {
            "name 'display_15_timeframe_table' is not defined": self.fix_display_table,
            "EnhancedMarketState not defined": self.fix_market_state
        }
        for key, fix_func in known_fixes.items():
            if key in error_msg:
                logger.warning(f"🚨 AUTO-FIXING: {key}")
                fix_func()
                send_telegram(f"🛠️ <b>SELF-HEALING SUCCESS</b>\nFixed: <code>{key[:50]}...</code>\nCycle: {cycle}")
                return True
        return False
    def fix_display_table(self):
        global display_15_timeframe_table
        exec("""
def display_15_timeframe_table(timeframe_analysis):
    print('\\n📊 15-TIMEFRAME ANALYSIS TABLE')
    for tf, data in timeframe_analysis.items():
        status = data.get('status', 'PENDING')
        print(f"{tf}: {status}")
""")
        with open(__file__, "r+", encoding="utf-8") as f:
            content = f.read()
            if "def display_15_timeframe_table" not in content:
                f.seek(0, 0)
                f.write(exec.__code__.co_consts[0] + "\\n\\n" + content)
    def fix_market_state(self):
        global EnhancedMarketState
        exec("""
class EnhancedMarketState:
    def __init__(self, symbol, config):
        self.symbol = symbol
        self.config = config
        self.market_history = []
""")
        globals()['EnhancedMarketState'] = EnhancedMarketState
    import requests
    # ==================== PATCH START ====================
    
    # FIX 1: Create default config if loading fails
    def load_config():
        """Load configuration or return default config."""
        try:
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            logger.info("✅ Configuration loaded from config.yaml")
            return config
        except Exception as e:
            logger.warning(f"⚠️ Could not load config.yaml: {e}. Using default configuration.")
            # Default configuration
            return {
                'symbol': 'NIFTY',
                'model_path': 'models/enhanced_bot_model.pkl',
                'data_path': 'data/training_data.csv',
                'telegram': {
                    'token': '',
                    'chat_id': ''
                },
                'time_window_analysis': {
                    'enabled': True,
                    'use_research_probabilities': True,
                    'golden_window_focus': True,
                    'avoid_lunch_trading': True,
                    'minute_level_analysis': True,
                    'volume_oi_integration': True
                },
                'ai_integration': {
                    'enabled': True,
                    'confidence_threshold': 0.7,
                    'learning_rate': 0.01
                }
            }
    
    # FIX 2: Define CANDLE_SYSTEM_ACTIVE before use
    CANDLE_SYSTEM_ACTIVE = False
    candle_system = None
    try:
        candle_system = CandleIntelligenceSystem()
        CANDLE_SYSTEM_ACTIVE = True
        logger.info("✅ Candle Intelligence System initialized")
    except Exception as e:
        logger.error(f"❌ Candle Intelligence System init failed: {e}")
        candle_system = None
        CANDLE_SYSTEM_ACTIVE = False
    
    # Add missing functions
    def display_15_timeframe_table(timeframe_analysis):
        """Display 15-timeframe analysis results in a table format."""
        print("\n" + "="*100)
        print("📊 15-TIMEFRAME ANALYSIS TABLE")
        print("="*100)
        
        if not timeframe_analysis:
            print("⚠️ No timeframe analysis data available")
            print("="*100)
            return
        
        # Print header
        print(f"{'Timeframe':<12} {'Price Change':<15} {'CE OI Change':<15} {'PE OI Change':<15} {'Momentum':<12} {'Strength':<10}")
        print("-" * 100)
        
        # Print data for each timeframe
        for timeframe, data in timeframe_analysis.items():
            if isinstance(data, dict) and 'spot_change' in data:
                spot_change = f"{data['spot_change']:+.2f}"
                ce_oi_change = f"{data['ce_oi_change']:+,}"
                pe_oi_change = f"{data['pe_oi_change']:+,}"
                momentum = data['momentum']
                strength = f"{data['strength_score']:.1f}/10"
                
                print(f"{timeframe:<12} {spot_change:<15} {ce_oi_change:<15} {pe_oi_change:<15} {momentum:<12} {strength:<10}")
        
        print("="*100)

    def print_all_15_timeframes_data(market_state):
        """Print all 15 timeframes data for diagnosis."""
        print("\n" + "="*100)
        print("📊 COMPLETE 15-TIMEFRAMES DATA")
        print("="*100)
        
        if not hasattr(market_state, 'current_analysis') or 'timeframe_analysis' not in market_state.current_analysis:
            print("⚠️ No timeframe analysis data available")
            print("="*100)
            return
        
        tf_analysis = market_state.current_analysis['timeframe_analysis']
        
        if not tf_analysis:
            print("⚠️ Timeframe analysis data is empty")
            print("="*100)
            return
        
        # Print summary
        print(f"📈 Market history snapshots: {len(market_state.market_history)}")
        print(f"🔍 Available timeframes: {list(tf_analysis.keys())}")
        print()
        
        # Print data for each timeframe
        for timeframe, data in tf_analysis.items():
            if isinstance(data, dict) and 'spot_change' in data:
                print(f"⏰ {timeframe.upper()} TIMEFRAME:")
                print(f"   💹 Price: {data['spot_change']:+.2f} ({data['spot_change_pct']:+.4f}%)")
                print(f"   📈 CE OI: {data['ce_oi_change']:+,} ({data['ce_oi_change_pct']:+.2f}%)")
                print(f"   📉 PE OI: {data['pe_oi_change']:+,} ({data['pe_oi_change_pct']:+.2f}%)")
                print(f"   🚀 Momentum: {data['momentum']}")
                print(f"   📊 Strength: {data['strength_score']:.2f}/10")
                print()
        
        print("="*100)

    def print_timeframe_data_summary(market_state: 'EnhancedMarketState') -> None:
        """Print a condensed summary of timeframe data for quick viewing."""
        
        if not hasattr(market_state, 'current_analysis') or 'timeframe_analysis' not in market_state.current_analysis:
            print("⚠️  No timeframe data available for summary.")
            return
        
        tf_analysis = market_state.current_analysis['timeframe_analysis']
        
        print(f"\n📊 QUICK 15-TIMEFRAME SUMMARY:")
        print("─" * 90)
        
        # Define timeframes in order
        all_timeframes = ["3min", "9min", "15min", "21min", "25min", "30min", "33min", "39min", 
                        "45min", "50min", "55min", "60min", "65min", "75min", "90min"]
        
        # Show active timeframes
        for timeframe in all_timeframes:
            if timeframe in tf_analysis:
                data = tf_analysis[timeframe]
                momentum = data.get('momentum', 'N/A')
                strength = data.get('strength_score', 0)
                price_pct = data.get('spot_change_pct', data.get('price_change_pct', 0))
                
                # Color coding based on momentum
                momentum_symbol = "🟢" if "BULLISH" in momentum else "🔴" if "BEARISH" in momentum else "⚪"
                
                print(f"{momentum_symbol} {timeframe:>8}: {price_pct:+6.2f}% | {momentum:>15} | Strength: {strength:>4.1f}/10")
            else:
                print(f"⏳ {timeframe:>8}: ⏳ PENDING | {'WAITING':>15} | Strength: {'0.0':>4}/10")
        
        print("─" * 90)

    def print_all_15_timeframes_data(market_state: 'EnhancedMarketState') -> None:
        """Print ALL 15 timeframes data in organized format with complete details."""
        
        print("\n" + "="*140)
        print("🕐 COMPLETE 15-TIMEFRAME DATA STORAGE ANALYSIS")
        print("="*140)
        
        # FIXED: Get timeframe data properly
        timeframe_analysis = {}
        
        # Try to get timeframe analysis from current_analysis
        if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
            timeframe_analysis = market_state.current_analysis['timeframe_analysis']
        
        # If still empty, try to get it from the MultiTimeframeAnalyzer
        if not timeframe_analysis and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
            analyzer = MultiTimeframeAnalyzer()
            if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
                timeframe_analysis = analyzer.last_analysis_results
        
        if not timeframe_analysis:
            print("⚠️  Timeframe analysis not available yet.")
            print(f"📊 Current snapshots: {len(market_state.market_history)}")
            print("🔄 Building data foundation...")
            print("="*140)
            return
        
        # Extract the timeframe data
        timeframe_data = timeframe_analysis.get('changes', {})
        
        print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Total Snapshots: {len(market_state.market_history)}")
        
        # Count completed timeframes
        completed_count = sum(1 for data in timeframe_data.values() if data.get('status') == 'COMPLETED')
        print(f"🎯 Timeframes Active: {completed_count}/15")
        
        # Define all 15 expected timeframes in order
        all_timeframes = [3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90]
        
        # SECTION 1: COMPREHENSIVE OVERVIEW TABLE
        print(f"\n📋 15-TIMEFRAME OVERVIEW TABLE:")
        print("-" * 140)
        print(f"{'Timeframe':>10} | {'Status':>12} | {'Price Δ':>8} | {'Price %':>8} | {'CE OI Δ':>10} | {'PE OI Δ':>10} | {'Momentum':>15} | {'Strength':>8}")
        print("-" * 140)
        
        for timeframe in all_timeframes:
            # Get the data for this timeframe
            data = timeframe_data.get(timeframe, {})
            
            if data and data.get('status') == 'COMPLETED':
                # Extract values with defaults
                price_delta = data.get('spot_change', 0.0)
                price_pct = data.get('spot_change_pct', 0.0)
                ce_oi = data.get('ce_oi_change', 0)
                pe_oi = data.get('pe_oi_change', 0)
                momentum = data.get('momentum', 'N/A')
                strength = data.get('strength_score', 0)
                status = "✅ COMPLETED"
            else:
                # Default values for pending timeframes
                price_delta = 0.0
                price_pct = 0.0
                ce_oi = 0
                pe_oi = 0
                momentum = 'WAITING'
                strength = 0.0
                status = "⏳ PENDING"
                
            print(f"{str(timeframe)+'min':>10} | {status:>12} | {price_delta:+8.2f} | {price_pct:+7.3f}% | {ce_oi:+10,} | {pe_oi:+10,} | {momentum:>15} | {strength:>6.2f}/10")
        
        print("-" * 140)
        
        # SECTION 2: PENDING TIMEFRAMES
        pending_timeframes = [tf for tf in all_timeframes if tf not in timeframe_data or timeframe_data.get(tf, {}).get('status') != 'COMPLETED']
        
        if pending_timeframes:
            print(f"\n⏳ PENDING TIMEFRAMES ({len(pending_timeframes)}/15):")
            print("─" * 80)
            for tf in pending_timeframes:
                # Calculate how many more snapshots are needed
                snapshots_needed = tf - len(market_state.market_history)
                if snapshots_needed < 0:
                    needed_str = "Ready (data available)"
                else:
                    needed_str = f"Need +{snapshots_needed} more snapshots"
                print(f"      {tf}min: {needed_str}")
            print("─" * 80)
        
        # SECTION 3: SUMMARY STATISTICS
        print(f"\n📊 ANALYSIS SUMMARY:")
        print("─" * 80)
        print(f"  🎯 Active Timeframes: {completed_count}/15 ({completed_count/15*100:.1f}%)")
        print(f"  📈 Total Snapshots: {len(market_state.market_history)}")
        print(f"  ⏰ Analysis Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"  🎯 Data Quality: {market_state.data_quality_score:.1f}/10")
        print("="*140)
        print("✅ 15-TIMEFRAME DATA DISPLAY COMPLETE")
        print("="*140)
    
# =============================================================================
# FIXED: Recommendation system with proper error handling
# =============================================================================
def generate_trading_recommendation(market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """Generate trading recommendation based on timeframe analysis."""
    try:
        # Get timeframe analysis
        timeframe_analysis = {}
        
        if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
            timeframe_analysis = market_state.current_analysis['timeframe_analysis']
        
        # If still empty, try to get it from the MultiTimeframeAnalyzer
        if not timeframe_analysis and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
            analyzer = MultiTimeframeAnalyzer()
            if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
                timeframe_analysis = analyzer.last_analysis_results
        
        # FIXED: Ensure timeframe_analysis is a dictionary
        if not isinstance(timeframe_analysis, dict):
            logger.warning("⚠️ Timeframe analysis is not a dictionary, using default values")
            timeframe_analysis = {}
        
        # Extract timeframe data
        timeframe_data = timeframe_analysis.get('changes', {})
        
        # Count market states
        bullish_count = 0
        bearish_count = 0
        sideways_count = 0
        total_strength = 0
        valid_timeframes = 0
        
        for data in timeframe_data.values():
            if data.get('status') == 'COMPLETED':
                momentum = data.get('momentum', '')
                if 'BULLISH' in momentum:
                    bullish_count += 1
                elif 'BEARISH' in momentum:
                    bearish_count += 1
                else:
                    sideways_count += 1
                
                strength = data.get('strength_score', 0)
                total_strength += strength
                valid_timeframes += 1
        
        # Determine overall market state
        if valid_timeframes == 0:
            market_state_str = "INSUFFICIENT_DATA"
            recommendation = "⏳ Building foundation for 9:30 AM first recommendation"
            confidence = "BUILDING"
        elif bullish_count > bearish_count and bullish_count > sideways_count:
            market_state_str = "BULLISH"
            recommendation = "🟢 Consider BUY positions"
            confidence = "HIGH" if bullish_count > bearish_count * 1.5 else "MEDIUM"
        elif bearish_count > bullish_count and bearish_count > sideways_count:
            market_state_str = "BEARISH"
            recommendation = "🔴 Consider SELL positions"
            confidence = "HIGH" if bearish_count > bullish_count * 1.5 else "MEDIUM"
        else:
            market_state_str = "SIDEWAYS"
            recommendation = "⚪ Range trading opportunities"
            confidence = "MEDIUM"
        
        # Calculate average strength
        avg_strength = total_strength / valid_timeframes if valid_timeframes > 0 else 0
        
        return {
            'status': 'PRE_RECOMMENDATION' if valid_timeframes < 5 else 'RECOMMENDATION',
            'recommendation': recommendation,
            'confidence': confidence,
            'market_state': market_state_str,
            'reason': f"Snapshots: {len(market_state.market_history)} | Active timeframes: {valid_timeframes}",
            'strength_score': avg_strength,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'sideways_count': sideways_count
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating trading recommendation: {e}")
        return {
            'status': 'ERROR',
            'recommendation': '⚠️ Error generating recommendation',
            'confidence': 'LOW',
            'market_state': 'UNKNOWN',
            'reason': f'Error: {str(e)}',
            'strength_score': 0,
            'bullish_count': 0,
            'bearish_count': 0,
            'sideways_count': 0
        }
    def print_candle_intelligence_output(candle_analysis_result):
        """Print candle intelligence output with proper formatting."""
        print("\n" + "="*80)
        print("🕯️ CANDLE INTELLIGENCE OUTPUT")
        print("="*80)
        
        if not candle_analysis_result:
            print("⚠️ No candle analysis data available")
            print("="*80)
            return
        
        status = candle_analysis_result.get('status', 'UNKNOWN')
        print(f"📊 Status: {status}")
        
        if status == 'CANDLE_COMPLETED':
            candle_num = candle_analysis_result.get('candle_number', 0)
            timestamp = candle_analysis_result.get('timestamp', 'N/A')
            pattern = candle_analysis_result.get('pattern_analysis', {}).get('pattern', 'NONE')
            confidence = candle_analysis_result.get('pattern_analysis', {}).get('confidence', 0)
            trade_rec = candle_analysis_result.get('trade_recommendation', {})
            
            print(f"🕯️ Candle #{candle_num} Completed at {timestamp}")
            print(f"🎯 Pattern: {pattern} ({confidence:.0%})")
            print(f"📊 Recommendation: {trade_rec.get('action', 'WAIT')} ({trade_rec.get('confidence', 0):.0%})")
            print(f"💡 Reasoning: {trade_rec.get('reasoning', 'N/A')}")
            
        elif status == 'BUILDING_CANDLE':
            progress = candle_analysis_result.get('candle_progress', 'N/A')
            print(f"🔄 Building Candle: {progress}")
            
            # Print building candle details if available
            building_candle = candle_analysis_result.get('building_candle', {})
            if building_candle:
                print(f"💹 Live Price: ₹{building_candle.get('close_price', 0):.2f}")
                print(f"📊 OHLC: O={building_candle.get('open_price', 0):.2f} H={building_candle.get('high_price', 0):.2f} L={building_candle.get('low_price', 0):.2f}")
        
        else:
            print(f"⚠️ Unknown status: {status}")
        
        print("="*80)

# ==================== PATCH END ====================
# =============================================================================
# GLOBAL VARIABLES AND MISSING FUNCTIONS
# =============================================================================

# Initialize global variables
session_start_time = datetime.now()
total_cycles = 0
successful_cycles = 0
failed_cycles = 0

# Define missing global variables
CANDLE_SYSTEM_ACTIVE = True
candle_system = None

def print_timeframe_data_summary(market_state: 'EnhancedMarketState') -> None:
    """Print a condensed summary of timeframe data for quick viewing."""
    
    if not hasattr(market_state, 'current_analysis') or 'timeframe_analysis' not in market_state.current_analysis:
        print("⚠️  No timeframe data available for summary.")
        return
    
    tf_analysis = market_state.current_analysis['timeframe_analysis']
    
    print(f"\n📊 QUICK 15-TIMEFRAME SUMMARY:")
    print("─" * 90)
    
    # Define timeframes in order
    all_timeframes = ["3min", "9min", "15min", "21min", "25min", "30min", "33min", "39min", 
                     "45min", "50min", "55min", "60min", "65min", "75min", "90min"]
    
    # Show active timeframes
    for timeframe in all_timeframes:
        if timeframe in tf_analysis:
            data = tf_analysis[timeframe]
            momentum = data.get('momentum', 'N/A')
            strength = data.get('strength_score', 0)
            price_pct = data.get('spot_change_pct', data.get('price_change_pct', 0))
            
            # Color coding based on momentum
            momentum_symbol = "🟢" if "BULLISH" in momentum else "🔴" if "BEARISH" in momentum else "⚪"
            
            print(f"{momentum_symbol} {timeframe:>8}: {price_pct:+6.2f}% | {momentum:>15} | Strength: {strength:>4.1f}/10")
        else:
            print(f"⏳ {timeframe:>8}: ⏳ PENDING | {'WAITING':>15} | Strength: {'0.0':>4}/10")
    
    print("─" * 90)
async def run_bot():
    """Main bot execution with 5-minute candle capture, 15-timeframe analysis, and recommendations."""
    global total_cycles, successful_cycles, failed_cycles

    # Initialize Smart AI
    try:
        smart_ai = SmartAITradingBot("NIFTY")
        logger.info("🤖 Smart AI Trading Advisor loaded successfully!")
    except Exception as e:
        smart_ai = None
        logger.warning(f"⚠️ Smart AI failed to load: {e}, continuing without AI")

    # Initialize Candle Intelligence
    global CANDLE_SYSTEM_ACTIVE, candle_system
    try:
        candle_system = CandleIntelligenceSystem()
        CANDLE_SYSTEM_ACTIVE = True
        logger.info("✅ Candle Intelligence System initialized successfully")
    except Exception as e:
        candle_system = None
        CANDLE_SYSTEM_ACTIVE = False
        logger.error(f"❌ Candle Intelligence System init failed: {e}")

    # Load config
    config = load_config()
    logger.info("🚀 Starting God Bot PRO: HYBRID EDITION v3.0")

    # Initialize components
    predictor = FifteenMinPredictor()
    engine = EnhancedStrategyEngine(config)
    market_state = EnhancedMarketState("NIFTY", config)
    day_profile = EnhancedMarketDayProfile("NIFTY", config)
    data_manager = MarketDataManager()
    analyzer = EnhancedSmartSelfAnalyzer()
    timeframe_analyzer = MultiTimeframeAnalyzer([3,9,15,21,25,30,33,39,45,50,55,60,65,75,90])

    logger.info("✅ All components initialized")
    await send_enhanced_telegram_message(
        f"🚀 GOD BOT PRO STARTED @ {session_start_time.strftime('%Y-%m-%d %H:%M:%S')}",
        priority="HIGH"
    )

    # For 5-minute candle tracking
    current_candle = None
    prev_snapshot = None

    while True:
        total_cycles += 1
        cycle_start = datetime.now()
        now = cycle_start.time()
        is_market_hours = dt_time(9,15) <= now <= dt_time(15,30)

        # Fetch and process snapshot
        raw, expiry, ts, spot, _ = data_manager.fetch_option_chain_data_from_nse()
        if not raw:
            failed_cycles += 1
            logger.error("❌ Failed to fetch NSE data")
            await asyncio.sleep(30)
            continue
        snapshot = data_manager.process_nse_snapshot(raw, expiry, ts, spot)
        updated = market_state.update(snapshot)

        # 5-minute candle alignment
        candle_min = (cycle_start.minute // 5) * 5
        candle_start = cycle_start.replace(minute=candle_min, second=0, microsecond=0)

        # Finalize previous candle
        if current_candle and current_candle.start_time != candle_start:
            finished = current_candle.finalize(prev_snapshot)
            five_minute_candles.append(finished)
            print_5min_candle(finished)
            current_candle = None

        # Start new candle
        if current_candle is None:
            current_candle = FiveMinuteCandle(candle_start, snapshot['underlying_value'])
        current_candle.update(snapshot)
        prev_snapshot = snapshot

        # Main analysis
        analysis = await analyze_snapshot(snapshot)

        # AI enhancement
        if smart_ai:
            ai_state = {
                "current_snapshot": snapshot,
                "market_history": list(market_state.market_history)[-20:],
                "main_bot_analysis": analysis
            }
            try:
                ai_result = await smart_ai.workflow.ainvoke(ai_state, config=config)
            except Exception:
                ai_result = {"trade_signals": []}
            # merge verdicts...
            merge_ai(analysis, ai_result)

        # 15-timeframe analysis
        tf_result = timeframe_analyzer.analyze_timeframe_changes(market_state.market_history)
        display_15_timeframe_table(tf_result)
        market_state.current_analysis['timeframe_analysis'] = tf_result
        print_all_15_timeframes_data(market_state)

        # 5-minute candle intelligence
        if CANDLE_SYSTEM_ACTIVE and candle_system:
            try:
                candle_ai = candle_system.process_snapshot(snapshot)
                print_enhanced_candle_intelligence_output(candle_ai)
                market_state.current_analysis['candle_intelligence'] = candle_ai
            except Exception as e:
                logger.error(f"❌ Candle intelligence error: {e}")

        # Recommendation
        recommendation = generate_trading_recommendation(market_state)
        print_recommendation(recommendation)
        if recommendation['status'] in ['FIRST_RECOMMENDATION_ISSUED', 'CRITICAL_SIGNAL_TRACKING']:
            await send_enhanced_telegram_message(
                f"🎯 {recommendation['recommendation']}\nConfidence: {recommendation['confidence']}",
                priority="HIGH"
            )

        # Logging absolute values periodically
        if total_cycles % 10 == 0:
            log_absolute(snapshot, market_state)

        # Foundation building sleep
        if len(market_state.market_history) < 5:
            successful_cycles += 1
            await asyncio.sleep(30 if is_market_hours else 60)
            continue

        # Progressive engine analysis
        try:
            prog_analysis = engine.analyze_market_progressive(market_state)
            engine_recommendation = engine.generate_progressive_recommendation(prog_analysis, market_state, day_profile)
            logger.info(f"💡 Engine Recommendation: {engine_recommendation}")
        except Exception as e:
            logger.error(f"❌ Engine analysis error: {e}")

        # Periodic status summary
        if total_cycles % 20 == 0:
            print_enhanced_market_status(market_state, analysis, day_profile)
            send_session_stats()

        successful_cycles += 1

        # Adaptive sleep
        cycle_time = (datetime.now() - cycle_start).total_seconds()
        base = 30 if is_market_hours and len(market_state.market_history)<15 else 60 if is_market_hours else 120
        sleep_time = max(10, base - cycle_time)
        logger.info(f"💤 Sleeping {sleep_time:.1f}s")
        await asyncio.sleep(sleep_time)

def generate_trading_recommendation(market_state: 'EnhancedMarketState') -> Dict[str, Any]:
    """Generate trading recommendation based on timeframe analysis."""
    try:
        # Get timeframe analysis
        timeframe_analysis = {}
        
        if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
            timeframe_analysis = market_state.current_analysis['timeframe_analysis']
        
        # If still empty, try to get it from the MultiTimeframeAnalyzer
        if not timeframe_analysis and hasattr(MultiTimeframeAnalyzer, 'last_analysis_results'):
            analyzer = MultiTimeframeAnalyzer()
            if hasattr(analyzer, 'last_analysis_results') and analyzer.last_analysis_results:
                timeframe_analysis = analyzer.last_analysis_results
        
        # FIXED: Ensure timeframe_analysis is a dictionary
        if not isinstance(timeframe_analysis, dict):
            logger.warning("⚠️ Timeframe analysis is not a dictionary, using default values")
            timeframe_analysis = {}
        
        # Extract timeframe data
        timeframe_data = timeframe_analysis.get('changes', {})
        
        # Count market states
        bullish_count = 0
        bearish_count = 0
        sideways_count = 0
        total_strength = 0
        valid_timeframes = 0
        
        for data in timeframe_data.values():
            if data.get('status') == 'COMPLETED':
                momentum = data.get('momentum', '')
                if 'BULLISH' in momentum:
                    bullish_count += 1
                elif 'BEARISH' in momentum:
                    bearish_count += 1
                else:
                    sideways_count += 1
                
                strength = data.get('strength_score', 0)
                total_strength += strength
                valid_timeframes += 1
        
        # Determine overall market state
        if valid_timeframes == 0:
            market_state_str = "INSUFFICIENT_DATA"
            recommendation = "⏳ Building foundation for 9:30 AM first recommendation"
            confidence = "BUILDING"
        elif bullish_count > bearish_count and bullish_count > sideways_count:
            market_state_str = "BULLISH"
            recommendation = "🟢 Consider BUY positions"
            confidence = "HIGH" if bullish_count > bearish_count * 1.5 else "MEDIUM"
        elif bearish_count > bullish_count and bearish_count > sideways_count:
            market_state_str = "BEARISH"
            recommendation = "🔴 Consider SELL positions"
            confidence = "HIGH" if bearish_count > bullish_count * 1.5 else "MEDIUM"
        else:
            market_state_str = "SIDEWAYS"
            recommendation = "⚪ Range trading opportunities"
            confidence = "MEDIUM"
        
        # Calculate average strength
        avg_strength = total_strength / valid_timeframes if valid_timeframes > 0 else 0
        
        return {
            'status': 'PRE_RECOMMENDATION' if valid_timeframes < 5 else 'RECOMMENDATION',
            'recommendation': recommendation,
            'confidence': confidence,
            'market_state': market_state_str,
            'reason': f"Snapshots: {len(market_state.market_history)} | Active timeframes: {valid_timeframes}",
            'strength_score': avg_strength,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'sideways_count': sideways_count,
            'timeframes_analyzed': valid_timeframes
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating trading recommendation: {e}")
        return {
            'status': 'ERROR',
            'recommendation': '⚠️ Error generating recommendation',
            'confidence': 'LOW',
            'market_state': 'UNKNOWN',
            'reason': f'Error: {str(e)}',
            'strength_score': 0,
            'bullish_count': 0,
            'bearish_count': 0,
            'sideways_count': 0,
            'timeframes_analyzed': 0
        }

# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================

async def send_enhanced_telegram_message(message: str, priority: str = "INFO") -> bool:
    """Send enhanced messages to Telegram with priority handling."""
    try:
        config = load_config()
        telegram_config = config.get('telegram', {})
        if not telegram_config.get('token') or not telegram_config.get('chat_id'):
            logger.warning("⚠️ Telegram not configured - skipping message")
            return False
        telegram_url = f"https://api.telegram.org/bot{telegram_config['token']}/sendMessage"
        # Add priority prefix
        priority_emojis = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "NORMAL": "📊",
            "INFO": "ℹ️"
        }
        prefixed_message = f"{priority_emojis.get(priority, '📊')} {message}"
        message_data = {
            'chat_id': telegram_config['chat_id'],
            'text': prefixed_message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(telegram_url, json=message_data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"❌ Telegram send error: {e}")
        return False

def print_enhanced_candle_intelligence_output(candle_result):
    """Print enhanced candle intelligence output with pattern detection"""
    # Check if candle_result is not None before accessing its attributes
    if candle_result is not None and candle_result.get('status') == 'CANDLE_COMPLETED':
        pattern = candle_result.get('pattern_analysis', {})
        volume_intel = candle_result.get('volume_intelligence', {})
        oi_intel = candle_result.get('oi_intelligence', {})
        print(f"\n🕯️ CANDLE #{candle_result['candle_number']} COMPLETED:")
        print(f"   ⏰ Time: {candle_result['timestamp']}")
        print(f"   🕯️ Type: {candle_result.get('candle_color', 'UNKNOWN')}")
        print(f"   🎯 Pattern: {pattern.get('pattern', 'NONE')} ({pattern.get('confidence', 0):.0%})")
        print(f"   📊 Volume: {volume_intel.get('pattern', 'NORMAL')} - {volume_intel.get('volume_bias', 'NEUTRAL')}")
        print(f"   💰 Smart Money: {oi_intel.get('smart_money_direction', 'NEUTRAL')}")
        print(f"   🚨 Action: {candle_result.get('trade_recommendation', {}).get('action', 'WAIT')}")
        # Show volume/OI changes if available
        if 'ce_oi_change' in oi_intel:
            print(f"   📈 OI Changes: CE={oi_intel['ce_oi_change']:+,} PE={oi_intel['pe_oi_change']:+,}")
    elif candle_result.get('status') == 'BUILDING_CANDLE':
        # Show building progress with potential patterns
        print(f"🔄 Building Candle: {candle_result.get('candle_progress', 'Unknown progress')}")

def print_enhanced_market_status(market_state, analysis, day_profile):
    """Print enhanced market status summary with complete details."""
    print("\n" + "="*80)
    print("📊 ENHANCED MARKET STATUS SUMMARY")
    print("="*80)
    # Basic market info
    print(f"💹 Current Spot: ₹{market_state.last_spot_price:.2f}")
    print(f"🎯 Analysis Verdict: {analysis.get('verdict', 'NEUTRAL')}")
    print(f"📊 Confidence Score: {analysis.get('score', 0):.2f}/10")
    print(f"📈 Market Snapshots: {len(market_state.market_history)}")
    print(f"🎯 Data Quality: {market_state.data_quality_score:.1f}/10")
    # Active trade status
    if hasattr(day_profile, 'active_trade') and day_profile.active_trade:
        trade = day_profile.active_trade
        duration = datetime.now() - trade['entry_time']
        duration_str = f"{duration.seconds // 60}m {duration.seconds % 60}s"
        print(f"🔥 Active Trade: {trade['type']} {trade['strike']} @ ₹{trade['entry']:.2f}")
        print(f"⏱️ Duration: {duration_str}")
        print(f"🎯 Targets: ₹{trade.get('partial_target', 0):.2f} / ₹{trade.get('target', 0):.2f}")
    else:
        print("💤 No Active Trade")
    # Performance summary if available
    if hasattr(day_profile, 'get_performance_summary'):
        perf = day_profile.get_performance_summary()
        print(f"📊 Today's Performance: {perf.get('trades', 0)} trades, {perf.get('win_rate', 0):.1f}% win rate")
        print(f"💰 Session PnL: {perf.get('daily_pnl', 0):+.2f}%")
    # Timeframe analysis summary
    if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
        tf_count = len(market_state.current_analysis['timeframe_analysis'])
        print(f"🕐 Active Timeframes: {tf_count}/15")
    else:
        print("🕐 Timeframe Analysis: Building...")
    print("="*80)

def print_enhanced_analysis(combined_result):
    main_analysis   = combined_result.get('main_bot_analysis', {})
    candle_analysis = combined_result.get('candle_intelligence', {})
    rec            = combined_result.get('combined_recommendation', {})
    print("\n" + "="*100)
    print("🤖 ENHANCED BOT ANALYSIS — MAIN + CANDLE INTELLIGENCE")
    print("="*100)
    # MAIN
    print("📊 MAIN BOT:")
    print(f"   Verdict: {main_analysis.get('verdict', 'N/A')}")
    if 'timeframe_analysis' in main_analysis:
        print(f"   Timeframes Active: {len(main_analysis['timeframe_analysis'])}/15")
    # CANDLE
    print("\n🕯️ CANDLE INTELLIGENCE:")
    status = candle_analysis.get('status', 'N/A')
    if status == 'CANDLE_COMPLETED':
        patt  = candle_analysis.get('pattern_analysis', {})
        trade = candle_analysis.get('trade_recommendation', {})
        print(f"   Candle #{candle_analysis.get('candle_number', 0)} Completed")
        print(f"   Pattern: {patt.get('pattern', 'NONE')} ({patt.get('confidence',0):.0%})")
        print(f"   Recommendation: {trade.get('action','WAIT')} ({trade.get('confidence',0):.0%})")
    elif status == 'BUILDING_CANDLE':
        print(f"   Building Candle: {candle_analysis.get('candle_progress','N/A')}")
    else:
        print(f"   Status: {status}")
    # FINAL
    print("\n🎯 FINAL RECOMMENDATION:")
    print(f"   Action: {rec.get('action', 'WAIT')}")
    print(f"   Confidence: {rec.get('confidence', 0)}%")
    print(f"   Strength: {rec.get('strength', 'UNKNOWN')}")
    print(f"   Reasoning: {rec.get('reasoning', 'No reasoning')}")
    print("="*100 + "\n")

def test_time_window_integration():
    """Test function for time window integration."""
    config = {'symbol': 'NIFTY'}
    market_state = EnhancedMarketState('NIFTY', config)
    # Sample snapshot (use real data in practice)
    test_snapshot = {
        'underlying_value': 25000,
        'CE_OI': 1000000,
        'PE_OI': 1200000,
        'CE_VOL': 500000,
        'PE_VOL': 600000,
        'OI_PCR': 1.2,
        'VOL_PCR': 1.2,
        'timestamp': datetime.now().isoformat()
    }
    # Update and get result
    # NEW
    combined_result = enhanced_market_processing(test_snapshot)
    print_enhanced_analysis(combined_result)      # new pretty-printer        
    # Check if working
    if 'time_window_analysis' in result:
        print("✅ Time window integration working!")
        print(f"Current Window: {result['current_time_window']}")
        print(f"Action: {result['time_window_analysis'].get('action')}")
    else:
        print("❌ Integration failed - Check logs")

def keyboard_interrupt_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n🛑 God Bot PRO terminated by user")
    sys.exit(0)

async def run_bot():
    """Main bot execution with 15-timeframe analysis and 9:30 AM recommendations."""
    # Use global variables
    global total_cycles, successful_cycles, failed_cycles
    
    # FIX 3: Initialize Smart AI here after all classes are defined
    try:
        smart_ai = SmartAITradingBot("NIFTY")
        logger.info("🤖 Smart AI Trading Advisor loaded successfully!")
    except Exception as e:
        smart_ai = None
        logger.warning(f"⚠️ Smart AI failed to load: {e}, continuing without AI")
    # Initialize candle system properly
    global CANDLE_SYSTEM_ACTIVE, candle_system

    try:
        from candle_intelligence import CandleIntelligenceSystem
        candle_system = CandleIntelligenceSystem()
        CANDLE_SYSTEM_ACTIVE = True
        logger.info("✅ Candle Intelligence System initialized successfully")
    except Exception as e:
        logger.error(f"❌ Candle Intelligence System init failed: {e}")
        candle_system = None
        CANDLE_SYSTEM_ACTIVE = False

    
    try:
        # Load configuration first
        config = load_config()
        logger.info("🚀 Starting God Bot PRO: HYBRID EDITION v3.0 - 15-Timeframe Analysis")
        logger.info("="*100)
        # Initialize core components
        predictor = FifteenMinPredictor()
        engine = EnhancedStrategyEngine(config)
        # FIX 1: Use local EnhancedMarketState class instead of importing from new3
        market_state = EnhancedMarketState("NIFTY", config)
        # Try to load historical data if method exists
        if hasattr(market_state, 'load_enhanced_historical_data'):
            try:
                market_state.load_enhanced_historical_data()
            except Exception as e:
                logger.warning(f"⚠️ Historical data loading failed: {e}")
        else:
            logger.info("📂 Historical data loading not available - starting fresh")
        # Initialize day profile and analyzer
        day_profile = EnhancedMarketDayProfile("NIFTY", config)
        analyzer = EnhancedSmartSelfAnalyzer()
        # Initialize MarketDataManager
        data_manager = MarketDataManager()
        # Initialize 15-timeframe analyzer
        # FIX 1: Use local MultiTimeframeAnalyzer class instead of importing from new3
        timeframe_analyzer = MultiTimeframeAnalyzer([3, 9, 15, 21, 25, 30, 33, 39, 45, 50, 55, 60, 65, 75, 90])
        logger.info("✅ All components initialized successfully")
        logger.info("🎯 15-Timeframe Analysis: READY")
        logger.info("🕘 9:30 AM Recommendation System: ACTIVE") 
        logger.info("🎯 Starting main trading loop")
        # Send startup notification
        startup_msg = f"""🚀 GOD BOT PRO STARTED - 15-TIMEFRAME EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Start Time: {session_start_time.strftime('%Y-%m-%d %H:%M:%S')}
🎯 Analysis Mode: 15-Timeframe Progressive Analysis
🕘 Recommendation: First signal at 9:30 AM (15 snapshots)
⚡ Intervals: 3,9,15,21,25,30,33,39,45,50,55,60,65,75,90 min
🎯 Strategy: Market Opening Intelligence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        await send_enhanced_telegram_message(startup_msg, priority="HIGH")
        
        # FIX 4: Define analyze_snapshot inside run_bot to access local variables
        async def analyze_snapshot(snapshot_data):
            """
            Analyze market snapshot and return trading analysis.
            This function integrates all analysis components.
            """
            try:
                logger.info("🔍 Starting comprehensive snapshot analysis...")
                
                # 1. Initialize analysis result
                analysis_result = {
                    "verdict": "NEUTRAL",
                    "confidence": 0.5,
                    "reasoning": "Initial analysis",
                    "technical_analysis": {},
                    "timeframe_analysis": {},
                    "ai_enhancement": None
                }
                
                # 2. Perform technical analysis using market state
                if hasattr(market_state, 'get_ai_features'):
                    try:
                        ai_features = market_state.get_ai_features()
                        analysis_result["technical_analysis"] = ai_features
                        logger.info("✅ Technical analysis completed")
                    except Exception as e:
                        logger.error(f"❌ Technical analysis failed: {e}")
                
                # 3. Perform timeframe analysis
                if hasattr(timeframe_analyzer, 'analyze_timeframe_changes'):
                    try:
                        # ✅ FIXED: Store 15-timeframe results with correct "3min", "9min" keys
                        timeframe_result = timeframe_analyzer.analyze_timeframe_changes(market_state.market_history)
                        if not hasattr(market_state, 'current_analysis'):
                            market_state.current_analysis = {}
                        formatted_data = {}
                        if isinstance(timeframe_result, dict) and 'changes' in timeframe_result:
                            for interval, data in timeframe_result['changes'].items():
                                key = f"{interval}min"  # e.g., "3min", "15min"
                                if isinstance(data, dict) and data.get('status') == 'COMPLETED':
                                    formatted_data[key] = {
                                        'status': 'COMPLETED',
                                        'spot_change': data.get('spot_change', 0.0),
                                        'spot_change_pct': data.get('spot_change_pct', 0.0),
                                        'ce_oi_change': data.get('ce_oi_change', 0),
                                        'pe_oi_change': data.get('pe_oi_change', 0),
                                        'momentum': data.get('momentum', 'NEUTRAL'),
                                        'strength_score': data.get('strength_score', 0.0),
                                        'baseline_price': data.get('start_price', 0),
                                        'current_price': data.get('end_price', 0)
                                    }
                                else:
                                    formatted_data[key] = {'status': 'PENDING'}
                        market_state.current_analysis['timeframe_analysis'] = formatted_data
                        logger.info(f"✅ 15-Timeframe analysis stored: {len([v for v in formatted_data.values() if v['status']=='COMPLETED'])}/15 completed")
                    except Exception as e:
                        logger.error(f"❌ Timeframe analysis failed: {e}")
                
                # 4. Perform candle analysis if available
                if CANDLE_SYSTEM_ACTIVE and candle_system is not None:
                    try:
                        # FIXED: Use process_snapshot instead of analyze_candle_patterns
                        candle_analysis_result = candle_system.process_snapshot(snapshot_data)
                        if candle_analysis_result:
                            analysis_result["candle_analysis"] = candle_analysis_result
                            logger.info("✅ Candle pattern analysis completed")
                    except Exception as e:
                        logger.error(f"❌ Candle analysis failed: {e}")
                
                # 5. Generate final verdict
                try:
                    # Simple verdict logic based on OI data
                    ce_oi = snapshot_data.get('CE_OI', 0)
                    pe_oi = snapshot_data.get('PE_OI', 0)
                    oi_pcr = snapshot_data.get('OI_PCR', 1.0)
                    
                    if ce_oi > pe_oi * 1.2 and oi_pcr < 0.8:
                        analysis_result["verdict"] = "BULLISH"
                        analysis_result["confidence"] = 0.7
                        analysis_result["reasoning"] = "Strong CE OI dominance with low PCR"
                    elif pe_oi > ce_oi * 1.2 and oi_pcr > 1.2:
                        analysis_result["verdict"] = "BEARISH"
                        analysis_result["confidence"] = 0.7
                        analysis_result["reasoning"] = "Strong PE OI dominance with high PCR"
                    else:
                        analysis_result["verdict"] = "NEUTRAL"
                        analysis_result["confidence"] = 0.5
                        analysis_result["reasoning"] = "Balanced OI and PCR values"
                        
                    logger.info(f"🎯 Final verdict: {analysis_result['verdict']} with confidence {analysis_result['confidence']:.2f}")
                    
                except Exception as e:
                    logger.error(f"❌ Verdict generation failed: {e}")
                
                return analysis_result
                
            except Exception as e:
                logger.error(f"❌ Critical analysis error: {e}")
                return {
                    "verdict": "NEUTRAL",
                    "confidence": 0.5,
                    "reasoning": f"Analysis error: {str(e)}",
                    "technical_analysis": {},
                    "timeframe_analysis": {}
                }
        
        while True:
            try:
                total_cycles += 1
                cycle_start = datetime.now()
                current_time = cycle_start.time()
                logger.info(f"\n🔄 CYCLE #{total_cycles} - {cycle_start.strftime('%H:%M:%S')}")
                logger.info("="*100)
                # Check if it's market hours
                is_market_hours = dt_time(9, 15) <= current_time <= dt_time(15, 30)
                if not is_market_hours:
                    logger.info("⏰ Outside market hours - Reduced frequency mode")
                # Fetch real NSE data
                raw_data, expiry, ts, spot, full_json_data = data_manager.fetch_option_chain_data_from_nse()
                if raw_data:
                    # Process the NSE data
                    snapshot = data_manager.process_nse_snapshot(raw_data, expiry, ts, spot)
                    logger.info("✅ NSE data fetched and processed successfully")
                else:
                    failed_cycles += 1
                    logger.error("❌ Failed to fetch NSE data. Skipping this cycle.")
                    await asyncio.sleep(30)
                    continue
                # Update market state
                updated_snapshot = market_state.update(snapshot)
                # ─── MAIN BOT ANALYSIS ───────────────────────────────────────────────────────
                # Ensure `analysis` is always initialized before AI enhancement
                # Replace undefined main_bot with the correct analysis function
                analysis = await analyze_snapshot(updated_snapshot)
                # ─── AI ENHANCEMENT PATCH ─────────────────────────────────────────────────
                if smart_ai:
                    ai_state = {
                        "current_snapshot": snapshot,
                        "market_history": list(market_state.market_history)[-20:],
                        "main_bot_analysis": analysis
                    }
                    # With this:
                    try:
                        ai_result = await smart_ai.workflow.ainvoke(
                            ai_state, config=config
                        )
                    except Exception as e:
                        logger.error(f"❌ AI workflow error: {e}")
                        # Provide a fallback AI result
                        ai_result = {
                            "strategy_updates": {"strategy": "NEUTRAL"},
                            "risk_assessment": {"should_trade": False},
                            "self_reflection": {"analysis": f"AI workflow failed: {str(e)}"},
                            "trade_signals": []
                        }
                    # Combine verdicts
                    main_verdict = analysis.get("verdict", "NEUTRAL")
                    main_conf = analysis.get("score", 0) / 10
                    ai_trades = ai_result.get("trade_signals", [])
                    if ai_trades:
                        last = ai_trades[-1]
                        ai_verdict = "BULLISH" if last["action"] == "BUY" else "BEARISH"
                        ai_conf = last["confidence"] / 100
                    else:
                        ai_verdict, ai_conf = main_verdict, main_conf
                    if main_verdict == ai_verdict:
                        final_conf = min(main_conf + 0.15, 0.95)
                        enhancement_note = f"✅ AI CONFIRMS {main_verdict}"
                    elif main_verdict == "NEUTRAL":
                        final_conf = ai_conf
                        enhancement_note = f"🤖 AI SUGGESTS {ai_verdict}"
                    else:
                        final_conf = max(main_conf - 0.1, 0.3)
                        enhancement_note = f"⚠️ AI DISAGREES You={main_verdict},AI={ai_verdict}"
                    analysis["verdict"] = main_verdict
                    analysis["score"] = final_conf * 10
                    analysis["ai_enhancement"] = enhancement_note
                    logger.info(f"🧠 AI Enhancement: {enhancement_note}")
                # ─ End AI PATCH ───────────────────────────────────────────────────────────────
                # **15-TIMEFRAME ANALYSIS INTEGRATION**
                try:
                    # Run 15-timeframe analysis
                    timeframe_result = timeframe_analyzer.analyze_timeframe_changes(market_state.market_history)
                    timeframe_analysis = timeframe_result  # Removed 'self.' references

                    # Display 15-timeframe table
                    display_15_timeframe_table(timeframe_analysis)

                    # Store in market state
                    if not hasattr(market_state, 'current_analysis'):
                        market_state.current_analysis = {}
                    market_state.current_analysis['timeframe_analysis'] = timeframe_result

                    # Print all 15 timeframes data
                    print_all_15_timeframes_data(market_state)

                    # ** FIX 3: ENHANCED 5-MINUTE CANDLE INTELLIGENCE INTEGRATION **
                    try:
                        logger.info("🕯️ Processing Enhanced 5-Minute Candle Intelligence...")
                        candle_analysis_result = None

                        if CANDLE_SYSTEM_ACTIVE and candle_system is not None:
                            try:
                                candle_analysis_result = candle_system.process_snapshot(snapshot)
                                logger.info("🕯️ Candle intelligence analysis completed successfully")

                                if candle_analysis_result.get('status') == 'CANDLE_COMPLETED':
                                    cdata = candle_analysis_result['candle_data']
                                    patt = candle_analysis_result['pattern_analysis']
                                    vol = candle_analysis_result['volume_intelligence']
                                    oi = candle_analysis_result['oi_intelligence']
                                    sr = candle_analysis_result['sr_context']
                                    rec = candle_analysis_result['trade_recommendation']

                                    print("\n" + "="*100)
                                    print(f"🕯️ 5-MINUTE CANDLE #{candle_analysis_result.get('candle_number',0)} COMPLETED @ {candle_analysis_result.get('timestamp','N/A')}")
                                    print("="*100)
                                    print(f"📊 OHLC: O={cdata['open']:.2f} H={cdata['high']:.2f} L={cdata['low']:.2f} C={cdata['close']:.2f}")
                                    print(f"🕯️ Pattern: {patt['pattern']} ({patt['confidence']:.0%}) Significance: {patt['significance']}")
                                    print(f"📈 Volume: {vol['pattern']} | Bias: {vol['volume_bias']} | Surge Ratio: {vol['surge_ratio']:.2f}")
                                    print(f"💰 OI: CE={oi['ce_oi_change']:+} PE={oi['pe_oi_change']:+} | Smart Money: {oi['smart_money_direction']}")
                                    print(f"🎯 Support=₹{sr['support_level']:.2f} ({cdata['close']-sr['support_level']:.2f} away)")
                                    print(f"🎯 Resistance=₹{sr['resistance_level']:.2f} ({sr['resistance_level']-cdata['close']:.2f} away)")
                                    print(f"🚨 TRADE: {rec['action']} (Conf: {rec['confidence']:.0%}) Strength: {rec['strength']}")
                                    print(f"💡 Reason: {rec['reasoning']}")
                                    print("="*100 + "\n")

                                    # Send Telegram notification
                                    candle_msg = f"""🕯️ CANDLE #{candle_analysis_result['candle_number']} COMPLETED
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                📊 Pattern: {patt['pattern']} ({patt['confidence']:.0%})
                🎯 Action: {rec['action']} ({rec['confidence']:.0%})
                💡 Reasoning: {rec['reasoning'][:100]}
                ⏰ Time: {cycle_start.strftime('%H:%M:%S')}
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                                    await send_enhanced_telegram_message(candle_msg, priority="HIGH")

                                elif candle_analysis_result.get('status') == 'BUILDING_CANDLE':
                                    progress = candle_analysis_result['candle_progress']
                                    building = candle_analysis_result['current_analysis']
                                    print(f"🔄 Building 5-min candle... Progress: {progress}")
                                    print(f"   Current Price: ₹{building['current_price']:.2f}")
                                    print(f"   Range: O={building['open_price']:.2f} H={building['high_price']:.2f} L={building['low_price']:.2f}")

                                else:
                                    print("⚠️ Candle not complete, analysis not available yet.")

                            except Exception as e:
                                logger.error(f"❌ Candle intelligence error: {e}")
                                candle_analysis_result = None
                        else:
                            logger.warning("⚠️ Candle system is not available, skipping candle analysis")

                        # Store candle analysis in market state
                        market_state.current_analysis['candle_intelligence'] = candle_analysis_result

                        # Log candle intelligence status
                        if candle_analysis_result:
                            status = candle_analysis_result['status']
                            logger.info(f"🕯️ Candle Status: {status}")
                            if status == 'CANDLE_COMPLETED':
                                num = candle_analysis_result['candle_number']
                                patt = candle_analysis_result['pattern_analysis']['pattern']
                                conf = candle_analysis_result['pattern_analysis']['confidence']
                                rec = candle_analysis_result['trade_recommendation']['action']
                                logger.info(f"✅ Candle #{num} completed: {patt} ({conf:.0%}), Rec: {rec}")
                            elif status == 'BUILDING_CANDLE':
                                prog = candle_analysis_result['candle_progress']
                                logger.info(f"🔄 Building candle progress: {prog}")
                        else:
                            logger.warning("⚠️ Candle analysis result is None, using default status")

                    except Exception as candle_error:
                        logger.error(f"❌ Candle intelligence outer error: {candle_error}")
                        logger.error(f"📍 Candle error traceback: {traceback.format_exc()}")

                except Exception as tf_error:
                    logger.error(f"❌ 15-Timeframe analysis error: {tf_error}")
                    logger.error(f"📍 Traceback: {traceback.format_exc()}")


                # **9:30 AM RECOMMENDATION SYSTEM**
                try:
                    # FIXED: Use the new generate_trading_recommendation function instead of get_market_recommendation
                    recommendation = generate_trading_recommendation(market_state)
                    print(f"\n🎯 TRADING RECOMMENDATION SYSTEM:")
                    print("="*80)
                    print(f"📊 Status: {recommendation.get('status', 'UNKNOWN')}")
                    print(f"💡 Recommendation: {recommendation.get('recommendation', 'No recommendation')}")
                    print(f"🎯 Confidence: {recommendation.get('confidence', 'LOW')}")
                    print(f"📋 Reason: {recommendation.get('reason', 'No reason provided')}")
                    # Additional details based on recommendation type
                    if 'timeframes_analyzed' in recommendation:
                        print(f"🕐 Timeframes Analyzed: {recommendation['timeframes_analyzed']}/15")
                    if 'action' in recommendation:
                        print(f"🎯 Suggested Action: {recommendation['action']}")
                    if 'bias' in recommendation:
                        print(f"📈 Market Bias: {recommendation['bias']}")
                    print("="*80)
                    # Send critical recommendations to Telegram
                    if recommendation.get('status') in ['FIRST_RECOMMENDATION_ISSUED', 'CRITICAL_SIGNAL_TRACKING']:
                        await send_enhanced_telegram_message(
                            f"🎯 {recommendation.get('recommendation', 'No recommendation')}\n"
                            f"Confidence: {recommendation.get('confidence', 'LOW')}\n"
                            f"Cycle: #{total_cycles}",
                            priority="HIGH" if recommendation.get('status') == 'FIRST_RECOMMENDATION_ISSUED' else "CRITICAL"
                        )
                except Exception as rec_error:
                    logger.error(f"❌ Recommendation system error: {rec_error}")
                # Enhanced timeframe data logging for diagnosis
                logger.info("📊 STORED TIMEFRAME DATA - Complete Analysis:")
                if hasattr(market_state, 'current_analysis') and 'timeframe_analysis' in market_state.current_analysis:
                    tf_analysis = market_state.current_analysis['timeframe_analysis']
                    logger.info(f"🔍 Available timeframes: {list(tf_analysis.keys())}")
                    logger.info(f"📈 Market history snapshots: {len(market_state.market_history)}")
                    # Log data for each available timeframe
                    for timeframe, data in tf_analysis.items():
                        if isinstance(data, dict) and 'spot_change' in data:
                            logger.info(f"\n⏰ {timeframe.upper()} TIMEFRAME DATA:")
                            logger.info(f"   Spot Change: {data['spot_change']:+.2f} ({data['spot_change_pct']:+.4f}%)")
                            ce_oi_change = data.get('ce_oi_change', 0)
                            ce_oi_change_pct = data.get('ce_oi_change_pct', 0.0)
                            logger.info(f"   CE OI Change: {ce_oi_change:+,} ({ce_oi_change_pct:+.2f}%)")
                            # Safe access to dictionary keys
                            pe_oi_change = data.get('pe_oi_change', 0)
                            pe_oi_change_pct = data.get('pe_oi_change_pct', 0.0)
                            logger.info(f"   PE OI Change: {pe_oi_change:+,} ({pe_oi_change_pct:+.2f}%)")                            
                            logger.info(f"   Momentum: {data['momentum']}")
                            logger.info(f"   Strength Score: {data['strength_score']:.2f}/10")
                else:
                    logger.info("🔄 Timeframe analysis building - need more snapshots")
                # Print absolute values for diagnosis
                logger.info("\n📊 FETCHED ABSOLUTE VALUES:")
                logger.info(f" CE_OI: {snapshot['CE_OI']:,}")
                logger.info(f" PE_OI: {snapshot['PE_OI']:,}")
                logger.info(f" Total OI: {snapshot['CE_OI'] + snapshot['PE_OI']:,}")
                logger.info(f" CE_VOL: {snapshot['CE_VOL']:,}")
                logger.info(f" PE_VOL: {snapshot['PE_VOL']:,}")
                logger.info(f" Total Volume: {snapshot['CE_VOL'] + snapshot['PE_VOL']:,}")
                logger.info(f" Spot Price: ₹{snapshot['underlying_value']:.2f}")
                logger.info(f" OI PCR: {snapshot['OI_PCR']:.4f}")
                logger.info(f" VOL PCR: {snapshot['VOL_PCR']:.4f}")
                # Send absolute values to Telegram for monitoring (every 10 cycles)
                if total_cycles % 10 == 0:
                    abs_values_msg = f"""📊 CYCLE #{total_cycles} - MARKET SNAPSHOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💹 Spot: ₹{snapshot['underlying_value']:.2f}
🟢 CE OI: {snapshot['CE_OI']:,} 📊 CE VOL: {snapshot['CE_VOL']:,}
🔴 PE OI: {snapshot['PE_OI']:,} 📊 PE VOL: {snapshot['PE_VOL']:,}
🎯 OI PCR: {snapshot['OI_PCR']:.4f} | VOL PCR: {snapshot['VOL_PCR']:.4f}
📈 Timeframes: {len(market_state.current_analysis.get('timeframe_analysis', {}))}/15
🕯️ Candle Status: {market_state.current_analysis.get('candle_intelligence', {}).get('status', 'N/A')}
⏰ Time: {cycle_start.strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                    await send_enhanced_telegram_message(abs_values_msg.strip(), priority="NORMAL")
                # Check if we have enough data for full analysis
                if len(market_state.market_history) < 5:
                    logger.info(f"📊 Building market history. Snapshots: {len(market_state.market_history)}/5 minimum")
                    successful_cycles += 1
                    # Dynamic sleep based on market hours
                    sleep_time = 30 if is_market_hours else 60
                    await asyncio.sleep(sleep_time)
                    continue
                # Analyze market using existing engine
                try:
                    analysis = engine.analyze_market_progressive(market_state)
                    # Save snapshots for AI training
                    if analysis["verdict"] in ["BULLISH", "BEARISH"]:
                        engine.save_snapshot_for_ai_training(snapshot, analysis["verdict"])
                    # Generate progressive recommendation from engine
                    engine_recommendation = engine.generate_progressive_recommendation(analysis, market_state, day_profile)
                    # Handle active trades
                    if hasattr(day_profile, 'active_trade') and day_profile.active_trade:
                        trade_update = engine.manage_active_trade(analysis, day_profile, market_state)
                        logger.info(f"🏃 Active Trade Update: {trade_update.get('verdict', 'MONITORING')}")
                    # Generate smart commentary
                    if hasattr(engine, 'commentary_bot') and engine.commentary_bot:
                        try:
                            commentary = engine.commentary_bot.generate_comprehensive_market_commentary(market_state, analysis)
                            logger.info(f"🧠 Smart Commentary Generated ({len(commentary)} chars)")
                        except Exception as e:
                            logger.warning(f"⚠️ Commentary generation failed: {e}")
                    # Display analysis results
                    logger.info(f"📊 Engine Analysis: {analysis.get('verdict', 'NEUTRAL')} (Score: {analysis.get('score', 0):.2f})")
                    logger.info(f"💡 Engine Recommendation: {engine_recommendation}")
                except Exception as engine_error:
                    logger.error(f"❌ Engine analysis error: {engine_error}")
                    logger.warning("⚠️ Continuing with timeframe analysis only")
                # Performance summary every 20 cycles
                if total_cycles % 20 == 0:
                    print_enhanced_market_status(market_state, analysis if 'analysis' in locals() else {}, day_profile)
                    # Session statistics
                    uptime = datetime.now() - session_start_time
                    success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0
                    session_msg = f"""📊 SESSION STATISTICS - CYCLE #{total_cycles}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ Uptime: {str(uptime).split('.')[0]}
📊 Success Rate: {success_rate:.1f}% ({successful_cycles}/{total_cycles})
🎯 Active Timeframes: {len(market_state.current_analysis.get('timeframe_analysis', {}))}/15
🕯️ Candle System: {market_state.current_analysis.get('candle_intelligence', {}).get('status', 'N/A')}
💹 Current Spot: ₹{market_state.last_spot_price:.2f}
📈 Data Quality: {market_state.data_quality_score:.1f}/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                    await send_enhanced_telegram_message(session_msg, priority="INFO")
                successful_cycles += 1
                logger.info(f"✅ Cycle #{total_cycles} completed successfully")
            except Exception as cycle_error:
                failed_cycles += 1
                logger.error(f"❌ Cycle #{total_cycles} error: {cycle_error}")
                logger.error(f"📍 Traceback: {traceback.format_exc()}")
                # Send error notification
                error_msg = f"❌ Cycle #{total_cycles} Error: {str(cycle_error)[:100]}..."
                await send_enhanced_telegram_message(error_msg, priority="HIGH")
                await asyncio.sleep(30)  # Wait before retry
                continue
            # Dynamic sleep timing based on market hours and cycle performance
            cycle_duration = (datetime.now() - cycle_start).total_seconds()
            if is_market_hours:
                base_sleep = 60  # 1 minute during market hours
                if len(market_state.market_history) < 15:
                    base_sleep = 30  # Faster during foundation building
            else:
                base_sleep = 120  # 2 minutes outside market hours
            # Adjust based on success rate
            success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 100
            if success_rate < 80:
                base_sleep *= 1.5  # Slower if having issues
            sleep_time = max(10, base_sleep - cycle_duration)
            logger.info(f"💤 Sleeping for {sleep_time:.1f}s until next cycle...")
            await asyncio.sleep(sleep_time)
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot shutdown requested by user")
        # Save data before exit
        try:
            if hasattr(market_state, 'save_enhanced_historical_data'):
                market_state.save_enhanced_historical_data()
            if hasattr(day_profile, 'save_session_data'):
                day_profile.save_session_data()
            logger.info("💾 Session data saved successfully")
        except Exception as e:
            logger.error(f"❌ Error saving session data: {e}")
        # Final statistics
        uptime = datetime.now() - session_start_time
        success_rate = (successful_cycles / total_cycles * 100) if total_cycles > 0 else 0
        final_msg = f"""🛑 GOD BOT PRO SHUTDOWN - 15-TIMEFRAME EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Session Summary:
• Total Cycles: {total_cycles}
• Successful: {successful_cycles} ({success_rate:.1f}%)
• Failed: {failed_cycles}
• Uptime: {str(uptime).split('.')[0]}
• Final Spot: ₹{market_state.last_spot_price:.2f}
• Max Timeframes: {len(market_state.current_analysis.get('timeframe_analysis', {}))}/15
🎯 Thank you for using God Bot PRO!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        await send_enhanced_telegram_message(final_msg, priority="HIGH")
    except Exception as e:
        logger.error(f"💥 Critical error in main loop: {e}")
        logger.error(f"📍 Full traceback: {traceback.format_exc()}")
        # Critical error notification
        critical_msg = f"""💥 CRITICAL ERROR - BOT STOPPED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Error: {str(e)[:200]}...
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Cycles Completed: {total_cycles}
Please check logs and restart manually.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        await send_enhanced_telegram_message(critical_msg, priority="CRITICAL")
        raise
    finally:
        logger.info("🏁 God Bot PRO shutdown complete")

def main():
    """Main entry point for the God Bot PRO."""
    try:
        logger.info("🚀 Launching God Bot PRO - 15-Timeframe Edition")
        
        # Configure Windows event loop policy
        if sys.platform.startswith('win'):
            if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            else:
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, keyboard_interrupt_handler)
        
        # Run the main bot
        asyncio.run(run_bot())
        
    except KeyboardInterrupt:
        print("\n🛑 God Bot PRO terminated")
    except Exception as e:
        import traceback
        print(f"\n💥 Critical startup error: {e}")
        print("📍 Full error details:")
        traceback.print_exc()
        
        # Additional error diagnosis
        print(f"\n🔍 ERROR DIAGNOSIS:")
        print(f"  - Error Type: {type(e).__name__}")
        print(f"  - Error Message: {str(e)}")
        print(f"  - Python Version: {sys.version}")
        print(f"  - Platform: {sys.platform}")
        
        if "SignalEngine" in str(e):
            print(f"\n💡 SOLUTION: Replace 'SignalEngine' with 'EnhancedStrategyEngine'")
        if "MultiTimeframeAnalyzer" in str(e):
            print(f"\n💡 SOLUTION: Ensure the 15-timeframe analyzer patch is applied")
        if "get_market_recommendation" in str(e):
            print(f"\n💡 SOLUTION: Ensure the 9:30 AM recommendation system patch is applied")
        
        sys.exit(1)

# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()