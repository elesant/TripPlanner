import lxml.html as lh

def extract_regular_tags(el):
  extracted_vals = {}
  title_tags = el.cssselect('title')
  for title in title_tags:
    if title.text_content() and len(title.text_content()) > 0:
      extracted_vals['title'] = title.text_content()
      break

  link_tags = el.cssselect('link')
  favicons = [tag for tag in link_tags if 'icon' in tag.get('rel')]
  if len(favicons) > 0 and favicons[0].get('href') is not None:
    extracted_vals['favicon'] = favicons[0].get('href')
  return extracted_vals
