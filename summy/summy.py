import sys
import lxml.html as lh
from open_graph_extractor import extract_open_graph_tags
from meta_extractor import extract_meta_tags
from regular_extractor import extract_regular_tags

def summarize(doc_contents):
  root = lh.fromstring(doc_contents)

  # TODO: add prioritization and let users pick sources through arguments
  # open graph meta tags
  og_vals = extract_open_graph_tags(root)

  # standard meta tags
  meta_vals = extract_meta_tags(root)

  # regular, non-meta tags
  vals = extract_regular_tags(root)

  vals.update(meta_vals)
  vals.update(og_vals)
  return vals

if __name__ == '__main__':
  print summarize(sys.stdin.read())

