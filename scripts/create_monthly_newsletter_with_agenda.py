#!/usr/bin/env python3
"""
Create monthly newsletter with agenda for Teams.
This script generates both the newsletter and the Teams agenda.
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_name):
    """Run a Python script and return success status."""
    try:
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            return True
        else:
            print(f"❌ {script_name} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Main function to create newsletter with agenda."""
    print("📰 Creating Monthly Newsletter with Teams Agenda")
    print("=" * 55)
    
    # Step 1: Generate newsletter with section IDs
    print("\n1️⃣ Generating newsletter with section IDs...")
    if not run_script("generate_monthly_newsletter_with_agenda.py"):
        print("❌ Newsletter generation failed. Stopping.")
        return
    
    # Step 2: Generate Teams agenda
    print("\n2️⃣ Generating Teams agenda...")
    if not run_script("generate_newsletter_agenda.py"):
        print("❌ Agenda generation failed. Stopping.")
        return
    
    print("\n🎉 Newsletter and agenda creation complete!")
    print("\n📋 Files created:")
    print("  - Monthly newsletter (HTML & Markdown)")
    print("  - Teams agenda (copy-paste ready)")
    print("  - HTML agenda (for web viewing)")
    
    print("\n💡 Next steps:")
    print("1. Review the newsletter draft")
    print("2. Copy the agenda from teams-copy-paste-*.txt")
    print("3. Paste the agenda into Microsoft Teams")
    print("4. Publish the newsletter")
    print("5. Share the newsletter link with your team")

if __name__ == "__main__":
    main()
