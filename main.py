from datetime import datetime
import re
from pathlib import Path

README_PATH = Path("README.md")

def update_readme():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = "# My Project\n\nLast run: <!-- LAST_RUN -->\n"

    # Replace the placeholder or add it if not found
    if "<!-- LAST_RUN -->" in content:
        updated_content = re.sub(
            r"<!-- LAST_RUN -->.*",
            f"<!-- LAST_RUN --> {now_str}",
            content
        )
    else:
        updated_content = content.strip() + f"\n\nLast run: <!-- LAST_RUN --> {now_str}\n"

    README_PATH.write_text(updated_content, encoding="utf-8")
    print(f"✅ README updated with timestamp {now_str}")

def main():
    print("Hi, I am a cron job")
    print(f"Now the time is {datetime.now()}")
    update_readme()

if __name__ == "__main__":
    main()
