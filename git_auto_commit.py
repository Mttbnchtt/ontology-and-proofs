import subprocess
import time
import datetime
import collections

def parse_git_status():
    """Parse git status --porcelain output into categorized changes."""
    changes = collections.defaultdict(list)
    
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
                
            # Get status codes and filename
            status = line[:2]
            filename = line[3:].strip()
            
            # Categorize changes
            if status == 'M ' or status == ' M':
                changes['modified'].append(filename)
            elif status == 'A ' or status == 'AM':
                changes['added'].append(filename)
            elif status == 'D ' or status == ' D':
                changes['deleted'].append(filename)
            elif status == '??':
                changes['untracked'].append(filename)
            elif status.startswith('R'):
                changes['renamed'].append(filename)
            
        return changes, len(result.stdout.splitlines())
    except Exception as e:
        print(f"Error checking git status: {e}")
        return collections.defaultdict(list), 0

def commit_changes():
    try:
        # Add all changes
        subprocess.run(['git', 'add', '--all'])
        
        # Get categorized changes
        changes, _ = parse_git_status()
        
        # Create commit message with changes
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        changes_list = []
        for change_type, files in changes.items():
            if files:
                changes_list.append(f"{change_type}: {', '.join(files)}")
        
        message = f"Auto-commit at {timestamp} {'; '.join(changes_list)}"
        
        # Commit
        subprocess.run(['git', 'commit', '-m', message])
        
        # Push
        subprocess.run(['git', 'push'])
        
        print(f"Successfully committed and pushed changes: {message}")
    except Exception as e:
        print(f"Error during git operations: {e}")

def count_changes():
    _, count = parse_git_status()
    return count

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
        
        time.sleep(600)  # Check every 600 seconds (10 minutes)

if __name__ == "__main__":
    main()