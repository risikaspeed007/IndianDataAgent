from analyzer import world_average
from data_service import (
    get_change,
    get_highest_improvement,
    compare_entities,
    rank_entities,
    get_value_for_year,
)
from intent import extract_entity
from india_data_agent.gemini_service import ask_gemini


def format_entity_results(results):
    if not results:
        return "No data found."

    return "\n".join(
        f"{r['entity']}: {r['old_value']:.1f}% → "
        f"{r['new_value']:.1f}% "
        f"(change: {r['change']:+.1f} percentage points)"
        for r in results
    )


def format_year_results(results, year):
    if not results:
        return "No data found."

    return "\n".join(
        f"{r['entity']}: {r['value']:.1f}% in {year}"
        for r in results
    )


def format_comparison(name1, name2):
    result = compare_entities(name1, name2)

    if isinstance(result, str):
        return result

    first = result["first"]
    second = result["second"]

    return (
        f"{first['entity']}: {first['old_value']:.1f}% → "
        f"{first['new_value']:.1f}% "
        f"(change: {first['change']:+.1f})\n"
        f"{second['entity']}: {second['old_value']:.1f}% → "
        f"{second['new_value']:.1f}% "
        f"(change: {second['change']:+.1f})\n\n"
        f"Difference in 2009–10: "
        f"{result['difference_2009']:+.1f} percentage points"
    )


def format_ranking():
    rows = rank_entities()

    lines = ["Ranking by 2009–10 gross enrolment ratio:"]

    for index, row in enumerate(rows, start=1):
        lines.append(
            f"{index}. {row['Countries/States']}: "
            f"{row['new']:.1f}%"
        )

    return "\n".join(lines)


def improve_with_gemini(question, answer):
    try:
        result = ask_gemini(
            question,
            f"Verified data-agent result:\n{answer}"
        )

        if result:
            return result

        return answer

    except Exception:
        return answer


print("🇮🇳 India Data Agent")
print("Ask questions about the gross enrolment dataset.")
print("Type 'exit' to quit.\n")


while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Agent: Goodbye!")
        break

    if not question:
        continue

    q = question.lower()

    # Year-specific questions
    if "1999-2000" in q or "1999–2000" in q:
        entity = extract_entity(question)
        results = get_value_for_year(entity, "1999-2000")
        answer = format_year_results(results, "1999-2000")

    elif "2009-10" in q or "2009–10" in q:
        entity = extract_entity(question)
        results = get_value_for_year(entity, "2009-10")
        answer = format_year_results(results, "2009-10")

    # World average
    elif "world average" in q:
        answer = world_average()

    # Highest improvement
    elif (
        "highest improvement" in q
        or "most improved" in q
        or "improved the most" in q
    ):
        result = get_highest_improvement()

        answer = (
            f"{result['entity']} had the highest improvement: "
            f"{result['old_value']:.1f}% → "
            f"{result['new_value']:.1f}% "
            f"(+{result['change']:.1f} percentage points)."
        )

    # Highest value
    elif "which country has the highest" in q:
        rows = rank_entities()

        excluded = {
            "World Average",
            "Developed countries",
            "Developing Countries",
        }

        country_rows = [
            row for row in rows
            if row["Countries/States"] not in excluded
        ]

        highest = country_rows[0]

        answer = (
            f"Highest value: "
            f"{highest['Countries/States']} "
            f"with {highest['new']:.1f}% in 2009–10."
        )

    # Ranking
    elif "rank" in q or "ranking" in q:
        answer = format_ranking()

    # Comparison
    elif "compare" in q and " and " in q:
        parts = q.split(" and ", 1)

        name1 = parts[0].replace("compare", "").strip(" ?.,!")
        name2 = parts[1].strip(" ?.,!")

        answer = format_comparison(name1, name2)

    # Normal entity question
    else:
        entity = extract_entity(question)
        results = get_change(entity)
        answer = format_entity_results(results)

    # Gemini explanation layer
    answer = improve_with_gemini(question, answer)

    print("\nAgent:")
    print(answer)
    print()