#!/usr/bin/env python3.9

"""Starts the heap runtime test CLI app.

Example:
    $ python3 start.py

Attributes:
    FILE_NAME_FILTER (Pattern[str]): Regular expression to filter out invalid
        characters from a filename.
    DATA_DIR (Path): The path to the data directory.
    CONFIG_DIR (Path): The path to the config directory.
    DEFAULT_OPTIONS (dict[str, (str or int)]): Default config for the gen
        module.
"""

from pathlib import Path
import re
import gen
import run

FILE_NAME_FILTER = re.compile("[^a-z0-9_\-]")
DATA_DIR = Path(__file__).parent.parent.absolute() / "data"
CONFIG_DIR = Path(__file__).parent.parent.absolute() / "config"
DEFAULT_OPTIONS = {
    "type": "none",
    "name": "default",
    "vertices": 100000,
    "edges": 1000000,
    "size": 0,
    "op": 1000000,
    "addfreq": 1,
    "decfreq": 1,
    "popfreq": 1,
    "minweight": 0,
    "maxweight": int(1e9),
    "minval": int(-1e9),
    "maxval": int(1e9),
}


def main():
    """Starts the heap tester."""

    print(
        "\n==================\n"
        "=  Heap-o-Matic  =\n"
        "=                =\n"
        "=  by charlotte  =\n"
        "=================="
    )
    display_help()
    try:
        while True:
            args = input_command()
            if args[0] == "gen":
                gen_command(args)
            elif args[0] == "run":
                run_command(args)
            elif args[0] == "help":
                display_help(args)
            else:
                print("Invalid command. Type 'help' to display all commands.")
    except ExitException:
        print("bye ^.^")


# Commands


def gen_command(args: tuple[str]) -> None:
    """Command to generate test data.

    Args:
        args (tuple[str]): The config filename.

        ("gen", filename)
    """

    if len(args) < 2:
        print("Invalid option. Type 'help gen' for usage")
        return
    config = CONFIG_DIR / args[1]
    if not config.is_file():
        print(f"File not found: {config}")
        return
    options = read_config(config)
    test_data = DATA_DIR / options["name"]
    print("generating...")
    if options["type"] == "heap":
        t, a, d, p, miv, mav = gen.random_test(
            test_data=test_data,
            size=options["size"],
            op=options["op"],
            addfreq=options["addfreq"],
            decfreq=options["decfreq"],
            popfreq=options["popfreq"],
            minval=options["minval"],
            maxval=options["maxval"],
        )
        display_test_data(options["name"], t, a, d, p, miv, mav)
    elif options["type"] == "graph":
        vertices, edges = gen.random_graph(
            test_data=test_data,
            vertices=options["vertices"],
            edges=options["edges"],
            minweight=options["minweight"],
            maxweight=options["maxweight"],
        )
        display_graph_data(options["name"], vertices, edges, options["minweight"])
    else:
        print("Unable to read config file: invalid type argument")


