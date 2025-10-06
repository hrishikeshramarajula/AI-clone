import numpy as np
import pandas as pd
from datetime import datetime, time as dt_time
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class FifteenMinPredictor:
    """Predict next 15-min price direction using gap, volume, VWAP, and timing."""
    def __init__(self):
        self.prediction_history = []
        self.accuracy_tracker = {"correct": 0, "total": 0}
        self.gap_threshold = 0.3  # 0.3% gap threshold
        self.volume_multiplier_threshold = 1.5  # 1.5x average volume
        self.vwap_deviation_threshold = 0.2  # 0.2% from VWAP
        logger.info("🔮 15-Minute Predictor initialized")

    def get_prediction(self, ohlc_data: tuple, volumes: List[float], oi_signal: Dict[str, Any], current_time=None) -> Dict[str, Any]:
        if not current_time:
            current_time = datetime.now()
        try:
            open_price, high_price, low_price, close_price = ohlc_data
            gap_signal = self._analyze_gap(open_price, close_price, current_time)
            volume_signal = self._analyze_volume_patterns(volumes, current_time)
            vwap_signal = self._analyze_vwap_relationship(ohlc_data, volumes)
            timing_signal = self._analyze_market_timing(current_time)

            # Boost weights based on OI signal strength
            weights = {"gap": 0.35, "volume": 0.30, "vwap": 0.25, "timing": 0.10}
            if oi_signal.get("direction") != "NEUTRAL":
                boost = oi_signal.get("strength", 0)
                weights["volume"] *= (1 + boost)
                weights["vwap"]   *= (1 + boost)

            combined_prediction = self._combine_signals(
                gap_signal, volume_signal, vwap_signal, timing_signal, weights=weights
            )
            confidence = self._calculate_confidence(
                gap_signal, volume_signal, vwap_signal, timing_signal
            )
            prediction_result = {
                "direction": combined_prediction,
                "confidence": confidence,
                "gap_signal": gap_signal,
                "volume_signal": volume_signal,
                "vwap_signal": vwap_signal,
                "timing_signal": timing_signal,
                "timestamp": current_time.isoformat(),
                "algorithm": "15_MIN_PREDICTOR"
            }
            self.prediction_history.append(prediction_result)
            logger.info(f"🔮 15-Min Prediction: {combined_prediction} (Confidence: {confidence:.2f})")
            return prediction_result
        except Exception as e:
            logger.error(f"❌ Error in 15-min prediction: {e}")
            return {"direction": "NEUTRAL", "confidence": 0.0, "error": str(e), "algorithm": "15_MIN_PREDICTOR"}

    def _analyze_volume_patterns(self, volumes: List[float], current_time: datetime) -> Dict[str, Any]:
        if len(volumes) < 10:
            return {"direction": "NEUTRAL", "strength": 0.0, "reason": "Insufficient volume data"}
        current_volume = volumes[-1]
        avg_volume_10 = np.mean(volumes[-10:])
        avg_volume_5 = np.mean(volumes[-5:])
        volume_ratio = current_volume / avg_volume_10 if avg_volume_10 > 0 else 1
        recent_volume_trend = avg_volume_5 / avg_volume_10 if avg_volume_10 > 0 else 1
        if volume_ratio > 2.0:
            pattern, strength = "VOLUME_EXPLOSION", 0.9
        elif volume_ratio > self.volume_multiplier_threshold:
            pattern, strength = "HIGH_VOLUME", 0.7
        elif recent_volume_trend > 1.2:
            pattern, strength = "VOLUME_BUILDING", 0.5
        elif current_volume < avg_volume_10 * 0.7:
            pattern, strength = "LOW_VOLUME", 0.2
        else:
            pattern, strength = "NORMAL_VOLUME", 0.4
        market_time = current_time.time()
        if pattern in ["VOLUME_EXPLOSION", "HIGH_VOLUME"]:
            if dt_time(9, 15) <= market_time <= dt_time(11, 30):
                direction = "BULLISH"
            elif dt_time(13, 30) <= market_time <= dt_time(15, 15):
                direction = "BEARISH"
            else:
                direction = "NEUTRAL"
        else:
            direction = "NEUTRAL"
        return {"direction": direction, "strength": strength, "pattern": pattern, "volume_ratio": volume_ratio}

    def _analyze_vwap_relationship(self, ohlc_data: tuple, volumes: List[float]) -> Dict[str, Any]:
        if len(ohlc_data) != 4 or len(volumes) < 5:
            return {"direction": "NEUTRAL", "strength": 0.0, "reason": "Insufficient data"}
        open_price, high_price, low_price, close_price = ohlc_data
        typical_price = (high_price + low_price + close_price) / 3
        recent_volumes = volumes[-5:]
        total_volume = sum(recent_volumes)
        vwap = typical_price  # Simplified for this version
        price_vwap_diff = ((close_price - vwap) / vwap) * 100
        deviation_abs = abs(price_vwap_diff)
        if deviation_abs > 0.5:
            strength = 0.8
        elif deviation_abs > 0.3:
            strength = 0.6
        elif deviation_abs > 0.1:
            strength = 0.4
        else:
            strength = 0.2
        if price_vwap_diff > self.vwap_deviation_threshold:
            direction = "BULLISH"
        elif price_vwap_diff < -self.vwap_deviation_threshold:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"
        return {"direction": direction, "strength": strength, "vwap": vwap, "current_price": close_price, "deviation_percent": price_vwap_diff}

    def _analyze_market_timing(self, current_time: datetime) -> Dict[str, Any]:
        market_time = current_time.time()
        if dt_time(9, 15) <= market_time <= dt_time(9, 45):
            phase, direction, strength = "OPENING_VOLATILE", "BULLISH", 0.7
        elif dt_time(9, 45) <= market_time <= dt_time(10, 30):
            phase, direction, strength = "MORNING_MOMENTUM", "BULLISH", 0.6
        elif dt_time(10, 30) <= market_time <= dt_time(11, 30):
            phase, direction, strength = "MID_MORNING", "NEUTRAL", 0.4
        elif dt_time(11, 30) <= market_time <= dt_time(13, 00):
            phase, direction, strength = "LUNCH_CONSOLIDATION", "NEUTRAL", 0.3
        elif dt_time(13, 00) <= market_time <= dt_time(14, 00):
            phase, direction, strength = "AFTERNOON_ACTIVITY", "NEUTRAL", 0.5
        elif dt_time(14, 00) <= market_time <= dt_time(15, 15):
            phase, direction, strength = "CLOSING_RUSH", "BEARISH", 0.6
        else:
            phase, direction, strength = "AFTER_HOURS", "NEUTRAL", 0.1
        return {"direction": direction, "strength": strength, "phase": phase}

    def _combine_signals(self, gap_signal: Dict, volume_signal: Dict, vwap_signal: Dict, timing_signal: Dict) -> str:
        weights = {"gap": 0.35, "volume": 0.30, "vwap": 0.25, "timing": 0.10}
        def direction_to_score(direction):
            return 1 if direction == "BULLISH" else -1 if direction == "BEARISH" else 0
        total_score = (
            direction_to_score(gap_signal.get("direction")) * gap_signal.get("strength", 0) * weights["gap"] +
            direction_to_score(volume_signal.get("direction")) * volume_signal.get("strength", 0) * weights["volume"] +
            direction_to_score(vwap_signal.get("direction")) * vwap_signal.get("strength", 0) * weights["vwap"] +
            direction_to_score(timing_signal.get("direction")) * timing_signal.get("strength", 0) * weights["timing"]
        )
        if total_score > 0.15:
            return "BULLISH"
        elif total_score < -0.15:
            return "BEARISH"
        return "NEUTRAL"
    
    def _calculate_confidence(self, gap_signal: Dict, volume_signal: Dict, vwap_signal: Dict, timing_signal: Dict) -> float:
        strengths = [x.get("strength", 0) for x in [gap_signal, volume_signal, vwap_signal, timing_signal]]
        directions = [x.get("direction", "NEUTRAL") for x in [gap_signal, volume_signal, vwap_signal, timing_signal]]
        bullish_count = directions.count("BULLISH")
        bearish_count = directions.count("BEARISH")
        max_agreement = max(bullish_count, bearish_count, directions.count("NEUTRAL"))
        agreement_bonus = (max_agreement - 1) * 0.1
        final_confidence = min(np.mean(strengths) + agreement_bonus, 1.0)
        return round(final_confidence, 3)
    def _analyze_gap(self, ohlc_data):
        """Analyze price gaps between candles"""
        try:
            if len(ohlc_data) < 2:
                return 0.0
            
            # Get previous close and current open
            prev_close = ohlc_data[-2][3] if len(ohlc_data) >= 2 else ohlc_data[-1][3]
            current_open = ohlc_data[-1][0]
            
            # Calculate gap
            gap = current_open - prev_close
            return gap
        except Exception as e:
            logger.error(f"Gap analysis error: {e}")
            return 0.0
    def get_prediction_summary(self) -> Dict[str, Any]:
        if not self.prediction_history:
            return {"total_predictions": 0, "accuracy": 0.0}
        recent_predictions = self.prediction_history[-10:]
        total = len(recent_predictions)
        high_confidence = sum(1 for p in recent_predictions if p.get("confidence", 0) > 0.7)
        return {
            "total_predictions": len(self.prediction_history),
            "recent_predictions": total,
            "high_confidence_predictions": high_confidence,
            "accuracy": self.accuracy_tracker["correct"] / max(self.accuracy_tracker["total"], 1) * 100,
            "last_prediction": recent_predictions[-1] if recent_predictions else None
        }

    def update_accuracy(self, prediction_id: str, actual_result: str):
        self.accuracy_tracker["total"] += 1
        if actual_result == "CORRECT":
            self.accuracy_tracker["correct"] += 1
        logger.info(f"📊 Accuracy updated: {self.accuracy_tracker['correct']}/{self.accuracy_tracker['total']}")

