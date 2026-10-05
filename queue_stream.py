"""
TalentPulse - Asynchronous Stream Ingestion Buffer
Simulates a decoupled Kafka/Redpanda Message Queue architecture for real-time interview transcripts.
Ensures zero-drop buffering when hundreds of video/audio transcripts arrive concurrently.
"""

import asyncio
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime

class InterviewStreamQueue:
    def __init__(self, maxsize: int = 10000):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self.total_ingested: int = 0
        self.total_processed: int = 0
        self.start_time: float = time.time()
        self.is_running: bool = False
        self._worker_task: Optional[asyncio.Task] = None
        self._consumer_handler: Optional[Callable] = None
        self.topic_counts: Dict[str, int] = {
            "interview.submissions": 0,
            "interview.telemetry": 0,
            "interview.agent_actions": 0
        }

    async def start_consumer(self, consumer_handler: Callable):
        """Starts the background worker to consume events from the queue."""
        self._consumer_handler = consumer_handler
        self.is_running = True
        self._worker_task = asyncio.create_task(self._worker_loop())

    async def stop(self):
        """Gracefully stops the worker."""
        self.is_running = False
        if self._worker_task:
            self._worker_task.cancel()

    async def produce(self, payload: Dict[str, Any]) -> bool:
        """Pushes an incoming interview submission into the stream queue (Default Topic)."""
        return await self.produce_event("interview.submissions", payload)

    async def produce_event(self, topic: str, payload: Dict[str, Any]) -> bool:
        """Pushes a typed event into the stream queue with offset and timestamp tracking."""
        payload["_topic"] = topic
        payload["_event_id"] = payload.get("event_id") or f"EVT-{self.total_ingested + 1:06d}"
        payload["queued_at"] = time.time()
        payload["offset"] = self.total_ingested + 1
        
        await self.queue.put(payload)
        self.total_ingested += 1
        self.topic_counts[topic] = self.topic_counts.get(topic, 0) + 1
        return True

    async def _worker_loop(self):
        """Continuous consumer loop dispatching events to appropriate handlers."""
        import storage
        while self.is_running:
            try:
                item = await self.queue.get()
                topic = item.get("_topic", "interview.submissions")

                if topic == "interview.telemetry":
                    storage.save_telemetry_event(item)
                elif self._consumer_handler:
                    await self._consumer_handler(item)

                self.total_processed += 1
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Stream Worker Error] {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Returns real-time queue throughput metrics and topic breakdown."""
        elapsed = max(time.time() - self.start_time, 1.0)
        return {
            "mode": "Lean In-Memory Event Stream (Redis/Kafka Alternative)",
            "queue_depth": self.queue.qsize(),
            "total_ingested": self.total_ingested,
            "total_processed": self.total_processed,
            "throughput_eps": round(self.total_processed / elapsed, 2),
            "topics": self.topic_counts
        }

# Global Singleton Stream Instance
stream_queue = InterviewStreamQueue()