def run_command(args: tuple[str]) -> None:
    """Command to run tests.

    Args:
        args (tuple[str]): The heap to use and test data filename.
            data/default used if no filename specified.

        ("run", "ph" or "fh" or "bh" or "pd" or "fd" or "bd" or "nd")
    """

    if len(args) < 3:
        print("Invalid options. Type 'help run' for usage")
        return
    data = DATA_DIR / args[2]
    if not data.is_file():
        print("Test data not found. Use the gen command if you haven't already.")
        return
    try:
        if args[1] == "ph":
            print("running...")
            time = run.pairing_time(data)
            print(f"\nPairing heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "fh":
            print("running...")
            time = run.fibonacci_time(data)
            print(f"\nFibonacci heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "bh":
            print("running...")
            time = run.binary_time(data)
            print(f"\nBinary heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "nh":
            print("running...")
            time = run.noheap_time(data)
            print(f"\nHeapless runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "pd":
            print("running...")
            time = run.dijkstra_pairing_time(data)
            print(f"\nPairing heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "fd":
            print("running...")
            time = run.dijkstra_fibonacci_time(data)
            print(f"\nFibonacci heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "bd":
            print("running...")
            time = run.dijkstra_binary_time(data)
            print(f"\nBinary heap runtime on {args[2]}: {time:.5} s\n")
        elif args[1] == "nd":
            print("running...")
            time = run.dijkstra_noheap_time(data)
            print(f"\nHeapless runtime on {args[2]}: {time:.5} s\n")
        else:
            print("Invalid option. Type 'help run' for usage.")
    except Exception as e:
        print(f"Error running test: {e}")


# I/O


def display_help(args: tuple[str] = ("help",)) -> None:
    """Prints the available commands and their usage.

    Args:
        args (tuple[str], optional): The command to display help for. Defaults to ("help",).

        ("help", optional(command: str))
    """

    if len(args) <= 1:
        print(
            "\nCommands\n"
            "  gen   Generate test data\n"
            "  run   Run a test\n"
            "  help  Display this help message\n"
            "  exit  Stop this app\n"
            "Type 'help <command>' to show more details.\n"
        )
    elif args[1] == "gen":
        print(
            "\nGenerate test data\n"
            "  usage: gen [config]\n"
            "  Where [config] is the name of the config file,\n"
            "  located in the config/ directory.\n"
        )
    elif args[1] == "run":
        print(
            "\nMeasure runtime\n"
            "  usage: run <test> <data>\n"
            "  Where <test> is one of the following:\n"
            "    Heap Operation Tests\n"
            "      ph -> pairing heap\n"
            "      fh -> Fibonacci heap\n"
            "      bh -> binary heap\n"
            "      nh -> do not use a heap\n"
            "    Dijkstra Graph Tests (single source shortest path on a graph)\n"
            "      pd -> use a pairing heap\n"
            "      fd -> use a Fibonacci heap\n"
            "      bd -> use a binary heap\n"
            "      nd -> do not use a heap\n"
            "  And <data> is the name of the test data file,\n"
            "  located in the data/ directory. Be sure to use the correct\n"
            "  data for a test.\n"
        )
    elif args.count("help") > 2:
        print("same qq")
    elif args[1] == "help":
        print(
            "\nDisplay command information\n"
            "  usage: help [command]\n"
            "  Where [command] is the command to get help for.\n"
            "  Omit [command] to display all commands.\n"
        )
    elif args[1] == "exit":
        print("\nExit this application\n  usage: exit\n")
    else:
        print("Unrecognized command. Type 'help' to show all commands.")


def display_graph_data(name: str, vertices: int, edges: int, minweight: int) -> None:
    """Prints a formatted graph composition message.

    Args:
        name (str): The name of the graph
        vertices (int): The number of vertices.
        edges (int): The number of edges.
        minweight (int): The minimum weight in the graph.
    """

    avg_deg = 2 * edges / vertices
    percent_complete = 2 * edges / (vertices * (vertices - 1))
    neg_weights = "yes" if minweight < 0 else "no"
    acyclic = "yes" if edges < vertices else "no"
    print(
        "\n-----Graph Composition-----\n"
        f"name           {name}\n"
        f"vertices       {vertices:,}\n"
        f"average degree {avg_deg:,.6}\n"
        f"completeness   {percent_complete:.3%}\n"
        f"edges          {edges:,}\n"
        f"neg weights?   {neg_weights}\n"
        f"acyclic?       {acyclic}\n"
        f"---------------------------\n"
    )


def display_test_data(
    name: str, total: int, add: int, dec: int, pop: int, minval: int, maxval: int
) -> None:
    """Prints a formatted test composition message.

    Args:
        name (str): The name of the test.
        total (int): The total number of operations.
        add (int): The number of add operations.
        dec (int): The number of decrease key operations.
        pop (int): The number of pop minimum operations.
        minval (int): The minimum possible value in the heap.
        maxval (int): The maximum possible value in the heap.
    """

    print(
        "\n-----Test  Composition-----\n"
        f"name       {name}\n"
        f"operations {total:,}\n"
        f"add        {add / total:.6%}\n"
        f"decrease   {dec / total:.6%}\n"
        f"pop min    {pop / total:.6%}\n"
        f"min value  {minval:,}\n"
        f"max value  {maxval:,}\n"
        f"---------------------------\n"
    )


def input_command() -> tuple[str]:
    """Takes input for a command.

    Returns:
        tuple[str]: The command and arguments passed.

    Raises:
        ExitException: If the command is "exit"
    """

    print("> ", end="")
    args = input().lower().split()
    if args[0] == "exit":
        raise ExitException()
    return args


def read_config(file: Path) -> dict[str, any]:
    """Reads a config file.

    Args:
        file (Path): The config file.

    Returns:
        dict[str, int]: Options and their values. Default values are
            used if the options wasn't read.
    """

    options = DEFAULT_OPTIONS.copy()
    options["name"] = file.name
    with file.open(mode="r") as config:
        for line in config:
            params = line.lower().split()
            if len(params) >= 2:
                if params[0] == "name":
                    options[params[0]] = params[1]
                elif params[0] == "type":
                    options[params[0]] = params[1]
                elif params[0] in options:
                    try:
                        options[params[0]] = int(params[1])
                    except ValueError:
                        pass
    options["name"] = FILE_NAME_FILTER.sub("", options["name"])
    return options


# Exceptions


class ExitException(Exception):
    """When the user wants to exit the application."""

    pass


if __name__ == "__main__":
    main()
