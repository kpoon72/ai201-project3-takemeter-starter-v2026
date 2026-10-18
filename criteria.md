# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.60 on the held-out test split

Measured as `accuracy` in `results.json`, and it must hold on all three seeds
next unit.

**Why this target:** With four labels, random guessing scores about 0.25, and
always guessing my biggest label scores roughly its share of the file
(capped at 0.40 by criterion 3). 0.60 is clearly above both, so a model that
reaches it has learned something real. It's not higher because my hardest
boundary (`analysis` vs `hot_take`) depends on whether a fact is used *as
support*, which is a judgment a small model may only partly pick up from 140
training posts.

---

## 2. Every label has an F1 of at least 0.45 on the held-out test split

Measured as the per-label `f1` for each of `analysis`, `hot_take`, `reaction`
and `trash_talk` in `results.json`. All four must clear it, on all three seeds.

**Why this target:** This stops one strong label from hiding a label the
model never learned. It's lower than criterion 1 because the test split is
only about 30 posts, roughly 7–8 per label, so a single wrong post moves a
label's F1 by more than 0.10. I expect `hot_take` to be the weakest, since it
borders both `analysis` (did they offer support?) and `reaction` (does the
claim reach past the moment?). 0.45 is roughly twice what guessing would get
on one label.

---

## 3. No label is more than 40% or less than 15% of `labels.csv`

Measured by counting the `label` column of `labels.csv` (the notebook's check
cell prints the shares).

**Why this target:** The course cap of 70% means nothing with four labels: a
file could be 70% `hot_take` and leave about 10% for each of the others,
which is about 3 test posts per label. At 15% of 200 rows, the thinnest label
still has about 30 examples, enough for roughly 20 training and 4–5 test
posts. I expect `analysis` to be the thinnest, since most r/nba comments
don't cite a number; in my 40-post reading sample only about 4 did. So I'll
probably have to collect extra stat-backed posts to hit this.

---

## 4. My labels agree with the staff labels on at least 22 of the 30 staff posts (73%)

Measured by `agreement.py` next unit, labelling `data/staff_posts.csv` under
the staff taxonomy in `data/staff_taxonomy.md`.

**Why this target:** This is the only check on whether *I* label
consistently, separate from whether the model learns. The staff taxonomy has
three labels close to mine (minus `trash_talk`), so I should be applying
similar judgments. 22/30 leaves room for 8 disagreements, because the course
says several of those posts were chosen to be genuinely ambiguous, and the
analysis-vs-opinion line is where I already had to tighten my own rules
three times in the stress test.

---

## 5. On the most confident third of test posts, accuracy is at least 0.20 higher than on the least confident third

Measured as `accuracy_most_confident_third` minus
`accuracy_least_confident_third` in `results.json`, on all three seeds.

**Why this target:** If confidence doesn't separate right from wrong, the
model's scores can't be used to decide which predictions to trust, for
example to send unsure posts to a human. I expect the unsure posts to be
exactly the `analysis`/`hot_take` and `reaction`/`hot_take` borderline cases,
while short `trash_talk` and `reaction` posts are easy and confident. A gap
of 0.20 means at least 2 more right answers out of about 10 posts per third,
which is the smallest difference I'd trust not to be one lucky post.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
