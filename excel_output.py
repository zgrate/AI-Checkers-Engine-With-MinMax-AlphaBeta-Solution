import os


def output_folder(folder="output2"):
    with open("output2.csv", "w", encoding="utf-8") as output:
        output.write("levels;alpha_beta;method;trial;turns;outcome;real_time;date;time\n")
        for file in os.listdir(folder):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as input:
                lines = input.readlines()
                for i in range(0, len(lines), 2):
                    if lines[i].strip() == "":
                        break
                    if i >= len(lines) - 2:
                        break
                    # {i} {repeat_game} {datetime.now()} {start_time} {levels} {alpha_beta} {method}
                    first_line = lines[i].split(" ")
                    # f"END {datetime.now()} {time.time() - start_time} {game.turn} {game.get_game_status()}\n"
                    second_line = lines[i + 1].split(" ")
                    assert second_line[0] == "END"
                    output.write(f"{first_line[5].strip()};{1 if first_line[6].strip() == 'True' else 0};"
                                 f"{first_line[7].strip()};{first_line[0].strip()};"
                                 f"{second_line[4].strip()};{second_line[5].strip()};{second_line[3].strip()};"
                                 f"{first_line[2].strip()};{first_line[3].strip()}\n")


output_folder()
