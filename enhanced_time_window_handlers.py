# enhanced_time_window_handlers.py - TEST VERSION FOR EVENING HOURS

# WARNING: This is a modified version for testing outside market hours.
# Time ranges shifted to 6:00 PM - 12:30 AM IST (approx 9-hour shift).
# Restore original file after testing!

from datetime import time, datetime

from collections import deque

from typing import Dict, Any, List, Tuple, Optional

import logging

import numpy as np

logger = logging.getLogger(__name__)

# Enhanced TIME_WINDOWS with Research-Based Insights - Shifted for Testing
TIME_WINDOWS = {
    # Pre-market phase - Order collection and sentiment building (Shifted: Original 9:00-9:08 -> 18:00-18:08)
    "pre_market_entry": {
        "time_range": (time(18, 0), time(18, 8)),
        "phase_type": "PREPARATION",
        "volatility_expected": "LOW",
        "volume_pattern": "INSTITUTIONAL_ORDERS",
        "key_focus": "overnight_gap_analysis",
        "direction_change_probability": 0.0  # No active trading
    },
    # Pre-opening matching - Price discovery (Shifted: 9:08-9:15 -> 18:08-18:15)
    "pre_open_matching": {
        "time_range": (time(18, 8), time(18, 15)),
        "phase_type": "PRICE_DISCOVERY",
        "volatility_expected": "MEDIUM",
        "volume_pattern": "ORDER_MATCHING",
        "key_focus": "opening_price_prediction",
        "direction_change_probability": 0.0  # System matching
    },
    # CRITICAL: Opening explosion - Highest volatility (Shifted: 9:15-9:20 -> 18:15-18:20)
    "opening_explosion": {
        "time_range": (time(18, 15), time(18, 20)),
        "phase_type": "EXPLOSIVE_VOLATILITY",
        "volatility_expected": "VERY_HIGH",
        "volume_pattern": "PEAK_VOLUME_5X",
        "key_focus": "gap_fill_patterns",
        "direction_change_probability": 0.90,  # Research: 90% probability
        "research_note": "Highest direction change window - overnight news impact"
    },
    # Initial discovery - Pattern formation (Shifted: 9:20-9:30 -> 18:20-18:30)
    "initial_discovery": {
        "time_range": (time(18, 20), time(18, 30)),
        "phase_type": "PATTERN_FORMATION",
        "volatility_expected": "HIGH",
        "volume_pattern": "SUSTAINED_HIGH_3X",
        "key_focus": "hammer_doji_engulfing_patterns",
        "direction_change_probability": 0.80,  # Research: 80% probability
        "research_note": "Initial range formation with high reliability patterns"
    },
    # GOLDEN WINDOW: Maximum direction changes (RESEARCH FOCUS) (Shifted: 9:30-9:45 -> 18:30-18:45)
    "golden_flip": {
        "time_range": (time(18, 30), time(18, 45)),
        "phase_type": "GOLDEN_WINDOW",
        "volatility_expected": "VERY_HIGH",
        "volume_pattern": "MAXIMUM_ACTIVITY_2-3X",
        "key_focus": "breakout_breakdown_patterns",
        "direction_change_probability": 0.85,  # Research: 85-90% probability
        "research_note": "60% of daily OI creation - Maximum predictive power",
        "special_windows": {
            "18:40-18:41": {"focus": "volume_surge_institutional", "success_rate": 0.78},
            "18:41-18:42": {"focus": "direction_confirmation", "success_rate": 0.82},
            "18:42-18:43": {"focus": "peak_volatility_hammer_doji", "success_rate": 0.85},
            "18:43-18:44": {"focus": "momentum_acceleration", "success_rate": 0.80},
            "18:44-18:45": {"focus": "direction_establishment", "success_rate": 0.87}
        }
    },
    # Momentum continuation - Trend following (Shifted: 9:45-10:00 -> 18:45-19:00)
    "momentum_continuation": {
        "time_range": (time(18, 45), time(19, 0)),
        "phase_type": "MOMENTUM_FOLLOW",
        "volatility_expected": "HIGH",
        "volume_pattern": "HIGH_MOMENTUM_2X",
        "key_focus": "continuation_patterns",
        "direction_change_probability": 0.75,  # Research: 75% probability
        "research_note": "High momentum volume continuation phase"
    },
    # Trend establishment - Morning stability (Shifted: 10:00-11:30 -> 19:00-20:30)
    "trend_establishment": {
        "time_range": (time(19, 0), time(20, 30)),
        "phase_type": "TREND_DEVELOPMENT",
        "volatility_expected": "MODERATE",
        "volume_pattern": "STEADY_MODERATE",
        "key_focus": "trend_following_patterns",
        "direction_change_probability": 0.65,  # Research: 65% probability
        "research_note": "Trend establishment with moderate volatility"
    },
    # Morning stability - Lower activity (Shifted: 11:30-12:00 -> 20:30-21:00)
    "morning_stability": {
        "time_range": (time(20, 30), time(21, 0)),
        "phase_type": "STABILITY",
        "volatility_expected": "LOW",
        "volume_pattern": "MODERATE_WITH_SPIKES",
        "key_focus": "range_bound_patterns",
        "direction_change_probability": 0.55,  # Research: 55% probability
        "research_note": "Morning session close activity"
    },
    # Lunch lull - Minimal activity (AVOID TRADING) (Shifted: 12:00-13:30 -> 21:00-22:30)
    "lunch_lull": {
        "time_range": (time(21, 0), time(22, 30)),
        "phase_type": "LUNCH_BREAK",
        "volatility_expected": "VERY_LOW",
        "volume_pattern": "MINIMAL_ACTIVITY",
        "key_focus": "avoid_trading",
        "direction_change_probability": 0.20,  # Research: 20% probability
        "research_note": "AVOID_ALL_TRADES - Lunch break effect, high trap probability"
    },
    # Afternoon revival - Activity pickup (Shifted: 13:30-14:00 -> 22:30-23:00)
    "afternoon_revival": {
        "time_range": (time(22, 30), time(23, 0)),
        "phase_type": "REVIVAL",
        "volatility_expected": "MODERATE",
        "volume_pattern": "GRADUAL_INCREASE",
        "key_focus": "revival_patterns",
        "direction_change_probability": 0.60,  # Research: 60% probability
        "research_note": "Afternoon session restart with fresh positioning"
    },
    # Mid afternoon - Building activity (Shifted: 14:00-14:30 -> 23:00-23:30)
    "mid_afternoon": {
        "time_range": (time(23, 0), time(23, 30)),
        "phase_type": "BUILDING_ACTIVITY",
        "volatility_expected": "MODERATE",
        "volume_pattern": "MODERATE_ACTIVITY",
        "key_focus": "moderate_volatility_patterns",
        "direction_change_probability": 0.65,  # Research: 65% probability
        "research_note": "Moderate institutional activity"
    },
    # Pre-close positioning - Increasing activity (Shifted: 14:30-15:00 -> 23:30-00:00 next day)
    "pre_close_positioning": {
        "time_range": (time(23, 30), time(0, 0)),
        "phase_type": "PRE_CLOSE",
        "volatility_expected": "HIGH",
        "volume_pattern": "INCREASING_VOLUME",
        "key_focus": "position_adjustment_patterns",
        "direction_change_probability": 0.75,  # Research: 75% probability
        "research_note": "Pre-close positioning and smart money adjustments"
    },
    # Closing rush - Second highest activity (Shifted: 15:00-15:30 -> 00:00-00:30 next day)
    "closing_rush": {
        "time_range": (time(0, 0), time(0, 30)),
        "phase_type": "CLOSING_EXPLOSION",
        "volatility_expected": "VERY_HIGH",
        "volume_pattern": "PEAK_CLOSING_4X",
        "key_focus": "closing_patterns",
        "direction_change_probability": 0.85,  # Research: 85% probability
        "research_note": "Second highest direction change probability - Position squaring"
    }
}

