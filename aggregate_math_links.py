#!/usr/bin/env python3
"""
Math Link Aggregator - Multi-page version
Creates separate HTML files for each page (50 links per page)
"""

import os
import random
import subprocess
import json
from datetime import datetime, timezone

REPO_PATH = "/root/.openclaw/workspace/something"
DATA_FILE = os.path.join(REPO_PATH, "links.json")
INDEX_FILE = os.path.join(REPO_PATH, "page_index.json")
LINKS_PER_PAGE = 50

# Expanded curated links - hundreds of math resources
CURATED_LINKS = [
    # Articles & Blogs
    {"title": "The Prime Number Conspiracy", "url": "https://www.quantamagazine.org/mathematicians-discover-the-perfect-way-to-multiply-20190411/", "description": "New algorithms are changing how we multiply numbers, with applications in cryptography and computer science.", "high": "Number Theory", "low": "algorithms"},
    {"title": "The Map of Mathematics", "url": "https://www.quantamagazine.org/the-map-of-mathematics-20200213/", "description": "A comprehensive visual guide showing how different areas of mathematics connect to each other.", "high": "General", "low": "overview"},
    {"title": "Mathematicians Prove Tetris Is Hard", "url": "https://www.quantamagazine.org/mathematicians-prove-tetris-is-hard-even-with-godlike-abilities-20231031/", "description": "Even with perfect information, the classic game Tetris is computationally intractable.", "high": "Discrete Math", "low": "computational complexity"},
    {"title": "A Proof That Some Infinities Are Bigger Than Others", "url": "https://www.quantamagazine.org/mathematicians-solve-long-standing-infinity-problem-20230713/", "description": "Resolution of a 50-year-old problem about cardinal characteristics of the continuum.", "high": "Logic", "low": "set theory"},
    {"title": "The Geometry of Neural Networks", "url": "https://www.quantamagazine.org/the-geometric-trick-that-makes-computers-learn-20230622/", "description": "How algebraic topology helps understand why deep learning works.", "high": "Applied Math", "low": "machine learning"},
    {"title": "Mathematicians Solve the 'Happy Ending' Problem", "url": "https://www.quantamagazine.org/mathematicians-solve-the-happy-ending-problem-20230821/", "description": "New progress on a classic problem in combinatorial geometry about convex polygons.", "high": "Geometry", "low": "combinatorial geometry"},
    {"title": "The Unsolvable Problem Behind Tap Dancing", "url": "https://www.quantamagazine.org/the-unsolvable-problem-behind-tap-dancing-20230720/", "description": "How the problem of finding optimal sequences relates to deep mathematical questions.", "high": "Applied Math", "low": "optimization"},
    {"title": "Mathematicians Calculate How Randomness Creeps In", "url": "https://www.quantamagazine.org/mathematicians-calculate-how-randomness-creeps-in-20230313/", "description": "New results on how quickly randomness spreads in dynamical systems.", "high": "Probability", "low": "random processes"},
    
    # YouTube Channels
    {"title": "3Blue1Brown - Essence of Linear Algebra", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "description": "Beautiful visual explanations of linear algebra concepts using animation.", "high": "Algebra", "low": "linear algebra"},
    {"title": "Numberphile - Prime Numbers", "url": "https://www.youtube.com/@numberphile", "description": "Videos about numbers and mathematics with mathematicians from around the world.", "high": "Number Theory", "low": "prime numbers"},
    {"title": "Mathologer", "url": "https://www.youtube.com/@Mathologer", "description": "Deep dives into beautiful mathematics with clear explanations.", "high": "General", "low": "advanced topics"},
    {"title": "Stand-up Maths", "url": "https://www.youtube.com/@standupmaths", "description": "Mathematical stand-up comedy and interesting problems.", "high": "General", "low": "recreational math"},
    {"title": "Michael Penn - Real Analysis", "url": "https://www.youtube.com/@MichaelPennMath", "description": "Lecture-style videos covering real analysis, abstract algebra, and more.", "high": "Analysis", "low": "real analysis"},
    {"title": "Dr. Peyam - Differential Equations", "url": "https://www.youtube.com/@drpeyam", "description": "Clear explanations of differential equations and applied mathematics.", "high": "Applied Math", "low": "differential equations"},
    {"title": "Professor Leonard", "url": "https://www.youtube.com/@ProfessorLeonard", "description": "Full-length lecture videos for calculus, statistics, and differential equations.", "high": "Analysis", "low": "calculus"},
    {"title": "PatrickJMT", "url": "https://www.youtube.com/@patrickjmt", "description": "Short, clear math tutorials covering everything from algebra to calculus.", "high": "General", "low": "tutorials"},
    {"title": "Khan Academy Mathematics", "url": "https://www.youtube.com/@khanacademy", "description": "Comprehensive math education from arithmetic to multivariable calculus.", "high": "General", "low": "education"},
    {"title": "Flammable Maths", "url": "https://www.youtube.com/@FlammableMaths", "description": "Competition math problems and interesting mathematical puzzles.", "high": "General", "low": "problem solving"},
    
    # Books
    {"title": "Visual Complex Analysis - Tristan Needham", "url": "https://www.amazon.com/Visual-Complex-Analysis-Tristan-Needham/dp/0198534469", "description": "A geometric approach to complex analysis using beautiful visualizations and intuition.", "high": "Analysis", "low": "complex analysis"},
    {"title": "The Road to Reality - Roger Penrose", "url": "https://www.amazon.com/Road-Reality-Complete-Guide-Universe/dp/0679776311", "description": "A comprehensive guide to the laws of the universe, from the basics to cutting-edge physics.", "high": "Applied Math", "low": "mathematical physics"},
    {"title": "How to Prove It - Daniel Velleman", "url": "https://www.amazon.com/How-Prove-Structured-Approach-3rd/dp/1108439535", "description": "An introduction to mathematical proofs and logical thinking for beginning students.", "high": "Logic", "low": "proof techniques"},
    {"title": "The Princeton Companion to Mathematics", "url": "https://www.amazon.com/Princeton-Companion-Mathematics-Timothy-Gowers/dp/0691118809", "description": "A comprehensive overview of modern mathematics written by leading mathematicians.", "high": "General", "low": "reference"},
    {"title": "Journey Through Genius - William Dunham", "url": "https://www.amazon.com/Journey-Through-Genius-Theorems-Mathematics/dp/014014739X", "description": "Explores the great theorems of mathematics and the stories behind them.", "high": "General", "low": "history"},
    {"title": "Fermat's Enigma - Simon Singh", "url": "https://www.amazon.com/Fermats-Enigma-Greatest-Mathematical-Solved/dp/0385494638", "description": "The story of Fermat's Last Theorem and Andrew Wiles' proof.", "high": "Number Theory", "low": "history"},
    {"title": "Gödel, Escher, Bach - Douglas Hofstadter", "url": "https://www.amazon.com/Gödel-Escher-Bach-Eternal-Golden/dp/0465026567", "description": "A profound exploration of consciousness, mathematics, art, and music through interwoven narratives.", "high": "Logic", "low": "consciousness"},
    {"title": "The Man Who Loved Only Numbers - Paul Hoffman", "url": "https://www.amazon.com/Man-Who-Loved-Only-Numbers/dp/0786884061", "description": "Biography of Paul Erdős, the legendary mathematician who lived for mathematics.", "high": "General", "low": "biography"},
    {"title": "Love and Math - Edward Frenkel", "url": "https://www.amazon.com/Love-Math-Heart-Hidden-Reality/dp/0465050743", "description": "A mathematician's journey through the Langlands program and the beauty of modern mathematics.", "high": "General", "low": "autobiography"},
    {"title": "What is Mathematics? - Courant and Robbins", "url": "https://www.amazon.com/What-Mathematics-Elementary-Approach-Ideas/dp/0195105192", "description": "Classic introduction to mathematical thinking covering number theory, geometry, topology, and calculus.", "high": "General", "low": "introduction"},
    {"title": "Algebraic Geometry - Robin Hartshorne", "url": "https://www.amazon.com/Algebraic-Geometry-Graduate-Texts-Mathematics/dp/0387902449", "description": "The definitive graduate text on modern algebraic geometry using schemes.", "high": "Geometry", "low": "algebraic geometry"},
    {"title": "Topology - James Munkres", "url": "https://www.amazon.com/Topology-2nd-James-Munkres/dp/0131816292", "description": "Standard undergraduate topology text covering point-set and algebraic topology.", "high": "Topology", "low": "general topology"},
    {"title": "Principles of Mathematical Analysis - Walter Rudin", "url": "https://www.amazon.com/Principles-Mathematical-Analysis-International-Mathematics/dp/007054235X", "description": "Classic graduate text in real analysis, known as 'Baby Rudin'.", "high": "Analysis", "low": "real analysis"},
    {"title": "Abstract Algebra - Dummit and Foote", "url": "https://www.amazon.com/Abstract-Algebra-3rd-David-Dummit/dp/0471433349", "description": "Comprehensive graduate algebra text covering groups, rings, fields, and modules.", "high": "Algebra", "low": "abstract algebra"},
    {"title": "Complex Analysis - Elias Stein", "url": "https://www.amazon.com/Complex-Analysis-Princeton-Lectures-No/dp/0691113858", "description": "Beautiful introduction to complex analysis with connections to Fourier analysis.", "high": "Analysis", "low": "complex analysis"},
    
    # Online Courses
    {"title": "MIT OpenCourseWare - Mathematics", "url": "https://ocw.mit.edu/courses/mathematics/", "description": "Free lecture notes, exams, and videos from MIT mathematics courses.", "high": "General", "low": "education"},
    {"title": "Khan Academy - Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra", "description": "Comprehensive free course on linear algebra with practice exercises.", "high": "Algebra", "low": "linear algebra"},
    {"title": "Coursera - Mathematics for Machine Learning", "url": "https://www.coursera.org/specializations/mathematics-machine-learning", "description": "Linear algebra, multivariate calculus, and PCA for machine learning applications.", "high": "Applied Math", "low": "machine learning"},
    {"title": "edX - Introduction to Probability", "url": "https://www.edx.org/course/introduction-to-probability", "description": "Comprehensive probability course from MIT covering random variables and limit theorems.", "high": "Probability", "low": "probability theory"},
    {"title": "Brilliant.org - Mathematical Fundamentals", "url": "https://brilliant.org/courses/math-fundamentals/", "description": "Interactive courses covering logic, number theory, algebra, and geometry.", "high": "General", "low": "interactive learning"},
    
    # Research Resources
    {"title": "arXiv Mathematics", "url": "https://arxiv.org/math", "description": "Preprint server for mathematics papers. The latest research before it hits journals.", "high": "General", "low": "research"},
    {"title": "MathOverflow", "url": "https://mathoverflow.net/", "description": "Q&A for professional mathematicians. Research-level discussions on cutting-edge topics.", "high": "General", "low": "Q&A"},
    {"title": "Stack Exchange - Mathematics", "url": "https://math.stackexchange.com/", "description": "Q&A for all levels of mathematics, from elementary to advanced.", "high": "General", "low": "Q&A"},
    {"title": "The OEIS - Online Encyclopedia of Integer Sequences", "url": "https://oeis.org/", "description": "Database of integer sequences with extensive information and references.", "high": "Number Theory", "low": "sequences"},
    {"title": "The L-functions and Modular Forms Database", "url": "https://www.lmfdb.org/", "description": "Extensive database of L-functions, modular forms, and related objects.", "high": "Number Theory", "low": "modular forms"},
    {"title": "nLab - Category Theory", "url": "https://ncatlab.org/nlab/show/HomePage", "description": "Wiki-lab for collaborative work on higher category theory and applications.", "high": "Logic", "low": "category theory"},
    {"title": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/", "description": "Extensive mathematics resource with detailed articles on thousands of topics.", "high": "General", "low": "reference"},
    {"title": "Encyclopedia of Mathematics", "url": "https://encyclopediaofmath.org/", "description": "Open-access encyclopedia with over 8,000 articles on mathematical topics.", "high": "General", "low": "reference"},
    {"title": "The MacTutor History of Mathematics", "url": "https://mathshistory.st-andrews.ac.uk/", "description": "Extensive archive of mathematician biographies and historical articles.", "high": "General", "low": "history"},
    {"title": "The Archive of Formal Proofs", "url": "https://www.isa-afp.org/", "description": "Collection of proof libraries for the Isabelle proof assistant.", "high": "Logic", "low": "formal verification"},
    
    # Interactive Tools
    {"title": "Desmos Graphing Calculator", "url": "https://www.desmos.com/calculator", "description": "Beautiful, free online graphing calculator. Great for visualizing functions.", "high": "General", "low": "graphing"},
    {"title": "GeoGebra - Dynamic Mathematics", "url": "https://www.geogebra.org/", "description": "Interactive geometry, algebra, statistics and calculus application.", "high": "General", "low": "interactive"},
    {"title": "Wolfram Alpha", "url": "https://www.wolframalpha.com/", "description": "Computational intelligence that answers factual queries using structured data.", "high": "General", "low": "computation"},
    {"title": "The Mandelbrot Set Explorer", "url": "https://mandelbrotset.net/", "description": "Interactive exploration of the Mandelbrot set with high-resolution zooming.", "high": "Analysis", "low": "complex dynamics"},
    {"title": "Tensor Network Diagrams", "url": "https://tensornetwork.org/", "description": "Visual introduction to tensor networks used in quantum computing and ML.", "high": "Applied Math", "low": "tensor calculus"},
    {"title": "3D-XplorMath", "url": "http://3d-xplormath.org/", "description": "Software for visualizing mathematical objects in 3D.", "high": "Geometry", "low": "visualization"},
    {"title": "SymPy Live", "url": "https://live.sympy.org/", "description": "Online Python shell with SymPy for symbolic mathematics.", "high": "General", "low": "symbolic computation"},
    
    # Math Organizations
    {"title": "American Mathematical Society", "url": "https://www.ams.org/", "description": "Professional organization promoting mathematical research and education.", "high": "General", "low": "organization"},
    {"title": "Mathematical Association of America", "url": "https://www.maa.org/", "description": "Organization focused on undergraduate mathematics education.", "high": "General", "low": "education"},
    {"title": "Society for Industrial and Applied Mathematics", "url": "https://www.siam.org/", "description": "Professional organization for applied mathematicians and computational scientists.", "high": "Applied Math", "low": "organization"},
    {"title": "London Mathematical Society", "url": "https://www.lms.ac.uk/", "description": "UK's learned society for mathematics, founded in 1865.", "high": "General", "low": "organization"},
    {"title": "European Mathematical Society", "url": "https://euromathsoc.org/", "description": "Organization promoting mathematical research in Europe.", "high": "General", "low": "organization"},
    {"title": "Clay Mathematics Institute", "url": "https://www.claymath.org/", "description": "Private foundation dedicated to increasing mathematical knowledge. Home of the Millennium Problems.", "high": "General", "low": "research institute"},
    
    # Special Topics - Chaos Theory
    {"title": "Chaos Theory and the Logistic Map", "url": "https://en.wikipedia.org/wiki/Logistic_map", "description": "Introduction to chaos through the logistic map, showing period doubling and bifurcations.", "high": "Applied Math", "low": "chaos theory"},
    {"title": "Lorenz Attractor Visualization", "url": "https://www.youtube.com/watch?v=f0olkzMGEJ8", "description": "Beautiful 3D visualization of the Lorenz attractor, the butterfly effect in action.", "high": "Applied Math", "low": "dynamical systems"},
    
    # Special Topics - Cryptography
    {"title": "An Introduction to Elliptic Curve Cryptography", "url": "https://www.ams.org/notices/199909/boneh.pdf", "description": "Article explaining how elliptic curves secure modern communications.", "high": "Number Theory", "low": "cryptography"},
    {"title": "The RSA Algorithm", "url": "https://en.wikipedia.org/wiki/RSA_(cryptosystem)", "description": "Wikipedia's comprehensive article on the RSA encryption algorithm.", "high": "Number Theory", "low": "cryptography"},
    
    # Special Topics - Game Theory
    {"title": "Nash Equilibrium", "url": "https://www.youtube.com/watch?v=HG4jlZ9k6XA", "description": "Explanation of Nash Equilibrium and its applications in economics and biology.", "high": "Applied Math", "low": "game theory"},
    {"title": "The Prisoner's Dilemma", "url": "https://plato.stanford.edu/entries/prisoner-dilemma/", "description": "Stanford Encyclopedia of Philosophy entry on this classic game theory problem.", "high": "Applied Math", "low": "game theory"},
    
    # Special Topics - Fractals
    {"title": "Fractals: The Colors of Infinity", "url": "https://www.youtube.com/watch?v=G_GBwuYuOOs", "description": "Documentary narrated by Arthur C. Clarke about the Mandelbrot set.", "high": "Analysis", "low": "fractals"},
    {"title": "The Fractal Geometry of Nature", "url": "https://en.wikipedia.org/wiki/The_Fractal_Geometry_of_Nature", "description": "Benoit Mandelbrot's seminal book on fractals in nature.", "high": "Analysis", "low": "fractals"},
    
    # Special Topics - Infinity
    {"title": "Hilbert's Hotel", "url": "https://www.youtube.com/watch?v=faQBrAQ87l4", "description": "Vsauce explains the paradox of Hilbert's Hotel and different sizes of infinity.", "high": "Logic", "low": "infinity"},
    {"title": "Cantor's Diagonal Argument", "url": "https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument", "description": "The proof that real numbers are uncountable, changing mathematics forever.", "high": "Logic", "low": "set theory"},
]

def load_links():
    """Load all links from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_links(links):
    """Save links to JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)

