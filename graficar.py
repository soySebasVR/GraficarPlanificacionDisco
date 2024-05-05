import argparse
from typing import TypedDict

import matplotlib.pyplot as plt


class Args(TypedDict):
    integers: list[int]
    algorithm: str


def main(args: Args):
    original_list = [*args["integers"]]
    ordered_list: list[int] = [args["integers"].pop(0)]
    if args["algorithm"] == "fcfs":
        ordered_list.extend(args["integers"])
    elif args["algorithm"] == "sstf":
        for i in range(len(args["integers"])):
            current = ordered_list[-1]
            next = min(
                args["integers"],
                key=lambda x: abs(x - current),
            )
            ordered_list.append(next)
            args["integers"].remove(next)
    elif args["algorithm"] == "scan":
        first_pass = True
        for i in range(len(args["integers"])):
            current = ordered_list[-1]
            posible_number = 0 if first_pass else 200
            for number in args["integers"]:
                if first_pass and number < current and number >= posible_number:
                    posible_number = number
                elif not first_pass and number > current and number < posible_number:
                    posible_number = number
            next = posible_number
            if next == 0:
                first_pass = False
            try:
                args["integers"].remove(next)
            except ValueError:
                pass
            ordered_list.append(next)
    elif args["algorithm"] == "cscan":
        min_list = []
        max_list = []
        for number in args["integers"]:
            if number < ordered_list[-1]:
                min_list.append(number)
            else:
                max_list.append(number)
        min_list.sort()
        max_list.sort()
        ordered_list.extend(max_list)
        if not 200 in ordered_list:
            ordered_list.append(200)
        if not 0 in min_list:
            ordered_list.append(0)
        ordered_list.extend(min_list)
    elif args["algorithm"] == "look":
        in_list_200 = True if 200 in args["integers"] else False
        in_list_0 = True if 0 in args["integers"] else False
        first_pass = True
        for i in range(len(args["integers"])):
            current = ordered_list[-1]
            posible_number = 0 if first_pass else 200
            for number in args["integers"]:
                if first_pass and number < current and number >= posible_number:
                    posible_number = number
                elif not first_pass and number > current and number < posible_number:
                    posible_number = number
            next = posible_number
            if next == 0:
                first_pass = False
            try:
                args["integers"].remove(next)
            except ValueError:
                pass
            ordered_list.append(next)
        if not in_list_200 and 200 in ordered_list:
            ordered_list.remove(200)
        if not in_list_0 and 0 in ordered_list:
            ordered_list.remove(0)
    elif args["algorithm"] == "clook":
        min_list = []
        max_list = []
        for number in args["integers"]:
            if number < ordered_list[-1]:
                min_list.append(number)
            else:
                max_list.append(number)
        min_list.sort()
        max_list.sort()
        ordered_list.extend(max_list)
        ordered_list.extend(min_list)

    print(ordered_list)

    time_taken = 0
    for i in range(len(ordered_list) - 1):
        time_taken += abs(ordered_list[i] - ordered_list[i + 1])

    ordered_list.reverse()

    # Graficador con Matplotlib y guardado en local
    fig, ax = plt.subplots()
    ax.set_title("Algoritmo: " + args["algorithm"] + "; Cola: " + str(original_list))
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xlabel("Tiempo total: " + str(time_taken))
    ax.plot(ordered_list, range(len(ordered_list)))
    ax.set_yticks([])
    ax.set_xticks(ordered_list)
    ax.set_xticklabels(ordered_list)
    plt.savefig("planificacion.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="GraficarPlanificacionDiscos",
        description="What the program does",
    )
    parser.add_argument("integers", metavar="N", type=int, nargs="+")
    parser.add_argument(
        "--algorithm",
        help="algorithm to use",
        choices=["fcfs", "sstf", "scan", "cscan", "look", "clook"],
    )
    args = parser.parse_args()

    main(vars(args))  # type: ignore
