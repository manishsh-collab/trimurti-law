import urllib.request
import re
from urllib.parse import urljoin
import tempfile
import os

URL = "https://www.supremecourt.gov/opinions/USReports.aspx"

print(f"Testing connection to {URL}...")
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Trimurti Legal crawler)'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        print(f"Success! HTML length: {len(html)}")
        
        # Find PDFs
        links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        pdfs = [l for l in links if l.lower().endswith('.pdf')]
        print(f"Found {len(pdfs)} PDF links.")
        
        if pdfs:
            pdf_url = urljoin(URL, pdfs[0])
            print(f"Testing download of: {pdf_url}")
            
            with urllib.request.urlopen(pdf_url, timeout=10) as pdf_resp:
                pdf_data = pdf_resp.read()
                print(f"Downloaded {len(pdf_data)} bytes.")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(pdf_data)
                    tmp_path = tmp.name
                
                print(f"Saved to {tmp_path}. Testing pypdf extraction...")
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(tmp_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    print(f"Extracted {len(text)} characters.")
                    print(f"Sample: {text[:200]}")
                except ImportError:
                    print("ERROR: pypdf not installed!")
                except Exception as e:
                    print(f"ERROR extracting text: {e}")
                finally:
                    os.unlink(tmp_path)
        else:
            print("No PDFs found on page!")

except Exception as e:
    print(f"Connection failed: {e}")
