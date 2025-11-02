"""
Storage Service
Handles data persistence with privacy-first approach
Uses in-memory storage by default (no permanent storage)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


# In-memory storage (resets on restart for privacy)
STORAGE = {
    "text": [],
    "audio": [],
    "image": [],
    "daily_aggregate": []
}

# Optional: File-based storage path (disabled by default)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USE_FILE_STORAGE = False  # Set to True to enable persistence


def store_analysis(modality: str, data: Dict) -> str:
    """
    Store analysis result
    
    Args:
        modality: One of 'text', 'audio', 'image', 'daily_aggregate'
        data: Analysis result dictionary
    
    Returns:
        Analysis ID (timestamp-based)
    """
    
    # Generate unique ID
    analysis_id = f"{modality}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    # Add metadata
    entry = {
        "id": analysis_id,
        "modality": modality,
        "timestamp": data.get("timestamp", datetime.now().isoformat()),
        "data": data
    }
    
    # Store in memory
    if modality in STORAGE:
        STORAGE[modality].append(entry)
    else:
        STORAGE[modality] = [entry]
    
    # Optional: Write to file
    if USE_FILE_STORAGE:
        _write_to_file(modality, entry)
    
    return analysis_id


def get_daily_entries(date_str: str) -> Dict[str, List[Dict]]:
    """
    Get all entries for a specific date
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        Dictionary with 'text', 'audio', 'image' lists
    """
    
    result = {
        "text": [],
        "audio": [],
        "image": []
    }
    
    for modality in ["text", "audio", "image"]:
        for entry in STORAGE.get(modality, []):
            entry_date = entry["timestamp"][:10]  # Extract YYYY-MM-DD
            if entry_date == date_str:
                result[modality].append(entry["data"])
    
    return result


def get_trend_data(days: int = 7) -> Dict:
    """
    Get trend data for the last N days
    
    Args:
        days: Number of days to retrieve
    
    Returns:
        {
            'dates': List[str],
            'scores': List[float],
            'buckets': List[str]
        }
    """
    
    # Generate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)
    
    dates = []
    scores = []
    buckets = []
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        dates.append(date_str)
        
        # Look for daily aggregate for this date
        daily_agg = None
        for entry in STORAGE.get("daily_aggregate", []):
            if entry["data"].get("date") == date_str:
                daily_agg = entry["data"]
                break
        
        if daily_agg:
            scores.append(daily_agg["final_score"])
            buckets.append(daily_agg["bucket"])
        else:
            # No data for this date - compute on-the-fly
            daily_data = get_daily_entries(date_str)
            if any(daily_data.values()):
                from services.fusion import aggregate_daily_scores
                result = aggregate_daily_scores(
                    daily_data["text"],
                    daily_data["audio"],
                    daily_data["image"]
                )
                scores.append(result["final_score"])
                buckets.append(result["bucket"])
            else:
                # No data at all
                scores.append(None)
                buckets.append("No Data")
        
        current_date += timedelta(days=1)
    
    return {
        "dates": dates,
        "scores": scores,
        "buckets": buckets
    }


def purge_all_data() -> int:
    """
    Delete all stored analysis data
    
    Returns:
        Number of entries deleted
    """
    
    total_deleted = 0
    
    for modality in STORAGE:
        total_deleted += len(STORAGE[modality])
        STORAGE[modality] = []
    
    # Optional: Delete files
    if USE_FILE_STORAGE and os.path.exists(STORAGE_DIR):
        import shutil
        shutil.rmtree(STORAGE_DIR)
        os.makedirs(STORAGE_DIR, exist_ok=True)
    
    return total_deleted


def get_stats() -> Dict:
    """Get storage statistics"""
    
    stats = {
        "total_entries": 0,
        "by_modality": {},
        "storage_mode": "in-memory" if not USE_FILE_STORAGE else "file-based",
        "oldest_entry": None,
        "newest_entry": None
    }
    
    all_timestamps = []
    
    for modality in STORAGE:
        count = len(STORAGE[modality])
        stats["by_modality"][modality] = count
        stats["total_entries"] += count
        
        for entry in STORAGE[modality]:
            all_timestamps.append(entry["timestamp"])
    
    if all_timestamps:
        stats["oldest_entry"] = min(all_timestamps)
        stats["newest_entry"] = max(all_timestamps)
    
    return stats


def _write_to_file(modality: str, entry: Dict):
    """Write entry to file (if file storage enabled)"""
    
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    # Organize by date
    date_str = entry["timestamp"][:10]  # YYYY-MM-DD
    date_dir = os.path.join(STORAGE_DIR, date_str)
    os.makedirs(date_dir, exist_ok=True)
    
    # Write entry
    filepath = os.path.join(date_dir, f"{entry['id']}.json")
    with open(filepath, 'w') as f:
        json.dump(entry, f, indent=2)
