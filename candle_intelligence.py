#!/usr/bin/env python3
# =============================================================================
#
# CANDLE INTELLIGENCE SYSTEM - HAND-BY-HAND TRADING SUPPORT
#
# =============================================================================
#
# Advanced 5-minute candlestick analysis system for NSE Options Trading
#
# Integrates with main trading bot to provide enhanced intelligence
#
# Author: Enhanced for ultimate candle pattern recognition
#
# =============================================================================
import json
import logging
import math
import os
from collections import deque
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

# Configure logging for candle system
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# =============================================================================
# CORE DATA STRUCTURES
# =============================================================================
class FiveMinuteCandle:
    """Represents a complete 5-minute candlestick with all market data"""
    def __init__(self):
        self.timestamp = None
        self.open_price = 0.0
        self.high_price = 0.0
        self.low_price = 0.0
        self.close_price = 0.0
        # Volume data
        self.ce_volume = 0
        self.pe_volume = 0
        self.total_volume = 0
        self.volume_bias = 0
        # OI data
        self.ce_oi = 0
        self.pe_oi = 0
        self.total_oi = 0
        self.oi_pcr = 0.0
        # Pattern analysis
        self.pattern_type = "NONE"
        self.pattern_strength = 0.0
        self.body_size = 0.0
        self.upper_wick = 0.0
        self.lower_wick = 0.0
        self.candle_range = 0.0
        # Context data
        self.support_level = 0.0
        self.resistance_level = 0.0
        self.distance_to_support = 0.0
        self.distance_to_resistance = 0.0
        self.time_window = "UNKNOWN"
        # Market intelligence
        self.volume_surge_ratio = 1.0
        self.oi_change_ratio = 1.0
        self.smart_money_direction = "NEUTRAL"
        self.institutional_activity = "LOW"

    def calculate_pattern_metrics(self):
        """Calculate all candlestick metrics"""
        if self.high_price == self.low_price:  # Avoid division by zero
            return
        self.candle_range = self.high_price - self.low_price
        self.body_size = abs(self.close_price - self.open_price)
        self.upper_wick = self.high_price - max(self.open_price, self.close_price)
        self.lower_wick = min(self.open_price, self.close_price) - self.low_price
        # Calculate pattern strength (0-1)
        if self.candle_range > 0:
            body_ratio = self.body_size / self.candle_range
            wick_ratio = (self.upper_wick + self.lower_wick) / self.candle_range
            self.pattern_strength = max(body_ratio, wick_ratio)

class PatternOutcome:
    """Tracks what happened after a pattern was detected"""
    def __init__(self, pattern_candle: FiveMinuteCandle):
        self.pattern_candle = pattern_candle
        self.formation_time = pattern_candle.timestamp
        # Pre-pattern context (5 minutes before)
        self.before_context = {
            'price_trend': 'UNKNOWN',
            'volume_trend': 'UNKNOWN',
            'oi_trend': 'UNKNOWN',
            'market_sentiment': 'NEUTRAL'
        }
        # Post-pattern outcome (5 minutes after)
        self.after_outcome = {
            'price_direction': 'UNKNOWN',
            'price_move_points': 0.0,
            'price_move_percent': 0.0,
            'volume_response': 'UNKNOWN',
            'oi_response': 'UNKNOWN',
            'breakout_confirmed': False,
            'target_achieved': False,
            'success': False
        }
        # Learning data
        self.prediction_accuracy = 0.0
        self.confidence_score = 0.0
        self.trade_recommendation = "NONE"

