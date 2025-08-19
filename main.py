import time
import re
from rich import box
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from rich.prompt import Prompt
from nltk.corpus import words
from rich.table import Table

word_list: list[str] = words.words()
word_count = len(word_list)

c = Console()

exact_match = False


def is_valid(word: str, pattern: re.Pattern[str]) -> str | None:
    if exact_match:
        matched = re.fullmatch(pattern, word)
    else:
        matched = re.match(pattern, word)
    return word if matched is not None else None


def run_match(pattern_s: str) -> list[str]:
    pattern = re.compile(pattern_s)
    with ThreadPoolExecutor() as pool:
        results = pool.map(is_valid, word_list, [pattern] * len(word_list))
    matches = list(filter(None, list(results)))
    return matches


def main():
    while True:
        inp = Prompt.ask("[green bold]Enter RegEx[/]")
        with c.status("iterating... over... the words... "):
            start = time.time()
            matches = run_match(inp)
            end = time.time()
            elapsed = end - start
            count = len(matches)
            per_word = elapsed / word_count
        matches_table = Table(
            box=box.SIMPLE,
        )
        matches_table.add_column(
            "#_",
            style="cyan dim",
            min_width=5,
            header_style="cyan bold",
            justify="right",
        )
        matches_table.add_column(
            "match",
            style="magenta",
            header_style="magenta bold",
            min_width=15,
            justify="center",
        )
        for i, match in enumerate(matches):
            matches_table.add_row(str(i + 1), match)
        c.print(matches_table, justify="center")
        c.print(
            f"found {count} words in {elapsed} sec. out of {word_count} words, {per_word} sec. per word"
        )


if __name__ == "__main__":
    main()
