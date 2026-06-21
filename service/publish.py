from flask import Blueprint, request, jsonify
from auth.auth import login_required
import datetime

publish_bp = Blueprint('publish', __name__)

# Basit bir sözlükte raporları tutuyoruz (gerçekte DB)
published_reports = {}

@publish_bp.route('/publish', methods=['POST'])
@login_required
def publish_report():
    data = request.get_json()
    name = data['name']
    # Rapor nesnesini kaydet (gerçekte model ve görseller)
    published_reports[name] = {
        'author': current_user.username,
        'published_date': datetime.datetime.now().isoformat(),
        'status': 'published'
    }
    return jsonify({'message': 'Rapor yayınlandı', 'report': name}), 201

@publish_bp.route('/share', methods=['POST'])
@login_required
def share_report():
    data = request.get_json()
    report = data['report']
    user_email = data['email']
    # Yetkilendirme kontrolü
    print(f"{report} raporu {user_email} ile paylaşıldı.")
    return jsonify({'message': 'Paylaşıldı'}), 200

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def scheduled_refresh():
    # Veri kaynağından tekrar çek, modeli güncelle
    print("Veri yenileniyor...")
    # model.load_table(...) güncelleme

scheduler.add_job(scheduled_refresh, 'interval', hours=1)
scheduler.start()