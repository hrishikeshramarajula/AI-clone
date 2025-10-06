import numpy as np
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def detect_candle_pattern(o, h, l, c, prev_o=None, prev_c=None):
    """Detect common candle patterns for technical analysis."""
    body = abs(o - c)
    total = h - l
    upper_wick = h - max(o, c)
    lower_wick = min(o, c) - l
    is_doji = body <= 0.1 * total
    is_pinbar = (max(upper_wick, lower_wick) >= 0.6 * total) and (body <= 0.3 * total)
    is_spinning = (body <= 0.3 * total) and (upper_wick >= 0.4 * total) and (lower_wick >= 0.4 * total)
    is_engulfing = False
    if prev_o is not None and prev_c is not None:
        prev_body = abs(prev_o - prev_c)
        engulfing_bull = (c > o) and (prev_c < prev_o) and (body > prev_body) and (o < prev_c)
        engulfing_bear = (c < o) and (prev_c > prev_o) and (body > prev_body) and (o > prev_c)
        is_engulfing = engulfing_bull or engulfing_bear
    return {
        "doji": is_doji,
        "pinbar": is_pinbar,
        "spinning_top": is_spinning,
        "engulfing": is_engulfing
    }

def detect_volume_spike(volumes, threshold=1.5):
    """Detect if the latest volume is a spike compared to recent average."""
    if len(volumes) < 2:
        return False, 0
    avg_vol = np.mean(volumes[:-1])
    spike_ratio = volumes[-1] / avg_vol if avg_vol > 0 else 0
    return spike_ratio >= threshold, spike_ratio

def detect_oi_change(oi_values, rev_thresh=(5, 15), fakeout_thresh=(10, 20)):
    """Detect meaningful OI changes (for reversal/fakeout signals)."""
    if len(oi_values) < 2 or oi_values[-2] == 0:
        return "neutral", 0
    change_pct = ((oi_values[-1] - oi_values[-2]) / oi_values[-2]) * 100
    if rev_thresh[0] <= change_pct <= rev_thresh[1]:
        return "reversal", change_pct
    elif fakeout_thresh <= change_pct <= fakeout_thresh[1]:
        return "fakeout_spike", change_pct
    return "neutral", change_pct

def detect_liquidity_grab(o, h, l, c, sr_level, vol_spike):
    """Detect liquidity grab patterns at support/resistance."""
    if h > sr_level and c < sr_level and vol_spike:
        return "liquidity_grab_short"
    elif l < sr_level and c > sr_level and vol_spike:
        return "liquidity_grab_long"
    return None

def calculate_confidence(candle_info, vol_spike, oi_signal_type, near_sr, liquidity_signal, higher_tf_alignment):
    """Calculate a composite confidence score for a trade signal."""
    score_details = {
        "candle_pattern": 0.0,
        "volume_confirmation": 0.0,
        "oi_confirmation": 0.0,
        "support_resistance_zone": 0.0,
        "liquidity_grab": 0.0,
        "higher_tf_alignment": 0.0
    }
    if candle_info["pinbar"]:
        score_details["candle_pattern"] = 0.25
    elif candle_info["engulfing"]:
        score_details["candle_pattern"] = 0.25
    elif candle_info["doji"] or candle_info["spinning_top"]:
        score_details["candle_pattern"] = 0.15
    if vol_spike[0]:
        score_details["volume_confirmation"] = 0.20
    if oi_signal_type == "reversal":
        score_details["oi_confirmation"] = 0.15
    elif oi_signal_type == "fakeout_spike":
        score_details["oi_confirmation"] = 0.10
    if near_sr:
        score_details["support_resistance_zone"] = 0.10
    if liquidity_signal:
        score_details["liquidity_grab"] = 0.20
    if higher_tf_alignment:
        score_details["higher_tf_alignment"] = 0.10
    return round(sum(score_details.values()), 2), score_details

def process_live_market(ohlc_data, sr_levels, volumes, oi_values, higher_tf_alignment=False):
    """Core signal processor for live market data."""
    if len(volumes) == 0 or len(oi_values) == 0:
        return {"action": "error", "error": "No volume or OI data"}
    try:
        o, h, l, c = ohlc_data
        prev_o, prev_c = (None, None)
        # Extract previous candle if available (not implemented in this minimal version)
        candle_info = detect_candle_pattern(o, h, l, c, prev_o, prev_c)
        vol_spike = detect_volume_spike(volumes)
        oi_signal_type, oi_signal_value = detect_oi_change(oi_values)
        sr_levels = [x for x in sr_levels if x is not None]
        near_sr = any(abs(c - level) <= 0.002 * c for level in sr_levels) if sr_levels else False
        liquidity_signal = None
        for level in sr_levels:
            lg = detect_liquidity_grab(o, h, l, c, level, vol_spike[0])
            if lg:
                liquidity_signal = lg
                break
        conf_score, details = calculate_confidence(
            candle_info, vol_spike, oi_signal_type, near_sr, liquidity_signal, higher_tf_alignment
        )

        # reversal-trade override
        if oi_signal_type == "reversal" and vol_spike[0]:
            return {
                "action": "reversal_trade",
                "confidence": conf_score + 0.1,
                "reason": "Volume–OI reversal detected",
                "ohlc": (o, h, l, c),
                "timestamp": pd.Timestamp.now().isoformat()
            }

        if conf_score >= 0.70:
            return {
                "action": "trade",
                "confidence": conf_score,
                "reason": details,
                "ohlc": (o, h, l, c),
                "timestamp": pd.Timestamp.now().isoformat()
            }
        return {
            "action": "skip",
            "confidence": conf_score,
            "reason": details,
            "ohlc": (o, h, l, c),
            "timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        return {"action": "error", "error": str(e), "ohlc": ohlc_data}
