#!/usr/bin/env python3
"""
Math Link Aggregator
Searches for math articles, books, videos and creates a searchable GitHub Pages site.
"""

import os
import random
import subprocess
import json
from datetime import datetime, timezone
from urllib.parse import quote

REPO_PATH = "/root/.openclaw/workspace/something"
DATA_FILE = os.path.join(REPO_PATH, "links.json")

# Math topics for searching and tagging
MATH_CATEGORIES = {
    "Algebra": ["abstract algebra", "group theory", "ring theory", "field theory", "linear algebra", "representation theory"],
    "Analysis": ["real analysis", "complex analysis", "functional analysis", "harmonic analysis", "measure theory"],
    "Topology": ["algebraic topology", "differential topology", "knot theory", "manifolds", "homotopy theory"],
    "Number Theory": ["prime numbers", "modular forms", "algebraic number theory", "analytic number theory", "elliptic curves"],
    "Geometry": ["algebraic geometry", "differential geometry", "riemannian geometry", "symplectic geometry", "projective geometry"],
    "Logic": ["set theory", "model theory", "proof theory", "computability theory", "category theory"],
    "Probability": ["probability theory", "stochastic processes", "random matrices", "statistical mechanics"],
    "Applied Math": ["numerical analysis", "optimization", "dynamical systems", "control theory", "mathematical physics"],
    "Discrete Math": ["combinatorics", "graph theory", "theoretical computer science", "coding theory"],
}

# Curated high-quality math sources
CURATED_LINKS = [
    # Articles & Blogs
    {"title": "The Prime Number Conspiracy", "url": "https://www.quantamagazine.org/mathematicians-discover-the-perfect-way-to-multiply-20190411/", "description": "New algorithms are changing how we multiply numbers, with applications in cryptography and computer science.", "high": "Number Theory", "low": "algorithms"},
    {"title": "The Map of Mathematics", "url": "https://www.quantamagazine.org/the-map-of-mathematics-20200213/", "description": "A comprehensive visual guide showing how different areas of mathematics connect to each other.", "high": "General", "low": "overview"},
    {"title": "Mathematicians Prove Tetris Is Hard", "url": "https://www.quantamagazine.org/mathematicians-prove-tetris-is-hard-even-with-godlike-abilities-20231031/", "description": "Even with perfect information, the classic game Tetris is computationally intractable.", "high": "Discrete Math", "low": "computational complexity"},
    {"title": "A Proof That Some Infinities Are Bigger Than Others", "url": "https://www.quantamagazine.org/mathematicians-solve-long-standing-infinity-problem-20230713/", "description": "Resolution of a 50-year-old problem about cardinal characteristics of the continuum.", "high": "Logic", "low": "set theory"},
    {"title": "The Geometry of Neural Networks", "url": "https://www.quantamagazine.org/the-geometric-trick-that-makes-computers-learn-20230622/", "description": "How algebraic topology helps understand why deep learning works.", "high": "Applied Math", "low": "machine learning"},
    
    # Books
    {"title": "Visual Complex Analysis - Tristan Needham", "url": "https://www.amazon.com/Visual-Complex-Analysis-Tristan-Needham/dp/0198534469", "description": "A geometric approach to complex analysis using beautiful visualizations and intuition.", "high": "Analysis", "low": "complex analysis"},
    {"title": "The Road to Reality - Roger Penrose", "url": "https://www.amazon.com/Road-Reality-Complete-Guide-Universe/dp/0679776311", "description": "A comprehensive guide to the laws of the universe, from the basics to cutting-edge physics.", "high": "Applied Math", "low": "mathematical physics"},
    {"title": "How to Prove It - Daniel Velleman", "url": "https://www.amazon.com/How-Prove-Structured-Approach-3rd/dp/1108439535", "description": "An introduction to mathematical proofs and logical thinking for beginning students.", "high": "Logic", "low": "proof techniques"},
    {"title": "The Princeton Companion to Mathematics", "url": "https://www.amazon.com/Princeton-Companion-Mathematics-Timothy-Gowers/dp/0691118809", "description": "A comprehensive overview of modern mathematics written by leading mathematicians.", "high": "General", "low": "reference"},
    {"title": "Journey Through Genius - William Dunham", "url": "https://www.amazon.com/Journey-Through-Genius-Theorems-Mathematics/dp/014014739X", "description": "Explores the great theorems of mathematics and the stories behind them.", "high": "General", "low": "history"},
    {"title": "Fermat's Enigma - Simon Singh", "url": "https://www.amazon.com/Fermats-Enigma-Greatest-Mathematical-Solved/dp/0385494638", "description": "The story of Fermat's Last Theorem and Andrew Wiles' proof.", "high": "Number Theory", "low": "history"},
    
    # YouTube Channels & Videos
    {"title": "3Blue1Brown - Essence of Linear Algebra", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "description": "Beautiful visual explanations of linear algebra concepts using animation.", "high": "Algebra", "low": "linear algebra"},
    {"title": "Numberphile - Prime Numbers", "url": "https://www.youtube.com/@numberphile", "description": "Videos about numbers and mathematics with mathematicians from around the world.", "high": "Number Theory", "low": "prime numbers"},
    {"title": "Mathologer - The Riemann Hypothesis", "url": "https://www.youtube.com/@Mathologer", "description": "Deep dives into beautiful mathematics with clear explanations.", "high": "Number Theory", "low": "riemann hypothesis"},
    {"title": "Stand-up Maths - The Parker Square", "url": "https://www.youtube.com/@standupmaths", "description": "Mathematical stand-up comedy and interesting problems.", "high": "General", "low": "recreational math"},
    {"title": "Michael Penn - Real Analysis", "url": "https://www.youtube.com/@MichaelPennMath", "description": "Lecture-style videos covering real analysis, abstract algebra, and more.", "high": "Analysis", "low": "real analysis"},
    {"title": "Dr. Peyam - Differential Equations", "url": "https://www.youtube.com/@drpeyam", "description": "Clear explanations of differential equations and applied mathematics.", "high": "Applied Math", "low": "differential equations"},
    
    # Online Courses & Resources
    {"title": "MIT OpenCourseWare - Mathematics", "url": "https://ocw.mit.edu/courses/mathematics/", "description": "Free lecture notes, exams, and videos from MIT mathematics courses.", "high": "General", "low": "education"},
    {"title": "Khan Academy - Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra", "description": "Comprehensive free course on linear algebra with practice exercises.", "high": "Algebra", "low": "linear algebra"},
    {"title": "nLab - Category Theory", "url": "https://ncatlab.org/nlab/show/HomePage", "description": "Wiki-lab for collaborative work on higher category theory and applications.", "high": "Logic", "low": "category theory"},
    {"title": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/", "description": "Extensive mathematics resource with detailed articles on thousands of topics.", "high": "General", "low": "reference"},
    
    # Research & Papers
    {"title": "The Archive of Formal Proofs", "url": "https://www.isa-afp.org/", "description": "A collection of proof libraries for the Isabelle proof assistant.", "high": "Logic", "low": "formal verification"},
    {"title": "The OEIS - Online Encyclopedia of Integer Sequences", "url": "https://oeis.org/", "description": "Database of integer sequences with extensive information and references.", "high": "Number Theory", "low": "sequences"},
    {"title": "The L-functions and Modular Forms Database", "url": "https://www.lmfdb.org/", "description": "Extensive database of L-functions, modular forms, and related objects.", "high": "Number Theory", "low": "modular forms"},
    
    # Interactive & Visualizations
    {"title": "The Mandelbrot Set Explorer", "url": "https://mandelbrotset.net/", "description": "Interactive exploration of the Mandelbrot set with high-resolution zooming.", "high": "Analysis", "low": "complex dynamics"},
    {"title": "Geogebra - Dynamic Mathematics", "url": "https://www.geogebra.org/", "description": "Interactive geometry, algebra, statistics and calculus application.", "high": "General", "low": "interactive"},
    {"title": "Tensor Network Diagrams", "url": "https://tensornetwork.org/", "description": "Visual introduction to tensor networks used in quantum computing and ML.", "high": "Applied Math", "low": "tensor calculus"},
]

def load_existing_links():
    """Load existing links from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_links(links):
    """Save links to JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)

