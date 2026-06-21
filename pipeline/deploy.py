import os
import shutil
import subprocess
import sys

def deploy(environment):
    print(f"Dağıtım başlıyor: {environment}")
    # Örnek: rapor PDF'lerini veya yapılandırmaları kopyala
    if environment == 'production':
        os.makedirs('deploy/prod', exist_ok=True)
        shutil.copy('sales.db', 'deploy/prod/sales.db')
        subprocess.run([sys.executable, 'app.py', '--env', 'prod'])
    elif environment == 'test':
        print("Test ortamına yayınlandı.")
    else:
        print("Geliştirme ortamında çalışıyor.")