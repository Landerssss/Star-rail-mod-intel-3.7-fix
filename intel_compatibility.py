import re
import os
import argparse
from pathlib import Path
from datetime import datetime

hash_data = {
    "Acheron": {
        "v3.2": {"Body": "f9910926", "Hair": "1e8e72ab", "HairBackUlt": "7ef00088", "Head": "0f1b35ea", "HeadBackUlt": "64b0f338"},
        "v3.1": {"HairBackUlt": "71633585", "Head": "008800e7", "HeadBackUlt": "6b23c635"},
        "v2.4": {"Body": "f6023c2b"},
        "v2.3": {"Hair": "111d47a6"}
    },
    "Aglaea": {
        "v3.2": {"Body": "6b23e8ee", "Hair": "1e0c0119"},
        "v3.1": {"Body": "64b0dde3", "Hair": "119f3414"}
    },
    "Anaxas": {
        "v3.2": {"Body": "4de13263", "Head": "be62cf9d", "Hair": "bdae3c65"},
        "v3.1": {"Body": "4272076e", "Head": "b1f1fa90", "Hair": "b23d0968"}
    },
    "Archer": {
        "v3.2": {"Body": "86f86c93", "Head": "40637760", "Hair": "2e6a7e20"},
        "v3.1": {"Body": "896b599e", "Head": "7457372c", "Hair": "21f94b2d"}
    },
    "Argenti": {
        "v3.2": {"Body": "9254e4a7", "Hair": "a31b0feb", "Head": "03a7a014"},
        "v3.1": {"Body": "9dc7d1aa", "Head": "0c349519"},
        "v2.3": {"Hair": "ac883ae6"}
    },
    "Arlan": {
        "v3.2": {"Body": "835494dc", "Hair": "a25d5385", "Head": "05d01e8f"},
        "v3.1": {"Body": "8cc7a1d1", "Hair": "adce6688", "Head": "0a432b82"}
    },
    "Asta": {
        "v3.2": {"Body": "0483ee84", "Hair": "1335fa30", "Head": "6e1e2998"},
        "v3.1": {"Body": "0b10db89", "Head": "618d1c95"},
        "v2.3": {"Hair": "1ca6cf3d"}
    },
    "Aventurine": {
        "v3.2": {"Body": "a62e1fae", "Hair": "25892278", "Head": "72661265"},
        "v3.1": {"Body": "a9bd2aa3", "Head": "7df52768"},
        "v2.3": {"Hair": "2a1a1775"}
    },
    "Bailu": {
        "v3.2": {"Body": "e19e70f3", "Hair": "a7cc99f5", "Head": "c4617c31"},
        "v3.1": {"Body": "ee0d45fe", "Hair": "a85facf8", "Head": "cbf2493c"}
    },
    "BlackSwan": {
        "v3.2": {"Body": "a51a0a3e", "Hair": "d236e57b", "Head": "7acd2899"},
        "v3.1": {"Body": "aa893f33", "Hair": "dda5d076", "Head": "755e1d94"}
    },
    "Blade": {
        "v3.2": {"Body": "5aa9d7f5", "Hair": "863caa28", "Head": "47c1b5e5"},
        "v3.1": {"Body": "553ae2f8", "Head": "485280e8"},
        "v2.3": {"Hair": "89af9f25"}
    },
    "Boothill": {
        "v3.2": {"Body": "fdf20423", "Hair": "c5357838", "Head": "1774a115"},
        "v3.1": {"Hair": "caa64d35", "Head": "18e79418"},
        "v2.3": {"Body": "f261312e"}
    },
    "Bronya": {
        "v3.2": {"Body": "a5ea3d65", "Hair": "41a14ff6", "Head": "2fd9f85e"},
        "v3.1": {"Body": "aa790868", "Head": "204acd53"},
        "v2.0": {"Hair": "4e327afb"}
    },
    "CaelusRemembrance": {
        "v3.2": {"Body": "3ca71eeb", "Hair": "3ba4eb10", "Head": "13e27600"},
        "v3.1": {"Body": "33342be6", "Hair": "3437de1d", "Head": "1c71430d"}
    },
    "Castorice": {
        "v3.2": {"Body": "cc41f6a0", "Head": "e31bfa54", "Hair": "e6d1f87b"},
        "v3.1": {"Body": "c3d2c3ad", "Head": "ec88cf59", "Hair": "e942cd76"}
    },
    "Cerydra": {
        "v3.2": {"Body": "41069e66", "Head": "44eac46a", "Hair": "2c101749"},
        "v3.1": {"Body": "4e95ab6b", "Head": "4b79f167", "Hair": "23832244"}
    },
    "Cipher": {
        "v3.2": {"Body": "1df7f900", "Head": "10b099f0", "Hair": "66577c58"},
        "v3.1": {"Body": "1264cc0d", "Head": "1f23acfd", "Hair": "69c44955"}
    },
    "Clara": {
        "v3.2": {"Body": "830f5c83", "Hair": "b3683156", "Head": "ce483868"},
        "v3.1": {"Head": "c1db0d65"},
        "v2.0": {"Body": "8c9c698e", "Hair": "bcfb045b"}
    },
    "Cyrene": {
        "v3.2": {"Body": "37146ceb", "Head": "5350fe4a", "Hair": "f1d16e9d", "Cape": "815bbcfa"},
        "v3.1": {"Body": "388759e6", "Head": "5cc3cb47", "Hair": "fe425b90", "Cape": "8ec889f7"}
    },
    "DanHeng": {
        "v3.2": {"Body": "23c966a6", "Hair": "a36a40a7", "Head": "c00f4d4c"},
        "v3.1": {"Body": "2c5a53ab", "Hair": "acf975aa", "Head": "cf9c7841"}
    },
    "DanHengIL": {
        "v3.2": {"Body": "d3b29940", "Hair": "20fa8734", "Head": "eac59924"},
        "v3.1": {"Body": "dc21ac4d", "Hair": "2f69b239", "Head": "e556ac29"}
    },
    "DanHengPT": {
        "v3.2": {"Body": "151553c4", "Head": "eac59924", "Hair": "54912be4"},
        "v3.1": {"Body": "1a8666c9", "Head": "e556ac29", "Hair": "5b021ee9"}
    },
    "DrRatio": {
        "v3.2": {"Body": "da642b03", "Hair": "bc83a613", "Head": "97c4cd9f"},
        "v2.3": {"Hair": "b310931e"},
        "v2.0": {"Body": "d5f71e0e", "Head": "9857f892"}
    },
    "Evernight": {
        "v3.2": {"Body": "86243a35", "Head": "b4289cef", "Hair": "bb226f33"},
        "v3.1": {"Body": "89b70f38", "Head": "bbbba9e2", "Hair": "b4b15a3e"}
    },
    "Feixiao": {
        "v3.2": {"Body": "a29c89d1", "Hair": "75041858", "Head": "0cc8a20d", "Mark": "b81da035"},
        "v3.1": {"Body": "ad0fbcdc", "Hair": "7a972d55", "Head": "035b9700", "Mark": "b78e9538"}
    },
    "Firefly": {
        "v3.2": {"Body": "d511a04e", "Hair": "186136d6", "Head": "33f2dacf"},
        "v3.1": {"Hair": "17f203db", "Head": "3c61efc2"},
        "v2.3": {"Body": "da829543"}
    },
    "FuXuan": {
        "v3.2": {"Body": "5d090c39", "Hair": "8b2930fc", "Head": "e4fb727f"},
        "v3.1": {"Body": "529a3934", "Hair": "84ba05f1", "Head": "eb684772"}
    },
    "Fugue": {
        "v3.2": {"Body": "cf67bb57", "Hair": "bcf9c26d", "Head": "10c9078f", "Tail": "a90245f5"},
        "v3.1": {"Body": "c0f48e5a", "Hair": "b36af760", "Head": "1f5a3282", "Tail": "a69170f8"}
    },
    "Gallagher": {
        "v3.2": {"Body": "6dacb01d", "Hair": "4373d23e", "Head": "05a980f0"},
        "v3.1": {"Body": "623f8510", "Head": "0a3ab5fd"},
        "v2.3": {"Hair": "4ce0e733"}
    },
    "Gepard": {
        "v3.2": {"Body": "6b730b83", "Hair": "030fa511"},
        "v3.1": {"Body": "64e03e8e", "Hair": "0c9c901c"}
    },
    "Guinaifen": {
        "v3.2": {"Hair": "fb960197", "Head": "b7c0dfd9"},
        "v3.1": {"Hair": "f405349a", "Head": "b853ead4"}
    },
    "Hanya": {
        "v3.2": {"Body": "c16cb300", "Hair": "c9d12e3c", "Head": "a10a513e"},
        "v3.1": {"Body": "ceff860d", "Hair": "c6421b31", "Head": "ae996433"}
    },
    "Herta": {
        "v3.2": {"Body": "cf1012f5", "Hair": "f67e9060", "Head": "0e8c035a"},
        "v3.1": {"Hair": "f9eda56d", "Head": "011f3657"},
        "v2.0": {"Body": "c08327f8"}
    },
    "Himeko": {
        "v3.2": {"Body": "6d460e12", "Hair": "738da645", "Head": "30f6c118"},
        "v3.1": {"Hair": "7c1e9348", "Head": "3f65f415"},
        "v2.3": {"Body": "62d53b1f"}
    },
    "Hook": {
        "v3.2": {"Body": "bf053fd2", "Hair": "5c438f67", "Head": "ef3973a2"},
        "v3.1": {"Body": "b0960adf", "Hair": "53d0ba6a", "Head": "e0aa46af"}
    },
    "Huohuo": {
        "v3.2": {"Body": "68334db0", "Hair": "dbb6a31f", "Head": "99456749"},
        "v3.1": {"Hair": "d4259612", "Head": "96d65244"},
        "v2.0": {"Body": "67a078bd"}
    },
    "Hyacine": {
        "v3.2": {"Body": "42915465", "Head": "51e9543e", "Hair": "c7ab6927"},
        "v3.1": {"Body": "4d026168", "Head": "5e7a6133", "Hair": "c8385c2a"}
    },
    "Hysilens": {
        "v3.2": {"Body": "5980bf33", "Head": "ce483868", "Hair": "73868d77"},
        "v3.1": {"Body": "56138a3e", "Head": "c1db0d65", "Hair": "7c15b87a"}
    },
    "Jade": {
        "v3.2": {"Body": "a6379d5f", "Hair": "0ac36fa2", "Head": "b416a575"},
        "v3.1": {"Body": "a9a4a852", "Hair": "05505aaf", "Head": "bb859078"}
    },
    "Jiaoqiu": {
        "v3.2": {"Body": "771c74f6", "Hair": "36ad1e7e"},
        "v3.1": {"Body": "788f41fb", "Hair": "393e2b73"}
    },
    "JingYuan": {
        "v3.2": {"Body": "04c1a42a", "Hair": "4aecf045", "Head": "c717230f"},
        "v3.1": {"Hair": "457fc548"},
        "v2.5": {"Body": "0b529127"},
        "v2.1": {"Head": "c8841602"}
    },
    "Jingliu": {
        "v3.2": {"Body": "7c4d555b", "Hair": "1e6c1d97", "Head": "9aad247f"},
        "v3.1": {"Body": "73de6056", "Hair": "11ff289a", "Head": "953e1172"}
    },
    "Kafka": {
        "v3.2": {"Body": "62d6efc5", "Hair": "1cb6a0c8", "Head": "47c458ae"},
        "v3.1": {"Hair": "132595c5", "Head": "48576da3"},
        "v2.0": {"Body": "6d45dac8"}
    },
    "Lingsha": {
        "v3.2": {"Body": "9b982e14", "Hair": "b47b8583", "Head": "34c0339f"},
        "v3.1": {"Body": "940b1b19", "Hair": "bbe8b08e", "Head": "3b530692"}
    },
    "Luka": {
        "v3.2": {"Body": "bf9f2dd9", "Hair": "9cdf77af", "Head": "a75cb220"},
        "v3.1": {"Body": "b00c18d4", "Hair": "934c42a2", "Head": "a8cf872d"}
    },
    "Luocha": {
        "v3.2": {"Body": "16d95198", "Hair": "a2f89b5c", "Head": "73ebad81"},
        "v3.1": {"Hair": "ad6bae51", "Head": "7c78988c"},
        "v2.0": {"Body": "194a6495"}
    },
    "Lynx": {
        "v3.2": {"Body": "b502f29b", "Hair": "ebfcbddb", "Head": "4fee1a45"},
        "v3.1": {"Body": "ba91c796", "Hair": "e46f88d6", "Head": "407d2f48"}
    },
    "March7thHunt": {
        "v3.2": {"Body": "58f7fff6", "Hair": "96a52a9a", "Head": "4635947e"},
        "v3.1": {"Body": "5764cafb", "Hair": "99361f97", "Head": "49a6a173"}
    },
    "March7thPreservation": {
        "v3.2": {"Body": "e9f678b6", "Hair": "b1bcbbd4"},
        "v3.1": {"Body": "e6654dbb", "Hair": "be2f8ed9"}
    },
    "Misha": {
        "v3.2": {"Body": "69c18ac5", "Hair": "c25783a1", "Head": "595d0add"},
        "v3.1": {"Body": "6652bfc8", "Head": "56ce3fd0"},
        "v2.3": {"Hair": "cdc4b6ac"}
    },
    "Moze": {
        "v3.2": {"Body": "045fb822", "Hair": "8ff677d1"},
        "v3.1": {"Body": "0bcc8d2f", "Hair": "806542dc"}
    },
    "Mydei": {
        "v3.2": {"Body": "d2fa0357", "Hair": "24998a31", "Head": "5172a57d"},
        "v3.1": {"Body": "dd69365a", "Hair": "2b0abf3c", "Head": "5ee19070"}
    },
    "Natasha": {
        "v3.2": {"Body": "b185764c", "Hair": "4125daaa"},
        "v3.1": {"Body": "be164341", "Hair": "4eb6efa7"}
    },
    "PaimonDemiurge": {
        "v3.2": {"Body": "c8740f82", "Head": "267be81a", "Hair": "6dfb56d6", "Wings": "130505d3"},
        "v3.1": {"Body": "c7e73a8f", "Head": "29e8dd17", "Hair": "626863db", "Wings": "1c9630de"}
    },
    "Pela": {
        "v3.2": {"Body": "7637086e", "Hair": "174a988f", "Head": "886a8cce"},
        "v3.1": {"Body": "79a43d63", "Hair": "18d9ad82", "Head": "87f9b9c3"}
    },
    "Phainon": {
        "v3.2": {"Body": "931c7eb0", "Head": "d4dc4c4d", "Hair": "844ee3d6"},
        "v3.1": {"Body": "9c8f4bbd", "Head": "db4f7940", "Hair": "8bddd6db"}
    },
    "Qingque": {
        "v3.2": {"Body": "3e8e9f4a", "Hair": "7829ac5c", "Head": "c60480e3"},
        "v3.1": {"Hair": "77ba9951", "Head": "c997b5ee"},
        "v2.2": {"Body": "311daa47"}
    },
    "Rappa": {
        "v3.2": {"Body": "fb3c1ddb", "Hair": "2f79ddcc", "Head": "4f97843a"},
        "v3.1": {"Body": "f4af28d6", "Hair": "20eae8c1", "Head": "4004b137"}
    },
    "Robin": {
        "v3.2": {"Body": "5343b4c1", "Hair": "07f14e1d", "Head": "31a91f87"},
        "v3.1": {"Body": "5cd081cc", "Hair": "08627b10", "Head": "3e3a2a8a"}
    },
    "RuanMei": {
        "v3.2": {"Body": "172e7ba6", "Head": "9d8b73a6"},
        "v3.1": {"Body": "18bd4eab", "Head": "921846ab"}
    },
    "Saber": {
        "v3.2": {"Body": "90edbf77", "Head": "5bc01067", "Hair": "4d5c6aa7"},
        "v3.1": {"Body": "9f7e8a7a", "Head": "5453256a", "Hair": "42cf5faa"}
    },
    "Sam": {
        "v3.2": {"Body": "33ab0bd9", "Wings": "d9a21081"},
        "v3.1": {"Body": "3c383ed4", "Wings": "d631258c"}
    },
    "Sampo": {
        "v3.2": {"Body": "82a86474", "Hair": "3ed74e5c", "Head": "69c57562"},
        "v3.1": {"Body": "8d3b5179", "Head": "6656406f"},
        "v2.3": {"Hair": "31447b51"}
    },
    "Seele": {
        "v3.2": {"Body": "4a62ad63", "Hair": "c97a209c", "Head": "446bbc7d"},
        "v3.1": {"Body": "45f1986e", "Hair": "c6e91591", "Head": "4bf88970"}
    },
    "Serval": {
        "v3.2": {"Body": "84539e80", "Hair": "4fafaaea"},
        "v3.1": {"Body": "8bc0ab8d", "Hair": "403c9fe7"}
    },
    "SilverWolf": {
        "v3.2": {"Body": "64213ba5"},
        "v2.0": {"Body": "6bb20ea8"}
    },
    "Sparkle": {
        "v3.2": {"Body": "cdbefc09", "Hair": "206f41aa", "Head": "bd2f4472"},
        "v3.1": {"Body": "c22dc904", "Hair": "2ffc74a7", "Head": "b2bc717f"}
    },
    "Stelle": {
        "v3.2": {"Body": "d52d7139", "Hair": "0f43f610", "Head": "9cfbc761"},
        "v3.1": {"Body": "dabe4434", "Head": "9368f26c"},
        "v2.2": {"Hair": "00d0c31d"}
    },
    "Sunday": {
        "v3.2": {"Body": "10a3d37b", "Hair": "aed42577", "Head": "891a3809"},
        "v3.1": {"Body": "1f30e676", "Hair": "a147107a", "Head": "86890d04"}
    },
    "Sushang": {
        "v3.2": {"Body": "708db391", "Hair": "897cc269", "Head": "e35c5db1"},
        "v3.1": {"Body": "7f1e869c", "Hair": "86eff764", "Head": "eccf68bc"}
    },
    "The": {
        "v3.2": {"Herta Body": "158aac84", "Herta Hair": "2deaf0ab", "Herta Head": "f68aa938"},
        "v3.1": {"Herta Body": "1a199989", "Herta Hair": "2279c5a6", "Herta Head": "f9199c35"}
    },
    "Tingyun": {
        "v3.2": {"Body": "65d006d1", "Fan": "fb03c709", "Hair": "02d2f998", "Head": "72dcbea3"},
        "v3.1": {"Body": "6a4333dc", "Fan": "f490f204", "Hair": "0d41cc95", "Head": "7d4f8bae"}
    },
    "Topaz": {
        "v3.2": {"Body": "92cfe440", "Hair": "c3143284", "Head": "7bc40221"},
        "v3.1": {"Body": "9d5cd14d", "Head": "7457372c"},
        "v2.3": {"Hair": "cc870789"}
    },
    "Trianne": {
        "v3.2": {"Head": "c3a0a99f"},
        "v3.1": {"Head": "cc339c92"}
    },
    "Tribbie": {
        "v3.2": {"Body": "9f177bf0", "Hair": "d1164e62", "Head": "396ae8c6"},
        "v3.1": {"Body": "90844efd", "Hair": "de857b6f", "Head": "36f9ddcb"}
    },
    "Trinnon": {
        "v3.2": {"Head": "fd080aa6"},
        "v3.1": {"Head": "f29b3fab"}
    },
    "Welt": {
        "v3.2": {"Body": "c1945568", "Hair": "2a61be98", "Head": "a9598daa"},
        "v3.1": {"Hair": "25f28b95", "Head": "a6cab8a7"},
        "v2.1": {"Body": "ce076065"}
    },
    "Xueyi": {
        "v3.2": {"Body": "9c0f0f9d", "Hair": "45e60399", "Head": "21d92a9f"},
        "v3.1": {"Body": "939c3a90", "Hair": "4a753694", "Head": "2e4a1f92"}
    },
    "Yanqing": {
        "v3.2": {"Body": "e0453b30", "Hair": "1aa7e433", "Head": "0beb189f"},
        "v3.1": {"Body": "efd60e3d"},
        "v2.4": {"Hair": "1534d13e", "Head": "04782d92"}
    },
    "Yukong": {
        "v3.2": {"Body": "e121317e", "Hair": "013abaae", "Head": "d731e230"},
        "v3.1": {"Body": "eeb20473", "Hair": "0ea98fa3", "Head": "d8a2d73d"}
    },
    "Yunli": {
        "v3.2": {"Body": "13d57de1", "Hair": "06b925ae", "Head": "6dcdbe7f"},
        "v3.1": {"Body": "1c4648ec", "Hair": "092a10a3", "Head": "625e8b72"}
    }
}