# =============================================================================
# PATTERN DETECTION ENGINE
# =============================================================================
class CandlestickPatternDetector:
    """Advanced candlestick pattern detection with context analysis"""
    def __init__(self):
        self.pattern_thresholds = {
            'doji_body_ratio': 0.1,  # Body < 10% of range
            'hammer_body_ratio': 0.3,  # Body < 30% of range
            'hammer_wick_ratio': 0.6,  # Lower wick > 60% of range
            'shooting_star_wick_ratio': 0.6,  # Upper wick > 60% of range
            'engulfing_min_ratio': 1.2  # Current body > 120% of previous
        }

    def detect_pattern(self, current_candle: FiveMinuteCandle, previous_candle: Optional[FiveMinuteCandle] = None) -> Dict[str, Any]:
        """Detect candlestick patterns with confidence scoring"""
        if current_candle.candle_range == 0:
            return {'pattern': 'NONE', 'confidence': 0.0, 'significance': 'LOW'}
        pattern_results = []
        # Doji Pattern Detection
        doji_result = self._detect_doji(current_candle)
        if doji_result['detected']:
            pattern_results.append(doji_result)
        # Hammer Pattern Detection
        hammer_result = self._detect_hammer(current_candle)
        if hammer_result['detected']:
            pattern_results.append(hammer_result)
        # Shooting Star Pattern Detection
        shooting_star_result = self._detect_shooting_star(current_candle)
        if shooting_star_result['detected']:
            pattern_results.append(shooting_star_result)
        # Engulfing Pattern Detection (needs previous candle)
        if previous_candle:
            engulfing_result = self._detect_engulfing(current_candle, previous_candle)
            if engulfing_result['detected']:
                pattern_results.append(engulfing_result)
        # Return strongest pattern
        if pattern_results:
            strongest_pattern = max(pattern_results, key=lambda x: x['confidence'])
            current_candle.pattern_type = strongest_pattern['pattern']
            current_candle.pattern_strength = strongest_pattern['confidence']
            return strongest_pattern
        return {'pattern': 'NONE', 'confidence': 0.0, 'significance': 'LOW'}

    def _detect_doji(self, candle: FiveMinuteCandle) -> Dict[str, Any]:
        """Detect Doji patterns (indecision candles)"""
        body_ratio = candle.body_size / candle.candle_range if candle.candle_range > 0 else 0
        if body_ratio <= self.pattern_thresholds['doji_body_ratio']:
            # Determine doji type
            upper_wick_ratio = candle.upper_wick / candle.candle_range
            lower_wick_ratio = candle.lower_wick / candle.candle_range
            if upper_wick_ratio > 0.4 and lower_wick_ratio > 0.4:
                doji_type = "LONG_LEGGED_DOJI"
                confidence = 0.85
            elif upper_wick_ratio > 0.6:
                doji_type = "DRAGONFLY_DOJI"
                confidence = 0.75
            elif lower_wick_ratio > 0.6:
                doji_type = "GRAVESTONE_DOJI"
                confidence = 0.80
            else:
                doji_type = "STANDARD_DOJI"
                confidence = 0.70
            return {
                'detected': True,
                'pattern': doji_type,
                'confidence': confidence,
                'significance': 'HIGH',
                'market_meaning': 'INDECISION_REVERSAL_SIGNAL',
                'body_ratio': body_ratio,
                'upper_wick_ratio': upper_wick_ratio,
                'lower_wick_ratio': lower_wick_ratio
            }
        return {'detected': False}

    def _detect_hammer(self, candle: FiveMinuteCandle) -> Dict[str, Any]:
        """Detect Hammer patterns (bullish reversal)"""
        body_ratio = candle.body_size / candle.candle_range if candle.candle_range > 0 else 0
        lower_wick_ratio = candle.lower_wick / candle.candle_range if candle.candle_range > 0 else 0
        upper_wick_ratio = candle.upper_wick / candle.candle_range if candle.candle_range > 0 else 0
        # Hammer conditions: Small body, long lower wick, small upper wick
        if (body_ratio <= self.pattern_thresholds['hammer_body_ratio'] and
            lower_wick_ratio >= self.pattern_thresholds['hammer_wick_ratio'] and
            upper_wick_ratio <= 0.1):
            confidence = 0.70 + (lower_wick_ratio * 0.2)  # Higher confidence for longer lower wick
            return {
                'detected': True,
                'pattern': 'HAMMER',
                'confidence': min(confidence, 0.90),
                'significance': 'HIGH',
                'market_meaning': 'BULLISH_REVERSAL_SIGNAL',
                'body_ratio': body_ratio,
                'lower_wick_ratio': lower_wick_ratio,
                'upper_wick_ratio': upper_wick_ratio
            }
        return {'detected': False}

    def _detect_shooting_star(self, candle: FiveMinuteCandle) -> Dict[str, Any]:
        """Detect Shooting Star patterns (bearish reversal)"""
        body_ratio = candle.body_size / candle.candle_range if candle.candle_range > 0 else 0
        upper_wick_ratio = candle.upper_wick / candle.candle_range if candle.candle_range > 0 else 0
        lower_wick_ratio = candle.lower_wick / candle.candle_range if candle.candle_range > 0 else 0
        # Shooting star conditions: Small body, long upper wick, small lower wick
        if (body_ratio <= self.pattern_thresholds['hammer_body_ratio'] and
            upper_wick_ratio >= self.pattern_thresholds['shooting_star_wick_ratio'] and
            lower_wick_ratio <= 0.1):
            confidence = 0.70 + (upper_wick_ratio * 0.2)  # Higher confidence for longer upper wick
            return {
                'detected': True,
                'pattern': 'SHOOTING_STAR',
                'confidence': min(confidence, 0.90),
                'significance': 'HIGH',
                'market_meaning': 'BEARISH_REVERSAL_SIGNAL',
                'body_ratio': body_ratio,
                'upper_wick_ratio': upper_wick_ratio,
                'lower_wick_ratio': lower_wick_ratio
            }
        return {'detected': False}

    def _detect_engulfing(self, current: FiveMinuteCandle, previous: FiveMinuteCandle) -> Dict[str, Any]:
        """Detect Engulfing patterns (strong reversal signals)"""
        current_body = current.body_size
        previous_body = previous.body_size
        if previous_body == 0:  # Avoid division by zero
            return {'detected': False}
        body_ratio = current_body / previous_body
        # Engulfing conditions: Current body significantly larger than previous
        if body_ratio >= self.pattern_thresholds['engulfing_min_ratio']:
            # Determine engulfing type
            current_bullish = current.close_price > current.open_price
            previous_bullish = previous.close_price > previous.open_price
            if current_bullish and not previous_bullish:
                # Bullish engulfing
                if (current.close_price > previous.open_price and current.open_price < previous.close_price):
                    confidence = 0.75 + min((body_ratio - 1.2) * 0.1, 0.15)
                    return {
                        'detected': True,
                        'pattern': 'BULLISH_ENGULFING',
                        'confidence': confidence,
                        'significance': 'VERY_HIGH',
                        'market_meaning': 'STRONG_BULLISH_REVERSAL',
                        'body_ratio': body_ratio
                    }
            elif not current_bullish and previous_bullish:
                # Bearish engulfing
                if (current.close_price < previous.open_price and current.open_price > previous.close_price):
                    confidence = 0.75 + min((body_ratio - 1.2) * 0.1, 0.15)
                    return {
                        'detected': True,
                        'pattern': 'BEARISH_ENGULFING',
                        'confidence': confidence,
                        'significance': 'VERY_HIGH',
                        'market_meaning': 'STRONG_BEARISH_REVERSAL',
                        'body_ratio': body_ratio
                    }
        return {'detected': False}

