"""
SIAPS - Database Module
Handles database operations
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import DATABASE_URL
from src.utils import setup_logger

logger = setup_logger(__name__)

Base = declarative_base()


class PredictionHistory(Base):
    """Prediction history table"""
    __tablename__ = 'prediction_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10), nullable=False)
    stock_name = Column(String(50))
    prediction_type = Column(String(20), nullable=False)  # 'short_term' or 'long_term'
    predicted_date = Column(DateTime, nullable=False)
    prediction_value = Column(Float)
    prediction_direction = Column(String(10))  # 'up', 'down', 'neutral'
    confidence_score = Column(Float)
    actual_value = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    notes = Column(Text)
    
    def __repr__(self):
        return f"<Prediction(code={self.stock_code}, type={self.prediction_type}, date={self.predicted_date})>"


class Watchlist(Base):
    """User watchlist table"""
    __tablename__ = 'watchlist'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10), nullable=False, unique=True)
    stock_name = Column(String(50))
    target_price = Column(Float)
    target_days = Column(Integer)  # Estimated days to reach target price
    stop_loss_price = Column(Float)
    stop_profit_price = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Watchlist(code={self.stock_code}, name={self.stock_name})>"


class DatabaseManager:
    """Database manager for SIAPS"""
    
    def __init__(self, database_url: str = DATABASE_URL):
        """
        Initialize database manager
        
        Args:
            database_url: Database connection URL
        """
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
        self.migrate_database()
        logger.info(f"Database initialized: {database_url}")
    
    def create_tables(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created/verified")
    
    def migrate_database(self):
        """Handle database migrations for new columns"""
        try:
            from sqlalchemy import text
            with self.engine.connect() as conn:
                # Check if target_days column exists in watchlist table
                try:
                    conn.execute(text("SELECT target_days FROM watchlist LIMIT 1"))
                except Exception:
                    # Column doesn't exist, add it
                    logger.info("Adding target_days column to watchlist table...")
                    conn.execute(text("ALTER TABLE watchlist ADD COLUMN target_days INTEGER"))
                    conn.commit()
                    logger.info("Successfully added target_days column")
        except Exception as e:
            logger.warning(f"Migration check failed (this is okay for new databases): {e}")
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def add_prediction(self, stock_code: str, prediction_type: str, 
                      predicted_date: datetime, prediction_value: float,
                      prediction_direction: str, confidence_score: float = None,
                      stock_name: str = None, notes: str = None):
        """
        Add a prediction record
        
        Args:
            stock_code: Stock code
            prediction_type: Type of prediction ('short_term' or 'long_term')
            predicted_date: Date of prediction
            prediction_value: Predicted value
            prediction_direction: Predicted direction ('up', 'down', 'neutral')
            confidence_score: Confidence score (0-1)
            stock_name: Stock name
            notes: Additional notes
        """
        session = self.get_session()
        try:
            prediction = PredictionHistory(
                stock_code=stock_code,
                stock_name=stock_name,
                prediction_type=prediction_type,
                predicted_date=predicted_date,
                prediction_value=prediction_value,
                prediction_direction=prediction_direction,
                confidence_score=confidence_score,
                notes=notes
            )
            session.add(prediction)
            session.commit()
            logger.info(f"Prediction saved for {stock_code}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving prediction: {str(e)}")
        finally:
            session.close()
    
    def add_to_watchlist(self, stock_code: str, stock_name: str = None,
                         target_price: float = None, target_days: int = None,
                         stop_loss_price: float = None,
                         stop_profit_price: float = None, notes: str = None):
        """
        Add a stock to watchlist
        
        Args:
            stock_code: Stock code
            stock_name: Stock name
            target_price: Target price
            target_days: Estimated days to reach target price
            stop_loss_price: Stop loss price
            stop_profit_price: Stop profit price
            notes: Additional notes
        """
        session = self.get_session()
        try:
            watchlist_item = Watchlist(
                stock_code=stock_code,
                stock_name=stock_name,
                target_price=target_price,
                target_days=target_days,
                stop_loss_price=stop_loss_price,
                stop_profit_price=stop_profit_price,
                notes=notes
            )
            session.add(watchlist_item)
            session.commit()
            logger.info(f"Added {stock_code} to watchlist")
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding to watchlist: {str(e)}")
        finally:
            session.close()
    
    def get_watchlist(self):
        """Get all items in watchlist"""
        session = self.get_session()
        try:
            items = session.query(Watchlist).all()
            return items
        finally:
            session.close()
    
    def remove_from_watchlist(self, stock_code: str):
        """
        Remove a stock from watchlist
        
        Args:
            stock_code: Stock code to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        session = self.get_session()
        try:
            item = session.query(Watchlist).filter(Watchlist.stock_code == stock_code).first()
            if item:
                session.delete(item)
                session.commit()
                logger.info(f"Removed {stock_code} from watchlist")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error removing from watchlist: {str(e)}")
            return False
        finally:
            session.close()
    
    def update_watchlist_item(self, stock_code: str, **kwargs):
        """
        Update a watchlist item
        
        Args:
            stock_code: Stock code to update
            **kwargs: Fields to update (stock_name, target_price, etc.)
            
        Returns:
            bool: True if updated, False if not found
        """
        session = self.get_session()
        try:
            item = session.query(Watchlist).filter(Watchlist.stock_code == stock_code).first()
            if item:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                session.commit()
                logger.info(f"Updated {stock_code} in watchlist")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating watchlist: {str(e)}")
            return False
        finally:
            session.close()

    def get_prediction_history(self, stock_code: str = None, limit: int = 100):
        """
        Get prediction history
        
        Args:
            stock_code: Optional stock code filter
            limit: Maximum number of records to return
        
        Returns:
            list: List of prediction records
        """
        session = self.get_session()
        try:
            query = session.query(PredictionHistory)
            if stock_code:
                query = query.filter(PredictionHistory.stock_code == stock_code)
            query = query.order_by(PredictionHistory.created_at.desc()).limit(limit)
            return query.all()
        finally:
            session.close()
    
    def clear_prediction_history(self):
        """
        Clear all prediction history records
        
        Returns:
            int: Number of deleted records
        """
        session = self.get_session()
        try:
            count = session.query(PredictionHistory).delete()
            session.commit()
            logger.info(f"Cleared {count} prediction history records")
            return count
        except Exception as e:
            session.rollback()
            logger.error(f"Error clearing prediction history: {str(e)}")
            raise
        finally:
            session.close()
