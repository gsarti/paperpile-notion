from typing import Dict, List


def match(string, candidates) -> str:
    for c in candidates:
        if c in string:
            return c
    return None


def format_entry(entry: Dict[str, str], journals: List[Dict[str, str]], conferences: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """ Produces a dictionary in format column_name: {type: x, value: y} for each value in the entry"""
    # Select the conference shortname based on proceedings
    if entry['Item type'] == 'Journal Article':
        if 'Full journal' in entry.keys() and entry['Full journal']:
            venue = [j['short'] for j in journals if j['name'] == entry['Full journal'].strip()]
        else:
            venue = [j['short'] for j in journals if j['name'] == entry['Journal'].strip()]
    elif entry['Item type'] == 'Conference Paper':
        venue = [
            c['short'] for c in conferences if c['name'] == match(
            entry['Proceedings title'].strip(), [c['name'] for c in conferences]
        )]
        if not venue:
            venue = [entry['Proceedings title'].strip()]
    elif entry['Item type'] == 'Preprint Manuscript':
        venue = [entry['Archive prefix'].strip()]
    # Arxiv links are privileged
    links = [x for x in entry['URLs'].strip().split(';')]
    arxiv_links = [x for x in links if 'arxiv' in x]
    if len(arxiv_links) > 0:
        selected_link = arxiv_links[0]
        venue.append('arXiv')
    else:
        selected_link = links[0]
    date = entry['Date published'].strip() if 'Date published' in entry.keys() else ''
    if len(date) > 10:
        date = date[:10]
    elif len(date) == 4 or not date:
        date = entry['Publication year'].strip() + '-01-01'
    all_labels = [x.strip() for x in entry['Labels filed in'].strip().split(';')]
    categories = [x for x in all_labels if ' - ' not in x]
    methods = [x.split(' - ')[1] for x in all_labels if ' - ' in x]
    formatted_entry = {
        'Item type':  {'type': 'select',       'value': entry['Item type'].strip()},
        'Authors':    {'type': 'multi_select', 'value': entry['Authors'].strip().split(',')},
        'Title':      {'type': 'title',        'value': entry['Title'].strip()},
        'Venues':     {'type': 'multi_select', 'value': venue},
        'Date':       {'type': 'date',         'value': date},
        'Link':       {'type': 'url',          'value': selected_link},
        'Categories': {'type': 'multi_select', 'value': categories},#, 'color': [COLOR_MAP[cat]['color'] for cat in categories]}
        'Methods':    {'type': 'multi_select', 'value': methods},
    }
    if not 'to read' in entry['Folders filed in'].lower():  
        formatted_entry['Status'] = {'type': 'select', 'value': 'Done'}
    return formatted_entry
