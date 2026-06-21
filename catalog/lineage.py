def generate_lineage(dataset_name):
    # Basit: transformation adımlarını sıralayarak döndürür
    conn = sqlite3.connect(CATALOG_DB)
    cur = conn.execute("""
        SELECT t.step_name, t.description
        FROM transformations t
        JOIN datasets d ON t.dataset_id = d.id
        WHERE d.name = ?
        ORDER BY t.timestamp
    """, (dataset_name,))
    steps = cur.fetchall()
    conn.close()
    lines = ["graph TD;"]
    for i, (name, desc) in enumerate(steps):
        lines.append(f"  step{i}[{name}: {desc}]")
        if i > 0:
            lines.append(f"  step{i-1} --> step{i}")
    return "\n".join(lines)