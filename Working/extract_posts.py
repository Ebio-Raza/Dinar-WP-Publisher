import re
from bs4 import BeautifulSoup, NavigableString


def extract_posts(content_html=None, soup=None):
    """
    Extract posts from HTML content.

    Each post has:
    - A date (e.g., "12-3-2025")
    - A title in <font color="#c23b3b">
    - Content until the next post begins

    Args:
        content_html: HTML string
        soup: BeautifulSoup object

    Returns:
        List of dicts with keys: no, date, title, content
    """
    if soup is None:
        if content_html is None:
            raise ValueError("Either content_html or soup must be provided")
        soup = BeautifulSoup(content_html, "html.parser")

    # Date pattern: matches formats like "12-3-2025", "12-03-2025", etc.
    date_pattern = re.compile(r'^\s*(\d{1,2}-\d{1,2}-\d{4})\s*$')

    posts = []

    # Find all <font color="#c23b3b"> elements (these contain titles)
    title_fonts = soup.find_all('font', attrs={'color': '#c23b3b'})

    for idx, title_font in enumerate(title_fonts):
        title_text = title_font.get_text(strip=True)

        # Skip empty fonts
        if not title_text:
            continue

        # Find the parent <strong> that contains both date and title
        parent_strong = title_font.find_parent('strong')
        if not parent_strong:
            continue

        # Extract date from the <strong> element (text before the <font>)
        date_text = ""
        for child in parent_strong.children:
            if isinstance(child, NavigableString):
                text = child.strip()
                if date_pattern.match(text):
                    date_text = text
                    break
            elif child == title_font:
                break

        if not date_text:
            # Try to find date in previous siblings
            for sibling in parent_strong.previous_siblings:
                if isinstance(sibling, NavigableString):
                    text = sibling.strip()
                    if date_pattern.match(text):
                        date_text = text
                        break

        if not date_text:
            continue

        # Now collect content until the next post
        content_parts = []
        current = parent_strong.next_sibling

        while current:
            # Check if we've hit the next post (another <strong> with date + title font)
            if hasattr(current, 'name') and current.name == 'strong':
                # Check if this strong contains a date and title font
                inner_font = current.find('font', attrs={'color': '#c23b3b'})
                if inner_font:
                    # Check for date
                    for child in current.children:
                        if isinstance(child, NavigableString):
                            if date_pattern.match(child.strip()):
                                # This is the start of next post, stop here
                                current = None
                                break
                    if current is None:
                        break

            # Add this element's text to content
            if isinstance(current, NavigableString):
                text = str(current)
                if text.strip():
                    content_parts.append(text)
            elif hasattr(current, 'get_text'):
                content_parts.append(current.get_text())

            current = current.next_sibling if current else None

        # Clean up content
        content = ''.join(content_parts)
        content = re.sub(r'\s+', ' ', content).strip()

        posts.append({
            "no": len(posts) + 1,
            "date": date_text,
            "title": title_text,
            "content": content
        })

    return posts


def extract_posts_v2(content_html=None, soup=None):
    """
    Alternative approach: Use regex on the raw HTML string to split posts.
    More reliable for this specific HTML structure.
    """
    if soup is not None:
        content_html = str(soup)
    elif content_html is None:
        raise ValueError("Either content_html or soup must be provided")

    # Pattern to match post headers: date followed by title in red font
    # Matches: <strong> [optional <br/>] date <font color="#c23b3b">title</font> </strong>
    post_header_pattern = re.compile(
        r'<strong>\s*(?:<br\s*/?>)?\s*(?:<br\s*/?>)?\s*(\d{1,2}-\d{1,2}-\d{4})\s*'
        r'<font\s+color="#c23b3b">\s*(.+?)\s*</font>\s*</strong>',
        re.DOTALL | re.IGNORECASE
    )

    # Find all matches with their positions
    matches = list(post_header_pattern.finditer(content_html))

    posts = []
    for idx, match in enumerate(matches):
        date_text = match.group(1).strip()
        title_text = match.group(2).strip()

        # Content starts after this match
        content_start = match.end()

        # Content ends at the start of the next post or end of document
        if idx + 1 < len(matches):
            # Find the <br/><br/><strong> before the next post
            next_match = matches[idx + 1]
            content_end = next_match.start()

            # Look for <br/><br/> or similar ending pattern
            content_html_slice = content_html[content_start:content_end]

            # Remove trailing <br/><br/> pattern
            content_html_slice = re.sub(r'\s*<br\s*/?>\s*<br\s*/?>\s*$', '', content_html_slice)
        else:
            content_html_slice = content_html[content_start:]
            # Remove trailing <br/><br/> and closing tags
            content_html_slice = re.sub(r'\s*<br\s*/?>\s*<br\s*/?>\s*</div>\s*$', '', content_html_slice)

        # Parse content HTML to get text
        content_soup = BeautifulSoup(content_html_slice, "html.parser")
        content_text = content_soup.get_text()

        # Clean up whitespace
        content_text = re.sub(r'\s+', ' ', content_text).strip()

        posts.append({
            "no": idx + 1,
            "date": date_text,
            "title": title_text,
            "content": content_text
        })

    return posts


# Test the function
if __name__ == "__main__":
    with open("test-1.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    posts = extract_posts_v2(content_html=html_content)

    for post in posts:
        print(f"Post #{post['no']}")
        print(f"  Date: {post['date']}")
        print(f"  Title: {post['title']}")
        print(f"  Content: {post['content'][:100]}...")
        print()
