#!/usr/bin/env python3
"""
File Watcher for Development
Monitors Python files and notifies you when changes are detected.
You need to manually restart the server to avoid PyTorch mutex errors.

This is a workaround since:
- uvicorn --reload uses watchfiles which triggers PyTorch mutex errors
- subprocess spawning also triggers the same errors on macOS

Usage: Run this in one terminal, run the server separately in another.
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeNotifier(FileSystemEventHandler):
    """Notifies when files change"""
    
    def __init__(self):
        self.last_change = {}
        self.debounce_seconds = 1
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if not event.src_path.endswith('.py'):
            return
            
        # Debounce multiple events for the same file
        current_time = time.time()
        last_time = self.last_change.get(event.src_path, 0)
        
        if current_time - last_time < self.debounce_seconds:
            return
            
        self.last_change[event.src_path] = current_time
        
        file_name = Path(event.src_path).name
        print(f"\n⚠️  FILE CHANGED: {file_name}")
        print("🔄 Please restart the server manually:")
        print("   ./restart_server.sh")
        print()

def main():
    print("=" * 60)
    print("� File Watcher - Development Mode")
    print("=" * 60)
    print("Watching: backend/*.py")
    print("Will notify you when files change")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    handler = ChangeNotifier()
    observer = Observer()
    watch_path = Path(__file__).parent
    observer.schedule(handler, str(watch_path), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✅ File watcher stopped")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
