import os
import sys
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.xml.xml_processor import XMLProcessor


class TestXMLProcessor:
    def test_processes_xml_file_with_episodes(self):
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
    <channel>
        <title>Test Podcast</title>
        <item>
            <title>Episode 1</title>
            <description>First episode description</description>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
            <enclosure url="https://example.com/episode1.mp3" type="audio/mpeg" length="25000000"/>
            <itunes:duration>00:16:53</itunes:duration>
        </item>
        <item>
            <title>Episode 2</title>
            <description><![CDATA[<p>Second episode with HTML</p>]]></description>
            <pubDate>Tue, 02 Jan 2024 11:00:00 GMT</pubDate>
            <enclosure url="https://example.com/episode2.mp3" type="audio/mpeg" length="30000000"/>
            <itunes:duration>10:30</itunes:duration>
        </item>
    </channel>
</rss>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_file = f.name
        
        try:
            processor = XMLProcessor()
            episodes = processor.run(temp_file)
            
            assert len(episodes) == 2
            
            assert episodes[0].title == "Episode 1"
            assert episodes[0].description == "First episode description"
            assert episodes[0].url == "https://example.com/episode1.mp3"
            assert isinstance(episodes[0].published_date, datetime)
            assert episodes[0].duration == 1013
            assert episodes[0].file_size == 25000000
            
            assert episodes[1].title == "Episode 2"
            assert episodes[1].description == "Second episode with HTML"
            assert episodes[1].url == "https://example.com/episode2.mp3"
            assert episodes[1].duration == 630
            assert episodes[1].file_size == 30000000
        finally:
            os.unlink(temp_file)
    
    def test_handles_missing_elements(self):
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <item>
            <title>Episode without description</title>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_file = f.name
        
        try:
            processor = XMLProcessor()
            episodes = processor.run(temp_file)
            
            assert len(episodes) == 1
            assert episodes[0].title == "Episode without description"
            assert episodes[0].description == ""
            assert episodes[0].url == ""
        finally:
            os.unlink(temp_file)
    
    def test_cleans_html_from_description(self):
        processor = XMLProcessor()
        
        html_text = "<p>This is <strong>bold</strong> text with <a href='#'>links</a></p>"
        clean_text = processor._clean_html(html_text)
        
        assert clean_text == "This is bold text with links"
    
    def test_parses_pub_date_correctly(self):
        processor = XMLProcessor()
        
        pub_date_str = "Mon, 01 Jan 2024 10:00:00 GMT"
        parsed_date = processor._parse_pub_date(pub_date_str)
        
        assert parsed_date.year == 2024
        assert parsed_date.month == 1
        assert parsed_date.day == 1
        assert parsed_date.hour == 10
    
    def test_handles_invalid_date_format(self):
        processor = XMLProcessor()
        
        invalid_date = "Invalid date format"
        parsed_date = processor._parse_pub_date(invalid_date)
        
        assert isinstance(parsed_date, datetime)
    
    def test_parses_duration_formats(self):
        processor = XMLProcessor()
        
        assert processor._parse_duration("00:16:53") == 1013
        assert processor._parse_duration("10:30") == 630
        assert processor._parse_duration("1800") == 1800
        assert processor._parse_duration("") is None
        assert processor._parse_duration("invalid") is None
    
    def test_extracts_file_size_from_enclosure(self):
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <item>
            <title>Test Episode</title>
            <enclosure url="https://example.com/test.mp3" type="audio/mpeg" length="12345678"/>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_file = f.name
        
        try:
            processor = XMLProcessor()
            episodes = processor.run(temp_file)
            
            assert len(episodes) == 1
            assert episodes[0].file_size == 12345678
        finally:
            os.unlink(temp_file)