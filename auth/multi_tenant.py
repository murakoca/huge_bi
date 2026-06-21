from flask import session
from security.rls import apply_rls

def get_tenant_filter():
    """Kullanıcının kiracı ID'sine göre veri filtreleme."""
    tenant_id = session.get('tenant_id', 'default')
    # Örnek: her kiracının farklı bir bölgesi varmış gibi
    tenant_region_map = {
        'tenant_a': ['EU'],
        'tenant_b': ['US', 'ASIA'],
        'default': ['EU']
    }
    return tenant_region_map.get(tenant_id, ['EU'])

def apply_tenant_rls(df):
    allowed_regions = get_tenant_filter()
    return apply_rls(df, 'Region', allowed_regions)