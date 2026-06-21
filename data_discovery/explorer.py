from flask import render_template_string, request

EXPLORER_TEMPLATE = '''
<h2>Veri Keşfi</h2>
<form method="get">
  <input type="text" name="term" placeholder="Ara...">
  <input type="submit" value="Ara">
</form>
{% if results %}
<ul>
  {% for key, val in results.items() %}
  <li><b>{{ key }}</b>: {{ val.description }}</li>
  {% endfor %}
</ul>
{% endif %}
'''