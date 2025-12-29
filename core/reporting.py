import json
from datetime import datetime

class ReportExporter:
    @staticmethod
    def generate_html(payload, grade):
        serial = payload['meta'].get('serial', 'Unknown')
        
        # Grading Colors
        color_map = {
            "GOLD": "#27ae60",
            "SILVER": "#f39c12",
            "FAIL": "#c0392b",
            "INCOMPLETE": "#8e44ad"
        }
        header_color = color_map.get(grade, "#333")
        
        html = f"""<!DOCTYPE html><html><head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #eee; padding: 20px; }}
            .header {{ background: {header_color}; color: white; padding: 20px; border-radius: 8px; }}
            .box {{ background: white; margin: 10px 0; padding: 15px; border-left: 6px solid #ccc; }}
            .PASS {{ border-color: #27ae60; }} .FAIL {{ border-color: #c0392b; }} 
            .WARN {{ border-color: #f39c12; }} .INFO {{ border-color: #3498db; }}
            pre {{ background: #f4f4f4; padding: 10px; font-size: 0.9em; overflow-x: auto; }}
        </style></head><body>
        <div class="header">
            <h1>Hardware Certification</h1>
            <h1>Grade: {grade}</h1>
            <p>SN: {serial} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>"""
        
        for r in payload['results']:
            # Inject SVG if present
            extra = ""
            if 'svg_graph' in r['data']:
                extra = f"<div style='margin-top:10px'>{r['data']['svg_graph']}</div>"
            
            html += f"""<div class="box {r['status']}">
                <h3>{r['name']} - {r['status']}</h3>
                <p><strong>{r['summary']}</strong></p>
                {extra}
                <details><summary>Technical Data</summary><pre>{json.dumps(r['data'], indent=2)}</pre></details>
            </div>"""
            
        html += "</body></html>"
        return html