hash_mapping = {}

for char_name, versions in hash_data.items():
    if 'v3.2' not in versions:
        continue
    
    v32 = versions['v3.2']
    
    for version_key, version_hashes in versions.items():
        if version_key == 'v3.2':
            continue
        
        for part_name in v32.keys():
            if part_name in version_hashes:
                hash_32 = v32[part_name]
                hash_old = version_hashes[part_name]
                
                if hash_32 != hash_old:
                    hash_mapping[hash_32] = hash_old

def backup_and_write(old_body, new_body, file_path, to_print):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}.txt"
    try:
        with open(backup_file_path, "w", encoding='utf-8') as f:
            f.write(old_body)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(new_body)
    except Exception as e:
        to_print.append(f"Error writing to file: {e}")
        return
    else:
        to_print.append(f"Backup created at {backup_file_path}")


def restore_backup(file_path, to_print):
    backup_pattern = f"{file_path.stem}_backup_*.txt"
    backup_files = list(file_path.parent.glob(backup_pattern))
    
    if not backup_files:
        to_print.append(f"\tNo backup found for {file_path}.")
        return
    
    most_recent_backup = max(backup_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(most_recent_backup, "r", encoding='utf-8') as f:
            content = f.read()
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        os.remove(most_recent_backup)
    except Exception as e:
        to_print.append(f"\tError restoring backup: {e}")
    else:
        to_print.append(f"\tRestored {file_path} from {most_recent_backup}.")


def process_ini_file(ini_path):
    
    with open(ini_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    current_pos = 0
    
    section_pattern = re.compile(r'^\[([^\]]+)\]', re.MULTILINE)
    
    for match in section_pattern.finditer(content):
        section_start = match.start()
        section_name = match.group(1)
        
        next_match = section_pattern.search(content, match.end())
        section_end = next_match.start() if next_match else len(content)
        
        section_content = content[section_start:section_end]
        
        sections.append({
            'name': section_name,
            'start': section_start,
            'end': section_end,
            'content': section_content
        })
    
    new_sections = []
    modifications_made = 0
    to_print = []
    
    for section in sections:
        section_content = section['content']
        section_name = section['name']
        
        found_hash_32 = None
        for hash_32 in hash_mapping.keys():
            hash_pattern = re.compile(rf'^[^;\n]*\bhash\s*=\s*{hash_32}\b', re.MULTILINE | re.IGNORECASE)
            if hash_pattern.search(section_content):
                found_hash_32 = hash_32
                break
        
        if found_hash_32:
            hash_31 = hash_mapping[found_hash_32]
            
            if '_Intel' in section_name or 'Intel' in section_name:
                continue
            
            has_v31_hash = hash_31 in content
            if has_v31_hash:
                to_print.append(f"  Skipping [{section_name}]: v3.1 hash already exists (already patched)")
                continue
            
            intel_section_name = section_name + '_Intel'
            intel_content = section_content.replace(f'[{section_name}]', f'[{intel_section_name}]')
            
            intel_content = intel_content.replace(found_hash_32, hash_31)
            
            new_sections.append({
                'original_section': section_name,
                'intel_section': intel_section_name,
                'intel_content': intel_content,
                'insert_after': section['end']
            })
            
            modifications_made += 1
            to_print.append(f"  [{section_name}] -> [{intel_section_name}]")
            to_print.append(f"    Hash: {found_hash_32} -> {hash_31}")
    
    modified_content = content
    for new_section in reversed(new_sections):
        insert_pos = new_section['insert_after']
        modified_content = (
            modified_content[:insert_pos] + 
            '\n' + new_section['intel_content'] + 
            modified_content[insert_pos:]
        )
    
    if modifications_made > 0:
        backup_and_write(content, modified_content, ini_path, to_print)
        to_print.append(f"\nModified {ini_path.name}: Added {modifications_made} Intel sections")
    else:
        to_print.append(f"\nNo modifications needed for {ini_path.name}")
    
    for line in to_print:
        print(line)
    
    return modifications_made
def main():
    parser = argparse.ArgumentParser(
        prog="HSR Intel Compatibility",
        description="Adds Intel GPU compatibility sections to HSR mod INI files by reversing the Hashes with pre CS Pose"
    )
    
    parser.add_argument(
        "--folder",
        type=str,
        default=os.getcwd(),
        help="Path to folder containing INI files to process recursively"
    )
    parser.add_argument(
        '-rb', '--restore-backups',
        action='store_true',
        help='Restore backups instead of processing INIs'
    )
    
    args = parser.parse_args()
    search_path = Path(args.folder)
    
    print(f"Searching for INI files in: {search_path}")
    
    ini_files = list(search_path.rglob('*.ini'))
    
    if not ini_files:
        print("No INI files found")
        return
    
    print(f"Found {len(ini_files)} INI file(s)\n")
    
    if args.restore_backups:
        print("Restoring backups...\n")
        for ini_file in ini_files:
            to_print = []
            restore_backup(ini_file, to_print)
            for line in to_print:
                print(line)
        print(f"\nRestoration complete for {len(ini_files)} file(s)")
        return
    
    total_modifications = 0
    for ini_file in ini_files:
        print(f"\n{'='*60}")
        print(f"Processing: {ini_file.name}")
        print('='*60)
        modifications = process_ini_file(ini_file)
        total_modifications += modifications
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: Added {total_modifications} Intel sections across {len(ini_files)} file(s)")
    print('='*60)
    
    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