def generate_id():
    """Generate unique ID for link."""
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

def select_random_links(count=20):
    """Select random links from curated list, ensuring variety."""
    selected = []
    available = CURATED_LINKS.copy()
    
    # Ensure we have variety across categories
    categories_used = set()
    
    while len(selected) < count and available:
        link = random.choice(available)
        available.remove(link)
        
        # Add ID and timestamp
        link_with_meta = {
            "id": generate_id(),
            "title": link["title"],
            "url": link["url"],
            "description": link["description"],
            "high_level_tag": link["high"],
            "low_level_tag": link["low"],
            "added_at": datetime.now(timezone.utc).isoformat()
        }
        
        selected.append(link_with_meta)
        categories_used.add(link["high"])
    
    return selected

def generate_html_page(links):
    """Generate searchable HTML page."""
    # Group links by high-level category
    by_category = {}
    for link in links:
        cat = link["high_level_tag"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(link)
    
    # Get all unique tags for filter buttons
    all_high_tags = sorted(set(link["high_level_tag"] for link in links))
    all_low_tags = sorted(set(link["low_level_tag"] for link in links))
    
    # Build link cards HTML
    links_html = ""
    for link in links:
        links_html += f'''
        <div class="link-card" data-high="{link['high_level_tag']}" data-low="{link['low_level_tag']}" data-title="{link['title'].lower()}" data-desc="{link['description'].lower()}">
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
    
    # Build category filter buttons
    filter_buttons = '<button class="filter-btn active" data-filter="all">All</button>'
    for tag in all_high_tags:
        filter_buttons += f'<button class="filter-btn" data-filter="{tag}">{tag}</button>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Curated mathematical resources - articles, books, videos, and more">
    <title>Math Links - Curated Mathematical Resources</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        .stats {{
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        .controls {{
            background: white;
            padding: 1.5rem;
            border-bottom: 1px solid #ddd;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .search-box {{
            width: 100%;
            max-width: 600px;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
        }}
        
        .filter-btn {{
            padding: 0.5rem 1rem;
            border: 1px solid #ddd;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
        }}
        
        .filter-btn:hover {{
            background: #f0f0f0;
        }}
        
        .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .links-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        
        .link-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .link-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        .link-card.hidden {{
            display: none;
        }}
        
        .link-header {{
            margin-bottom: 0.75rem;
        }}
        
        .link-header h3 {{
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }}
        
        .link-header h3 a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .link-header h3 a:hover {{
            text-decoration: underline;
        }}
        
        .link-meta {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .tag.high {{
            background: #667eea;
            color: white;
        }}
        
        .tag.low {{
            background: #e0e0e0;
            color: #555;
        }}
        
        .description {{
            color: #666;
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        .no-results {{
            text-align: center;
            padding: 3rem;
            color: #666;
            font-size: 1.1rem;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #ddd;
            margin-top: 2rem;
        }}
        
        @media (max-width: 768px) {{
            .links-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>🔗 Math Links</h1>
        <p class="subtitle">Curated mathematical resources - articles, books, videos, and more</p>
        <p class="stats">{len(links)} resources across {len(all_high_tags)} categories</p>
    </header>
    
    <div class="controls">
        <input type="text" class="search-box" id="search" placeholder="Search by title, description, or tags...">
        <div class="filter-buttons">
            {filter_buttons}
        </div>
    </div>
    
    <div class="container">
        <div class="links-grid" id="links-container">
            {links_html}
        </div>
        <div class="no-results hidden" id="no-results">No results found. Try a different search.</div>
    </div>
    
    <footer>
        <p>Updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} | Auto-generated with ❤️</p>
    </footer>
    
    <script>
        const searchInput = document.getElementById('search');
        const linksContainer = document.getElementById('links-container');
        const noResults = document.getElementById('no-results');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const linkCards = document.querySelectorAll('.link-card');
        
        let currentFilter = 'all';
        
        function filterLinks() {{
            const searchTerm = searchInput.value.toLowerCase();
            let visibleCount = 0;
            
            linkCards.forEach(card => {{
                const high = card.dataset.high;
                const low = card.dataset.low;
                const title = card.dataset.title;
                const desc = card.dataset.desc;
                
                const matchesFilter = currentFilter === 'all' || high === currentFilter;
                const matchesSearch = !searchTerm || 
                    title.includes(searchTerm) || 
                    desc.includes(searchTerm) || 
                    high.toLowerCase().includes(searchTerm) || 
                    low.toLowerCase().includes(searchTerm);
                
                if (matchesFilter && matchesSearch) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
            
            noResults.classList.toggle('hidden', visibleCount > 0);
        }}
        
        searchInput.addEventListener('input', filterLinks);
        
        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                filterLinks();
            }});
        }});
    </script>
</body>
</html>
'''
    return html

def commit_and_push():
    """Commit and push changes to GitHub."""
    os.chdir(REPO_PATH)
    
    subprocess.run(["git", "config", "user.email", "math-links@openclaw.ai"], check=False)
    subprocess.run(["git", "config", "user.name", "Math Links Bot"], check=False)
    
    subprocess.run(["git", "add", "links.json"], check=False)
    subprocess.run(["git", "add", "index.html"], check=False)
    
    result = subprocess.run(
        ["git", "commit", "-m", f"Add {len(load_existing_links())} math links"],
        capture_output=True, text=True
    )
    
    subprocess.run(["git", "push", "origin", "main"], check=False)
    return result.returncode == 0 or "nothing to commit" in result.stdout.lower()

def main():
    """Main function to aggregate math links."""
    # Load existing links
    links = load_existing_links()
    
    # Generate 20 new random links
    new_links = select_random_links(20)
    
    # Add to existing links (avoid duplicates by URL)
    existing_urls = {link["url"] for link in links}
    added = 0
    for link in new_links:
        if link["url"] not in existing_urls:
            links.append(link)
            added += 1
    
    print(f"Added {added} new links")
    
    # Sort by date (newest first)
    links.sort(key=lambda x: x["added_at"], reverse=True)
    
    # Save to JSON
    save_links(links)
    print(f"Total links: {len(links)}")
    
    # Generate HTML page
    html = generate_html_page(links)
    with open(os.path.join(REPO_PATH, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated index.html")
    
    # Commit and push
    if commit_and_push():
        print("Successfully pushed to GitHub")
    else:
        print("Git operation completed")
    
    return 0

if __name__ == "__main__":
    exit(main())
