# CANDLESTICK PATTERN RECOGNITION SYSTEM FOR YOUR TRADING BOT
# Add this to your v.py file to detect Doji, Hammer, Morning Star, Evening Star patterns

import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

class CandlestickPatternRecognizer:
    """
    Advanced Candlestick Pattern Recognition System
    Detects: Doji, Hammer, Shooting Star, Morning Star, Evening Star, Engulfing patterns
    """
    
    def __init__(self):
        self.patterns_detected = []
        self.pattern_history = []
        
    def analyze_candle_patterns(self, ohlc_data: List[Dict]) -> Dict:
        """
        Main function to analyze candlestick patterns
        ohlc_data: List of dictionaries with 'open', 'high', 'low', 'close', 'volume'
        """
        if len(ohlc_data) < 3:
            return {"status": "insufficient_data", "patterns": []}
        
        patterns_found = []
        current_candle = ohlc_data[-1]
        
        # Single candle patterns
        doji_result = self.detect_doji(current_candle)
        if doji_result['detected']:
            patterns_found.append(doji_result)
            
        hammer_result = self.detect_hammer(current_candle)
        if hammer_result['detected']:
            patterns_found.append(hammer_result)
            
        shooting_star_result = self.detect_shooting_star(current_candle)
        if shooting_star_result['detected']:
            patterns_found.append(shooting_star_result)
        
        # Multi-candle patterns (need at least 3 candles)
        if len(ohlc_data) >= 3:
            morning_star_result = self.detect_morning_star(ohlc_data[-3:])
            if morning_star_result['detected']:
                patterns_found.append(morning_star_result)
                
            evening_star_result = self.detect_evening_star(ohlc_data[-3:])
            if evening_star_result['detected']:
                patterns_found.append(evening_star_result)
        
        # Two-candle patterns
        if len(ohlc_data) >= 2:
            engulfing_result = self.detect_engulfing_pattern(ohlc_data[-2:])
            if engulfing_result['detected']:
                patterns_found.append(engulfing_result)
        
        return {
            "status": "analysis_complete",
            "patterns": patterns_found,
            "total_patterns": len(patterns_found),
            "candle_analyzed": current_candle,
            "timestamp": "current"
        }
    
    def detect_doji(self, candle: Dict) -> Dict:
        """Detect Doji pattern - open and close are very close"""
        o, h, l, c = candle['open'], candle['high'], candle['low'], candle['close']
        
        body = abs(c - o)
        range_size = h - l
        
        # Doji: body is less than 10% of the total range
        if range_size > 0 and body / range_size <= 0.1:
            
            # Determine doji type
            upper_wick = h - max(o, c)
            lower_wick = min(o, c) - l
            
            if upper_wick > lower_wick * 2:
                doji_type = "Dragonfly Doji"
                signal = "BULLISH"
            elif lower_wick > upper_wick * 2:
                doji_type = "Gravestone Doji"
                signal = "BEARISH"
            else:
                doji_type = "Standard Doji"
                signal = "NEUTRAL"
            
            return {
                "detected": True,
                "pattern": "DOJI",
                "type": doji_type,
                "signal": signal,
                "confidence": 85,
                "description": f"{doji_type} detected - Market indecision",
                "body_percentage": (body / range_size) * 100,
                "recommendation": f"Watch for next candle confirmation - {signal} bias"
            }
        
        return {"detected": False}
    
    def detect_hammer(self, candle: Dict) -> Dict:
        """Detect Hammer pattern - long lower wick, small body at top"""
        o, h, l, c = candle['open'], candle['high'], candle['low'], candle['close']
        
        body = abs(c - o)
        range_size = h - l
        lower_wick = min(o, c) - l
        upper_wick = h - max(o, c)
        
        if range_size == 0:
            return {"detected": False}
        
        # Hammer criteria:
        # 1. Lower wick at least 2x the body
        # 2. Upper wick very small (less than body)
        # 3. Body in upper portion of range
        
        if (lower_wick >= body * 2 and 
            upper_wick <= body and 
            min(o, c) > l + (range_size * 0.6)):
            
            hammer_type = "Hammer" if c > o else "Hanging Man"
            signal = "BULLISH" if hammer_type == "Hammer" else "BEARISH"
            
            return {
                "detected": True,
                "pattern": "HAMMER",
                "type": hammer_type,
                "signal": signal,
                "confidence": 80,
                "description": f"{hammer_type} - Strong reversal signal",
                "lower_wick_ratio": lower_wick / body if body > 0 else 0,
                "recommendation": f"Strong {signal} reversal signal - Consider entry"
            }
        
        return {"detected": False}
    
    def detect_shooting_star(self, candle: Dict) -> Dict:
        """Detect Shooting Star pattern - long upper wick, small body at bottom"""
        o, h, l, c = candle['open'], candle['high'], candle['low'], candle['close']
        
        body = abs(c - o)
        range_size = h - l
        upper_wick = h - max(o, c)
        lower_wick = min(o, c) - l
        
        if range_size == 0:
            return {"detected": False}
        
        # Shooting Star criteria:
        # 1. Upper wick at least 2x the body
        # 2. Lower wick very small
        # 3. Body in lower portion of range
        
        if (upper_wick >= body * 2 and 
            lower_wick <= body * 0.5 and 
            max(o, c) < h - (range_size * 0.6)):
            
            return {
                "detected": True,
                "pattern": "SHOOTING_STAR",
                "type": "Shooting Star",
                "signal": "BEARISH",
                "confidence": 78,
                "description": "Shooting Star - Bearish reversal signal",
                "upper_wick_ratio": upper_wick / body if body > 0 else 0,
                "recommendation": "BEARISH reversal signal - Consider short entry"
            }
        
        return {"detected": False}
    
    def detect_morning_star(self, candles: List[Dict]) -> Dict:
        """Detect Morning Star pattern - 3 candle bullish reversal"""
        if len(candles) < 3:
            return {"detected": False}
        
        c1, c2, c3 = candles[0], candles[1], candles[2]
        
        # Morning Star criteria:
        # 1. First candle: Large bearish candle
        # 2. Second candle: Small body (star) - gap down
        # 3. Third candle: Large bullish candle
        
        body1 = c1['open'] - c1['close']  # Bearish
        body2 = abs(c2['close'] - c2['open'])  # Small
        body3 = c3['close'] - c3['open']  # Bullish
        
        range1 = c1['high'] - c1['low']
        range2 = c2['high'] - c2['low']
        range3 = c3['high'] - c3['low']
        
        if (body1 > range1 * 0.6 and  # First candle bearish
            body2 < range2 * 0.3 and  # Second candle small
            body3 > range3 * 0.6 and  # Third candle bullish
            c2['high'] < c1['close'] and  # Gap down
            c3['close'] > (c1['open'] + c1['close']) / 2):  # Third closes above midpoint
            
            return {
                "detected": True,
                "pattern": "MORNING_STAR",
                "type": "Morning Star",
                "signal": "BULLISH",
                "confidence": 85,
                "description": "Morning Star - Strong bullish reversal pattern",
                "recommendation": "Strong BULLISH reversal - Consider long entry"
            }
        
        return {"detected": False}
    
    def detect_evening_star(self, candles: List[Dict]) -> Dict:
        """Detect Evening Star pattern - 3 candle bearish reversal"""
        if len(candles) < 3:
            return {"detected": False}
        
        c1, c2, c3 = candles[0], candles[1], candles[2]
        
        # Evening Star criteria:
        # 1. First candle: Large bullish candle
        # 2. Second candle: Small body (star) - gap up
        # 3. Third candle: Large bearish candle
        
        body1 = c1['close'] - c1['open']  # Bullish
        body2 = abs(c2['close'] - c2['open'])  # Small
        body3 = c2['open'] - c3['close']  # Bearish
        
        range1 = c1['high'] - c1['low']
        range2 = c2['high'] - c2['low']
        range3 = c3['high'] - c3['low']
        
        if (body1 > range1 * 0.6 and  # First candle bullish
            body2 < range2 * 0.3 and  # Second candle small
            body3 > range3 * 0.6 and  # Third candle bearish
            c2['low'] > c1['close'] and  # Gap up
            c3['close'] < (c1['open'] + c1['close']) / 2):  # Third closes below midpoint
            
            return {
                "detected": True,
                "pattern": "EVENING_STAR",
                "type": "Evening Star",
                "signal": "BEARISH",
                "confidence": 85,
                "description": "Evening Star - Strong bearish reversal pattern",
                "recommendation": "Strong BEARISH reversal - Consider short entry"
            }
        
        return {"detected": False}
    
    def detect_engulfing_pattern(self, candles: List[Dict]) -> Dict:
        """Detect Bullish/Bearish Engulfing patterns"""
        if len(candles) < 2:
            return {"detected": False}
        
        prev, curr = candles[0], candles[1]
        
        prev_body = abs(prev['close'] - prev['open'])
        curr_body = abs(curr['close'] - curr['open'])
        
        # Bullish Engulfing
        if (prev['close'] < prev['open'] and  # Previous bearish
            curr['close'] > curr['open'] and  # Current bullish
            curr['open'] < prev['close'] and  # Opens below prev close
            curr['close'] > prev['open']):    # Closes above prev open
            
            return {
                "detected": True,
                "pattern": "BULLISH_ENGULFING",
                "type": "Bullish Engulfing",
                "signal": "BULLISH",
                "confidence": 82,
                "description": "Bullish Engulfing - Current candle engulfs previous bearish candle",
                "recommendation": "BULLISH reversal - Strong buy signal"
            }
        
        # Bearish Engulfing
        if (prev['close'] > prev['open'] and  # Previous bullish
            curr['close'] < curr['open'] and  # Current bearish
            curr['open'] > prev['close'] and  # Opens above prev close
            curr['close'] < prev['open']):    # Closes below prev open
            
            return {
                "detected": True,
                "pattern": "BEARISH_ENGULFING",
                "type": "Bearish Engulfing",
                "signal": "BEARISH",
                "confidence": 82,
                "description": "Bearish Engulfing - Current candle engulfs previous bullish candle",
                "recommendation": "BEARISH reversal - Strong sell signal"
            }
        
        return {"detected": False}
    
    def format_pattern_output(self, pattern_results: Dict) -> str:
        """Format pattern detection results for display"""
        if not pattern_results['patterns']:
            return "📊 CANDLESTICK ANALYSIS: No significant patterns detected"
        
        output = ["🕯️ CANDLESTICK PATTERNS DETECTED:"]
        output.append("=" * 60)
        
        for i, pattern in enumerate(pattern_results['patterns'], 1):
            output.append(f"")
            output.append(f"🔍 PATTERN {i}: {pattern['pattern']}")
            output.append(f"   Type: {pattern['type']}")
            output.append(f"   Signal: {pattern['signal']}")
            output.append(f"   Confidence: {pattern['confidence']}%")
            output.append(f"   Description: {pattern['description']}")
            output.append(f"   💡 Recommendation: {pattern['recommendation']}")
        
        output.append("=" * 60)
        output.append(f"📈 Total Patterns: {pattern_results['total_patterns']}")
        
        return "\n".join(output)

