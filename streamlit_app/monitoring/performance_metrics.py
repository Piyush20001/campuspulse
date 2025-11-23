"""
Performance Metrics Tracker for Campus Pulse
Tracks response time, latency, and system performance metrics
"""
import time
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
import streamlit as st
from typing import Dict, List, Optional
import statistics


class PerformanceMetricsTracker:
    """Track and store performance metrics for monitoring"""

    def __init__(self, db_path="campus_pulse_performance.db"):
        """Initialize performance metrics tracker"""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create performance metrics tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Response time metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS response_times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                response_time_ms REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_email TEXT,
                status TEXT DEFAULT 'success'
            )
        """)

        # API call latency table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_latency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                latency_ms REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)

        # Page load times table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_loads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_name TEXT NOT NULL,
                load_time_ms REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_email TEXT
            )
        """)

        # Model inference times table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_inference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                inference_time_ms REAL NOT NULL,
                num_predictions INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Database query performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS db_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_type TEXT NOT NULL,
                execution_time_ms REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rows_affected INTEGER
            )
        """)

        conn.commit()
        conn.close()

    @contextmanager
    def track_response_time(self, endpoint: str, user_email: Optional[str] = None):
        """
        Context manager to track response time for an endpoint

        Usage:
            with metrics_tracker.track_response_time("crowd_heatmap"):
                # Your code here
                process_heatmap_data()
        """
        start_time = time.time()
        status = "success"

        try:
            yield
        except Exception as e:
            status = "error"
            raise
        finally:
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000

            # Store metric
            self.record_response_time(endpoint, response_time_ms, user_email, status)

    def record_response_time(self, endpoint: str, response_time_ms: float,
                            user_email: Optional[str] = None, status: str = "success"):
        """Record response time for an endpoint"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO response_times (endpoint, response_time_ms, user_email, status)
                VALUES (?, ?, ?, ?)
            """, (endpoint, response_time_ms, user_email, status))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error recording response time: {str(e)}")

    def record_api_latency(self, operation: str, latency_ms: float, metadata: Optional[str] = None):
        """Record API call latency"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO api_latency (operation, latency_ms, metadata)
                VALUES (?, ?, ?)
            """, (operation, latency_ms, metadata))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error recording API latency: {str(e)}")

    def record_page_load(self, page_name: str, load_time_ms: float, user_email: Optional[str] = None):
        """Record page load time"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO page_loads (page_name, load_time_ms, user_email)
                VALUES (?, ?, ?)
            """, (page_name, load_time_ms, user_email))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error recording page load: {str(e)}")

    def record_model_inference(self, model_name: str, inference_time_ms: float, num_predictions: int = 1):
        """Record model inference time"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO model_inference (model_name, inference_time_ms, num_predictions)
                VALUES (?, ?, ?)
            """, (model_name, inference_time_ms, num_predictions))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error recording model inference: {str(e)}")

    def record_db_query(self, query_type: str, execution_time_ms: float, rows_affected: int = 0):
        """Record database query execution time"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO db_queries (query_type, execution_time_ms, rows_affected)
                VALUES (?, ?, ?)
            """, (query_type, execution_time_ms, rows_affected))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error recording DB query: {str(e)}")

    def get_response_time_stats(self, endpoint: Optional[str] = None, hours: int = 24) -> Dict:
        """Get response time statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()

            if endpoint:
                cursor.execute("""
                    SELECT response_time_ms FROM response_times
                    WHERE endpoint = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (endpoint, since_time))
            else:
                cursor.execute("""
                    SELECT response_time_ms FROM response_times
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                """, (since_time,))

            times = [row[0] for row in cursor.fetchall()]
            conn.close()

            if not times:
                return {
                    'count': 0,
                    'avg_ms': 0,
                    'min_ms': 0,
                    'max_ms': 0,
                    'median_ms': 0,
                    'p95_ms': 0,
                    'p99_ms': 0
                }

            times_sorted = sorted(times)

            return {
                'count': len(times),
                'avg_ms': statistics.mean(times),
                'min_ms': min(times),
                'max_ms': max(times),
                'median_ms': statistics.median(times),
                'p95_ms': times_sorted[int(len(times_sorted) * 0.95)] if len(times_sorted) > 0 else 0,
                'p99_ms': times_sorted[int(len(times_sorted) * 0.99)] if len(times_sorted) > 0 else 0
            }

        except Exception as e:
            print(f"Error getting response time stats: {str(e)}")
            return {}

    def get_all_endpoint_stats(self, hours: int = 24) -> List[Dict]:
        """Get stats for all endpoints"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()

            cursor.execute("""
                SELECT DISTINCT endpoint FROM response_times
                WHERE timestamp >= ?
            """, (since_time,))

            endpoints = [row[0] for row in cursor.fetchall()]
            conn.close()

            return [
                {
                    'endpoint': endpoint,
                    **self.get_response_time_stats(endpoint, hours)
                }
                for endpoint in endpoints
            ]

        except Exception as e:
            print(f"Error getting endpoint stats: {str(e)}")
            return []

    def get_model_performance_stats(self, model_name: Optional[str] = None, hours: int = 24) -> Dict:
        """Get model inference performance statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            since_time = (datetime.now() - timedelta(hours=hours)).isoformat()

            if model_name:
                cursor.execute("""
                    SELECT inference_time_ms, num_predictions FROM model_inference
                    WHERE model_name = ? AND timestamp >= ?
                """, (model_name, since_time))
            else:
                cursor.execute("""
                    SELECT inference_time_ms, num_predictions FROM model_inference
                    WHERE timestamp >= ?
                """, (since_time,))

            results = cursor.fetchall()
            conn.close()

            if not results:
                return {}

            times = [r[0] for r in results]
            total_predictions = sum(r[1] for r in results)

            return {
                'count': len(times),
                'total_predictions': total_predictions,
                'avg_inference_ms': statistics.mean(times),
                'min_inference_ms': min(times),
                'max_inference_ms': max(times)
            }

        except Exception as e:
            print(f"Error getting model performance stats: {str(e)}")
            return {}

    def cleanup_old_metrics(self, days: int = 7):
        """Clean up metrics older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cutoff_time = (datetime.now() - timedelta(days=days)).isoformat()

            tables = ['response_times', 'api_latency', 'page_loads', 'model_inference', 'db_queries']

            for table in tables:
                cursor.execute(f"""
                    DELETE FROM {table}
                    WHERE timestamp < ?
                """, (cutoff_time,))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error cleaning up metrics: {str(e)}")


# Global instance
_metrics_tracker = None

def get_metrics_tracker() -> PerformanceMetricsTracker:
    """Get global metrics tracker instance"""
    global _metrics_tracker
    if _metrics_tracker is None:
        _metrics_tracker = PerformanceMetricsTracker()
    return _metrics_tracker
