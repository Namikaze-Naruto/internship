
import json
import re
from datetime import datetime

# Load the JSON data
FILE_PATH = "data/internships/internships_2026-01-24.json"
OUTPUT_FILE = "digest_output.txt"

def clean_html(raw_html):
    """Remove HTML tags and extra whitespace."""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return " ".join(cleantext.split())

def main():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {FILE_PATH}")
        return

    items = data.get("items", [])
    
    # Header
    today_str = datetime.now().strftime("%d %B %Y")
    message = f"*Internship Updates - {today_str}*\n\n"
    
    filtered_count = 0
    
    for item in items:
        # Title
        title = item.get("title", "Untitled Opportunity").strip()
        
        # Summary (first 1-2 sentences or truncated)
        details_html = item.get("details", "")
        summary_text = clean_html(details_html)
        # Simple truncation for summary - first 150 chars plus ellipsis if needed
        summary = (summary_text[:150] + '...') if len(summary_text) > 150 else summary_text
        
        # Link
        link = item.get("seo_url", "#")
        
        # Stipend Logic
        filters = item.get("filters", [])
        is_undergrad = any(f.get("name") == "Undergraduate" for f in filters)
        
        stipend_info = ""
        if is_undergrad:
            job_detail = item.get("jobDetail", {})
            min_sal = job_detail.get("min_salary")
            max_sal = job_detail.get("max_salary")
            currency = job_detail.get("currency", "")
            
            # Basic currency symbol mapping
            curr_sym = "₹" if "rupee" in str(currency).lower() else "$"
            
            if min_sal and max_sal:
                stipend_info = f"\n💰 *Stipend:* {curr_sym}{min_sal} - {curr_sym}{max_sal}"
            elif min_sal:
                 stipend_info = f"\n💰 *Stipend:* {curr_sym}{min_sal}"
            elif max_sal:
                 stipend_info = f"\n💰 *Stipend:* Up to {curr_sym}{max_sal}"
                 
        
        # Assemble Entry
        entry = (
            f"📌 *{title}*\n"
            f"_{summary}_\n"
            f"🔗 Apply: {link}"
            f"{stipend_info}\n\n"
            "---------------------------------\n\n"
        )
        
        message += entry
        filtered_count += 1

    if filtered_count == 0:
        message += "No internships found for today."
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"Generated digest with {filtered_count} items in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
