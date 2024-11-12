import os
import subprocess
import time
import datetime

def count_changes():
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        return len(result.stdout.splitlines())
    except Exception as e:
        print(f"Error checking git status: {e}")
        return 0

def commit_changes():
    try:
        # Add all changes
        subprocess.run(['git', 'add', '--all'])
        
        # Create commit message with timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Auto-commit: Batch of changes at {timestamp}"
        
        # Commit
        subprocess.run(['git', 'commit', '-m', message])
        
        # Push
        subprocess.run(['git', 'push'])
        
        print(f"Successfully committed and pushed changes: {message}")
    except Exception as e:
        print(f"Error during git operations: {e}")

def main():
    change_count = 0
    last_change_count = 0
    
    print("Monitoring git changes... (Press Ctrl+C to stop)")
    
    while True:
        current_changes = count_changes()
        
        if current_changes != last_change_count:
            change_count += abs(current_changes - last_change_count)
            last_change_count = current_changes
            
            print(f"Changes detected. Total changes: {change_count}")
            
            if change_count >= 1:
                print("Committing changes...")
                commit_changes()
                change_count = 0
        
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()