# =============================================================================
# VOLUME & OI INTELLIGENCE ANALYZER
# =============================================================================
class VolumeOIAnalyzer:
    """Analyzes volume and OI patterns for trade confirmation"""
    def __init__(self):
        self.volume_history = deque(maxlen=20)  # Last 20 candles
        self.oi_history = deque(maxlen=20)

    def analyze_volume_context(self, current_candle: FiveMinuteCandle, historical_candles: List[FiveMinuteCandle]) -> Dict[str, Any]:
        """Analyze volume patterns and provide trading context"""
        if len(historical_candles) < 3:
            return {'pattern': 'INSUFFICIENT_DATA', 'significance': 'LOW'}
        # Calculate volume metrics
        recent_volumes = [c.total_volume for c in historical_candles[-5:]]
        avg_volume = np.mean(recent_volumes) if recent_volumes else 1
        current_volume = current_candle.total_volume
        volume_surge_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        # Analyze volume bias
        ce_dominance = current_candle.ce_volume / current_volume if current_volume > 0 else 0.5
        pe_dominance = current_candle.pe_volume / current_volume if current_volume > 0 else 0.5
        # Determine volume pattern
        if volume_surge_ratio >= 3.0:
            volume_pattern = "EXPLOSIVE_VOLUME"
            significance = "VERY_HIGH"
        elif volume_surge_ratio >= 2.0:
            volume_pattern = "HIGH_VOLUME"
            significance = "HIGH"
        elif volume_surge_ratio >= 1.5:
            volume_pattern = "ELEVATED_VOLUME"
            significance = "MEDIUM"
        else:
            volume_pattern = "NORMAL_VOLUME"
            significance = "LOW"
        # Determine market bias from volume
        if ce_dominance >= 0.65:
            volume_bias = "STRONG_BULLISH"
        elif ce_dominance >= 0.55:
            volume_bias = "BULLISH"
        elif pe_dominance >= 0.65:
            volume_bias = "STRONG_BEARISH"
        elif pe_dominance >= 0.55:
            volume_bias = "BEARISH"
        else:
            volume_bias = "NEUTRAL"
        current_candle.volume_surge_ratio = volume_surge_ratio
        return {
            'pattern': volume_pattern,
            'significance': significance,
            'volume_bias': volume_bias,
            'surge_ratio': volume_surge_ratio,
            'ce_dominance': ce_dominance,
            'pe_dominance': pe_dominance,
            'institutional_activity': self._assess_institutional_activity(volume_surge_ratio, current_volume)
        }

    def analyze_oi_context(self, current_candle: FiveMinuteCandle, historical_candles: List[FiveMinuteCandle]) -> Dict[str, Any]:
        """Analyze Open Interest patterns for position flow intelligence"""
        if len(historical_candles) < 2:
            return {'pattern': 'INSUFFICIENT_DATA', 'significance': 'LOW'}
        previous_candle = historical_candles[-1]
        # Calculate OI changes
        ce_oi_change = current_candle.ce_oi - previous_candle.ce_oi
        pe_oi_change = current_candle.pe_oi - previous_candle.pe_oi
        total_oi_change = ce_oi_change + pe_oi_change
        # Calculate OI change ratios
        ce_oi_change_pct = (ce_oi_change / previous_candle.ce_oi * 100) if previous_candle.ce_oi > 0 else 0
        pe_oi_change_pct = (pe_oi_change / previous_candle.pe_oi * 100) if previous_candle.pe_oi > 0 else 0
        # Determine OI pattern
        if abs(total_oi_change) >= 50000:
            oi_pattern = "MASSIVE_OI_ACTIVITY"
            significance = "VERY_HIGH"
        elif abs(total_oi_change) >= 20000:
            oi_pattern = "HIGH_OI_ACTIVITY"
            significance = "HIGH"
        elif abs(total_oi_change) >= 5000:
            oi_pattern = "MODERATE_OI_ACTIVITY"
            significance = "MEDIUM"
        else:
            oi_pattern = "LOW_OI_ACTIVITY"
            significance = "LOW"
        # Determine smart money direction
        if ce_oi_change > pe_oi_change and ce_oi_change > 0:
            smart_money_direction = "BULLISH"
        elif pe_oi_change > ce_oi_change and pe_oi_change > 0:
            smart_money_direction = "BEARISH"
        elif total_oi_change < -10000:
            smart_money_direction = "PROFIT_BOOKING"
        else:
            smart_money_direction = "NEUTRAL"
        current_candle.smart_money_direction = smart_money_direction
        current_candle.oi_change_ratio = abs(total_oi_change) / previous_candle.total_oi if previous_candle.total_oi > 0 else 0
        return {
            'pattern': oi_pattern,
            'significance': significance,
            'smart_money_direction': smart_money_direction,
            'ce_oi_change': ce_oi_change,
            'pe_oi_change': pe_oi_change,
            'total_oi_change': total_oi_change,
            'ce_oi_change_pct': ce_oi_change_pct,
            'pe_oi_change_pct': pe_oi_change_pct,
            'position_type': self._determine_position_type(ce_oi_change, pe_oi_change, total_oi_change)
        }

    def _assess_institutional_activity(self, volume_surge: float, total_volume: int) -> str:
        """Assess level of institutional activity based on volume patterns"""
        if volume_surge >= 3.0 and total_volume >= 1000000:
            return "VERY_HIGH"
        elif volume_surge >= 2.0 and total_volume >= 500000:
            return "HIGH"
        elif volume_surge >= 1.5 and total_volume >= 200000:
            return "MEDIUM"
        else:
            return "LOW"

    def _determine_position_type(self, ce_change: int, pe_change: int, total_change: int) -> str:
        """Determine the type of positioning activity"""
        if total_change > 10000:
            if ce_change > pe_change:
                return "FRESH_BULLISH_POSITIONS"
            else:
                return "FRESH_BEARISH_POSITIONS"
        elif total_change < -10000:
            return "POSITION_UNWINDING"
        else:
            return "NEUTRAL_POSITIONING"

