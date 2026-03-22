import xml.etree.ElementTree as ET
import argparse
import logging
import re
import gc

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def parse_wiktionary_stream(xml_file: str, language_code: str, limit: int = None):
    """
    Memory-safe streaming parser for massive Wiktionary XML dumps.
    Uses iterparse to process elements one at a time and clear them from RAM.
    """
    logging.info(f"Starting memory-safe stream of {xml_file} (Lang: {language_code})...")
    
    # Regex to catch basic IPA templates like {{IPA|fr|/pau/}} or {{pron|/pau/|fr}}
    # Note: Wiktionary templates vary wildly, this is a baseline heuristic.
    ipa_pattern = re.compile(r'\{\{(?:IPA|pron)\|' + language_code + r'\|([^}]+)\}\}')
    
    extracted_data = {}
    count = 0

    # iterparse yields events as the XML stream is read
    context = ET.iterparse(xml_file, events=('end',))
    
    for event, elem in context:
        # Strip namespace to make tag checking easier (Wiktionary usually uses xmlns)
        tag = elem.tag.split('}')[-1] 

        if tag == 'page':
            title_elem = elem.find('.//*{*}title')
            text_elem = elem.find('.//*{*}text')
            
            if title_elem is not None and text_elem is not None and text_elem.text:
                title = title_elem.text
                
                # Exclude meta-pages (Wiktionary:, Help:, etc.)
                if ":" not in title:
                    # Search for IPA pronunciation
                    match = ipa_pattern.search(text_elem.text)
                    if match:
                        ipa_string = match.group(1).split('|')[0] # Grab the first IPA entry if piped
                        extracted_data[title] = ipa_string
                        count += 1
                        
                        if count % 1000 == 0:
                            logging.info(f"Parsed {count} entries... (Latest: {title} -> {ipa_string})")
            
            # CRITICAL: Free memory immediately
            elem.clear()
            
            # Also clear previous siblings from root to prevent memory leaks in iterparse
            while elem.getprevious() is not None:
                del elem.getparent()[0]
                
            if limit and count >= limit:
                logging.info(f"Reached limit of {limit}. Stopping early.")
                break

    # Force garbage collection just to be safe
    gc.collect()
    logging.info(f"Finished parsing. Extracted {len(extracted_data)} phonetically mapped words.")
    return extracted_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Memory-Safe Wiktionary XML Parser")
    parser.add_argument('--xml', required=True, help='Path to the Wiktionary XML dump')
    parser.add_argument('--lang', required=True, help='Language code (e.g., fr, es, it)')
    parser.add_argument('--limit', type=int, default=1000, help='Max entries to parse (for testing)')
    args = parser.parse_args()
    
    data = parse_wiktionary_stream(args.xml, args.lang, args.limit)
