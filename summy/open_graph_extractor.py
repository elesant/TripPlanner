import lxml.html as lh

def extract_open_graph_tags(el):
  tags = el.cssselect('meta')
  tags = [tag for tag in tags if tag is not None]
  tags = [tag for tag in tags if tag.get('property') is not None]
  tags = [tag for tag in tags if 'og:' in tag.get('property')]

  extracted_vals = {}

  for tag in tags:
    content = tag.get('content')
    prop = tag.get('property')

    if not content: continue

    if prop == 'og:title': extracted_vals['title'] = content
    elif prop == 'og:description': extracted_vals['description'] = content
    elif prop == 'og:url': extracted_vals['url'] = content
    elif prop == 'og:image': extracted_vals['image'] = content
  return extracted_vals
