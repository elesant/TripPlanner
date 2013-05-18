import lxml.html as lh

def extract_meta_tags(el):
  tags = el.cssselect('meta')
  tags = [tag for tag in tags if tag is not None]
  tags = [tag for tag in tags if tag.get('name') is not None]

  extracted_vals = {}

  for tag in tags:
    content = tag.get('content')
    name = tag.get('name')

    if not content: continue
    if name == 'description': extracted_vals['description'] = content
  return extracted_vals

