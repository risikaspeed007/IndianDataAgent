import json
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, "src")

from india_data_agent.data_service import (
    get_change,
    get_highest_improvement,
    compare_entities,
    rank_entities,
    get_value_for_year,
)
from india_data_agent.analyzer import world_average
from india_data_agent.intent import extract_entity


def get_answer(question):
    q = question.lower()

    if "world average" in q:
        return world_average()

    if (
        "highest improvement" in q
        or "most improved" in q
        or "improved the most" in q
    ):
        result = get_highest_improvement()

        return (
            f"{result['entity']} had the highest improvement: "
            f"{result['old_value']:.1f}% → "
            f"{result['new_value']:.1f}% "
            f"(+{result['change']:.1f} percentage points)."
        )

    if "which country has the highest" in q:
        rows = rank_entities()

        excluded = {
            "World Average",
            "Developed countries",
            "Developing Countries",
        }

        rows = [
            row for row in rows
            if row["Countries/States"] not in excluded
        ]

        highest = rows[0]

        return (
            f"Highest value: {highest['Countries/States']} "
            f"with {highest['new']:.1f}% in 2009–10."
        )

    if "compare" in q and " and " in q:
        parts = q.split(" and ", 1)

        name1 = parts[0].replace("compare", "").strip()
        name2 = parts[1].strip()

        result = compare_entities(name1, name2)

        if isinstance(result, str):
            return result

        first = result["first"]
        second = result["second"]

        return (
            f"{first['entity']}: "
            f"{first['old_value']:.1f}% → "
            f"{first['new_value']:.1f}% "
            f"(change: {first['change']:+.1f})\n\n"
            f"{second['entity']}: "
            f"{second['old_value']:.1f}% → "
            f"{second['new_value']:.1f}% "
            f"(change: {second['change']:+.1f})\n\n"
            f"Difference in 2009–10: "
            f"{result['difference_2009']:+.1f} percentage points"
        )

    if "1999-2000" in q or "1999–2000" in q:
        entity = extract_entity(question)
        results = get_value_for_year(entity, "1999-2000")

        if not results:
            return "No data found."

        return "\n".join(
            f"{r['entity']}: {r['value']:.1f}% in 1999-2000"
            for r in results
        )

    if "2009-10" in q or "2009–10" in q:
        entity = extract_entity(question)
        results = get_value_for_year(entity, "2009-10")

        if not results:
            return "No data found."

        return "\n".join(
            f"{r['entity']}: {r['value']:.1f}% in 2009-10"
            for r in results
        )

    entity = extract_entity(question)
    results = get_change(entity)

    if not results:
        return "No data found."

    return "\n".join(
        f"{r['entity']}: "
        f"{r['old_value']:.1f}% → "
        f"{r['new_value']:.1f}% "
        f"(change: {r['change']:+.1f} percentage points)"
        for r in results
    )


class handler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        self.send_json(
            200,
            {
                "status": "online",
                "name": "India Data Agent",
            },
        )

    def do_POST(self):

        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)
            data = json.loads(body)

            question = data.get("question", "").strip()

            if not question:
                self.send_json(
                    400,
                    {"error": "Question is required."},
                )
                return

            answer = get_answer(question)

            self.send_json(
                200,
                {
                    "answer": answer
                },
            )

        except Exception as error:

            self.send_json(
                500,
                {
                    "error": str(error)
                },
            )