"""Extraction Pipeline for Data.p4k Files.

Parses the original StarCraft 2 .p4k archive files (used by the old Tkinter OAM)
and creates reference SQLite databases for use in the new sc-oam-app.

This mirrors the extraction pipeline from the old OAM application and provides
a programmatic API for creating reference databases from legacy game data.
"""

import struct
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─── Extraction Constants ───────────────────────────────────────────────

# Magic bytes for SC2 .p4k archives (signature validation)
P4K_MAGIC = b"P4K\0\0\0"

# Expected structure constants (derived from original OAM pipeline)
P4K_HEADER_SIZE = 16  # 4 magic + 12 reserved/flags
CHUNK_HEADER_SIZE = 8  # 4 length + 4 type


# ─── Core Extraction Logic ─────────────────────────────────────────────

def parse_p4k_archive(filepath: Path) -> Dict[str, List[dict]]:
    """Parse a single .p4k archive file and return extracted records.
    
    Returns a dict with category keys mapping to lists of record dicts.
    Categories typically include: ships, inventory, blueprints, etc.
    """
    records = {
        "ships": [],
        "inventory": [],
        "blueprints": [],
        "unknown": [],
    }
    
    try:
        with open(filepath, "rb") as f:
            # Validate magic bytes
            magic = f.read(4)
            if magic != P4K_MAGIC:
                raise ValueError(f"Invalid .p4k magic bytes: {magic}")
            
            # Read header (remaining 12 bytes: reserved/flags)
            header = f.read(P4K_HEADER_SIZE - 4)
            
            # Read chunks until EOF
            while True:
                chunk_header = f.read(CHUNK_HEADER_SIZE)
                if not chunk_header or len(chunk_header) < CHUNK_HEADER_SIZE:
                    break
                
                chunk_length = struct.unpack("<I", chunk_header[:4])[0]
                chunk_type = chunk_header[4:8].decode("ascii", errors="replace").strip("\x00")
                
                # Validate chunk length isn't absurd
                if chunk_length > 10 * 1024 * 1024:  # 10MB max per chunk
                    raise ValueError(f"Chunk length unreasonably large: {chunk_length}")
                
                chunk_data = f.read(chunk_length)
                if len(chunk_data) < chunk_length:
                    break  # Truncated file
                
                # Parse based on chunk type
                records_by_type = _parse_chunk_type(chunk_type, chunk_data)
                for category, recs in records_by_type.items():
                    records[category].extend(recs)
                    
    except Exception as e:
        raise RuntimeError(f"Failed to parse .p4k archive {filepath}: {e}") from e
    
    return records


def _parse_chunk_type(chunk_type: str, data: bytes) -> Dict[str, List[dict]]:
    """Parse a chunk based its type identifier."""
    records = {"ships": [], "inventory": [], "blueprints": [], "unknown": []}
    
    if chunk_type == "ship":
        records["ships"] = _parse_ship_chunk(data)
    elif chunk_type == "inventory":
        records["inventory"] = _parse_inventory_chunk(data)
    elif chunk_type == "blueprint":
        records["blueprints"] = _parse_blueprint_chunk(data)
    else:
        records["unknown"].append({
            "raw_data": data.hex()[:100],  # First 100 hex chars as summary
            "chunk_type": chunk_type,
            "chunk_length": len(data),
        })
    
    return records


def _parse_ship_chunk(data: bytes) -> List[dict]:
    """Parse a ship chunk from .p4k data."""
    ships = []
    
    # The original Tk OAM stored ship data in a specific binary format.
    # This is a simplified parser; the actual format depends on the SC2 .p4k spec.
    # We'll read a basic structure: name (32 bytes), manufacturer (32 bytes), size (4 bytes), cost (4 bytes)
    
    offset = 0
    while offset < len(data):
        try:
            # Read fields (exact format depends on original Tk OAM binary spec)
            name = data[offset:offset+32].rstrip(b"\x00").decode("utf-8", errors="replace")
            manufacturer = data[offset+32:offset+64].rstrip(b"\x00").decode("utf-8", errors="replace")
            size = struct.unpack("<I", data[offset+64:offset+68])[0]
            cost = struct.unpack("<f", data[offset+68:offset+72])[0]  # float cost
            
            ships.append({
                "name": name if name else "Unknown Ship",
                "manufacturer": manufacturer if manufacturer else "Unknown",
                "size": size,
                "cost": round(cost, 2),
                "source_file": "unknown",
            })
            
            offset += 72  # Stride per ship record
        except struct.error:
            break  # Not enough data for another record
    
    return ships