# INTEGRATION STEPS FOR YOUR v.py FILE:

"""
STEP 1: Add the CandlestickPatternRecognizer class above to your v.py file

STEP 2: Initialize in your bot's __init__ method:
    self.pattern_recognizer = CandlestickPatternRecognizer()
    self.completed_candles = []  # Store completed candle data

STEP 3: Modify your candle building system to store OHLC data:
    When a 5-minute candle completes, store it as:
    
    completed_candle = {
        'open': candle_open_price,
        'high': candle_high_price, 
        'low': candle_low_price,
        'close': candle_close_price,
        'volume': total_volume
    }
    self.completed_candles.append(completed_candle)

STEP 4: Add pattern analysis to your cycle processing:
    
    # Add this in your main analysis cycle after candle completion
    if len(self.completed_candles) >= 3:
        pattern_results = self.pattern_recognizer.analyze_candle_patterns(self.completed_candles[-3:])
        
        if pattern_results['patterns']:
            pattern_output = self.pattern_recognizer.format_pattern_output(pattern_results)
            logger.info(pattern_output)
            
            # Send to Telegram
            send_telegram_msg(pattern_output)
            
            # Store in current analysis
            if hasattr(self, 'current_analysis'):
                self.current_analysis['candlestick_patterns'] = pattern_results

STEP 5: Integrate with trading decisions:
    
    # In your trading logic, check for patterns
    if hasattr(self, 'current_analysis') and 'candlestick_patterns' in self.current_analysis:
        patterns = self.current_analysis['candlestick_patterns']['patterns']
        
        for pattern in patterns:
            if pattern['confidence'] > 80:
                if pattern['signal'] == 'BULLISH':
                    logger.info(f"🔥 STRONG BULLISH PATTERN: {pattern['type']} - {pattern['confidence']}%")
                    # Add to bullish signals
                    
                elif pattern['signal'] == 'BEARISH':
                    logger.info(f"🔥 STRONG BEARISH PATTERN: {pattern['type']} - {pattern['confidence']}%")
                    # Add to bearish signals

EXPECTED OUTPUT:
================
🕯️ CANDLESTICK PATTERNS DETECTED:
============================================================

🔍 PATTERN 1: DOJI
   Type: Standard Doji
   Signal: NEUTRAL
   Confidence: 85%
   Description: Standard Doji detected - Market indecision
   💡 Recommendation: Watch for next candle confirmation - NEUTRAL bias

🔍 PATTERN 2: HAMMER
   Type: Hammer
   Signal: BULLISH
   Confidence: 80%
   Description: Hammer - Strong reversal signal
   💡 Recommendation: Strong BULLISH reversal signal - Consider entry

============================================================
📈 Total Patterns: 2
"""