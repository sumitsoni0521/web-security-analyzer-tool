from flask import Flask, render_template, request, send_file, session
from urllib.parse import urlparse
import socket

# ReportLab PDF Imports
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Import Project Modules
from port_scanner import scan_ports
from header_check import check_headers
from ssl_check import check_ssl
from vulnerability_scan import check_sql_injection
from xss_detector import detect_xss
from subdomain_scanner import scan_subdomains
from whois_lookup import get_whois
from safety_score import calculate_score

app = Flask(__name__)
app.secret_key = "cyber_security_project_key"


# ================= HOME ROUTE =================

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        url = request.form.get('url')

        try:

            if not url.startswith("http"):
                url = "http://" + url

            parsed_url = urlparse(url)
            hostname = parsed_url.hostname

            if hostname is None:
                return render_template('index.html', error="Invalid URL")

            domain = hostname.replace("www.", "")

            host_ip = socket.gethostbyname(hostname)

            # Run All Modules
            ports = scan_ports(host_ip)
            headers = check_headers(url)
            ssl_data = check_ssl(hostname)
            ssl_status = ssl_data["status"]
            sql = check_sql_injection(url)
            xss = detect_xss(url)
            subs = scan_subdomains(domain)
            whois_info = get_whois(domain)

            # Safety Score
            score = calculate_score(ports, headers, ssl_status, sql, xss)

            # Store Data in Session for PDF
            session['report'] = {
                "score": score,
                "ssl_status": ssl_status,
                "ssl_data": ssl_data,
                "sql": sql,
                "xss": xss,
                "ports": ports,
                "headers": headers,
                "subs": subs,
                "whois": whois_info
            }

            return render_template('index.html',
                                   ports=ports,
                                   headers=headers,
                                   ssl=ssl_status,
                                   ssl_data=ssl_data,
                                   sql=sql,
                                   xss=xss,
                                   subs=subs,
                                   whois=whois_info,
                                   score=score)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')


# ================= DOWNLOAD REPORT =================

@app.route('/download_report')
def download_report():

    report = session.get('report')

    if not report:
        return "Please scan a website first."

    doc = SimpleDocTemplate("Security_Report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Website Security Analysis Report</b>", styles['Title']))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"Safety Score : {report['score']}%", styles['Normal']))
    story.append(Paragraph(f"SSL Status : {report['ssl_status']}", styles['Normal']))
    story.append(Paragraph(f"SQL Injection : {report['sql']}", styles['Normal']))
    story.append(Paragraph(f"XSS Risk : {report['xss']}", styles['Normal']))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>SSL Information</b>", styles['Heading2']))
    story.append(Paragraph(f"Issuer : {report['ssl_data']['issuer']}", styles['Normal']))
    story.append(Paragraph(f"Expiry Date : {report['ssl_data']['expiry_date']}", styles['Normal']))
    story.append(Paragraph(f"Days Remaining : {report['ssl_data']['days_remaining']}", styles['Normal']))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Open Ports</b>", styles['Heading2']))
    for p in report['ports']:
        story.append(Paragraph(f"{p['port']} - {p['service']}", styles['Normal']))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Security Headers</b>", styles['Heading2']))
    for key,value in report['headers'].items():
        story.append(Paragraph(f"{key} : {value}", styles['Normal']))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Subdomains</b>", styles['Heading2']))
    for s in report['subs']:
        story.append(Paragraph(s, styles['Normal']))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>WHOIS Information</b>", styles['Heading2']))
    for key,value in report['whois'].items():
        story.append(Paragraph(f"{key} : {value}", styles['Normal']))

    doc.build(story)

    return send_file("Security_Report.pdf", as_attachment=True)


# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)
