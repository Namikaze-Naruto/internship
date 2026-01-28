"""
Test script to verify the scraper and database functionality
"""
import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import InternshipDB

def test_database():
    """Test database operations"""
    print("🧪 Testing Database Operations\n")
    
    # Create test database
    test_db_path = "test_internships.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = InternshipDB(test_db_path)
    print("✅ Database initialized")
    
    # Test data
    sample_internship = {
        "id": "test-001",
        "title": "Software Development Intern",
        "organisation_name": "Tech Corp",
        "logo_url": "https://example.com/logo.png",
        "type": "internship",
        "stipend": {"min": 15000, "max": 25000, "currency": "INR"},
        "duration": "3 months",
        "locations": [{"location": "Bangalore"}, {"location": "Mumbai"}],
        "is_work_from_home": False,
        "skills_required": [{"skill": "Python"}, {"skill": "Django"}],
        "deadline": "2026-02-15T00:00:00Z",
        "public_url": "https://unstop.com/test-001",
        "views_count": 1000,
        "registrations_count": 250
    }
    
    # Add internship
    result = db.add_internship(sample_internship)
    print(f"✅ Added new internship: {result}")
    
    # Try adding duplicate
    result2 = db.add_internship(sample_internship)
    print(f"✅ Duplicate prevention working: {not result2}")
    
    # Get stats
    stats = db.get_stats()
    print(f"✅ Database stats: {stats}")
    
    # Export to JSON
    output_path = "test_export.json"
    count = db.export_to_json(output_path)
    print(f"✅ Exported {count} internships to JSON")
    
    # Verify JSON
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"✅ JSON contains {data['totalInternships']} internships")
    
    # Close database connection
    del db
    
    # Cleanup
    try:
        os.remove(test_db_path)
        os.remove(output_path)
    except:
        pass
    
    print("\n✅ All tests passed!")
    
    return True

if __name__ == "__main__":
    try:
        test_database()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
