import os
import sys
from typing import Any, Dict, List, Optional

# Pastikan bisa import dari root project (scraper, models, processors, exporters)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from scraper.api_scraper import APIScraper
from processors.filter import LeadFilter
from processors.tagger import LeadTagger


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def home():
        """
        Root endpoint — info singkat & link docs.
        """
        return jsonify(
            {
                "message": "🚀 Lead Scraper API is running",
                "docs": "/docs",
                "endpoints": {
                    "health": "/health",
                    "leads": "/leads?limit=20&city=Jakarta&tag_keyword=Tech",
                },
            }
        )

    @app.route("/health", methods=["GET"])
    def health():
        """
        Health check sederhana
        """
        return jsonify({"status": "ok"}), 200

    @app.route("/docs", methods=["GET"])
    def docs():
        """
        Dokumentasi ringkas endpoint (tanpa swagger, ringan).
        """
        return jsonify(
            {
                "title": "Lead Scraper API",
                "endpoints": [
                    {
                        "path": "/",
                        "method": "GET",
                        "desc": "Info API & link ke docs.",
                        "params": [],
                    },
                    {
                        "path": "/health",
                        "method": "GET",
                        "desc": "Health check sederhana.",
                        "params": [],
                        "response_example": {"status": "ok"},
                    },
                    {
                        "path": "/leads",
                        "method": "GET",
                        "desc": "Ambil leads dari Random User API, bisa difilter & ditag.",
                        "params": [
                            {
                                "name": "limit",
                                "type": "int",
                                "required": False,
                                "default": 20,
                                "example": 50,
                                "desc": "Jumlah lead yang diambil.",
                            },
                            {
                                "name": "city",
                                "type": "str",
                                "required": False,
                                "example": "Jakarta",
                                "desc": "Filter berdasarkan nama kota (case-insensitive).",
                            },
                            {
                                "name": "tag_keyword",
                                "type": "str",
                                "required": False,
                                "example": "Tech",
                                "desc": "Jika ada, tambahkan tag untuk lead yang company-nya mengandung keyword ini.",
                            },
                        ],
                        "response_example": {
                            "meta": {
                                "limit": 20,
                                "count": 5,
                                "city": "Jakarta",
                                "tag_keyword": "Tech",
                            },
                            "data": [
                                {
                                    "name": "John Doe",
                                    "email": "john@example.com",
                                    "company": "Unknown Company",
                                    "position": "Unknown",
                                    "location": "Jakarta",
                                    "tags": ["Tech Industry"],
                                }
                            ],
                        },
                    },
                ],
            }
        )

    @app.route("/leads", methods=["GET"])
    def get_leads():
        """
        Ambil leads → optional filter by city → optional tagging by keyword.
        Query:
          - limit: int (default 20)
          - city: str (optional)
          - tag_keyword: str (optional)
        """
        # --- Query params & validasi ringan
        limit = _parse_int(request.args.get("limit"), default=20, minimum=1, maximum=500)
        city: Optional[str] = _normalize_str(request.args.get("city"))
        tag_keyword: Optional[str] = _normalize_str(request.args.get("tag_keyword"))

        try:
            # --- Scrape
            scraper = APIScraper()
            leads = scraper.fetch(results=limit)

            # --- Filter (jika ada city)
            if city:
                leads = LeadFilter().filter_by_location(leads, city)

            # --- Tagging (jika ada keyword)
            if tag_keyword:
                LeadTagger().tag_industry(leads, keyword=tag_keyword)

            # --- Response
            payload: Dict[str, Any] = {
                "meta": {
                    "limit": limit,
                    "count": len(leads),
                    "city": city,
                    "tag_keyword": tag_keyword,
                },
                "data": [lead.to_dict() for lead in leads],
            }
            return jsonify(payload), 200

        except Exception as exc:  # fallback guardrail
            return (
                jsonify(
                    {
                        "error": "internal_error",
                        "message": str(exc),
                    }
                ),
                500,
            )

    return app


# ----------------- Helpers -----------------
def _parse_int(
    value: Optional[str], default: int = 20, minimum: int = 1, maximum: int = 1000
) -> int:
    """
    Safely parse int with bounds.
    """
    try:
        parsed = int(value) if value is not None else default
        if parsed < minimum:
            return minimum
        if parsed > maximum:
            return maximum
        return parsed
    except Exception:
        return default


def _normalize_str(value: Optional[str]) -> Optional[str]:
    """
    Trim & handle empty strings.
    """
    if value is None:
        return None
    v = value.strip()
    return v if v else None


# -------------- Entrypoint ---------------
if __name__ == "__main__":
    app = create_app()
    # Gunakan host=0.0.0.0 jika ingin diakses dari device lain di jaringan lokal
    app.run(debug=True, port=5000)
