import datetime
import json
import os
import time
import logging
from dateutil import parser


from . import config, api_client, utils
from .database import InternshipDB


def main() -> None:
    utils.setup_logging()
    os.makedirs(config.DATA_DIR, exist_ok=True)

    db = InternshipDB()
    
    all_items = []
    new_items = 0
    duplicate_items = 0
    page = 1
    
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=config.HOURS_LOOKBACK)
    consecutive_old_items = 0

    logging.info("Starting scraper...")
    
    while True:
        items = api_client.fetch_page(page)
        if not items:
            break
        
        for item in items:
            date_str = item.get("approved_date") or item.get("server_time") or item.get("created_at")
            if date_str:
                try:
                    dt = parser.parse(date_str)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                    
                    if dt > cutoff_date:
                        all_items.append(item)
                        consecutive_old_items = 0
                    else:
                        consecutive_old_items += 1
                except Exception:
                     all_items.append(item)
            else:
                all_items.append(item)

        if consecutive_old_items > 20:
            logging.info("Reached old items limit, stopping.")
            break
        
        if page > 50:
            logging.info("Reached max pages limit, stopping.")
            break

        page += 1
        time.sleep(config.REQUEST_DELAY_SECONDS)

    # Add to database with duplicate prevention
    logging.info(f"Processing {len(all_items)} items...")
    for item in all_items:
        if db.add_internship(item):
            new_items += 1
        else:
            duplicate_items += 1
    
    # Export to JSON for web
    web_json_path = os.path.join(config.ROOT_DIR, "docs", "data", "internships.json")
    total_exported = db.export_to_json(web_json_path)
    
    # Also save daily backup
    out_path = os.path.join(
        config.DATA_DIR, f"internships_{datetime.date.today().isoformat()}.json"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "scrape_date": datetime.datetime.utcnow().isoformat() + "Z",
                "hours_lookback": config.HOURS_LOOKBACK,
                "per_page": config.API_PER_PAGE,
                "total_items": len(all_items),
                "new_items": new_items,
                "duplicate_items": duplicate_items,
                "items": all_items,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    stats = db.get_stats()
    logging.info(f"Scraping complete:")
    logging.info(f"  - Found {len(all_items)} items from API")
    logging.info(f"  - Added {new_items} new internships")
    logging.info(f"  - Skipped {duplicate_items} duplicates")
    logging.info(f"  - Total in database: {stats['total_internships']}")
    logging.info(f"  - Exported {total_exported} to web JSON")
    logging.info(f"  - Backup saved to {out_path}")


if __name__ == "__main__":
    main()
