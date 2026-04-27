import subprocess
import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotRestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_bot()
    
    def restart_bot(self):
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
        
        print("\n" + "="*50)
        print("🔄 Перезапуск бота...")
        print("="*50 + "\n")
        
        
        self.process = subprocess.Popen([sys.executable, "main.py"])
    
    def on_modified(self, event):
        if event.src_path.endswith('.py') and not event.src_path.endswith('run.py'):
            print(f"\n📝 Обнаружено изменение в файле: {event.src_path}")
            time.sleep(0.5)  
            self.restart_bot()

if __name__ == '__main__':
    print("🚀 Запуск бота с автоперезагрузкой...")
    print("📁 Отслеживание изменений в .py файлах...")
    print("⏹️  Нажмите Ctrl+C для остановки\n")
    
    event_handler = BotRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Остановка бота...")
        if event_handler.process:
            event_handler.process.terminate()
            event_handler.process.wait()
        observer.stop()
    observer.join()
    print("✅ Бот остановлен")

