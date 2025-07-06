# backend/app/worker/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from app.services.stats import update_stats
import logging
import atexit

logger = logging.getLogger(__name__)

# Create scheduler instance
scheduler = BackgroundScheduler()

def start_scheduler():
    """Start the background scheduler with all jobs."""
    
    logger.info("Starting background scheduler...")
    
    # Add stats update job - every 30 minutes
    scheduler.add_job(
        func=update_stats,
        trigger=IntervalTrigger(minutes=30),
        id='update_stats_job',
        name='Update daily statistics',
        replace_existing=True
    )
    
    # Add daily cleanup job - at midnight
    scheduler.add_job(
        func=daily_cleanup,
        trigger=CronTrigger(hour=0, minute=0),
        id='daily_cleanup_job',
        name='Daily cleanup tasks',
        replace_existing=True
    )
    
    # Add health check job - every 5 minutes
    scheduler.add_job(
        func=health_check,
        trigger=IntervalTrigger(minutes=5),
        id='health_check_job',
        name='System health check',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Background scheduler started successfully")
    
    # Shut down scheduler when exiting
    atexit.register(lambda: scheduler.shutdown())

def daily_cleanup():
    """Daily cleanup tasks."""
    try:
        logger.info("Running daily cleanup tasks...")
        
        # Clean up old log files, temp files, etc.
        # This is where you'd add cleanup logic
        
        # Run stats update as part of daily cleanup
        update_stats()
        
        logger.info("Daily cleanup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during daily cleanup: {e}")

def health_check():
    """Basic system health check."""
    try:
        # Check database connection
        from app.db.session import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        logger.debug("Health check passed")
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")

# For testing/manual execution
if __name__ == "__main__":
    start_scheduler()
    
    # Keep the script running
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        scheduler.shutdown()