from flask import Flask, render_template_string, request, redirect, send_file, jsonify
import os, threading, time
from scraper import run_scraper

app = Flask(__name__)
scraping_status = {'active': False, 'keyword': None}

def background_scrape(keyword):
    run_scraper(keyword)
    scraping_status['active'] = False

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Amazon Scraper</title>
    <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;padding:2rem}
    .container{max-width:800px;margin:auto;border:1px solid #444;padding:2rem}
    h1{margin-bottom:1rem;color:#fff}
    form{display:flex;gap:10px;margin:2rem 0}
    input{flex:1;padding:1rem;background:transparent;color:#fff;border:1px solid #666}
    button{padding:1rem 2rem;background:#fff;color:#000;border:none;cursor:pointer}
    button:hover{background:#ddd}
    </style></head>
    <body><div class="container">
    <h1>Amazon Scraper</h1>
    <form method="POST" action="/search">
    <input name="keyword" placeholder="Search products..." required autofocus>
    <button>Search</button>
    </form>
    </div></body></html>
    ''')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '').strip()
    if not keyword: return redirect('/')
    
    global scraping_status
    if not scraping_status['active']:
        scraping_status['active'] = True
        scraping_status['keyword'] = keyword
        
        thread = threading.Thread(target=background_scrape, args=(keyword,))
        thread.daemon = True
        thread.start()
    
    # Show progress page
    return render_template_string('''
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Searching Amazon</title>
    <style>
    body{background:#000;color:#fff;font-family:sans-serif;padding:4rem;text-align:center}
    .spinner{width:50px;height:50px;border:4px solid #666;border-top-color:#fff;border-radius:50%;
    animation:spin 1s linear infinite;margin:2rem auto}
    @keyframes spin{100%{transform:rotate(360deg)}}
    .progress{width:300px;height:10px;background:#333;margin:2rem auto;border-radius:5px}
    .progress-bar{width:0%;height:100%;background:#0ff;border-radius:5px;transition:width 3s}
    </style>
    <script>
    let progress = 0;
    function updateProgress(){
        progress += 20;
        if(progress > 100) progress = 100;
        document.getElementById('bar').style.width = progress + '%';
        if(progress < 100) setTimeout(updateProgress, 1000);
    }
    setTimeout(updateProgress, 500);
    setTimeout(()=>window.location.href='/results', 6000);
    </script>
    </head>
    <body>
    <h2>Searching Amazon for "{{keyword}}"</h2>
    <p>Scraping product data...</p>
    <div class="spinner"></div>
    <div class="progress"><div class="progress-bar" id="bar"></div></div>
    <p><em>Results will load automatically...</em></p>
    </body></html>
    ''', keyword=keyword)

@app.route('/results')
def results():
    if os.path.exists("data/output/products.html"):
        with open("data/output/products.html", 'r', encoding='utf-8') as f:
            return f.read()
    return '''
    <!DOCTYPE html><html><head><meta http-equiv="refresh" content="2">
    <style>body{background:#000;color:#fff;padding:4rem;text-align:center}</style></head>
    <body>
    <h2>Still processing...</h2>
    <p>This may take 10-15 seconds</p>
    <div class="spinner" style="width:30px;height:30px;border:3px solid #666;border-top-color:#fff;
    border-radius:50%;animation:spin 1s linear infinite;margin:1rem auto"></div>
    <script>setTimeout(()=>location.reload(),2000)</script>
    </body></html>
    '''

@app.route('/download')
def download():
    if os.path.exists("data/output/products.csv"):
        return send_file("data/output/products.csv", as_attachment=True, 
                        download_name=f"amazon_products_{time.strftime('%Y%m%d')}.csv")
    return "No data available", 404

if __name__ == '__main__':
    os.makedirs("data/output", exist_ok=True)
    print("🚀 Server running at http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)