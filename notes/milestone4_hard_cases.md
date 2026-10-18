# Milestone 4 — Hard cases and labelling log

## Workflow
1. **Cold set** (`cold20.csv`): 20 posts set aside before any AI labelling.
   I labelled **16** of them by hand (note `cold`), using only the README
   definitions and without seeing any AI labels. For the other 4 I asked the
   AI to choose, so they are marked as pre-labelled, not cold. Merged into
   `labels.csv` with `scripts/merge_cold.py`.
2. **Pre-labelled 256** (note `pre-labelled by AI`): an AI tool (Claude) was
   given the four definitions, the label order and the decision rules, and
   labelled candidate posts from `data/nba_pool.csv`. The AI then did a
   second consistency pass (every non-analysis post containing a number, and
   every analysis post without one, re-checked against the decision rule): no
   labels changed. My own review: I spot-checked 20 random rows (see the
   spot-check section below) and changed none of them; the other 236 I did
   not review individually.
3. **Skipped:** 40 candidates got no label and were left out of `labels.csv`:
   off-topic tangents (politics, Ballmer's wealth, other sports), personal
   stories ("I saw him in a bar in 2018"), bare questions, and bare facts
   with no claim attached ("9-8 is when things got crazy"). These have no home
   in the taxonomy, which is a finding in itself: r/nba threads drift off
   basketball a lot.
4. **Targeted collection:** `analysis` and `trash_talk` were thin in a random
   sample, so I pulled extra stat-citing posts (`collect_nba.py --stat`) and
   extra posts addressed to "you / fans / this sub" to keep every label at
   15% or more (criterion 3).

## Hard cases

**1. A stat with no argument**
> holy shit, he went 56-104 on threes in the 16-17 season

*Could have been:* `analysis` or `reaction`. *Chose:* `reaction`. It
contains a checkable number, but it isn't used *as support* for any claim;
it's surprise at a fact. The analysis rule needs a claim for the fact to
support.

**2. Made-up numbers as a joke**
> If brad tried to trade brown for edwards in offseason, he would've had to attach 69 first round picks and $420m in incentives

*Could have been:* `analysis` or `hot_take`. *Chose:* `hot_take`. The
numbers are deliberately fake, so they aren't checkable facts. Underneath the
joke is an unsupported claim (Edwards is worth far more than Brown).

**3. Long, reasoned, but nothing checkable**
> Gordon is bigger, more athletic, can shoot 3s, a better decision maker, and is more skilled than Sochan. He's also a way more impactful defender. ... He's just not a good player and I think he'll be out of the league soon.

*Could have been:* `analysis` or `hot_take`. *Chose:* `hot_take`. It reads
like analysis because it's long and gives reasons, but every reason is
itself an opinion. Length and effort are not the test; a checkable fact is.

**4. A reaction that turns into a prediction**
> Damn Collins just got ragebaited in preseason game 1 on a brand new team. Could easily be nothing but honestly that just does not bode well for his season/future in the league.

*Could have been:* `reaction` or `hot_take`. *Chose:* `hot_take`. It starts
as a reaction to one clip, but the second sentence makes a claim about his
whole season, and the label order puts `hot_take` ahead of `reaction`.

**5. A number that's context, not support**
> Don't know why some people said he couldn't move well. He moves incredibly well for a 7'2" C.

*Could have been:* `analysis` or `hot_take`. *Chose:* `hot_take`. 7'2" is
checkable, but it sets the bar ("for a 7-footer"); it isn't evidence that
he moves well.

**6. Insult aimed at a player, not a user**
> Rollins is a bitch, charge him when hes looking at you. but he wont. what a pussy

*Could have been:* `trash_talk` or `reaction`. *Chose:* `reaction`. It's
aimed at a player in a clip, not at another user or fanbase (second decision
rule).

## Spot-check of the AI pre-labels

I reviewed a random sample of 20 AI pre-labelled rows (5 per label) and
picked my own label for each before moving on. Results are in
`notes/milestone4_spot_check.csv`.

- **I agreed with the AI on 3 of 20 (15%).** That's below the 25% you'd get
  by guessing at random with four labels.
- I chose to **record** my picks rather than overwrite the training labels.
  Several of my picks contradicted my own written rules (for example, I
  called a post with no fact in it `analysis`, and a stat-backed argument
  `reaction`), so I kept the labels that follow the README definitions.
- **What this means:** my own labelling, both here and in the cold set, is
  not yet applying my definitions consistently. Next unit's agreement report
  (criterion 4) is where this will show up, and it's the first thing to check
  if the model misses its targets.
