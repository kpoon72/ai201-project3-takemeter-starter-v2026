# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments from **r/nba**, Reddit's main NBA discussion
community, into four kinds of post: **`analysis`** (a basketball claim backed
by a checkable fact), **`hot_take`** (a confident claim with no support),
**`reaction`** (a response to one play, clip or piece of news) and
**`trash_talk`** (aimed at another user, fanbase or the sub, not at
basketball). The point is to separate the comments worth reading for an
argument from the noise around them. It's a DistilBERT model fine-tuned on
276 r/nba comments I collected and labelled.

**Stretch feature:** a fourth label, `trash_talk`. In my first 40 posts, about
1 in 8 were people sniping at each other, and analysis / hot_take / reaction
had no home for them.

---

## Label Taxonomy

Four labels. Every post gets exactly one. When a post seems to fit two, check
them in this order and stop at the first that applies: **analysis → hot_take
→ reaction → trash_talk**.

### `analysis`

**Definition:** Makes a basketball claim and supports it with at least one
specific, checkable fact: a stat, record, date, contract figure, award, or a
named game or event.

**Example 1:**
> That is honestly the biggest problem with Maravich: he never hesitated to take a shot from anywhere on the court if he felt like it. The all-time record for attempts in a season (1168) is held by Pete Maravich, set his senior year. Second in attempts (1022) is Pete Maravich, during his junior year. Third in attempts (976) is Pete Maravich, during his sophomore year. Fourth is Bill Mikvy with 964. Pete took more than half of his team's shots in college.

**Example 2:**
> Pretty good indeed. 50.4 points and 25.7 rebounds a night in 1961-62, and he never fouled out of a single game in his whole career.

### `hot_take`

**Definition:** A confident basketball opinion, ranking or prediction that
reaches beyond a single moment and offers no checkable fact in support.

**Example 1:**
> Look for the Knicks to make a move for a more viable backup 5. I predict Deuce won't make it past the trade deadline

**Example 2:**
> Obviously Knicks are the top but after them I think the Celtics weirdly will be the second best team

### `reaction`

**Definition:** An immediate response to one specific play, clip or piece of
news (a feeling, joke or exclamation) that makes no claim beyond that moment.

**Example 1:**
> insane. ive actually never seen someone get hit in the face like that and not even move

**Example 2:**
> Hand on the throat is a bit much for 5mins in preseason basketball

### `trash_talk`

**Definition:** Aimed at another user, a fanbase or the subreddit rather than
at basketball, such as an insult, mockery or banter, with no basketball claim
of its own.

**Example 1:**
> Damn you Wolves fans can't let it go huh. Lol

**Example 2:**
> Maybe stop being obtuse and contrarian. I'm out on a walk to happy hour right now. Hard to tell people to stop making dumb comments on Reddit when you're busy making dumb comments on Reddit

### The hardest boundary

**Which two labels:** `analysis` vs `hot_take`.

**The post that sits between them:**
> Knecht scored 30 against the tanking jazz 2 years ago then never got better. He got plenty of opportunities and would forget offensive plays and miss defensive assignments. Bronny literally had productive playoff minutes last year. JJ is a good coach you think he doesn't want to play the movement shooter guy off screens? The guy is just bad

