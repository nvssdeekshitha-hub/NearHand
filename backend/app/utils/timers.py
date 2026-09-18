import asyncio
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Active background tasks keyed by request_id
active_timers: Dict[int, asyncio.Task] = {}

def schedule_caretaker_timeout_timer(request_id: int, delay_seconds: float):
    """
    Schedules an asynchronous background task that fires escalation_service.handle_caretaker_timeout
    after delay_seconds.
    MUST be called from within a running async event loop (i.e. from an async def route handler).
    """
    # Cancel existing task if any
    cancel_caretaker_timeout_timer(request_id)

    async def _timer_worker():
        try:
            logger.info(f"Starting timeout timer for request {request_id} ({delay_seconds} seconds)...")
            await asyncio.sleep(delay_seconds)

            # Execute escalation service
            from app.db.database import SessionLocal
            from app.services.escalation_service import handle_caretaker_timeout

            db = SessionLocal()
            try:
                handle_caretaker_timeout(db=db, request_id=request_id)
            finally:
                db.close()
        except asyncio.CancelledError:
            logger.info(f"Timer for request {request_id} was cancelled.")
        except Exception as e:
            logger.error(f"Error executing timeout timer for request {request_id}: {e}")

    try:
        # get_running_loop() raises RuntimeError if there is no running loop.
        # This is intentional — this function must only be called from async context.
        loop = asyncio.get_running_loop()
        task = loop.create_task(_timer_worker())
        active_timers[request_id] = task
        logger.info(f"Timeout timer scheduled for request {request_id} ({delay_seconds}s).")
    except RuntimeError:
        logger.error(
            f"schedule_caretaker_timeout_timer called outside of async context for request {request_id}. "
            "Timer NOT scheduled. Call this from an async route handler."
        )

def cancel_caretaker_timeout_timer(request_id: int):
    """
    Cancels an active timer if caretaker accepted/rejected before timeout.
    Safe to call from sync or async context.
    """
    if request_id in active_timers:
        task = active_timers.pop(request_id)
        if not task.done():
            task.cancel()