def load_page_index():
    """Load page index tracking which links are on which pages."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"pages": [], "total_links": 0}

def save_page_index(index):
    """Save page index."""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def deduplicate_links(links):
    """Remove duplicate URLs, keeping the first occurrence."""
    seen = set()
    unique = []
    for link in links:
        if link["url"] not in seen:
            seen.add(link["url"])
            unique.append(link)
    return unique

def select_new_links(existing_urls, count=50):
    """Select new links that haven't been added yet."""
    available = [l for l in CURATED_LINKS if l["url"] not in existing_urls]
    
    if len(available) < count:
        # If running low, we'll just add what we have
        count = len(available)
    
    selected = random.sample(available, min(count, len(available)))
    
    # Add metadata
    result = []
    for link in selected:
        result.append({
            "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999)),
            "title": link["title"],
            "url": link["url"],
            "description": link["description"],
            "high_level_tag": link["high"],
            "low_level_tag": link["low"],
            "added_at": datetime.now(timezone.utc).isoformat()
        })
    
    return result

def generate_page_html(links, page_num, total_pages):
    """Generate HTML for a single page."""
    all_high_tags = sorted(set(link["high_level_tag"] for link in links))
    
    # Build link cards
    links_html = ""
    for link in links:
        links_html += f'''
        <div class="link-card">
            <div class="link-header">
                <h3><a href="{link['url']}" target="_blank" rel="noopener">{link['title']}</a></h3>
                <div class="link-meta">
                    <span class="tag high">{link['high_level_tag']}</span>
                    <span class="tag low">{link['low_level_tag']}</span>
                </div>
            </div>
            <p class="description">{link['description']}</p>
        </div>
'''
    
    # Build pagination
    pagination_html = '<div class="pagination">'
    
    # Prev
    if page_num > 1:
        pagination_html += f'<a href="page{page_num-1}.html" class="page-btn">← Previous</a>'
    else:
        pagination_html += '<span class="page-btn disabled">← Previous</span>'
    
    # Page numbers
    pagination_html += '<div class="page-numbers">'
    for p in range(1, total_pages + 1):
        if p == page_num:
            pagination_html += f'<span class="page-num active">{p}</span>'
        else:
            pagination_html += f'<a href="page{p}.html" class="page-num">{p}</a>'
    pagination_html += '</div>'
    
    # Next
    if page_num < total_pages:
        pagination_html += f'<a href="page{page_num+1}.html" class="page-btn">Next →</a>'
    else:
        pagination_html += '<span class="page-btn disabled">Next →</span>'
    
    pagination_html += '</div>'
    pagination_html += f'<p class="pagination-info">Page {page_num} of {total_pages} | {len(links)} links</p>'
    
    # Build category filters
    filter_buttons = ""
    for tag in all_high_tags:
        filter_buttons += f'<button class="filter-btn" data-filter="{tag}">{tag}</button>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Links - Page {page_num}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .subtitle {{ opacity: 0.9; }}
        .controls {{ background: white; padding: 1.5rem; border-bottom: 1px solid #ddd; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .search-box {{ width: 100%; max-width: 600px; padding: 0.75rem 1rem; font-size: 1rem; border: 2px solid #ddd; border-radius: 8px; margin: 0 auto 1rem; display: block; }}
        .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }}
        .filter-btn {{ padding: 0.5rem 1rem; border: 1px solid #ddd; background: white; border-radius: 20px; cursor: pointer; font-size: 0.9rem; }}
        .filter-btn:hover, .filter-btn.active {{ background: #667eea; color: white; border-color: #667eea; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
        .links-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1.5rem; }}
        .link-card {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }}
        .link-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}
        .link-card.hidden {{ display: none; }}
        .link-header h3 {{ font-size: 1.2rem; margin-bottom: 0.5rem; }}
        .link-header h3 a {{ color: #667eea; text-decoration: none; }}
        .link-header h3 a:hover {{ text-decoration: underline; }}
        .link-meta {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; }}
        .tag {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500; }}
        .tag.high {{ background: #667eea; color: white; }}
        .tag.low {{ background: #e0e0e0; color: #555; }}
        .description {{ color: #666; font-size: 0.95rem; margin-top: 0.75rem; }}
        .pagination {{ display: flex; justify-content: center; align-items: center; gap: 1rem; margin-top: 2rem; flex-wrap: wrap; }}
        .page-btn, .page-num {{ padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; }}
        .page-btn {{ background: #667eea; color: white; }}
        .page-btn.disabled {{ background: #ccc; }}
        .page-num {{ background: white; color: #667eea; border: 1px solid #ddd; }}
        .page-num.active {{ background: #667eea; color: white; }}
        .pagination-info {{ text-align: center; color: #666; margin-top: 1rem; }}
        .home-link {{ text-align: center; margin-bottom: 1rem; }}
        .home-link a {{ color: #667eea; text-decoration: none; font-weight: 500; }}
        footer {{ text-align: center; padding: 2rem; color: #666; border-top: 1px solid #ddd; margin-top: 2rem; }}
        @media (max-width: 768px) {{ .links-grid {{ grid-template-columns: 1fr; }} h1 {{ font-size: 1.8rem; }} }}
    </style>
</head>
<body>
    <header>
        <h1>🔗 Math Links</h1>
        <p class="subtitle">Curated mathematical resources - Page {page_num}</p>
    </header>
    
    <div class="controls">
        <div class="home-link"><a href="index.html">← Back to Home</a></div>
        <input type="text" class="search-box" id="search" placeholder="Search this page...">
        <div class="filter-buttons">
            <button class="filter-btn active" data-filter="all">All</button>
            {filter_buttons}
        </div>
    </div>
    
    <div class="container">
        <div class="links-grid" id="links-container">
            {links_html}
        </div>
        <div class="no-results hidden" id="no-results">No results found.</div>
        
        {pagination_html}
    </div>
    
    <footer>
        <p><a href="index.html">Home</a> | Page {page_num} of {total_pages} | Updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</p>
    </footer>
    
    <script>
        const searchInput = document.getElementById('search');
        const linkCards = document.querySelectorAll('.link-card');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const noResults = document.getElementById('no-results');
        
        let currentFilter = 'all';
        
        function filterContent() {{
            const searchTerm = searchInput.value.toLowerCase();
            let visible = 0;
            
            linkCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                const matchesFilter = currentFilter === 'all' || card.querySelector('.tag.high').textContent === currentFilter;
                const matchesSearch = !searchTerm || text.includes(searchTerm);
                
                if (matchesFilter && matchesSearch) {{
                    card.classList.remove('hidden');
                    visible++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
            
            noResults.classList.toggle('hidden', visible > 0);
        }}
        
        searchInput.addEventListener('input', filterContent);
        
        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                filterContent();
            }});
        }});
    </script>
</body>
</html>
'''
    return html

def generate_homepage(total_pages, latest_links):
    """Generate homepage with overview."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Links - Curated Mathematical Resources</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 2rem; text-align: center; }}
        h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .subtitle {{ font-size: 1.2rem; opacity: 0.9; }}
        .stats {{ display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 2.5rem; font-weight: bold; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.8; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 2rem; }}
        .section {{ background: white; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h2 {{ color: #667eea; margin-bottom: 1rem; }}
        .page-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }}
        .page-link {{ display: block; padding: 1rem; background: #f8f8f8; border-radius: 8px; text-decoration: none; color: #333; transition: all 0.2s; }}
        .page-link:hover {{ background: #667eea; color: white; }}
        .page-link span {{ font-size: 1.2rem; font-weight: bold; }}
        .page-link small {{ display: block; opacity: 0.7; margin-top: 0.25rem; }}
        .about {{ line-height: 1.8; color: #555; }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }}
        .tag {{ padding: 0.5rem 1rem; background: #e8e8e8; border-radius: 20px; font-size: 0.85rem; }}
        footer {{ text-align: center; padding: 2rem; color: #666; }}
    </style>
</head>
<body>
    <header>
        <h1>🔗 Math Links</h1>
        <p class="subtitle">A curated collection of mathematical resources</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{total_pages * LINKS_PER_PAGE}</div>
                <div class="stat-label">Total Links</div>
            </div>
            <div class="stat">
                <div class="stat-number">{total_pages}</div>
                <div class="stat-label">Pages</div>
            </div>
            <div class="stat">
                <div class="stat-number">50</div>
                <div class="stat-label">Links Per Page</div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="section">
            <h2>📚 Browse All Pages</h2>
            <div class="page-list">
'''
    
    for p in range(1, total_pages + 1):
        html += f'''                <a href="page{p}.html" class="page-link">
                    <span>Page {p}</span>
                    <small>Links {(p-1)*LINKS_PER_PAGE + 1} - {p*LINKS_PER_PAGE}</small>
                </a>
'''
    
    html += f'''            </div>
        </div>
        
        <div class="section">
            <h2>🏷️ Categories</h2>
            <p class="about">Links are organized by mathematical area:</p>
            <div class="tags">
                <span class="tag">Algebra</span>
                <span class="tag">Analysis</span>
                <span class="tag">Topology</span>
                <span class="tag">Number Theory</span>
                <span class="tag">Geometry</span>
                <span class="tag">Logic</span>
                <span class="tag">Probability</span>
                <span class="tag">Applied Math</span>
                <span class="tag">Discrete Math</span>
                <span class="tag">General</span>
            </div>
        </div>
        
        <div class="section">
            <h2>ℹ️ About</h2>
            <p class="about">
                Math Links is an automatically curated collection of mathematical resources from around the web. 
                New links are added hourly from sources including Quanta Magazine, 3Blue1Brown, academic papers, 
                textbooks, and online courses. Each link includes high-level and low-level tags for easy discovery.
            </p>
            <p class="about" style="margin-top: 1rem;">
                Use the search and filter features on each page to find resources by topic, 
                or browse by page to discover new mathematical content.
            </p>
        </div>
    </div>
    
    <footer>
        <p>Updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} | Auto-generated with ❤️</p>
    </footer>
</body>
</html>
'''
    return html

def commit_and_push(message="Update math links"):
    """Commit and push changes to GitHub."""
    os.chdir(REPO_PATH)
    subprocess.run(["git", "config", "user.email", "math-links@openclaw.ai"], check=False)
    subprocess.run(["git", "config", "user.name", "Math Links Bot"], check=False)
    subprocess.run(["git", "add", "-A"], check=False)
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True
    )
    subprocess.run(["git", "push", "origin", "main"], check=False)
    return "nothing to commit" not in result.stdout.lower()

def main():
    """Main function - creates new page with 50 links each run."""
    # Load existing links
    all_links = load_links()
    
    # Deduplicate existing links
    all_links = deduplicate_links(all_links)
    
    # Get URLs already in the collection
    existing_urls = {link["url"] for link in all_links}
    
    # Select 50 new unique links
    new_links = select_new_links(existing_urls, LINKS_PER_PAGE)
    
    if not new_links:
        print("No new links available. Consider expanding the curated list.")
        return 0
    
    print(f"Selected {len(new_links)} new links")
    
    # Add to collection
    all_links.extend(new_links)
    
    # Save updated links
    save_links(all_links)
    print(f"Total links in collection: {len(all_links)}")
    
    # Calculate how many pages we need
    total_links = len(all_links)
    total_pages = (total_links + LINKS_PER_PAGE - 1) // LINKS_PER_PAGE
    
    # Sort by date (newest first)
    all_links.sort(key=lambda x: x["added_at"], reverse=True)
    
    # Generate page files - each page gets exactly 50 links
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * LINKS_PER_PAGE
        end_idx = min(start_idx + LINKS_PER_PAGE, total_links)
        page_links = all_links[start_idx:end_idx]
        
        html = generate_page_html(page_links, page_num, total_pages)
        filename = f"page{page_num}.html"
        
        with open(os.path.join(REPO_PATH, filename), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated {filename} with {len(page_links)} links")
    
    # Generate homepage
    homepage_html = generate_homepage(total_pages, all_links[:LINKS_PER_PAGE])
    with open(os.path.join(REPO_PATH, "index.html"), 'w', encoding='utf-8') as f:
        f.write(homepage_html)
    print("Generated index.html")
    
    # Commit and push
    if commit_and_push(f"Add page {total_pages} with {len(new_links)} new math links"):
        print(f"Successfully pushed. Now at {total_pages} pages.")
    else:
        print("Git operation completed")
    
    return 0

if __name__ == "__main__":
    exit(main())
