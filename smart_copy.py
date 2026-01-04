import yaml
import shutil
import os
import sys
from datetime import datetime

class SmartCopy:
    def __init__(self, config_path="copy_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            print(f"Error: Config file not found at {self.config_path}")
            sys.exit(1)
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def execute_tasks(self):
        """Execute all tasks defined in the configuration."""
        tasks = self.config.get('tasks', [])
        if not tasks:
            print("No tasks found in configuration.")
            return

        print(f"Starting Smart Copy... found {len(tasks)} tasks.\n")

        for i, task in enumerate(tasks, 1):
            description = task.get('description', f'Task {i}')
            src_dir = task.get('source_dir')
            dest_dir = task.get('destination_dir')
            files = task.get('files', [])

            print(f"--- Running: {description} ---")
            
            if not src_dir or not dest_dir:
                print("  [SKIPPED] Source or Destination directory missing in config.")
                continue

            # Ensure absolute paths or resolve relative to CWD if needed
            # For this script, we assume paths are either absolute or relative to CWD
            
            if not os.path.exists(src_dir):
                print(f"  [ERROR] Source directory does not exist: {src_dir}")
                continue

            # Create destination if it doesn't exist
            if not os.path.exists(dest_dir):
                try:
                    os.makedirs(dest_dir)
                    print(f"  [INFO] Created destination directory: {dest_dir}")
                except OSError as e:
                    print(f"  [ERROR] Failed to create destination: {e}")
                    continue

            success_count = 0
            
            for filename in files:
                src_file_path = os.path.join(src_dir, filename)
                dest_file_path = os.path.join(dest_dir, filename)

                if os.path.exists(src_file_path):
                    try:
                        shutil.copy2(src_file_path, dest_file_path)
                        print(f"  [OK] Copied: {filename}")
                        success_count += 1
                    except Exception as e:
                        print(f"  [FAIL] Error copying {filename}: {e}")
                else:
                    print(f"  [WARN] Source file not found: {filename}")
            
            print(f"  Completed: {success_count}/{len(files)} files copied.\n")

if __name__ == "__main__":
    app = SmartCopy()
    app.execute_tasks()