# Enhanced MarketState with Bot Integration
class EnhancedTimeWindowState:
    """Enhanced market state specifically designed for time window analysis and bot integration."""
    def __init__(self):
        # Core market data (matching main bot structure)
        self.current_snapshot = {}
        self.history_5min = deque(maxlen=500)
        self.volume_history = deque(maxlen=50)
        self.oi_history = deque(maxlen=50)

        # Time window specific data
        self.current_window = None
        self.window_start_time = None
        self.window_analytics = {}

        # Pattern detection results
        self.detected_patterns = []
        self.volume_analysis = {}
        self.oi_analysis = {}

        # Performance tracking
        self.window_predictions = deque(maxlen=100)
        self.accuracy_by_window = {}

        # Research-based metrics
        self.direction_changes_detected = 0
        self.successful_predictions = 0

        logger.info("🕐 Enhanced Time Window State initialized")

    def update_market_data(self, snapshot: Dict[str, Any]) -> None:
        """Update market data and analyze time window context."""
        self.current_snapshot = snapshot
        self.history_5min.append(snapshot)

        # Extract volume and OI data (standardized field names)
        ce_vol = snapshot.get('CE_VOL', 0)
        pe_vol = snapshot.get('PE_VOL', 0)
        ce_oi = snapshot.get('CE_OI', 0)
        pe_oi = snapshot.get('PE_OI', 0)

        self.volume_history.append({
            'ce_vol': ce_vol,
            'pe_vol': pe_vol,
            'total_vol': ce_vol + pe_vol,
            'volume_bias': pe_vol - ce_vol,
            'timestamp': snapshot.get('timestamp', datetime.now().isoformat())
        })

        self.oi_history.append({
            'ce_oi': ce_oi,
            'pe_oi': pe_oi,
            'total_oi': ce_oi + pe_oi,
            'oi_pcr': pe_oi / ce_oi if ce_oi > 0 else 0,
            'timestamp': snapshot.get('timestamp', datetime.now().isoformat())
        })

    def get_window_context(self) -> Dict[str, Any]:
        """Get current time window context and analysis."""
        return {
            'current_window': self.current_window,
            'window_analytics': self.window_analytics,
            'detected_patterns': self.detected_patterns[-5:],  # Recent patterns
            'volume_analysis': self.volume_analysis,
            'oi_analysis': self.oi_analysis,
            'accuracy_stats': self.accuracy_by_window
        }