# =============================================================================
# SUPPORT/RESISTANCE TRACKER
# =============================================================================
class SupportResistanceTracker:
    """Dynamic support and resistance level tracking"""
    def __init__(self):
        self.price_history = deque(maxlen=50)  # Last 50 candles for S/R calculation
        self.support_levels = []
        self.resistance_levels = []

    def update_levels(self, candle: FiveMinuteCandle):
        """Update support and resistance levels based on price action"""
        self.price_history.append({
            'timestamp': candle.timestamp,
            'high': candle.high_price,
            'low': candle.low_price,
            'close': candle.close_price
        })
        if len(self.price_history) >= 10:
            self._calculate_dynamic_levels()
        self._update_candle_sr_context(candle)

    def _calculate_dynamic_levels(self):
        """Calculate support and resistance levels from recent price action"""
        highs = [p['high'] for p in list(self.price_history)[-20:]]
        lows = [p['low'] for p in list(self.price_history)[-20:]]
        # Find significant highs and lows
        self.resistance_levels = self._find_significant_levels(highs, level_type='resistance')
        self.support_levels = self._find_significant_levels(lows, level_type='support')
        # Keep only top 3 most significant levels
        self.resistance_levels = sorted(self.resistance_levels, reverse=True)[:3]
        self.support_levels = sorted(self.support_levels)[:3]

    def _find_significant_levels(self, prices: List[float], level_type: str) -> List[float]:
        """Find significant support or resistance levels"""
        if len(prices) < 5:
            return []
        levels = []
        prices_array = np.array(prices)
        if level_type == 'resistance':
            # Find local maxima
            for i in range(2, len(prices) - 2):
                if (prices[i] > prices[i-1] and prices[i] > prices[i-2] and
                    prices[i] > prices[i+1] and prices[i] > prices[i+2]):
                    levels.append(prices[i])
        else:  # support
            # Find local minima
            for i in range(2, len(prices) - 2):
                if (prices[i] < prices[i-1] and prices[i] < prices[i-2] and
                    prices[i] < prices[i+1] and prices[i] < prices[i+2]):
                    levels.append(prices[i])
        return levels

    def _update_candle_sr_context(self, candle: FiveMinuteCandle):
        """Update candle with support/resistance context"""
        current_price = candle.close_price
        # Find nearest support and resistance
        if self.support_levels:
            supports_below = [s for s in self.support_levels if s <= current_price]
            candle.support_level = max(supports_below) if supports_below else min(self.support_levels)
            candle.distance_to_support = current_price - candle.support_level
        if self.resistance_levels:
            resistances_above = [r for r in self.resistance_levels if r >= current_price]
            candle.resistance_level = min(resistances_above) if resistances_above else max(self.resistance_levels)
            candle.distance_to_resistance = candle.resistance_level - current_price

