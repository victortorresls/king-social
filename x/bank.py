"""Banco de posts educativos/marca para o X, 1 por dia, seguindo a tabela semanal.
Gera x/posts.json: {"YYYY-MM-DD": {"type": ..., "posts": [tweet, (tweet2, ...)]}}
Cada item de "posts" é um tweet; mais de um = thread.
"""
import json, datetime

H = "\n\n#football #soccerstats"

BY_TYPE = {
 # Segunda: estatística do dia
 0: [
  ["Goals scored only tell part of a team's story.\n\nFrequency, attacking volume and context explain how those goals happened, and whether they're likely to repeat." + H],
  ["A team averaging 2.5 goals per game can still go three matches without scoring more than one.\n\nAverages hide distribution. Always look at how often, not just how much." + H],
  ["Home and away are two different teams in the data.\n\nMany sides change pace, shape and output completely on the road. Splitting the numbers matters." + H],
  ["The first 15 minutes are statistically different from the rest of the first half.\n\nTempo, pressing and risk-taking change as teams settle. Period-specific data beats full-match averages." + H],
 ],
 # Terça: análise pré-jogo (modelo)
 1: [
  ["Before analyzing any match:\n\n1. Home team's form at home\n2. Away team's form away\n3. Sample size of each\n4. What changed recently\n\nThe overall average rarely tells the whole story." + H],
  ["Pre-match checklist:\n\n• Last 10, not last 3\n• Home/away split\n• Goals for AND against\n• Schedule congestion\n\nContext first, conclusions later." + H],
  ["A strong attack vs a weak defense looks obvious on paper.\n\nBut check the opponents those numbers came from. Stats built against bottom teams don't transfer automatically." + H],
  ["When two teams' numbers point in opposite directions, that's information too.\n\nNot every match has a clear statistical edge. Knowing when to pass is part of the analysis." + H],
  ["Pre-match tip: compare each team's numbers with the league average.\n\nA team with 1.8 goals per game means more in a league that averages 2.2 than in one that averages 3.0." + H],
 ],
 # Quarta: debate / enquete
 2: [
  ["You're analyzing a match. Where do you start?\n\nA) Recent form\nB) Goal averages\nC) Event frequency\nD) Home/away split\n\nReply with your letter. The analysis starts with the right question." + H],
  ["A team won 5 in a row. Are they in great form?\n\nDepends on how they won, who they played and what the underlying numbers say.\n\nWhat do you look at first?" + H],
  ["Which matters more for first-half goals?\n\nA) Attacking team's early tempo\nB) Defending team's early errors\n\nReply A or B and tell us why." + H],
  ["Unpopular opinion: a 1-0 win can be a worse performance than a 2-2 draw.\n\nResult and performance are not the same thing. Agree or disagree?" + H],
  ["How many matches do you need before trusting a stat?\n\nA) 5\nB) 10\nC) 20+\nD) Depends on the stat\n\nReply below." + H],
 ],
 # Quinta: gráfico / comparação (thread educativa)
 3: [
  ["1/3 An 80% stat means an event happened in 8 out of 10 observations.",
   "2/3 It doesn't mean an 80% chance next time. The sample can be small and the context can change.",
   "3/3 Good analysis weighs frequency, context, sample size and uncertainty together. Data without interpretation can mislead." + H],
  ["Frequency vs probability:\n\nFrequency = what happened in a sample.\nProbability = an estimate of what may happen.\n\nMixing them up breaks any analysis." + H],
  ["1/3 Variance is why good analysis can have bad weeks.",
   "2/3 Even a solid edge produces losing streaks over short samples. That's math, not failure.",
   "3/3 Judge a method over hundreds of events, never over a weekend." + H],
  ["Mean vs median in football data:\n\nOne 6-0 thrashing can inflate a team's goal average for weeks. The median often tells a more honest story." + H],
  ["Consistency beats peaks.\n\nA team that hits a number in 7 of 10 games is often more readable than one that hits it 10 of 20 with huge swings." + H],
 ],
 # Sexta: eSoccer
 4: [
  ["Virtual football generates data too.\n\nBut the analysis has to respect the competition format, the history available and how each environment behaves." + H + " #esoccer"],
  ["In eSoccer, match length changes everything.\n\nAn 8-minute league and a 12-minute league produce completely different goal patterns. Never mix them in one average." + H + " #esoccer"],
  ["eSoccer samples grow fast: dozens of matches per day.\n\nThat's an advantage for analysis, as long as you track player-level data, not just team names." + H + " #esoccer"],
  ["eSoccer tip: the player matters more than the team badge.\n\nSame club, different player, different numbers. Analyze who's on the controller." + H + " #esoccer"],
 ],
 # Sábado: dia de jogos
 5: [
  ["Matchday reminder:\n\nThe numbers don't predict football. They describe scenarios. Use them to understand the game, not to expect certainty." + H],
  ["Big matchday. Before you watch, check:\n\n• First-half tempo of both teams\n• Goals for and against at this venue\n• Sample size\n\nWatch the game with the numbers in mind." + H],
  ["Live football and stats tell different stories in real time.\n\nA 0-0 at halftime can hide a match with huge attacking volume. Look beyond the score." + H],
  ["Saturday rule: no stat is a guarantee.\n\nUse data to filter, compare and understand. Football keeps its uncertainty, and that's why it's worth analyzing." + H],
 ],
 # Domingo: aprendizado da semana / marca
 6: [
  ["Since 2019, THE KING STATS has worked with football statistics.\n\nThe vision hasn't changed: read the numbers, understand the patterns, analyze opportunities with method.\n\nthekingstats.com"],
  ["Lesson of the week: track everything.\n\nWithout a record, you can't tell skill from luck. Every selection we make is logged and resolved publicly, green, red or void.\n\nthekingstats.com"],
  ["Our approach in one line:\n\nRaw data free for everyone. Method applied automatically. Results tracked in the open.\n\nFootball, data and technology. thekingstats.com"],
  ["Lesson of the week: a bad day doesn't break a method, and a great day doesn't prove one.\n\nOnly volume and time do. That's why we look at the month, not the match.\n\nthekingstats.com"],
 ],
}

def build(start, days):
    used = {k: 0 for k in BY_TYPE}
    names = ["stat", "pregame", "debate", "education", "esoccer", "matchday", "brand"]
    out = {}
    d = start
    for _ in range(days):
        wd = d.weekday()
        pool = BY_TYPE[wd]
        out[d.isoformat()] = {"type": names[wd], "posts": pool[used[wd] % len(pool)]}
        used[wd] += 1
        d += datetime.timedelta(days=1)
    return out

if __name__ == "__main__":
    data = build(datetime.date(2026, 10, 14), 30)
    for k, v in data.items():
        for t in v["posts"]:
            assert len(t) <= 280, (k, len(t), t)
    json.dump(data, open("x/posts.json", "w"), indent=1, ensure_ascii=False)
    print(len(data), "days")
