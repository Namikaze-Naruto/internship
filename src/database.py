import sqlite3
import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from . import config


class InternshipDB:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(config.ROOT_DIR, "data", "internships.db")
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database with required tables"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only create directory if path has a directory component
            os.makedirs(db_dir, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS internships (
                    id INTEGER PRIMARY KEY,
                    unstop_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    company_name TEXT,
                    logo_url TEXT,
                    type TEXT,
                    stipend_min INTEGER,
                    stipend_max INTEGER,
                    currency TEXT,
                    duration TEXT,
                    location TEXT,
                    work_from_home INTEGER,
                    skills TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    deadline TEXT,
                    url TEXT,
                    views INTEGER,
                    registrations INTEGER,
                    raw_data TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_unstop_id ON internships(unstop_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_scraped_at ON internships(scraped_at)
            """)
            
            conn.commit()
            logging.info(f"Database initialized at {self.db_path}")
    
    def add_internship(self, item: Dict[str, Any]) -> bool:
        """
        Add internship to database if it doesn't exist.
        Returns True if added, False if duplicate.
        """
        unstop_id = str(item.get("id") or item.get("entity_id") or "")
        
        if not unstop_id:
            logging.warning("Skipping item without ID")
            return False
        
        # Extract and normalize data
        title = item.get("title") or item.get("opportunity_title") or "Unknown"
        company_name = item.get("organisation_name") or item.get("company_name") or "Unknown"
        logo_url = item.get("logo_url") or item.get("organisation_logo") or ""
        opportunity_type = item.get("type") or item.get("opportunity_type") or "internship"
        
        # Stipend
        stipend_min = item.get("stipend", {}).get("min") if isinstance(item.get("stipend"), dict) else None
        stipend_max = item.get("stipend", {}).get("max") if isinstance(item.get("stipend"), dict) else None
        currency = item.get("stipend", {}).get("currency") if isinstance(item.get("stipend"), dict) else "INR"
        
        # Duration
        duration = item.get("duration") or item.get("internship_duration") or ""
        
        # Location
        location_data = item.get("locations") or []
        if isinstance(location_data, list) and location_data:
            location = ", ".join([loc.get("location") or loc.get("city") or str(loc) for loc in location_data[:3]])
        else:
            location = str(location_data) if location_data else ""
        
        work_from_home = 1 if item.get("is_work_from_home") or item.get("work_from_home") else 0
        
        # Skills
        skills_data = item.get("skills_required") or item.get("skills") or []
        if isinstance(skills_data, list):
            skills = ", ".join([s.get("skill") or s.get("name") or str(s) for s in skills_data if s])
        else:
            skills = str(skills_data) if skills_data else ""
        
        # Dates
        start_date = item.get("start_date") or item.get("registration_start_date") or ""
        end_date = item.get("end_date") or item.get("registration_end_date") or ""
        deadline = item.get("deadline") or item.get("registration_end_date") or ""
        
        # URL
        url = item.get("public_url") or item.get("url") or f"https://unstop.com/internships/{unstop_id}"
        
        # Stats
        views = item.get("views_count") or item.get("views") or 0
        registrations = item.get("registrations_count") or item.get("registrations") or 0
        
        # Store raw JSON
        raw_data = json.dumps(item, ensure_ascii=False)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO internships (
                        unstop_id, title, company_name, logo_url, type,
                        stipend_min, stipend_max, currency, duration,
                        location, work_from_home, skills,
                        start_date, end_date, deadline, url,
                        views, registrations, raw_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    unstop_id, title, company_name, logo_url, opportunity_type,
                    stipend_min, stipend_max, currency, duration,
                    location, work_from_home, skills,
                    start_date, end_date, deadline, url,
                    views, registrations, raw_data
                ))
                conn.commit()
                logging.info(f"Added new internship: {title} at {company_name}")
                return True
        except sqlite3.IntegrityError:
            logging.debug(f"Duplicate internship skipped: {title} at {company_name}")
            return False
        except Exception as e:
            logging.error(f"Error adding internship: {e}")
            return False
    
    def get_all_internships(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all internships, ordered by most recent first"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = "SELECT * FROM internships ORDER BY scraped_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    def export_to_json(self, output_path: str) -> int:
        """Export all internships to JSON file for web display"""
        internships = self.get_all_internships()
        
        # Convert to web-friendly format
        web_data = []
        for item in internships:
            web_item = {
                "id": item["unstop_id"],
                "title": item["title"],
                "company": item["company_name"],
                "logo": item["logo_url"],
                "type": item["type"],
                "stipend": {
                    "min": item["stipend_min"],
                    "max": item["stipend_max"],
                    "currency": item["currency"]
                } if item["stipend_min"] or item["stipend_max"] else None,
                "duration": item["duration"],
                "location": item["location"],
                "workFromHome": bool(item["work_from_home"]),
                "skills": item["skills"].split(", ") if item["skills"] else [],
                "deadline": item["deadline"],
                "url": item["url"],
                "views": item["views"],
                "registrations": item["registrations"],
                "scrapedAt": item["scraped_at"],
                "firstSeen": item["first_seen"]
            }
            web_data.append(web_item)
        
        # Create directory if it has a parent
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "lastUpdated": datetime.utcnow().isoformat() + "Z",
                "totalInternships": len(web_data),
                "internships": web_data
            }, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Exported {len(web_data)} internships to {output_path}")
        return len(web_data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM internships").fetchone()[0]
            today = conn.execute(
                "SELECT COUNT(*) FROM internships WHERE DATE(scraped_at) = DATE('now')"
            ).fetchone()[0]
            
            return {
                "total_internships": total,
                "added_today": today
            }
