import psutil

def platform_health():
    """Sistem sağlığını döndürür."""
    return {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }

def auto_heal():
    """Eğer bellek %90'ı aşarsa basit bir iyileştirme dene (şimdilik sadece True döner)."""
    if psutil.virtual_memory().percent > 90:
        # Burada önbellek temizleme vb. yapılabilir.
        return True
    return False