import csv

def save_results(data, keyword):
    # Save CSV
    with open("data/output/products.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Rating", "Image", "Type", "URL"])
        writer.writerows(data)
    
    # Generate HTML
    rows = ""
    for i, row in enumerate(data):
        if row[0].startswith("No products") or row[0].startswith("Error"):
            rows = f'<tr><td colspan="6" style="padding:2rem;text-align:center;color:#f00">{row[0]}</td></tr>'
            break
            
        rows += f'''
        <tr style="border-bottom:1px solid #333">
            <td style="padding:1rem"><img src="{row[3]}" width="60" height="60" style="object-fit:contain" onerror="this.style.display='none'"></td>
            <td style="padding:1rem">{row[0][:80]}</td>
            <td style="color:#0f0;padding:1rem">{row[1]}</td>
            <td style="padding:1rem">{row[2]}</td>
            <td style="color:{"#ff0" if row[4]=="Sponsored" else "#0ff"};padding:1rem">{row[4]}</td>
            <td style="padding:1rem"><a href="{row[5]}" style="color:#fff;border:1px solid #666;padding:5px 10px;text-decoration:none" target="_blank">View</a></td>
        </tr>'''
    
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
    <title>Amazon: {keyword}</title>
    <style>
    body{{background:#000;color:#fff;font-family:sans-serif;margin:0;padding:2rem}}
    table{{width:100%;border-collapse:collapse;margin-top:1rem}}
    th{{background:#111;padding:1rem;text-align:left;border-bottom:2px solid #fff}}
    a:hover{{background:#333}}
    .header{{display:flex;justify-content:space-between;align-items:center}}
    </style></head>
    <body>
    <div class="header">
        <h1 style="margin: auto;width: fit-content">Amazon: {keyword}</h1>
        <div style="margin: auto;width: fit-content;margin-top: 50px;margin-bottom: 50px;"><a href="/" style="color:#fff;margin-right:1rem;width: 50%; border: 1px solid #fff; padding: 10px; border-radius: 10px;text-decoration:none">New Search</a>
        <a href="/download" style="color:#0ff;width: 50%; border: 1px solid #fff; padding: 10px; border-radius: 10px;text-decoration:none">CSV</a></div>
    </div>
    <div style="height: 600px; overflow: scroll; scrollbar-width: none; border: 1px solid #fff;padding: 20px; border-radius: 10px;margin: auto;width: fit-content">  
    <table style="margin: auto;border: 1px solid #fff"><thead><tr>
    <th>Image</th><th>Title</th><th>Price</th><th>Rating</th><th>Type</th><th>Link</th>
    </tr></thead><tbody>{rows}</tbody></table>
    </div>
    </body></html>'''
    
    with open("data/output/products.html", "w", encoding='utf-8') as f:
        f.write(html)