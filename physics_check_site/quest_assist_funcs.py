def get_quest_for_table():
    quests = []
    with open("./data/quests.csv", "r", encoding="utf-8") as f:
        num = 1
        for line in f.readlines()[1:]:
            quest, answer, source = line.split(";")
            quests.append([num, quest, answer])
            num += 1
    return quests


def add_quest(new_quest, new_answer):
    new_quest_line = f"{new_quest};{new_answer};user"
    with open("./data/quests.csv", "r", encoding="utf-8") as f:
        existing_quests = [l.strip("\n") for l in f.readlines()]
        title = existing_quests[0]
        old_quest = existing_quests[1:]
    quests_sorted = old_quest + [new_quest_line]
    initial_quests = [title] + quests_sorted
    with open("./data/quests.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(initial_quests))


def get_quests_stats():
    initial_quests = 0
    user_quests = 0
    answer_len = []
    with open("./data/quests.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            quest, answer, added_by = line.split(";")
            words = answer.split()
            answer_len.append(len(words))
            if "user" in added_by:
                user_quests += 1
            elif "initial" in added_by:
                initial_quests += 1
    stats = {
        "quests_all": initial_quests + user_quests,
        "quests_own": initial_quests,
        "quests_added": user_quests,
        "words_avg": round(sum(answer_len)/len(answer_len)),
        "words_max": max(answer_len),
        "words_min": min(answer_len)
    }
    return stats