# =============================================================================
# MAIN CANDLE INTELLIGENCE SYSTEM
# =============================================================================
class CandleIntelligenceSystem:
    """Main system coordinator - This is what your main bot imports"""
    def __init__(self):
        logger.info("🕯️ Initializing Candle Intelligence System...")
        # Core components
        self.pattern_detector = CandlestickPatternDetector()
        self.volume_oi_analyzer = VolumeOIAnalyzer()
        self.sr_tracker = SupportResistanceTracker()
        # Data storage
        self.minute_data_buffer = deque(maxlen=10)  # 10 minutes of data for 5-min candles
        self.completed_candles = deque(maxlen=100)  # Last 100 completed candles
        self.pattern_outcomes = deque(maxlen=200)  # Pattern learning database
        # Current state
        self.current_candle_start = None
        self.building_candle = FiveMinuteCandle()
        self.candle_count = 0
        # Performance tracking
        self.total_patterns_detected = 0
        self.successful_predictions = 0
        self.accuracy_rate = 0.0
        logger.info("✅ Candle Intelligence System initialized successfully")

    def process_snapshot(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function - called by main bot every minute"""
        try:
            current_time = datetime.now()
            
            logger.info(f"\n🕯️ Processing snapshot at {current_time.strftime('%H:%M:%S')}")
            
            # Add snapshot to minute buffer
            self.minute_data_buffer.append({
                'timestamp': current_time,
                'snapshot': snapshot
            })
            
            # Check if we need to start a new 5-minute candle
            if self._should_start_new_candle(current_time):
                self._start_new_candle(current_time)
            
            # Update building candle with current data
            self._update_building_candle(snapshot)
            
            # Check if 5-minute candle is complete
            if self._is_candle_complete(current_time):
                result = self._complete_candle_analysis()
                logger.info(f"🕯️ Candle analysis completed at {current_time.strftime('%H:%M:%S')}")
                return result
            
            # Return building status
            progress = self._get_candle_progress(current_time)
            logger.info(f"🕯️ Building candle: {progress}")
            
            return {
                'status': 'BUILDING_CANDLE',
                'candle_progress': progress,
                'current_analysis': self._get_current_building_analysis()
            }
        except Exception as e:
            logger.error(f"❌ Error processing snapshot: {e}")
            return {'status': 'ERROR', 'error': str(e)}
    # NEW METHOD: Add analyze_candle_patterns to fix the error
    def analyze_candle_patterns(self, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze candle patterns from snapshot data.
        This method provides a simplified interface for pattern analysis.
        """
        try:
            # Process the snapshot through the main system
            result = self.process_snapshot(snapshot_data)
            
            # Extract pattern information if available
            if result.get('status') == 'CANDLE_COMPLETED':
                pattern_analysis = result.get('pattern_analysis', {})
                return {
                    'pattern': pattern_analysis.get('pattern', 'NONE'),
                    'confidence': pattern_analysis.get('confidence', 0.0),
                    'significance': pattern_analysis.get('significance', 'LOW'),
                    'market_meaning': pattern_analysis.get('market_meaning', 'UNKNOWN'),
                    'status': 'COMPLETED',
                    'candle_data': result.get('candle_data', {}),
                    'volume_intelligence': result.get('volume_intelligence', {}),
                    'oi_intelligence': result.get('oi_intelligence', {}),
                    'trade_recommendation': result.get('trade_recommendation', {})
                }
            else:
                # For building candles, return current pattern information
                current_analysis = result.get('current_analysis', {})
                return {
                    'pattern': 'BUILDING',
                    'confidence': 0.0,
                    'significance': 'LOW',
                    'market_meaning': 'PATTERN_FORMING',
                    'status': 'BUILDING',
                    'candle_progress': result.get('candle_progress', '0%'),
                    'current_analysis': current_analysis
                }
        except Exception as e:
            logger.error(f"❌ Error in analyze_candle_patterns: {e}")
            return {
                'pattern': 'ERROR',
                'confidence': 0.0,
                'significance': 'LOW',
                'market_meaning': 'ANALYSIS_FAILED',
                'status': 'ERROR',
                'error': str(e)
            }

    def _should_start_new_candle(self, current_time: datetime) -> bool:
        """Check if we should start a new 5-minute candle"""
        if self.current_candle_start is None:
            return True
        # Check if 5 minutes have passed
        time_diff = (current_time - self.current_candle_start).total_seconds()
        return time_diff >= 300  # 5 minutes = 300 seconds

    def _start_new_candle(self, start_time: datetime):
        """Start building a new 5-minute candle"""
        self.current_candle_start = start_time
        self.building_candle = FiveMinuteCandle()
        self.building_candle.timestamp = start_time
        logger.info(f"🕯️ Starting new 5-minute candle at {start_time.strftime('%H:%M:%S')}")

    def _update_building_candle(self, snapshot: Dict[str, Any]):
        """Update the building candle with current market data"""
        current_price = float(snapshot.get('underlying_value', 0))
        # Initialize OHLC if first update
        if self.building_candle.open_price == 0:
            self.building_candle.open_price = current_price
            self.building_candle.high_price = current_price
            self.building_candle.low_price = current_price
        # Update OHLC
        self.building_candle.high_price = max(self.building_candle.high_price, current_price)
        self.building_candle.low_price = min(self.building_candle.low_price, current_price)
        self.building_candle.close_price = current_price
        # Update volume and OI (accumulate)
        self.building_candle.ce_volume = int(snapshot.get('CE_VOL', 0))
        self.building_candle.pe_volume = int(snapshot.get('PE_VOL', 0))
        self.building_candle.total_volume = self.building_candle.ce_volume + self.building_candle.pe_volume
        self.building_candle.volume_bias = self.building_candle.pe_volume - self.building_candle.ce_volume
        self.building_candle.ce_oi = int(snapshot.get('CE_OI', 0))
        self.building_candle.pe_oi = int(snapshot.get('PE_OI', 0))
        self.building_candle.total_oi = self.building_candle.ce_oi + self.building_candle.pe_oi
        self.building_candle.oi_pcr = float(snapshot.get('OI_PCR', 0))

    def _is_candle_complete(self, current_time: datetime) -> bool:
        """Check if the current 5-minute candle is complete"""
        if self.current_candle_start is None:
            return False
        time_diff = (current_time - self.current_candle_start).total_seconds()
        return time_diff >= 300  # 5 minutes

    def _complete_candle_analysis(self) -> Dict[str, Any]:
        """Complete analysis when 5-minute candle is finished"""
        try:
            self.candle_count += 1
            logger.info(f"🎯 Completing 5-minute candle #{self.candle_count} analysis")
            # Calculate pattern metrics
            self.building_candle.calculate_pattern_metrics()
            # Detect candlestick patterns
            previous_candle = self.completed_candles[-1] if self.completed_candles else None
            pattern_result = self.pattern_detector.detect_pattern(self.building_candle, previous_candle)
            # Analyze volume context
            volume_analysis = self.volume_oi_analyzer.analyze_volume_context(
                self.building_candle, list(self.completed_candles)
            )
            # Analyze OI context
            oi_analysis = self.volume_oi_analyzer.analyze_oi_context(
                self.building_candle, list(self.completed_candles)
            )
            # Update support/resistance levels
            self.sr_tracker.update_levels(self.building_candle)
            # Generate trade recommendation
            trade_recommendation = self._generate_trade_recommendation(
                pattern_result, volume_analysis, oi_analysis
            )
            # Store completed candle
            self.completed_candles.append(self.building_candle)

            # Log detailed candle data for terminal
            c = self.building_candle
            logger.info(f"🕯️ Candle #{self.candle_count} Summary:")
            logger.info(f"  Timestamp: {c.timestamp}")
            logger.info(f"  OHLC: O={c.open_price} H={c.high_price} L={c.low_price} C={c.close_price}")
            logger.info(f"  Volume: CE={c.ce_volume} PE={c.pe_volume} Total={c.total_volume} Bias={c.volume_bias}")
            logger.info(f"  OI: CE={c.ce_oi} PE={c.pe_oi} Total={c.total_oi} PCR={c.oi_pcr:.4f}")
            logger.info(f"  Wick sizes: Upper={c.upper_wick} Lower={c.lower_wick} Body={c.body_size}")
            logger.info(f"  Pattern: {c.pattern_type} with strength {c.pattern_strength:.2f}")
            logger.info(f"  Support Level: {c.support_level}, Resistance Level: {c.resistance_level}")
            logger.info(f"  Distance to Support: {c.distance_to_support}, Distance to Resistance: {c.distance_to_resistance}")
            logger.info(f"  Market Bias: Volume Surge={c.volume_surge_ratio}, OI Change Ratio={c.oi_change_ratio}, Smart Money={c.smart_money_direction}")

            # Create comprehensive analysis result
            analysis_result = {
                'status': 'CANDLE_COMPLETED',
                'candle_number': self.candle_count,
                'timestamp': self.building_candle.timestamp.isoformat(),
                # Candle data
                'candle_data': {
                    'open': self.building_candle.open_price,
                    'high': self.building_candle.high_price,
                    'low': self.building_candle.low_price,
                    'close': self.building_candle.close_price,
                    'range': self.building_candle.candle_range,
                    'body_size': self.building_candle.body_size,
                    'upper_wick': self.building_candle.upper_wick,
                    'lower_wick': self.building_candle.lower_wick
                },
                # Pattern analysis
                'pattern_analysis': pattern_result,
                # Volume intelligence
                'volume_intelligence': volume_analysis,
                # OI intelligence
                'oi_intelligence': oi_analysis,
                # Support/Resistance context
                'sr_context': {
                    'support_level': self.building_candle.support_level,
                    'resistance_level': self.building_candle.resistance_level,
                    'distance_to_support': self.building_candle.distance_to_support,
                    'distance_to_resistance': self.building_candle.distance_to_resistance
                },
                # Trade recommendation
                'trade_recommendation': trade_recommendation,
                # System metrics
                'system_metrics': {
                    'total_candles_analyzed': self.candle_count,
                    'patterns_detected': self.total_patterns_detected,
                    'accuracy_rate': self.accuracy_rate
                }
            }

            # Track patterns for learning
            if pattern_result['pattern'] != 'NONE':
                self.total_patterns_detected += 1
                self._track_pattern_for_learning(analysis_result)

            # Log comprehensive analysis
            self._log_candle_analysis(analysis_result)
            return analysis_result

        except Exception as e:
            logger.error(f"❌ Error completing candle analysis: {e}")
            return {'status': 'ANALYSIS_ERROR', 'error': str(e)}

    
# =============================================================================
# PART 2: CANDLE INTELLIGENCE TRADE RECOMMENDATION (UPDATED)
# =============================================================================

    def _generate_trade_recommendation(self, pattern_result: Dict, volume_analysis: Dict, oi_analysis: Dict) -> Dict[str, Any]:
        """Generate trade recommendation with sideways market detection."""
        logger.info("=" * 60)
        logger.info("🕯️ CANDLE PATTERN ANALYSIS")
        logger.info("=" * 60)
        logger.info(f"Pattern: {pattern_result.get('pattern', 'NONE')}")
        logger.info(f"Pattern Confidence: {pattern_result.get('confidence', 0):.2f}")
        logger.info(f"Volume Pattern: {volume_analysis.get('pattern', 'UNKNOWN')}")
        logger.info(f"Volume Bias: {volume_analysis.get('volume_bias', 'NEUTRAL')}")
        logger.info(f"Smart Money: {oi_analysis.get('smart_money_direction', 'NEUTRAL')}")
        
        # Base recommendation from pattern
        pattern_type = pattern_result.get('pattern', 'NONE')
        pattern_confidence = pattern_result.get('confidence', 0.0)
        
        # Volume confirmation
        volume_significance = volume_analysis.get('significance', 'LOW')
        volume_bias = volume_analysis.get('volume_bias', 'NEUTRAL')
        
        # OI confirmation
        oi_significance = oi_analysis.get('significance', 'LOW')
        smart_money_direction = oi_analysis.get('smart_money_direction', 'NEUTRAL')
        
        # NEW: Detect sideways market conditions
        if len(self.completed_candles) >= 3:
            recent_candles = list(self.completed_candles)[-3:]
            price_changes = []
            
            for i in range(1, len(recent_candles)):
                change = abs(recent_candles[i].close_price - recent_candles[i-1].close_price) / recent_candles[i-1].close_price * 100
                price_changes.append(change)
            
            avg_price_change = sum(price_changes) / len(price_changes) if price_changes else 0
            
            # If average price change is very small, consider it sideways
            if avg_price_change < 0.03:  # Less than 0.03% average change
                return {
                    'action': "WAIT",
                    'confidence': 0.6,
                    'strength': "MEDIUM",
                    'reasoning': f"Sideways market detected (avg change: {avg_price_change:.3f}%). Waiting for clearer signals.",
                    'entry_strategy': "Wait for breakout or stronger pattern",
                    'risk_assessment': "LOW",
                    'market_condition': "SIDEWAYS",
                    'overall_trend': "SIDEWAYS",
                    'trend_adjustment': "📊 Sideways market - no trend adjustment"
                }
        
        # Get overall market trend
        overall_trend = self._get_overall_market_trend()
        
        # Calculate combined confidence
        base_confidence = pattern_confidence
        
        # Boost confidence with volume confirmation
        if volume_significance in ['HIGH', 'VERY_HIGH']:
            base_confidence += 0.1
        
        # Boost confidence with OI confirmation
        if oi_significance in ['HIGH', 'VERY_HIGH']:
            base_confidence += 0.1
        
        # Alignment bonus
        alignment_bonus = self._calculate_alignment_bonus(pattern_type, volume_bias, smart_money_direction)
        final_confidence = min(base_confidence + alignment_bonus, 0.95)
        
        # Trend persistence adjustments
        if overall_trend == "BULLISH":
            # Boost confidence for bullish signals in bullish market
            if pattern_type in ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']:
                final_confidence = min(final_confidence + 0.15, 0.95)
            # Reduce confidence for bearish signals in bullish market
            elif pattern_type in ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']:
                final_confidence = max(final_confidence - 0.2, 0.3)
        
        elif overall_trend == "BEARISH":
            # Boost confidence for bearish signals in bearish market
            if pattern_type in ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']:
                final_confidence = min(final_confidence + 0.15, 0.95)
            # Reduce confidence for bullish signals in bearish market
            elif pattern_type in ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']:
                final_confidence = max(final_confidence - 0.2, 0.3)
        
        # Generate recommendation
        if final_confidence >= 0.8:
            action = self._determine_trade_action(pattern_type, volume_bias, smart_money_direction)
            strength = "VERY_HIGH"
        elif final_confidence >= 0.65:
            action = self._determine_trade_action(pattern_type, volume_bias, smart_money_direction)
            strength = "HIGH"
        elif final_confidence >= 0.5:
            action = "MONITOR"
            strength = "MEDIUM"
        else:
            action = "WAIT"
            strength = "LOW"
        
        # Final trend validation
        if overall_trend == "BULLISH" and action == "SELL":
            if final_confidence < 0.8:
                action = "MONITOR"
                strength = "MEDIUM"
        
        elif overall_trend == "BEARISH" and action == "BUY":
            if final_confidence < 0.8:
                action = "MONITOR"
                strength = "MEDIUM"
        
        return {
            'action': action,
            'confidence': round(final_confidence, 2),
            'strength': strength,
            'reasoning': self._generate_reasoning(pattern_type, volume_analysis, oi_analysis, final_confidence),
            'entry_strategy': self._suggest_entry_strategy(action, pattern_type),
            'risk_assessment': self._assess_risk(pattern_type, volume_analysis, oi_analysis),
            'overall_trend': overall_trend,
            'trend_adjustment': self._get_trend_adjustment_text(overall_trend, pattern_type)
        }
        
    # NEW: Helper method to get overall market trend
    def _get_overall_market_trend(self) -> str:
        """Get overall market trend from recent candles."""
        if len(self.completed_candles) < 3:
            return "UNKNOWN"
        
        recent_candles = list(self.completed_candles)[-3:]
        if recent_candles[-1].close_price > recent_candles[0].close_price * 1.002:
            return "BULLISH"
        elif recent_candles[-1].close_price < recent_candles[0].close_price * 0.998:
            return "BEARISH"
        else:
            return "SIDEWAYS"

    # NEW: Helper method to get trend adjustment text
    def _get_trend_adjustment_text(self, overall_trend: str, pattern_type: str) -> str:
        """Generate text explaining trend adjustment."""
        if overall_trend == "BULLISH":
            if pattern_type in ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']:
                return "✅ Boosted: Bullish pattern in bullish market"
            elif pattern_type in ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']:
                return "⚠️ Reduced: Bearish pattern in bullish market"
        
        elif overall_trend == "BEARISH":
            if pattern_type in ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']:
                return "✅ Boosted: Bearish pattern in bearish market"
            elif pattern_type in ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']:
                return "⚠️ Reduced: Bullish pattern in bearish market"
        
        return "📊 No trend adjustment"

    def _calculate_alignment_bonus(self, pattern: str, volume_bias: str, smart_money: str) -> float:
        """Calculate bonus confidence for aligned signals"""
        alignment_score = 0.0
        # Pattern-Volume alignment
        if pattern in ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']:
            if volume_bias in ['BULLISH', 'STRONG_BULLISH']:
                alignment_score += 0.15
        elif pattern in ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']:
            if volume_bias in ['BEARISH', 'STRONG_BEARISH']:
                alignment_score += 0.15
        # Volume-SmartMoney alignment
        if volume_bias in ['BULLISH', 'STRONG_BULLISH'] and smart_money == 'BULLISH':
            alignment_score += 0.1
        elif volume_bias in ['BEARISH', 'STRONG_BEARISH'] and smart_money == 'BEARISH':
            alignment_score += 0.1
        return alignment_score

    def _determine_trade_action(self, pattern: str, volume_bias: str, smart_money: str) -> str:
        """Determine specific trade action based on signals"""
        bullish_patterns = ['HAMMER', 'BULLISH_ENGULFING', 'DRAGONFLY_DOJI']
        bearish_patterns = ['SHOOTING_STAR', 'BEARISH_ENGULFING', 'GRAVESTONE_DOJI']
        bullish_signals = (pattern in bullish_patterns,
                           volume_bias in ['BULLISH', 'STRONG_BULLISH'],
                           smart_money == 'BULLISH')
        bearish_signals = (pattern in bearish_patterns,
                           volume_bias in ['BEARISH', 'STRONG_BEARISH'],
                           smart_money == 'BEARISH')
        if sum(bullish_signals) >= 2:
            return "BUY"
        elif sum(bearish_signals) >= 2:
            return "SELL"
        else:
            return "MONITOR"

    def _generate_reasoning(self, pattern: str, volume_analysis: Dict,
                            oi_analysis: Dict, confidence: float) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        if pattern != 'NONE':
            reasons.append(f"{pattern} pattern detected")
        if volume_analysis.get('significance') in ['HIGH', 'VERY_HIGH']:
            reasons.append(f"{volume_analysis['pattern']} with {volume_analysis['volume_bias']} bias")
        if oi_analysis.get('significance') in ['HIGH', 'VERY_HIGH']:
            reasons.append(f"Smart money flow: {oi_analysis['smart_money_direction']}")
        return f"Confidence {confidence:.0%}: " + " + ".join(reasons)

    def _suggest_entry_strategy(self, action: str, pattern: str) -> str:
        """Suggest entry strategy based on action and pattern"""
        if action == "BUY":
            if pattern in ['HAMMER', 'BULLISH_ENGULFING']:
                return "Enter on breakout above candle high with volume confirmation"
            else:
                return "Enter on next bullish confirmation candle"
        elif action == "SELL":
            if pattern in ['SHOOTING_STAR', 'BEARISH_ENGULFING']:
                return "Enter on breakdown below candle low with volume confirmation"
            else:
                return "Enter on next bearish confirmation candle"
        else:
            return "Wait for clearer signals or confirmation"

    def _assess_risk(self, pattern: str, volume_analysis: Dict, oi_analysis: Dict) -> str:
        """Assess risk level based on analysis"""
        risk_factors = 0
        if volume_analysis.get('significance') == 'LOW':
            risk_factors += 1
        if oi_analysis.get('significance') == 'LOW':
            risk_factors += 1
        if pattern == 'NONE':
            risk_factors += 1
        if risk_factors >= 2:
            return "HIGH"
        elif risk_factors == 1:
            return "MEDIUM"
        else:
            return "LOW"

    def _track_pattern_for_learning(self, analysis_result: Dict):
        """Track pattern for future learning and accuracy improvement"""
        pattern_outcome = PatternOutcome(self.building_candle)
        pattern_outcome.trade_recommendation = analysis_result['trade_recommendation']['action']
        pattern_outcome.confidence_score = analysis_result['trade_recommendation']['confidence']
        self.pattern_outcomes.append(pattern_outcome)

    def _get_candle_progress(self, current_time: datetime) -> str:
        """Get current candle building progress with time window details"""
        if self.current_candle_start is None:
            return "0% | No active candle | Next: Starting soon"
        
        elapsed = (current_time - self.current_candle_start).total_seconds()
        progress = min(elapsed / 300 * 100, 100) # 300 seconds = 5 minutes
        remaining = max(0, 300 - elapsed)
        
        # Determine current time window
        current_time_obj = current_time.time()
        from datetime import time as dt_time
        
        if dt_time(9, 15) <= current_time_obj <= dt_time(10, 30):
            window = "OPENING_HOUR"
        elif dt_time(10, 30) <= current_time_obj <= dt_time(11, 30):
            window = "MORNING_MOMENTUM" 
        elif dt_time(11, 30) <= current_time_obj <= dt_time(13, 30):
            window = "LUNCH_LULL"
        elif dt_time(13, 30) <= current_time_obj <= dt_time(15, 00):
            window = "AFTERNOON_ACTIVITY"
        else:
            window = "CLOSING_HOUR"
        
        return f"{progress:.0f}% | Remaining: {remaining:.0f}s | Window: {window}"

    def _get_current_building_analysis(self) -> Dict:
        """Get detailed analysis of currently building candle"""
        return {
            'current_price': self.building_candle.close_price,
            'open_price': self.building_candle.open_price,
            'high_price': self.building_candle.high_price,
            'low_price': self.building_candle.low_price,
            'candle_range': self.building_candle.candle_range,
            'body_size': self.building_candle.body_size,
            'upper_wick': self.building_candle.upper_wick,
            'lower_wick': self.building_candle.lower_wick,
            'ce_volume': self.building_candle.ce_volume,
            'pe_volume': self.building_candle.pe_volume,
            'total_volume': self.building_candle.total_volume,
            'volume_bias': self.building_candle.volume_bias,
            'ce_oi': self.building_candle.ce_oi,
            'pe_oi': self.building_candle.pe_oi,
            'total_oi': self.building_candle.total_oi,
            'oi_pcr': self.building_candle.oi_pcr
        }

    # Also update the output method:
    def print_candle_intelligence_output(self, current_time: datetime):
        """Print enhanced candle intelligence output."""
        progress_info = self._get_candle_progress(current_time)
        
        print("\n🕯️ 5-Minute Candle Intelligence Output 🕯️")
        print("="*50)
        print(f"📅 Current Candle: {progress_info['current_window']}")
        print(f"⏱️ Progress: {progress_info['progress_pct']} ({progress_info['time_remaining']} remaining)")
        print(f"📊 Status: {progress_info['candle_status']}")
        print(f"🕯️ Last Completed: {progress_info['last_completed']}")
        print("="*50)

    def _log_candle_analysis(self, analysis: Dict):
        """Log comprehensive candle analysis"""
        candle_data = analysis['candle_data']
        pattern = analysis['pattern_analysis']
        recommendation = analysis['trade_recommendation']
        logger.info("=" * 80)
        logger.info(f"🕯️ CANDLE #{analysis['candle_number']} COMPLETE ANALYSIS")
        logger.info("=" * 80)
        logger.info(f"⏰ Time: {analysis['timestamp']}")
        logger.info(f"📊 OHLC: O={candle_data['open']:.1f} H={candle_data['high']:.1f} L={candle_data['low']:.1f} C={candle_data['close']:.1f}")
        logger.info(f"🕯️ Pattern: {pattern['pattern']} (Confidence: {pattern['confidence']:.0%})")
        logger.info(f"📈 Volume: {analysis['volume_intelligence']['pattern']} - {analysis['volume_intelligence']['volume_bias']}")
        logger.info(f"🎯 OI Flow: {analysis['oi_intelligence']['smart_money_direction']}")
        logger.info(f"🚨 RECOMMENDATION: {recommendation['action']} (Confidence: {recommendation['confidence']:.0%})")
        logger.info(f"💡 Reasoning: {recommendation['reasoning']}")
        logger.info("=" * 80)

# =============================================================================
# PUBLIC METHODS FOR MAIN BOT INTEGRATION
# =============================================================================
    def get_enhancement_for_main_bot(self, main_bot_analysis: Dict) -> Dict[str, Any]:
        """Provide enhancement intelligence for main bot recommendations"""
        if not self.completed_candles:
            return {'enhancement': 'INSUFFICIENT_DATA', 'boost': 0.0}
        latest_candle_analysis = self._get_latest_analysis()
        if not latest_candle_analysis:
            return {'enhancement': 'NO_RECENT_ANALYSIS', 'boost': 0.0}
        # Compare main bot signal with candle intelligence
        main_signal = main_bot_analysis.get('verdict', 'NEUTRAL')
        candle_signal = latest_candle_analysis['trade_recommendation']['action']
        candle_confidence = latest_candle_analysis['trade_recommendation']['confidence']
        # Calculate enhancement
        if self._signals_aligned(main_signal, candle_signal):
            confidence_boost = candle_confidence * 0.3  # Up to 30% boost
            enhancement = f"✅ Candle analysis CONFIRMS {main_signal}"
        elif self._signals_conflicting(main_signal, candle_signal):
            confidence_boost = -candle_confidence * 0.2  # Up to 20% reduction
            enhancement = f"⚠️ Candle analysis CONTRADICTS - Suggests {candle_signal}"
        else:
            confidence_boost = 0.1  # Small neutral boost
            enhancement = "🔍 Candle analysis provides additional context"
        return {
            'enhancement': enhancement,
            'confidence_boost': confidence_boost,
            'candle_signal': candle_signal,
            'candle_confidence': candle_confidence,
            'reasoning': latest_candle_analysis['trade_recommendation']['reasoning']
        }

    def _get_latest_analysis(self) -> Optional[Dict]:
        """Get the most recent completed candle analysis"""
        # This would store the latest analysis result
        # For now, return None - implement based on your storage strategy
        return None

    def _signals_aligned(self, main_signal: str, candle_signal: str) -> bool:
        """Check if main bot and candle signals are aligned"""
        bullish_signals = ['BULLISH', 'EARLY_BULLISH', 'BUY']
        bearish_signals = ['BEARISH', 'EARLY_BEARISH', 'SELL']
        return ((main_signal in bullish_signals and candle_signal == 'BUY') or
                (main_signal in bearish_signals and candle_signal == 'SELL'))

    def _signals_conflicting(self, main_signal: str, candle_signal: str) -> bool:
        """Check if main bot and candle signals are conflicting"""
        bullish_signals = ['BULLISH', 'EARLY_BULLISH', 'BUY']
        bearish_signals = ['BEARISH', 'EARLY_BEARISH', 'SELL']
        return ((main_signal in bullish_signals and candle_signal == 'SELL') or
                (main_signal in bearish_signals and candle_signal == 'BUY'))

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status for monitoring"""
        return {
            'system_active': True,
            'candles_completed': len(self.completed_candles),
            'patterns_detected': self.total_patterns_detected,
            'accuracy_rate': self.accuracy_rate,
            'current_candle_progress': self._get_candle_progress(datetime.now()),
            'last_analysis_time': self.completed_candles[-1].timestamp.isoformat() if self.completed_candles else None
        }

# =============================================================================
# EXPORT FOR MAIN BOT INTEGRATION
# =============================================================================
if __name__ == "__main__":
    # Test the system
    logger.info("🧪 Testing Candle Intelligence System...")
    candle_system = CandleIntelligenceSystem()
    # Sample test data
    test_snapshot = {
        'underlying_value': 19850.0,
        'CE_VOL': 45000,
        'PE_VOL': 52000,
        'CE_OI': 1250000,
        'PE_OI': 1180000,
        'OI_PCR': 0.944
    }
    result = candle_system.process_snapshot(test_snapshot)
    logger.info(f"Test result: {result}")
    logger.info("✅ Candle Intelligence System test completed")