def _parse_inventory_chunk(data: bytes) -> List[dict]:
    """Parse an inventory chunk from .p4k data."""
    items = []
    
    # Similar simplified parser for inventory items
    offset = 0
    while offset < len(data):
        try:
            name = data[offset:offset+32].rstrip(b"\x00").decode("utf-8", errors="replace")
            category = data[offset+32:offset+48].rstrip(b"\x00").decode("utf-8", errors="replace")
            quantity = struct.unpack("<I", data[offset+48:offset+52])[0]
            quality = struct.unpack("<I", data[offset+52:offset+56])[0]
            
            items.append({
                "item_name": name if name else "Unknown Item",
                "category": category if category else "Uncategorized",
                "quantity": quantity,
                "quality": quality,
                "source_file": "unknown",
            })
            
            offset += 56  # Stride per item record
        except struct.error:
            break
    
    return items


def _parse_blueprint_chunk(data: bytes) -> List[dict]:
    """Parse a blueprint chunk from .p4k data."""
    blueprints = []
    
    # Blueprint parser - simplified
    offset = 0
    while offset < len(data):
        try:
            bp_id = data[offset:offset+20].rstrip(b"\x00").decode("utf-8", errors="replace")
            bp_name = data[offset+20:offset+60].rstrip(b"\x00").decode("utf-8", errors="replace")
            output_item = data[offset+60:offset+80].rstrip(b"\x00").decode("utf-8", errors="replace")
            
            blueprints.append({
                "bp_id": bp_id if bp_id else "unknown_id",
                "bp_name": bp_name if bp_name else "Unknown Blueprint",
                "output_item": output_item if output_item else "unknown_item",
                "source_file": "unknown",
            })
            
            offset += 80  # Stride per blueprint record
        except struct.error:
            break
    
    return blueprints


# ─── Database Creation ──────────────────────────────────────────────────

def create_database_from_extraction(
    records: Dict[str, List[dict]],
    output_path: Path,
    overwrite: bool = False,
) -> Dict[str, str]:
    """Create SQLite databases from extracted records.
    
    Creates separate databases per category, or a consolidated database.
    This is the reference database creation that the old Tkinter OAM pipeline did.
    """
    import sqlite3
    
    results = {}
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create separate databases per category, or a consolidated one
    for category, records_list in records.items():
        if not records_list:
            continue
        
        db_path = output_path.parent / f"{output_path.stem}_{category}.db"
        if not overwrite and db_path.exists():
            results[category] = str(db_path)
            continue
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        if category == "ships":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    manufacturer TEXT,
                    size INTEGER,
                    cost REAL,
                    source_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            for rec in records_list:
                cursor.execute(
                    "INSERT INTO ships (name, manufacturer, size, cost, source_file) VALUES (?, ?, ?, ?, ?)",
                    (rec.get("name", "Unknown"), rec.get("manufacturer", "Unknown"),
                     rec.get("size", 0), rec.get("cost", 0.0), rec.get("source_file", "unknown")),
                )
                
        elif category == "inventory":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER DEFAULT 0,
                    quality INTEGER DEFAULT 500,
                    source_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            for rec in records_list:
                cursor.execute(
                    "INSERT INTO inventory (item_name, category, quantity, quality, source_file) VALUES (?, ?, ?, ?, ?)",
                    (rec.get("item_name", "Unknown Item"), rec.get("category", "Uncategorized"),
                     rec.get("quantity", 0), rec.get("quality", 500), rec.get("source_file", "unknown")),
                )
                
        elif category == "blueprints":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blueprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bp_id TEXT UNIQUE,
                    bp_name TEXT NOT NULL,
                    output_item TEXT,
                    source_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            for rec in records_list:
                cursor.execute(
                    "INSERT INTO blueprints (bp_id, bp_name, output_item, source_file) VALUES (?, ?, ?, ?)",
                    (rec.get("bp_id", "unknown"), rec.get("bp_name", "Unknown"),
                     rec.get("output_item", "unknown"), rec.get("source_file", "unknown")),
                )
        
        conn.commit()
        conn.close()
        results[category] = str(db_path)
    
    return results


