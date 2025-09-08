import os, sys
import markdown
from flask import Blueprint, render_template, abort
from pathlib import Path

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

blogs_bp = Blueprint('blogs', __name__, 
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/blogs')

def get_md_files():
    """Scan learning_md directory and return structured content"""
    base_path = Path('apps/blogs')
    print(f"{base_path=}")
    content_structure = {}
    
    for category in base_path.iterdir():
        if category.is_dir():
            content_structure[category.name] = {}
            for topic_file in category.iterdir():
                if topic_file.is_file() and topic_file.suffix == '.md':
                    topic_name = topic_file.stem.replace('_', ' ').title()
                    content_structure[category.name][topic_name] = {
                        'filename': topic_file.name,
                        'path': str(topic_file.relative_to(base_path))
                    }
    
    return content_structure

def markdown_to_html(md_content):
    """Convert markdown to HTML with extensions for better formatting"""
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc'
    ]
    
    return markdown.markdown(md_content, extensions=extensions)

@blogs_bp.route('/')
@blogs_bp.route('/<category>/')
@blogs_bp.route('/<category>/<topic>')
def show_content(category=None, topic=None):
    content_structure = get_md_files()
    
    # If no category specified, show first category's first topic
    if not category:
        first_category = next(iter(content_structure.keys()))
        first_topic = next(iter(content_structure[first_category].keys()))
        return render_template('blogs/content.html',
                             content_structure=content_structure,
                             current_category=first_category,
                             current_topic=first_topic,
                             content_html="Select a topic from the sidebar")
    
    # Validate category exists
    if category not in content_structure:
        abort(404)
    
    # If no topic specified, show first topic in category
    if not topic:
        first_topic = next(iter(content_structure[category].keys()))
        topic = first_topic
    
    # Find the topic file
    topic_data = None
    for topic_name, data in content_structure[category].items():
        if topic_name.lower().replace(' ', '_') == topic.lower().replace(' ', '_'):
            topic_data = data
            break
    
    if not topic_data:
        abort(404)
    
    # Read and convert markdown file
    file_path = Path('apps/blogs') / topic_data['path']
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        content_html = markdown_to_html(md_content)
    except FileNotFoundError:
        abort(404)
    
    return render_template('blogs/content.html',
                         content_structure=content_structure,
                         current_category=category,
                         current_topic=topic.replace('_', ' ').title(),
                         content_html=content_html)

# def register_blueprint(app):
#     """Register the blueprint with the app"""
#     app.register_blueprint(learning_bp)