import random

from discord_base_bots.base import BaseBot, run_bot


class DiceBot(BaseBot):

    bot_name = None
    hot_word = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_count = 150
        self.max_die_range = 1000

    async def roll(self, command_content, message):
        try:
            count, die_range = command_content.lower().split("d")
            count = int(count)
            die_range = int(die_range)
        except ValueError:
            await message.channel.send("Buddy, that's not how dice work.")
            return
        if die_range == 1:
            await message.channel.send("Learning to count on your own is an opportuinty for growth.")
            return
        elif count < 1 or die_range < 1:
            await message.channel.send("None. You get none. Don't be an ass.")
            return
        elif count > self.max_count or die_range > self.max_die_range:
            await message.channel.send(f"I can't do that yet. Current max is {self.max_count}d{self.max_die_range}."
                                       " Dynamic limits may come eventually.")
            return
        results = [random.randint(1, die_range) for x in range(count)]
        result_string = f"You rolled {sum(results)}. "
        if count < 100:
            result_string += f"({', '.join(str(r) for r in results)})"
        else:
            result_string += f"(Not showing individual rolls. {count} is too high.)"
        await message.channel.send(result_string)


if __name__ == "__main__":
    from pathlib import Path

    class RollBot(DiceBot):
        bot_name = "RollBot"
        hot_word = "rollbot"

    run_bot(DiceBot, Path(".env").resolve())
