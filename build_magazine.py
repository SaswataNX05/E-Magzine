#!/usr/bin/env python3
"""
E-Magazine Generator: "Securing the Northeast: Indian Army’s Role in Stability, Peace & National Security"
Generates a complete, high-quality, visually appealing 50-page e-magazine in HTML
and compiles it into a publication-ready PDF using headless Chromium.
All articles published on or after 01 September 2026 with associated sources/links.
Includes Appendix 1 (Source Directory & Article Counts) and Appendix 2 (Selection Rationale & Citations).
"""

import os
import sys
import subprocess

OUTPUT_DIR = "/home/saswata/PROGRAMING/Projects/e-magazine"
HTML_PATH = os.path.join(OUTPUT_DIR, "magazine.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "Securing_The_Northeast_EMagazine.pdf")

def get_css():
    return """
    @page {
        size: A4 portrait;
        margin: 0;
    }
    *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #1e293b;
        background: #e2e8f0;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .page {
        width: 210mm;
        height: 297mm;
        max-height: 297mm;
        page-break-after: always;
        position: relative;
        background: #ffffff;
        padding: 13mm 18mm 12mm 18mm;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    /* Running Header */
    .running-header {
        border-bottom: 2px solid #0f2b48;
        padding-bottom: 4px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #475569;
    }
    .running-header .tag-pill {
        background: #0f2b48;
        color: #f8fafc;
        padding: 2px 8px;
        border-radius: 3px;
        font-weight: 700;
        font-size: 7.5pt;
    }
    .running-header .issue-stamp {
        color: #b45309;
        font-weight: 600;
    }

    /* Running Footer */
    .running-footer {
        margin-top: auto;
        border-top: 1px solid #cbd5e1;
        padding-top: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 8pt;
        color: #64748b;
    }
    .running-footer .doc-info {
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .running-footer .page-number {
        font-weight: 700;
        color: #0f2b48;
        background: #f1f5f9;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }

    /* Common Article Layout */
    .article-container {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .article-kicker {
        font-size: 8.5pt;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #b45309;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .article-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 17.5pt;
        line-height: 1.25;
        color: #0a192f;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .meta-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 8pt;
        color: #475569;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 5px 10px;
        border-radius: 4px;
        margin-bottom: 11px;
    }
    .meta-bar span strong {
        color: #0f2b48;
    }

    /* Article 2-Column Content */
    .article-body {
        font-size: 8.7pt;
        line-height: 1.48;
        color: #273444;
        column-count: 2;
        column-gap: 18px;
        text-align: justify;
        flex: 1;
    }
    .article-body p {
        margin-bottom: 9px;
        text-indent: 10px;
    }
    .article-body p:first-of-type {
        text-indent: 0;
    }
    .article-body p:first-of-type::first-letter {
        font-size: 26pt;
        font-family: Georgia, serif;
        float: left;
        line-height: 0.85;
        margin-right: 6px;
        color: #0f2b48;
        font-weight: bold;
    }

    /* Sidebars & Pullouts */
    .highlight-card {
        background: #f1f5f9;
        border-left: 3px solid #b45309;
        padding: 7px 10px;
        margin: 8px 0;
        font-size: 8.2pt;
        line-height: 1.35;
        color: #1e293b;
        break-inside: avoid;
        border-radius: 0 4px 4px 0;
    }
    .highlight-card strong {
        color: #b45309;
        display: block;
        margin-bottom: 2px;
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .quote-box {
        background: #eff6ff;
        border-left: 3px solid #1d4ed8;
        padding: 7px 10px;
        margin: 8px 0;
        font-style: italic;
        font-size: 8.2pt;
        line-height: 1.35;
        color: #1e3a8a;
        break-inside: avoid;
    }
    .quote-box .author {
        font-style: normal;
        font-weight: 600;
        text-align: right;
        display: block;
        margin-top: 3px;
        font-size: 7.5pt;
        color: #3b82f6;
    }

    /* Citation Box */
    .citation-strip {
        margin-top: 8px;
        padding: 5px 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0f2b48;
        border-radius: 3px;
        font-size: 7.5pt;
        color: #475569;
        line-height: 1.3;
    }
    .citation-strip strong {
        color: #0f2b48;
    }
    .citation-strip a {
        color: #1d4ed8;
        text-decoration: underline;
    }

    /* Section Divider Pages */
    .divider-page {
        background: linear-gradient(145deg, #0b1d3a 0%, #152c50 60%, #1e3a8a 100%);
        color: #ffffff;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 22mm 20mm;
    }
    .divider-badge {
        display: inline-block;
        background: #f59e0b;
        color: #0b1d3a;
        font-weight: 800;
        font-size: 9pt;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .divider-title {
        font-family: Georgia, serif;
        font-size: 32pt;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .divider-subtitle {
        font-size: 13pt;
        color: #cbd5e1;
        max-width: 150mm;
        margin: 0 auto 30px auto;
        line-height: 1.5;
        font-weight: 300;
    }
    .divider-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        width: 100%;
        max-width: 160mm;
        margin-bottom: 30px;
    }
    .divider-stat-box {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 12px 10px;
        border-radius: 6px;
    }
    .divider-stat-val {
        font-size: 20pt;
        font-weight: 800;
        color: #f59e0b;
        margin-bottom: 3px;
        font-family: Georgia, serif;
    }
    .divider-stat-label {
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #e2e8f0;
    }
    .divider-desc {
        font-size: 9.3pt;
        line-height: 1.55;
        color: #e2e8f0;
        max-width: 150mm;
        margin: 0 auto;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding-top: 18px;
        text-align: justify;
    }

    /* Tables in Appendices */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 7.5pt;
        line-height: 1.3;
        margin-top: 6px;
    }
    .data-table th {
        background: #0f2b48;
        color: #ffffff;
        text-align: left;
        padding: 5px 7px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: 1px solid #0f2b48;
    }
    .data-table td {
        padding: 3.5px 7px;
        border: 1px solid #cbd5e1;
        color: #334155;
    }
    .data-table tr:nth-child(even) td {
        background: #f8fafc;
    }
    .data-table tr:hover td {
        background: #f1f5f9;
    }

    /* Compact Tables for Appendix 2 */
    .data-table-compact {
        width: 100%;
        border-collapse: collapse;
        font-size: 6.7pt;
        line-height: 1.22;
        margin-top: 4px;
    }
    .data-table-compact th {
        background: #0f2b48;
        color: #ffffff;
        text-align: left;
        padding: 4px 6px;
        font-weight: 600;
        letter-spacing: 0.4px;
        border: 1px solid #0f2b48;
        font-size: 6.8pt;
    }
    .data-table-compact td {
        padding: 2.2px 5px;
        border: 1px solid #cbd5e1;
        color: #334155;
    }
    .data-table-compact tr:nth-child(even) td {
        background: #f8fafc;
    }
    """

def main():
    print("Beginning generation of 50-page e-magazine...")
    # Generate the HTML using the comprehensive generator
    import generate_pages
    html_content = generate_pages.build_full_magazine_html(get_css())
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML successfully written to: {HTML_PATH} (Length: {len(html_content)} chars)")
    
    print("Compiling HTML to PDF with headless Chromium...")
    cmd = [
        "chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error during Chromium PDF compilation:", res.stderr)
        sys.exit(1)
    
    print(f"PDF successfully compiled to: {PDF_PATH}")
    
    # Check page count with pdfinfo
    pdfinfo_res = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
    print(pdfinfo_res.stdout)

if __name__ == "__main__":
    main()
