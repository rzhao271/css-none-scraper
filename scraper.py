import ast
import re
import requests
from lxml import etree

valid_property_re = re.compile('^[^(@:]+$')

# scrape_properties: void -> [(link, property-name)] 
def scrape_properties():
    main_page_url = 'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference'
    content = requests.get(main_page_url).text
    tree = etree.HTML(content)
    nodes = tree.xpath('//div[@class=\'index\']/ul/li')
    processed_nodes = []
    for node in nodes:
        link = node.xpath('a')[0].get('href')
        text = node.xpath('a/code')[0].text
        if valid_property_re.match(text):
            processed_nodes.append((link, text))
    return processed_nodes

# scrape_prop
#: str -> initial_value: str|None
def scrape_prop(page_url):
    content = requests.get(page_url).text
    tree = etree.HTML(content)
    try:
        node = tree.xpath('//table[@class=\'properties\']/tbody/tr')[0]
        heading = node.xpath('th/a')[0].text
        value = etree.tostring(node.xpath('td')[0]).decode('UTF-8')
        if heading.lower() == 'initial value':
            return value
        else:
            return None
    except:
        return None

def main():
    scrape = 1

    # Scrape properties along with their initial values
    properties_iv_dict = dict()
    
    if scrape:
        properties = scrape_properties()
        for link, name in properties:
            initial_value = scrape_prop(f'https://developer.mozilla.org/{link}')
            properties_iv_dict[name] = initial_value
        
        with open('prop-iv-dict.txt', 'w') as f:
            f.write(str(properties_iv_dict))
    else:
        with open('prop-iv-dict.txt', 'r') as f:
            properties_iv_dict = ast.literal_eval(f.read())

    properties_with_none_value = [key for key, val in properties_iv_dict.items() 
        if val is not None and '<code>none</code>' in val]
    print('\n'.join(properties_with_none_value))

if __name__ == '__main__':
    main()