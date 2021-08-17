from typing import List, Dict, Any

class Properties:
    def __init__(self, properties: Dict[str, Any] = None):
        if properties is not None:
            self.result = properties
        self.result = {}
    
    @classmethod
    def from_entry(cls, properties: Dict[str, Dict[str, str]]):
        """ Entries contain fields having format column_name: {type: x, value: y} 
        
        column_name is the name of the column in Notion.
        type is one of the Notion native types (see Notion API)
        value is the value taken by the column for the entry.
        """
        result = cls()
        for prop, prop_dic in properties.items():
            result.set_property(prop, prop_dic)
        return result

    def set_title(self, col, text=None):
        text = [{"type": "text", "text": {"content": text}}] if text else {}
        self.result.update({col: {"type": "title", "title": text}})

    def set_rich_text(self, col, text=None):
        text = [{"type": "text", "text": {"content": text}}] if text else {}
        self.result.update({col: {"type": "rich_text", "rich_text": text}})

    def set_number(self, col, text=None):
        text = int(text) if text else {}
        self.result.update({col: {"type": "number", "number": text}})

    def set_select(self, col, text=None, color=None):
        text = {"name": text} if text else {}#, "color": 'default' if color is None else color}
        self.result.update({col: {"type": "select", "select": text}})

    def set_multi_select(self, col, text_list=None, color_list=None):
        data = [{"name": text} for text in text_list] if text_list else {}
        self.result.update({col: {"type": "multi_select", "multi_select": data}})

    def set_checkbox(self, col, text=None):
        self.result.update({col: {"type": "checkbox", "checkbox": text if text else {}}})

    def set_url(self, col, text=None):
        self.result.update({col: {"type": "url", "url": text if text else {}}})
    
    def set_date(self, col, text=None):
        text = {'start': text} if text else {}
        self.result.update({col: {"type": "date", "date": text}})
    
    def set_property(self, prop, prop_dic):
        if prop_dic['type'] == 'title':
            self.set_title(prop, prop_dic['value'])
        elif prop_dic['type'] == 'text':
            self.set_rich_text(prop, prop_dic['value'])
        elif prop_dic['type'] == 'number':
            self.set_number(prop, prop_dic['value'])
        elif prop_dic['type'] == 'select':
            self.set_select(prop, prop_dic['value'], prop_dic.get('color', None))
        elif prop_dic['type'] == 'multi_select':
            self.set_multi_select(prop, prop_dic['value'], prop_dic.get('color', None))
        elif prop_dic['type'] == 'checkbox':
            self.set_checkbox(prop, prop_dic['value'])
        elif prop_dic['type'] == 'url':
            self.set_url(prop, prop_dic['value'])
        elif prop_dic['type'] == 'date':
            self.set_date(prop, prop_dic['value'])

    def clear(self):
        self.result.clear()


def get_field_content(field: Dict[str, Any]) -> str:
    if field['type'] == 'text':
        return field['text']['content']
    elif field['type'] == 'select':
        return field['select']['name']
    elif field['type'] == 'multi_select':
        return [item['name'] for item in field['multi_select']]
    elif field['type'] == 'date':
        return field['date']['start']
    elif field['type'] == 'url':
        return field['url']
    elif field['type'] == 'title':
        return get_field_content(field['title'][0])


def parse_db_content(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for page in pages:
        new_page = {'id': page['id']}
        for prop, prop_value in page['properties'].items():
            new_page[prop] = get_field_content(prop_value)
        result.append(new_page)
    return result