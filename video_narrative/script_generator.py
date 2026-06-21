from ai.report_writer import ReportWriter

def generate_script(df):
    writer = ReportWriter()
    summary = writer.summarize(df)
    lines = summary.split('. ')
    script = []
    for line in lines:
        if line.strip():
            script.append({'text': line.strip(), 'duration': 3})  # saniye
    return script