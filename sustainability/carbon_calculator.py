def calculate_report_carbon(report_size_mb, server_location='EU'):
    """
    Basit karbon ayak izi modeli.
    - 1 MB veri aktarımı ~ 0.001 kWh elektrik tüketir.
    - Bölgeye göre karbon yoğunluğu (kg CO₂ / kWh).
    """
    energy_kwh = report_size_mb * 0.001
    carbon_intensity = {
        'EU': 0.3,
        'US': 0.4,
        'ASIA': 0.5
    }.get(server_location, 0.4)
    return energy_kwh * carbon_intensity