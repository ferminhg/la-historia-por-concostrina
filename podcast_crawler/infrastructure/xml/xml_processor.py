import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

from domain.entities.podcast import Episode
from shared.logger import get_logger


class XMLProcessor:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.namespaces = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

    def run(self, xml_file_path: str) -> List[Episode]:
        self.logger.info(f"Processing XML file: {xml_file_path}")

        with open(xml_file_path, "r", encoding="utf-8") as f:
            xml_content = f.read()

        root = ET.fromstring(xml_content)
        episodes = []

        for item in root.findall(".//item"):
            episode = self._extract_episode_from_item(item)
            if episode:
                episodes.append(episode)

        self.logger.info(f"Extracted {len(episodes)} episodes from {xml_file_path}")
        return episodes

    def _extract_episode_from_item(self, item) -> Episode:
        title = self._get_text_or_empty(item, "title")
        description = self._get_text_or_empty(item, "description")
        pub_date_str = self._get_text_or_empty(item, "pubDate")
        enclosure = item.find("enclosure")

        itunes_duration = item.find("itunes:duration", self.namespaces)
        duration_str = itunes_duration.text if itunes_duration is not None else ""

        url = (
            enclosure.attrib["url"]
            if enclosure is not None and "url" in enclosure.attrib
            else ""
        )
        file_size = (
            int(enclosure.attrib["length"])
            if enclosure is not None and "length" in enclosure.attrib
            else None
        )

        description_clean = self._clean_html(description)
        published_date = self._parse_pub_date(pub_date_str)
        duration_seconds = self._parse_duration(duration_str)

        return Episode(
            title=title,
            description=description_clean,
            url=url,
            published_date=published_date,
            duration=duration_seconds,
            file_size=file_size,
        )

    def _get_text_or_empty(self, item, tag_name: str) -> str:
        element = item.find(tag_name)
        return element.text if element is not None else ""

    def _clean_html(self, raw_html: str) -> str:
        clean_regex = re.compile("<.*?>")
        return re.sub(clean_regex, "", raw_html)

    def _parse_pub_date(self, pub_date_str: str) -> datetime:
        try:
            return datetime.strptime(pub_date_str[:25], "%a, %d %b %Y %H:%M:%S")
        except Exception as e:
            self.logger.warning(f"Error parsing date: {pub_date_str} -> {e}")
            return datetime.now()

    def _parse_duration(self, duration_str: str) -> Optional[int]:
        if not duration_str:
            return None

        try:
            if ":" in duration_str:
                parts = duration_str.split(":")
                if len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                    return hours * 3600 + minutes * 60 + seconds
                elif len(parts) == 2:
                    minutes, seconds = map(int, parts)
                    return minutes * 60 + seconds
            else:
                return int(duration_str)
        except Exception as e:
            self.logger.warning(f"Error parsing duration: {duration_str} -> {e}")
            return None