# ─── API-Integrated Extraction ─────────────────────────────────────────

def run_extraction_pipeline(
    input_folder: Path,
    output_db_path: Path,
    overwrite: bool = False,
) -> Dict[str, str]:
    """Run the full extraction pipeline: parse .p4k files → create reference databases.
    
    This is the main entry point for the extraction API endpoint.
    
    Args:
        input_folder: Path containing .p4k files to extract
        output_db_path: Base path for output databases (e.g., ./database.db → creates .db per category)
        overwrite: Whether to overwrite existing databases
    
    Returns:
        Dict mapping category names to database file paths
    """
    # ① Step 1: Discover .p4k files
    p4k_files = list(input_folder.rglob("*.p4k"))
    
    if not p4k_files:
        return {"status": "no_files", "message": f"No .p4k files found in {input_folder}"}
    
    # ② Step 2: Parse all archives
    all_records = {}
    for p4k_file in p4k_files:
        records = parse_p4k_archive(p4k_file)
        for category, recs in records.items():
            all_records.setdefault(category, []).extend(recs)
    
    # ③ Step 2b: Dedup records by (name, category) to avoid duplicates from multiple .p4k files
    deduped = {}
    for category, recs in all_records.items():
        seen = set()
        unique_recs = []
        for rec in recs:
            # Create a hashable key from the record
            key = (rec.get("name", ""), rec.get("category", ""))
            if key not in seen:
                seen.add(key)
                unique_recs.append(rec)
        deduped[category] = unique_recs
    
    # ④ Step 3: Create reference databases
    results = create_database_from_extraction(deduped, output_path, overwrite=overwrite)
    
    return {
        "status": "success",
        "p4k_files_scanned": len(p4k_files),
        "records_extracted": {k: len(v) for k, v in deduped.items()},
        "databases_created": results,
        "message": f"Extracted data from {len(p4k_files)} .p4k files into reference databases",
    }


# ─── CLI Entrypoint (for running outside API) ──────────────────────────

def main_cli() -> None:
    """CLI entrypoint for running the extraction pipeline from the command line."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract Data.p4k files for sc-oam-app")
    parser.add_argument(
        "input_folder",
        type=Path,
        help="Folder containing .p4k files to extract",
    )
    parser.add_argument(
        "output_db",
        type=Path,
        help="Base path for output databases (e.g., ./database)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing databases",
    )
    
    args = parser.parse_args()
    
    if not args.input_folder.exists():
        print(f"Error: Input folder does not exist: {args.input_folder}")
        sys.exit(1)
    
    result = run_extraction_pipeline(args.input_folder, args.output_db, overwrite=args.overwrite)
    
    if result["status"] == "success":
        print(f"✅ Extraction complete!")
        print(f"  • .p4k files scanned: {result['p4k_files_scanned']}")
        print(f"  • Records extracted: {result['records_extracted']}")
        print(f"  • Databases created: {list(results.values()) if 'results' in result else 'N/A'}")
        for cat, db_path in results.items():
            print(f"    • {cat}: {db_path}")
    else:
        print(f"❌ Extraction failed: {result.get('message', 'unknown error')}")
        sys.exit(1)


# ─── When run as script ────────────────────────────────────────────────
if __name__ == "__main__":
    main_cli()