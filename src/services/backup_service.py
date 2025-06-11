import os
import shutil
from datetime import datetime
from typing import List, Tuple

try:
from ..models.database import DB_PATH, get_data_dir
except ImportError:
    # Для работы в тестах
    from models.database import DB_PATH, get_data_dir

class BackupService:
    """Сервис для резервного копирования базы данных"""
    
    @staticmethod
    def get_backup_dir() -> str:
        """Получить директорию для резервных копий"""
        backup_dir = os.path.join(get_data_dir(), 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        return backup_dir
    
    @staticmethod
    def create_backup(custom_path: str = None) -> Tuple[bool, str]:
        """
        Создать резервную копию базы данных
        custom_path: пользовательский путь для сохранения
        Возвращает (success, message)
        """
        try:
            if not os.path.exists(DB_PATH):
                return False, "База данных не найдена"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"autoparts_backup_{timestamp}.db"
            
            if custom_path:
                backup_path = os.path.join(custom_path, backup_filename)
                # Создаем директорию если её нет
                os.makedirs(custom_path, exist_ok=True)
            else:
                backup_path = os.path.join(BackupService.get_backup_dir(), backup_filename)
            
            shutil.copy2(DB_PATH, backup_path)
            
            return True, f"Резервная копия создана: {backup_path}"
            
        except Exception as e:
            return False, f"Ошибка создания резервной копии: {str(e)}"
    
    @staticmethod
    def restore_backup(backup_path: str) -> Tuple[bool, str]:
        """
        Восстановить базу данных из резервной копии
        backup_path: путь к файлу резервной копии
        Возвращает (success, message)
        """
        try:
            if not os.path.exists(backup_path):
                return False, "Файл резервной копии не найден"
            
            # Создаем копию текущей базы на случай отката
            current_backup = f"{DB_PATH}.current_backup"
            if os.path.exists(DB_PATH):
                shutil.copy2(DB_PATH, current_backup)
            
            # Восстанавливаем из резервной копии
            shutil.copy2(backup_path, DB_PATH)
            
            # Удаляем временную копию
            if os.path.exists(current_backup):
                os.remove(current_backup)
            
            return True, f"База данных восстановлена из: {backup_path}"
            
        except Exception as e:
            # Пытаемся восстановить оригинал
            current_backup = f"{DB_PATH}.current_backup"
            if os.path.exists(current_backup):
                shutil.copy2(current_backup, DB_PATH)
                os.remove(current_backup)
            
            return False, f"Ошибка восстановления: {str(e)}"
    
    @staticmethod
    def get_backup_list() -> List[dict]:
        """Получить список доступных резервных копий"""
        backup_dir = BackupService.get_backup_dir()
        backups = []
        
        try:
            for filename in os.listdir(backup_dir):
                if filename.endswith('.db') and filename.startswith('autoparts_backup_'):
                    filepath = os.path.join(backup_dir, filename)
                    stat = os.stat(filepath)
                    
                    backups.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'modified': datetime.fromtimestamp(stat.st_mtime)
                    })
            
            # Сортируем по дате создания (новые первыми)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            print(f"Ошибка получения списка копий: {e}")
        
        return backups
    
    @staticmethod
    def delete_backup(backup_path: str) -> Tuple[bool, str]:
        """Удалить резервную копию"""
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
                return True, "Резервная копия удалена"
            else:
                return False, "Файл не найден"
        except Exception as e:
            return False, f"Ошибка удаления: {str(e)}"
    
    @staticmethod
    def cleanup_old_backups(keep_count: int = 10) -> int:
        """
        Очистка старых резервных копий
        keep_count: количество копий для сохранения
        Возвращает количество удаленных файлов
        """
        backups = BackupService.get_backup_list()
        deleted_count = 0
        
        if len(backups) > keep_count:
            backups_to_delete = backups[keep_count:]
            
            for backup in backups_to_delete:
                try:
                    os.remove(backup['filepath'])
                    deleted_count += 1
                except Exception as e:
                    print(f"Ошибка удаления {backup['filename']}: {e}")
        
        return deleted_count
    
    @staticmethod
    def auto_backup() -> Tuple[bool, str]:
        """Автоматическое резервное копирование"""
        return BackupService.create_backup() 