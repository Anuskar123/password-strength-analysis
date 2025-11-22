from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
GUIDE_MD = ROOT / "docs" / "setup_guide.md"
PDF_OUT = ROOT / "docs" / "password_tool_guide.pdf"

TITLE = "Password Strength & Hygiene Toolkit - Setup Guide"

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, TITLE, 0, 1, "C")
        self.ln(2)
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def main():
    if not GUIDE_MD.exists():
        raise SystemExit(f"Guide file not found: {GUIDE_MD}")
    text = GUIDE_MD.read_text(encoding="utf-8")
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    def write_wrapped(line: str, font_size: int = 11):
        # Strip unsupported unicode for core font (latin-1 only)
        line = line.encode('latin-1', 'ignore').decode('latin-1')
        max_len = 120
        if len(line) == 0:
            pdf.ln(5)
            return
        if len(line) <= max_len:
            pdf.multi_cell(pdf.epw, 5, line)
        else:
            start = 0
            while start < len(line):
                chunk = line[start:start+max_len]
                pdf.multi_cell(pdf.epw, 5, chunk)
                start += max_len
    for raw in text.splitlines():
        line = raw.rstrip()
        # Simple formatting: headings start with '#'
        if line.startswith("#"):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            pdf.set_font("Helvetica", "B", 12 if level == 1 else 11)
            write_wrapped(title)
            pdf.set_font("Helvetica", size=11)
        elif line.strip() == "```bash":
            # Begin code block; set monospace-ish font
            pdf.set_font("Courier", size=9)
        elif line.strip() == "```":
            # End code block
            pdf.set_font("Helvetica", size=11)
        else:
            write_wrapped(line)
    pdf.output(str(PDF_OUT))
    print(f"[+] PDF written to {PDF_OUT}")

if __name__ == "__main__":
    main()
