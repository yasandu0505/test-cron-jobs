from datetime import datetime
import re
from pathlib import Path

README_PATH = Path("README.md")

def update_readme():
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%B %d, %Y")
    
    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = """# 🤖 Automated Cron Job Test

Welcome to my automated cron job repository! This README is updated automatically every 5 minutes.

## 📊 Run Statistics
<!-- STATS_START -->
**Total Runs:** 0  
**Last Updated:** Never  
**Status:** 🟢 Active
<!-- STATS_END -->

## 📝 Recent Run History
<!-- HISTORY_START -->
<!-- HISTORY_END -->

---
*This file is automatically updated by GitHub Actions* ⚡
"""
    
    # Extract current stats
    stats_match = re.search(r'<!-- STATS_START -->(.*?)<!-- STATS_END -->', content, re.DOTALL)
    current_runs = 0
    
    if stats_match:
        run_match = re.search(r'\*\*Total Runs:\*\* (\d+)', stats_match.group(1))
        if run_match:
            current_runs = int(run_match.group(1))
    
    new_run_count = current_runs + 1
    
    # Update stats section
    new_stats = f"""<!-- STATS_START -->
**Total Runs:** {new_run_count}  
**Last Updated:** {date_str} at {now.strftime("%I:%M:%S %p")}  
**Status:** 🟢 Active
<!-- STATS_END -->"""
    
    if "<!-- STATS_START -->" in content:
        content = re.sub(
            r'<!-- STATS_START -->.*?<!-- STATS_END -->',
            new_stats,
            content,
            flags=re.DOTALL
        )
    else:
        # Add stats section if not found
        content = content.replace("# 🤖 Automated Cron Job Test", 
                                f"# 🤖 Automated Cron Job Test\n\n## 📊 Run Statistics\n{new_stats}")
    
    # Create new log entry
    emoji_list = ["🚀", "⭐", "🎯", "💫", "🔥", "✨", "🎉", "🌟", "💪", "🎊"]
    emoji = emoji_list[new_run_count % len(emoji_list)]
    
    new_log_entry = f"""
### {emoji} Run #{new_run_count} - {timestamp_str}
- **Date:** {date_str}
- **Time:** {now.strftime("%I:%M:%S %p")} UTC
- **Status:** ✅ Success
- **Action:** README updated automatically
"""
    
    # Add to history section
    if "<!-- HISTORY_START -->" in content and "<!-- HISTORY_END -->" in content:
        history_match = re.search(r'<!-- HISTORY_START -->(.*?)<!-- HISTORY_END -->', content, re.DOTALL)
        
        if history_match:
            existing_history = history_match.group(1).strip()
            
            # Keep only last 10 entries to prevent file from getting too large
            history_entries = re.findall(r'### [^\n]+ - \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*?(?=### |$)', existing_history, re.DOTALL)
            
            # Keep most recent 9 entries and add the new one
            recent_entries = history_entries[:9] if len(history_entries) >= 9 else history_entries
            
            new_history = f"<!-- HISTORY_START -->{new_log_entry}"
            for entry in recent_entries:
                new_history += f"\n{entry.strip()}\n"
            new_history += "<!-- HISTORY_END -->"
            
            content = re.sub(
                r'<!-- HISTORY_START -->.*?<!-- HISTORY_END -->',
                new_history,
                content,
                flags=re.DOTALL
            )
        else:
            # First entry
            content = content.replace(
                "<!-- HISTORY_START -->\n<!-- HISTORY_END -->",
                f"<!-- HISTORY_START -->{new_log_entry}\n<!-- HISTORY_END -->"
            )
    else:
        # Add history section if not found
        history_section = f"\n## 📝 Recent Run History\n<!-- HISTORY_START -->{new_log_entry}\n<!-- HISTORY_END -->"
        content = content.strip() + history_section
    
    README_PATH.write_text(content, encoding="utf-8")
    print(f"✅ README updated! Run #{new_run_count} logged at {timestamp_str}")

def main():
    print("🤖 Hi, I am a cron job!")
    print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📝 Updating README with new run log...")
    update_readme()
    print("🎉 All done!")

if __name__ == "__main__":
    main()