# ENHANCED HANDLER FUNCTIONS WITH RESEARCH-BASED LOGIC
def handle_pre_market_entry(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle pre-market order entry phase."""
    logger.info("🌅 PRE-MARKET ENTRY: Analyzing overnight gap potential")
    prev_close = snapshot.get('prev_close', 0)
    current_price = snapshot.get('underlying_value', 0)
    if prev_close > 0:
        gap_percent = ((current_price - prev_close) / prev_close) * 100
        gap_analysis = {
            'gap_percent': gap_percent,
            'gap_type': 'BULLISH_GAP' if gap_percent > 0.2 else 'BEARISH_GAP' if gap_percent < -0.2 else 'NO_GAP',
            'expected_opening_volatility': 'HIGH' if abs(gap_percent) > 0.5 else 'MODERATE'
        }
        state.window_analytics['gap_analysis'] = gap_analysis
        return {
            'phase': 'pre_market_entry',
            'action': 'PREPARE',
            'analysis': gap_analysis,
            'recommendation': 'Monitor for opening explosion signals'
        }
    return {'phase': 'pre_market_entry', 'action': 'WAIT', 'analysis': {}}

def handle_pre_open_matching(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle pre-open matching phase."""
    logger.info("⚙️ PRE-OPEN MATCHING: System price discovery phase")
    analysis = {
        'phase_type': 'PRICE_DISCOVERY',
        'expected_volatility': 'MEDIUM',
        'research_note': 'System order matching - No active trading'
    }
    return {
        'phase': 'pre_open_matching',
        'action': 'MONITOR_ONLY',
        'analysis': analysis,
        'trade_signal': 'NONE'
    }

def handle_opening_explosion(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle opening explosion phase - CRITICAL RESEARCH WINDOW."""
    logger.info("💥 OPENING EXPLOSION: Highest volatility window - 90% direction change probability")
    if len(state.volume_history) >= 2:
        current_vol = state.volume_history[-1]
        prev_vol = state.volume_history[-2] if len(state.volume_history) > 1 else current_vol
        volume_surge = current_vol['total_vol'] / prev_vol['total_vol'] if prev_vol['total_vol'] > 0 else 1
        # Research-based analysis
        analysis = {
            'volume_surge_ratio': volume_surge,
            'is_peak_volume': volume_surge > 5.0,  # Research: 5x average
            'direction_change_probability': 0.90,
            'pattern_reliability': 'VERY_HIGH',
            'research_note': 'Overnight news impact - highest direction change window'
        }
        # Detect gap patterns
        current_price = snapshot.get('underlying_value', 0)
        open_price = snapshot.get('open_price', current_price)
        prev_close = snapshot.get('prev_close', current_price)
        if prev_close > 0:
            gap_percent = ((open_price - prev_close) / prev_close) * 100
            if abs(gap_percent) > 0.3:
                pattern = 'GAP_OPENING'
                if volume_surge > 3.0:
                    recommendation = 'HIGH_CONFIDENCE_TRADE' if gap_percent > 0 else 'HIGH_CONFIDENCE_SHORT'
                else:
                    recommendation = 'WAIT_FOR_VOLUME_CONFIRMATION'
            else:
                pattern = 'NORMAL_OPENING'
                recommendation = 'MONITOR_FOR_BREAKOUT'
        else:
            pattern = 'INSUFFICIENT_DATA'
            recommendation = 'COLLECT_MORE_DATA'
        analysis.update({
            'detected_pattern': pattern,
            'gap_percent': gap_percent if 'gap_percent' in locals() else 0,
            'confidence_level': 'VERY_HIGH' if volume_surge > 3.0 else 'HIGH'
        })
        state.detected_patterns.append({
            'timestamp': datetime.now(),
            'pattern': pattern,
            'confidence': analysis['confidence_level'],
            'window': 'opening_explosion'
        })
        return {
            'phase': 'opening_explosion',
            'action': recommendation,
            'analysis': analysis,
            'trade_signal': 'STRONG' if analysis['confidence_level'] == 'VERY_HIGH' else 'MODERATE'
        }
    return {'phase': 'opening_explosion', 'action': 'COLLECT_DATA', 'analysis': {}}

def handle_initial_discovery(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle initial discovery phase - Pattern formation window."""
    logger.info("🔍 INITIAL DISCOVERY: Pattern formation with 80% direction change probability")
    if len(state.volume_history) >= 2:
        current_vol = state.volume_history[-1]
        prev_vol = state.volume_history[-2]
        volume_analysis = {
            'change': current_vol['total_vol'] - prev_vol['total_vol'],
            'is_sustained_high': current_vol['total_vol'] > prev_vol['total_vol'] * 3,  # 3x threshold
            'bias': current_vol['volume_bias']
        }
        # Pattern reliability from research
        analysis = {
            'volume_analysis': volume_analysis,
            'direction_change_probability': 0.80,
            'key_patterns': 'hammer_doji_engulfing',
            'research_note': 'Initial range formation with high reliability patterns'
        }
        if volume_analysis['is_sustained_high']:
            pattern = 'STRONG_PATTERN_FORMATION'
            confidence = 'HIGH'
            recommendation = 'PATTERN_TRADE'
        else:
            pattern = 'WEAK_FORMATION'
            confidence = 'MEDIUM'
            recommendation = 'MONITOR'
        analysis['detected_pattern'] = pattern
        analysis['confidence_level'] = confidence
        state.detected_patterns.append({
            'timestamp': datetime.now(),
            'pattern': pattern,
            'confidence': confidence,
            'window': 'initial_discovery'
        })
        return {
            'phase': 'initial_discovery',
            'action': recommendation,
            'analysis': analysis,
            'trade_signal': 'STRONG' if confidence == 'HIGH' else 'MODERATE'
        }
    return {'phase': 'initial_discovery', 'action': 'COLLECT_DATA', 'analysis': {}}

def handle_golden_flip(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle golden flip phase - MAXIMUM RESEARCH FOCUS."""
    current_time = datetime.now().time()
    logger.info(f"🏆 GOLDEN FLIP: {current_time} - Maximum direction change window (85-90% probability)")
    # Minute-by-minute analysis based on research
    minute_analysis = {}
    if time(18, 40) <= current_time <= time(18, 41):
        minute_analysis = {
            'specific_window': '18:40-18:41',
            'focus': 'volume_surge_institutional',
            'success_rate': 0.78,
            'key_indicator': 'institutional_activity_detection'
        }
    elif time(18, 41) <= current_time <= time(18, 42):
        minute_analysis = {
            'specific_window': '18:41-18:42',
            'focus': 'direction_confirmation',
            'success_rate': 0.82,
            'key_indicator': 'continuation_or_reversal_patterns'
        }
    elif time(18, 42) <= current_time <= time(18, 43):
        minute_analysis = {
            'specific_window': '18:42-18:43',
            'focus': 'peak_volatility_hammer_doji',
            'success_rate': 0.85,
            'key_indicator': 'highest_probability_hammer_doji_formation'
        }
    elif time(18, 43) <= current_time <= time(18, 44):
        minute_analysis = {
            'specific_window': '18:43-18:44',
            'focus': 'momentum_acceleration',
            'success_rate': 0.80,
            'key_indicator': 'breakout_or_breakdown_candles'
        }
    elif time(18, 44) <= current_time <= time(18, 45):
        minute_analysis = {
            'specific_window': '18:44-18:45',
            'focus': 'direction_establishment',
            'success_rate': 0.87,
            'key_indicator': 'trend_confirmation_for_next_hour'
        }

    # Volume-OI analysis
    if len(state.volume_history) >= 2 and len(state.oi_history) >= 2:
        curr_vol = state.volume_history[-1]
        prev_vol = state.volume_history[-2]
        curr_oi = state.oi_history[-1]
        prev_oi = state.oi_history[-2]

        volume_analysis = {
            'volume_change': curr_vol['total_vol'] - prev_vol['total_vol'],
            'volume_bias': curr_vol['volume_bias'],
            'is_high_volume': curr_vol['total_vol'] > prev_vol['total_vol'] * 2,
            'bias_intensity': abs(curr_vol['volume_bias']) / curr_vol['total_vol'] if curr_vol['total_vol'] > 0 else 0
        }
        oi_analysis = {
            'oi_change': curr_oi['total_oi'] - prev_oi['total_oi'],
            'oi_pcr_change': curr_oi['oi_pcr'] - prev_oi['oi_pcr'],
            'new_position_creation': curr_oi['total_oi'] > prev_oi['total_oi'],
            'smart_money_flow': 'BULLISH' if curr_oi['oi_pcr'] < prev_oi['oi_pcr'] else 'BEARISH'
        }

        price_change = snapshot.get('underlying_value', 0) - snapshot.get('prev_price', 0)

        # pattern detection + reversal override
        if price_change > 0 and volume_analysis['volume_bias'] > 15000:
            pattern = 'BEARISH_DIVERGENCE'; confidence = 'VERY_HIGH'; recommendation = 'STRONG_SELL_SIGNAL'
        elif price_change < 0 and volume_analysis['volume_bias'] < -15000:
            pattern = 'BULLISH_DIVERGENCE'; confidence = 'VERY_HIGH'; recommendation = 'STRONG_BUY_SIGNAL'
        elif volume_analysis['is_high_volume'] and oi_analysis['new_position_creation']:
            # override pullback reversal
            if price_change < 0:
                pattern = 'BULLISH_OI_VOLUME_REVERSAL'; confidence = 'VERY_HIGH'; recommendation = 'STRONG_BUY_SIGNAL'
            else:
                pattern = 'BEARISH_OI_VOLUME_REVERSAL'; confidence = 'VERY_HIGH'; recommendation = 'STRONG_SELL_SIGNAL'
        else:
            pattern = 'CONSOLIDATION_PHASE'; confidence = 'MEDIUM'; recommendation = 'WAIT_FOR_CLEAR_SIGNAL'

        comprehensive_analysis = {
            'minute_analysis': minute_analysis,
            'volume_analysis': volume_analysis,
            'oi_analysis': oi_analysis,
            'detected_pattern': pattern,
            'confidence_level': confidence,
            'direction_change_probability': 0.85,
            'research_validation': '60% of daily OI creation occurs in this window'
        }
        state.volume_analysis = volume_analysis
        state.oi_analysis = oi_analysis
        state.detected_patterns.append({
            'timestamp': datetime.now(),
            'pattern': pattern,
            'confidence': confidence,
            'window': 'golden_flip',
            'specific_time': minute_analysis.get('specific_window', 'unknown')
        })
        return {
            'phase': 'golden_flip',
            'action': recommendation,
            'analysis': comprehensive_analysis,
            'trade_signal': 'CRITICAL' if confidence == 'VERY_HIGH' else 'STRONG'
        }

    return {'phase': 'golden_flip', 'action': 'COLLECT_DATA', 'analysis': minute_analysis}
    
def handle_momentum_continuation(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle momentum continuation phase."""
    logger.info("🚀 MOMENTUM CONTINUATION: 75% direction change probability")
    analysis = {
        'phase_type': 'MOMENTUM_FOLLOW',
        'direction_change_probability': 0.75,
        'key_patterns': 'continuation_patterns',
        'research_note': 'High momentum volume continuation phase'
    }
    return {
        'phase': 'momentum_continuation',
        'action': 'TREND_FOLLOW',
        'analysis': analysis,
        'trade_signal': 'MODERATE'
    }

def handle_trend_establishment(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle trend establishment phase."""
    logger.info("📈 TREND ESTABLISHMENT: 65% direction change probability")
    analysis = {
        'phase_type': 'TREND_DEVELOPMENT',
        'direction_change_probability': 0.65,
        'key_patterns': 'trend_following_patterns',
        'research_note': 'Trend establishment with moderate volatility'
    }
    return {
        'phase': 'trend_establishment',
        'action': 'TREND_TRADE',
        'analysis': analysis,
        'trade_signal': 'MODERATE'
    }

def handle_morning_stability(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle morning stability phase."""
    logger.info("🧘 MORNING STABILITY: 55% direction change probability")
    analysis = {
        'phase_type': 'STABILITY',
        'direction_change_probability': 0.55,
        'key_patterns': 'range_bound_patterns',
        'research_note': 'Morning session close activity'
    }
    return {
        'phase': 'morning_stability',
        'action': 'RANGE_TRADE',
        'analysis': analysis,
        'trade_signal': 'LOW'
    }

def handle_lunch_lull(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle lunch lull phase - AVOID TRADING."""
    logger.info("🍽️ LUNCH LULL: Avoid trading - High trap probability (20% direction change)")
    analysis = {
        'phase_type': 'LUNCH_BREAK',
        'direction_change_probability': 0.20,  # Research: Very low
        'trap_probability': 'HIGH',
        'research_recommendation': 'AVOID_ALL_TRADES',
        'reasoning': 'Minimal participation leads to false signals and traps'
    }
    return {
        'phase': 'lunch_lull',
        'action': 'AVOID_TRADING',
        'analysis': analysis,
        'trade_signal': 'NONE'
    }

def handle_afternoon_revival(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle afternoon revival phase."""
    logger.info("🌞 AFTERNOON REVIVAL: 60% direction change probability")
    analysis = {
        'phase_type': 'REVIVAL',
        'direction_change_probability': 0.60,
        'key_patterns': 'revival_patterns',
        'research_note': 'Afternoon session restart with fresh positioning'
    }
    return {
        'phase': 'afternoon_revival',
        'action': 'REVIVAL_TRADE',
        'analysis': analysis,
        'trade_signal': 'MODERATE'
    }

def handle_mid_afternoon(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle mid-afternoon phase."""
    logger.info("⏳ MID AFTERNOON: 65% direction change probability")
    analysis = {
        'phase_type': 'BUILDING_ACTIVITY',
        'direction_change_probability': 0.65,
        'key_patterns': 'moderate_volatility_patterns',
        'research_note': 'Moderate institutional activity'
    }
    return {
        'phase': 'mid_afternoon',
        'action': 'MODERATE_TRADE',
        'analysis': analysis,
        'trade_signal': 'MODERATE'
    }

def handle_pre_close_positioning(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle pre-close positioning phase."""
    logger.info("📉 PRE-CLOSE POSITIONING: 75% direction change probability")
    analysis = {
        'phase_type': 'PRE_CLOSE',
        'direction_change_probability': 0.75,
        'key_patterns': 'position_adjustment_patterns',
        'research_note': 'Pre-close positioning and smart money adjustments'
    }
    return {
        'phase': 'pre_close_positioning',
        'action': 'POSITION_TRADE',
        'analysis': analysis,
        'trade_signal': 'STRONG'
    }

def handle_closing_rush(snapshot: Dict, state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Handle closing rush phase - Second highest activity."""
    logger.info("🏁 CLOSING RUSH: Second highest direction change probability (85%)")
    if len(state.volume_history) >= 2 and len(state.oi_history) >= 2:
        current_vol = state.volume_history[-1]
        current_oi = state.oi_history[-1]
        # Closing-specific analysis
        closing_analysis = {
            'volume_surge': current_vol['total_vol'] > 1000000,  # High volume threshold
            'position_unwinding': current_oi['total_oi'] < state.oi_history[-2]['total_oi'],
            'direction_change_probability': 0.85,  # Research: Second highest
            'phase_type': 'POSITION_SQUARING'
        }
        if closing_analysis['volume_surge'] and closing_analysis['position_unwinding']:
            pattern = 'HEAVY_POSITION_SQUARING'
            recommendation = 'SCALPING_OPPORTUNITY'
            confidence = 'HIGH'
        elif closing_analysis['volume_surge']:
            pattern = 'CLOSING_VOLUME_SPIKE'
            recommendation = 'MOMENTUM_TRADE'
            confidence = 'MEDIUM'
        else:
            pattern = 'NORMAL_CLOSING'
            recommendation = 'MONITOR_ONLY'
            confidence = 'LOW'
        closing_analysis.update({
            'detected_pattern': pattern,
            'confidence_level': confidence
        })
        state.detected_patterns.append({
            'timestamp': datetime.now(),
            'pattern': pattern,
            'confidence': confidence,
            'window': 'closing_rush'
        })
        return {
            'phase': 'closing_rush',
            'action': recommendation,
            'analysis': closing_analysis,
            'trade_signal': 'STRONG' if confidence == 'HIGH' else 'MODERATE'
        }
    return {'phase': 'closing_rush', 'action': 'MONITOR', 'analysis': {}}

# Create handler mapping with all functions implemented
ENHANCED_WINDOW_HANDLERS = {
    "pre_market_entry": handle_pre_market_entry,
    "pre_open_matching": handle_pre_open_matching,
    "opening_explosion": handle_opening_explosion,
    "initial_discovery": handle_initial_discovery,
    "golden_flip": handle_golden_flip,
    "momentum_continuation": handle_momentum_continuation,
    "trend_establishment": handle_trend_establishment,
    "morning_stability": handle_morning_stability,
    "lunch_lull": handle_lunch_lull,
    "afternoon_revival": handle_afternoon_revival,
    "mid_afternoon": handle_mid_afternoon,
    "pre_close_positioning": handle_pre_close_positioning,
    "closing_rush": handle_closing_rush
}

# MAIN INTEGRATION FUNCTIONS
def get_current_time_window(current_time: datetime = None) -> Tuple[str, Dict]:
    """Get current time window and its configuration."""
    if current_time is None:
        current_time = datetime.now()
    current_time_obj = current_time.time()
    for window_name, window_config in TIME_WINDOWS.items():
        start_time, end_time = window_config["time_range"]
        # Handle cross-midnight ranges (e.g., 23:30 to 00:00)
        if start_time > end_time:  # Crosses midnight
            if current_time_obj >= start_time or current_time_obj <= end_time:
                return window_name, window_config
        elif start_time <= current_time_obj <= end_time:
            return window_name, window_config
    return "after_hours", {"phase_type": "CLOSED", "direction_change_probability": 0.0}

def process_time_window_analysis(snapshot: Dict[str, Any], state: EnhancedTimeWindowState) -> Dict[str, Any]:
    """Main function to process time window analysis - INTEGRATION POINT."""
    current_time = datetime.now()
    window_name, window_config = get_current_time_window(current_time)
    # Update state
    state.current_window = window_name
    state.window_start_time = current_time if state.window_start_time is None else state.window_start_time
    state.update_market_data(snapshot)
    # Get handler and process
    handler = ENHANCED_WINDOW_HANDLERS.get(window_name)
    if handler:
        result = handler(snapshot, state)
        result['window_config'] = window_config
        result['timestamp'] = current_time.isoformat()
        # Update accuracy tracking
        if window_name not in state.accuracy_by_window:
            state.accuracy_by_window[window_name] = {'correct': 0, 'total': 0}
        logger.info(f"🕐 Time Window: {window_name} | Action: {result.get('action', 'NONE')} | Signal: {result.get('trade_signal', 'NONE')}")
        return result
    return {
        'phase': window_name,
        'action': 'NO_HANDLER',
        'analysis': {},
        'window_config': window_config,
        'timestamp': current_time.isoformat()
    }

# Export for integration
__all__ = [
    "TIME_WINDOWS",
    "EnhancedTimeWindowState",
    "ENHANCED_WINDOW_HANDLERS",
    "get_current_time_window",
    "process_time_window_analysis"
]
