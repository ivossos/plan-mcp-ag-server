"""Extract all content from rooms.docx to check for dimension intersections."""

import zipfile
import xml.etree.ElementTree as ET

def extract_docx_content(filename):
    """Extract all text content from a docx file."""
    z = zipfile.ZipFile(filename)
    xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # Extract all text
    all_text = []
    for t in root.findall('.//w:t', ns):
        if t.text:
            all_text.append(t.text)
    
    # Extract tables
    tables = root.findall('.//w:tbl', ns)
    print(f"Found {len(tables)} tables")
    
    # Extract table content
    table_data = []
    for i, table in enumerate(tables):
        rows = table.findall('.//w:tr', ns)
        table_rows = []
        for row in rows:
            cells = row.findall('.//w:tc', ns)
            row_data = []
            for cell in cells:
                cell_text = ' '.join([t.text or '' for t in cell.findall('.//w:t', ns)])
                row_data.append(cell_text.strip())
            if any(row_data):
                table_rows.append(row_data)
        if table_rows:
            table_data.append(table_rows)
    
    return {
        'text': ' '.join(all_text),
        'paragraphs': [p for p in all_text if p.strip()],
        'tables': table_data
    }

if __name__ == "__main__":
    content = extract_docx_content('rooms.docx')
    
    print("="*60)
    print("FULL TEXT CONTENT:")
    print("="*60)
    print(content['text'])
    
    print("\n" + "="*60)
    print("PARAGRAPHS:")
    print("="*60)
    for i, para in enumerate(content['paragraphs'], 1):
        print(f"{i}. {para}")
    
    print("\n" + "="*60)
    print("TABLES:")
    print("="*60)
    for i, table in enumerate(content['tables'], 1):
        print(f"\nTable {i}:")
        for j, row in enumerate(table, 1):
            print(f"  Row {j}: {' | '.join(row)}")
    
    # Check for dimension-related keywords
    print("\n" + "="*60)
    print("DIMENSION KEYWORDS CHECK:")
    print("="*60)
    keywords = ['dimension', 'entity', 'scenario', 'period', 'year', 'intersection', 
                'pov', 'column', 'row', 'account', 'fccs', 'total geography', 
                'actual', 'budget', 'fy24', 'fy25', 'jan', 'feb', 'mar']
    found_keywords = []
    text_lower = content['text'].lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            found_keywords.append(keyword)
    
    if found_keywords:
        print(f"Found keywords: {', '.join(found_keywords)}")
    else:
        print("No dimension-related keywords found in text content")