**The decision rule I used every time:** If the post offers at least one
specific, checkable fact *as support for its claim*, it's `analysis`, even if
the tone is heated, the conclusion is extreme, or the reasoning is weak. Vague
appeals ("he's been bad all year", "ask anyone who watched", "everyone knows")
are not checkable facts. A fact the post concedes or waves away ("30/12 means
nothing") is not support either. Under this rule, the Knecht post is
`analysis`: "scored 30 against the tanking Jazz" and "productive playoff
minutes last year" are checkable, and both are used to argue the conclusion.

**Second rule (reaction vs trash_talk):** Ask who the post is aimed at. A
player, play or piece of news makes it `reaction`, even when the language is
insulting ("this makes Stew look like a huge bitch"). Another user, a fanbase
or the sub makes it `trash_talk`. A post that insults a user *and* makes a
basketball claim is labelled by the claim (`analysis` or `hot_take`), which
is what the label order above enforces.

---

## The Dataset

**Where the posts came from:** public r/nba comments posted between
2026-09-01 and 2026-10-16 (offseason and preseason), pulled from the Arctic
Shift public Reddit archive with `scripts/collect_nba.py`, because Reddit's
own JSON endpoint blocked automated requests (403). Filters: 40–1200
characters, comment score ≥ 2, no links, no AutoModerator or deleted posts.
That gave a pool of 958 posts (`data/nba_pool.csv`). `analysis` and
`trash_talk` were thin in a random sample, so I added two targeted pulls: a
second pass of posts that cite a number (`--stat`), and posts addressed to
"you / fans / this sub". 40 candidates were skipped because they fit no label
(off-topic politics or other sports, personal stories, bare questions).

**How I labelled them:**
- **Cold set:** 20 posts set aside before any AI labelling. I labelled **16**
  of them by hand from the definitions alone (note `cold`). For the other 4 I
  asked the AI to choose, so they are marked pre-labelled, not cold.
- **Pre-labelled:** the other 256 rows were pre-labelled by an AI (Claude)
  given my definitions, label order and decision rules (note `pre-labelled
  by AI`). The AI then did a second consistency pass (every non-analysis post
  containing a number, and every analysis post without one), which changed
  nothing.
- **My review:** I spot-checked 20 random pre-labelled rows (5 per label) and
  agreed with the AI on **3 of 20**. Several of my picks contradicted my own
  written rules, so I recorded them in `notes/milestone4_spot_check.csv`
  instead of overwriting the training labels. The other 236 rows I did not
  review individually. Full log: `notes/milestone4_hard_cases.md`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| analysis | 93 | 33.7% |
| hot_take | 80 | 29.0% |
| reaction | 54 | 19.6% |
| trash_talk | 49 | 17.8% |
| **Total** | 276 | 100% |

**Three hard cases**

**1.**
> *The post:* "holy shit, he went 56-104 on threes in the 16-17 season"
>
> *Could have been:* `analysis` or `reaction`
>
> *I chose, because:* `reaction`. It has a checkable number, but the number
> isn't used to support any claim; it's surprise at a fact. My analysis rule
> needs a claim for the fact to support.

**2.**
> *The post:* "Gordon is bigger, more athletic, can shoot 3s, a better decision maker, and is more skilled than Sochan. He's also a way more impactful defender. ... He's just not a good player and I think he'll be out of the league soon."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. It's long and gives reasons, so it reads
> like analysis, but every reason is itself an opinion. Effort isn't the test;
> a checkable fact is.

**3.**
> *The post:* "Damn Collins just got ragebaited in preseason game 1 on a brand new team. Could easily be nothing but honestly that just does not bode well for his season/future in the league."
>
> *Could have been:* `reaction` or `hot_take`
>
> *I chose, because:* `hot_take`. It starts as a reaction to one clip, but the
> second sentence makes a claim about his whole season, and my label order
> puts `hot_take` ahead of `reaction`.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on **`mps` (Apple Silicon GPU)**, torch 2.14.1, as
recorded in `results.json`.

**Anything I changed from the defaults, and why:** nothing. The only notebook
edits were my name and the label list (four labels instead of the example
three).

**Split sizes:** train 192 · val 42 · test 42 (stratified 70/15/15).

| Label | Train | Val | Test |
|---|---|---|---|
| analysis | 65 | 14 | 14 |
| hot_take | 56 | 12 | 12 |
| reaction | 38 | 8 | 8 |
| trash_talk | 33 | 8 | 8 |

`reaction` and `trash_talk` have exactly 8 posts each in test, right at the
edge where one wrong prediction moves a label's F1 a lot. Expect those two
to be the jumpiest across seeds next unit.

---

## How I Used AI

I used Claude (in Claude Code) throughout this unit.

**Moment 1: stress-testing the labels**

- *What I asked for:* eight posts that sit on the boundaries between my four
  labels, to classify using only my definitions.
- *What came back:* eight posts. Five were clean; three weren't: a stat the
  poster waves away ("30/12 means nothing"), a reaction that ends in a
  prediction, and an insult to a user that also cites a stat.
- *What I changed:* three rule changes, all now in the taxonomy: a fact must be
  used *as support*; a label order (analysis → hot_take → reaction →
  trash_talk); and a basketball claim beats an insult. Log:
  `notes/milestone2_stress_test.md`.

**Moment 2: drafting the acceptance criteria**

- *What I asked for:* after checking with course staff that it was allowed,
  I had Claude draft the five criteria, using the metrics the notebook
  actually records.
- *What came back:* five criteria, one per area (accuracy 0.60, per-label F1
  0.45, balance 15–40%, staff agreement 22/30, confidence gap 0.20), each
  with a reason tied to my data.
- *What I changed:* I kept the numbers. The balance criterion changed my
  collection plan: `analysis` was too rare in a random sample, so I pulled
  extra stat-citing posts to reach 15%.

**Other AI use:** Claude wrote the collection script, picked the README
example posts, drafted the definitions and this README, and ran the
notebook.

**Pre-labelling disclosure:** 260 of 276 rows were labelled by AI (256
pre-labelled, plus 4 cold-set posts I asked it to choose). 16 rows are my own
cold labels. I spot-checked 20 AI rows, agreed with 3, and kept the AI
labels because my picks didn't follow my written rules. I did not review the
remaining 236 individually. Each row's `note` column says which group it is
in.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both scored on the same 42 held-out posts in `test_split.csv`. Baseline:
`facebook/bart-large-mnli` zero-shot, given my four definitions from
`label_definitions.txt`. Trained: the unit 5 run (seed 42, `mps`).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.357 | 0.500 | +0.143 |
| Macro F1 | 0.199 | 0.371 | +0.171 |
| F1 — `analysis` | 0.531 | 0.683 | +0.152 |
| F1 — `hot_take` | 0.267 | 0.400 | +0.133 |
| F1 — `reaction` | 0.000 | 0.000 | +0.000 |
| F1 — `trash_talk` | 0.000 | 0.400 | +0.400 |

**What my definitions were worth:** the same baseline with bare label names
instead of definitions (`baseline_results_bare_names.json`) scored accuracy
**0.310** and macro F1 **0.184**, versus 0.357 / 0.199 with definitions. So
the definitions bought about 5 points of accuracy. They also changed *what*
it got right: with bare names it never predicted `analysis` correctly
(F1 0.000) and leaned on `hot_take` (0.537). With definitions, `analysis`
became its best label (0.531). The baseline reported above is the run with
definitions.

The baseline took a few seconds per post; the trained model scores all 42 in
about a second.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
Written before running the baseline: the trained model will beat the
baseline on overall accuracy, mostly on `analysis`, because it learned what
"a checkable fact used as support" looks like in r/nba posts.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
The prediction was right in direction: the trained model beat the
baseline on accuracy (+0.14) and on `analysis` (+0.15). But `analysis` was
not where it gained most. The biggest gain was `trash_talk` (0.000 → 0.400):
a general model reading "aimed at another user… rather than at basketball"
never picked it, while the fine-tuned model learned r/nba's surface signs of
it ("you", "y'all", "this sub"). Neither model got a single `reaction` right,
so fine-tuning added nothing there. That points at the label, not the
training method. All of this is one split of 42 posts, so a 0.14 gap is
about 6 posts.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
