# Splinterlands Assistant

## Motivations

When the crypto games appeared, it seemed to be a nice way of earning small amounts of money while playing games. Obviously you would not earn a living out of it, but still, why not give it a try.

Splinterlands is a card game where your actions are limited. You pick on character at the beginning of the game, then you spend your capital on cards that are going to be played automatically. Then the game unfolds, and you win or lose.

The specificity of those crypto games is that they are connected to a blockchain, either only for the currency, or as it is for Splinterlands, also to save any action in the game.

So reading the blockchain would show you battles played in the past, cards played by both players during the battle, result of the battle and so on.

I then thought to myself: "But is my goal to play the game or to earn money?". This is where I started writing this little assistant so I would not have to play to earn money.

Keep in mind that it is something that I wrote for myself. The code might be a bit unstable but it allowed me to have a very good win rate anyway ;).

## How does it work

This program is a command line based tool that you use at the beginning of a battle.

It does not play by itself.

It performs the following actions:
- fetches previous played games to configure itself
- asks what is the mana capital that you're allowed to spend before the game
- displays what cards you should by to maximise the probability of winning.

Because it is only possible to fetch games played by a specific player, the tool fetches your game, and fetches games played by the opponents you faced to generate a database big enough to be interesting.

## Usage

To make it work, just run the ```main.py``` file.

```
python main.py
```

The best thing to do is first to play a game on your own, so the program will be able to fetch the history from your own profile. See **Limitations** for more information about it.

## Requirements

It works on Python3.9 and it should work on most python versions.

The necessary modules are saved in ```requirements.txt```.

## Improvements

I do not plan on working more on this code. However, I'll happily review any change anyone would want to add to it. Do not hesitate to create a PR!

## Limitations

There are two main limitations:

### API limitation

The API only allows someone to look so far in the past. If you have not played a game in a while, calling the API with your username won't return anything. The best thing to do would then be to check the leaderboard and pick a player that plays often.

Obviously, you could also play a game just so the code can access you history.

### Code limitation

When a player gets better, it may unlock cards that are not available to you. The system won't take that into account so you might have some recommendation that are outside what you can do. If it happens, please pick a card that costs the same and you should be fine.

## Licence

Do as you please!

