import yaml  # Import the PyYAML module to work with YAML files
import xml.etree.ElementTree as xml_tree  # Import the XML module to create and manage XML structures

# Open the file 'feed.yaml' in read mode ('r') and give it the name 'file'
with open('feed.yaml', 'r') as file:
    # Use safe_load to parse the YAML file into a Python dictionary (safer than load)
    yaml_data = yaml.safe_load(file)

    # Create the root XML element <rss> with some attributes
    # These attributes include the RSS version and two namespace declarations for iTunes and content modules
    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

# Create a child element <channel> inside the <rss> root element
channel_element = xml_tree.SubElement(rss_element, 'channel')

# Store the 'link' value from the YAML data (used later to prefix other links)
link_prefix = yaml_data['link']

# Add core metadata to the <channel> section using data from the YAML file

# Add the <title> element and set its text to the podcast title
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']

# Add the <format> element (custom tag, possibly describing the audio/video format)
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']

# Add the <subtitle> element with a short description or tagline
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']

# Add the iTunes <itunes:author> tag, which is a required tag in podcast feeds
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']

# Add the <description> element, a required field for RSS feeds
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']

# Add an <itunes:image> element with an href attribute pointing to the podcast cover art
# The URL is built by combining the base link (link_prefix) and the image path from YAML
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})

# Add a <language> tag, e.g., "en-us"
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']

# Add a <link> tag pointing to the podcast's main webpage
xml_tree.SubElement(channel_element, 'link').text = link_prefix

# Add the <itunes:category> tag with a category attribute (e.g., "Technology", "Health", etc.)
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

# Loop through each episode/item in the YAML data and create a corresponding <item> in XML
for item in yaml_data['item']:
    # Create a new <item> element under <channel> for each episode
    item_element = xml_tree.SubElement(channel_element, 'item')

    # Add <title> tag with the episode title
    xml_tree.SubElement(item_element, 'title').text = item['title']

    # Add <itunes:author> tag with the author (using same author as channel)
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']

    # Add <description> tag with the episode description
    xml_tree.SubElement(item_element, 'description').text = item['description']

    # Add <itunes:duration> tag with the episode duration (e.g., "00:30:12")
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']

    # Add <pubDate> tag with the episode's publication date
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']

    # Add an <enclosure> tag which tells podcast apps where to download the episode
    # The attributes are:
    #   - url: full path to the audio file (link_prefix + item['file'])
    #   - type: MIME type (should be 'audio/mpeg' for MP3)
    #   - length: file size in bytes (as a string)
    xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

# Create an ElementTree object starting from the root <rss> element
output_tree = xml_tree.ElementTree(rss_element)

# Write the XML tree to a file called 'podcast.xml'
# encoding='UTF-8' sets the character encoding
# xml_declaration=True adds the standard XML declaration line at the top of the file
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)