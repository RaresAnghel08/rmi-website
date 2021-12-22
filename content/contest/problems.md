---
title: "Problems"
menu:
  main:
    parent: "contest"
    weight: 4
draft: false
---

<!-- Tasks will be published after the contest days. -->

<!-- {{< section title="Download problems" >}}

Problem statements, graders, checkers and parameters.

[Download in `.zip` format](/problems.zip)

[Download in `.tar.gz` format](/problems.tar.gz)

{{< section title="Download tests" >}}

Problem tests. Warning: large archive!

[Download in `.zip` format](/tests.zip)

[Download in `.tar.gz` format](/tests.tar.gz)

{{< section title="Download submissions" >}}

Solutions submitted by the participants during the contest.

[Download in `.zip` format](/submissions.zip)

[Download in `.tar.gz` format](/submissions.tar.gz) -->

{{< section title="Problem Statements" link="/statements.pdf" >}}
{{< pdf file="/statements.pdf" >}}

{{< section title="Announcements and Erratas" >}}

### Day 1

In chronological order:

1. About the meaning of A \ {max A} in task Present

    * A is a set, max A is the maximum of set A (e.g. if A = {1, 2, 3} then max A = 3). Then, {max A} is the one-element set consisting of just max A (in my example {max A} = {3}). Finally, A \ {max A} means the set A without its maximum (in my example A \ {max A} = {1, 2, 3} \ {3} = {1, 2}). The operator "\" here means set difference.

2. Task Gardening

    * 1 <= T <= 100 000

3. Task Gardening

    * Correction: "(i.e. where the output is not -1)" should read "(i.e. where the output is not NO)" in the English version.

4. Speedrun

    * If the index of the goTo() function is invalid the grader will give 0 points.

5. Interval between submissions increased

    * Due to high load, all tasks now have a 2 minutes requirement between submissions to the respective tasks. This limit might be ammended later.

6. Present

    * Due to high load, submissions to task present now have to be made at least 5 minutes apart. We hope to decrease this limit soon.

7. Interval between submissions decreased

    * All tasks now have a 1 minute requirement between submissions to the respective tasks. The contest will not be extended.
    * According to the rules, feedback in the last 30 minutes is possible to get but not guaranteed.

### Day 2

In chronological order:

1. Paths IT translation

    * Under "Spiegazione" the following: "(1, 2), (2, 3), (3, 4), (2, 5), (1, 7) e (7, 9)" should be "(1, 2), (2, 3), (3, 4), (2, 6), (1, 7) e (7, 9)".

2. Nom RO translation

    * The following: "daca distanta dintre doua pietre care au acelasi numar scrie pe ele este egala cu un multiplu de M inchi" should be "daca distanta dintre doua pietre care au acelasi numar scri*s* pe ele este egala cu un multiplu de M inchi".

3. NoM Clarification
    
    * The phrasing "if the distance between two stones that have the same number written on them is a multiple of M inches" means "if there exist two stones with the same number written on them such that the distance between them is a multiple of M inches".

4. Weirdtree Clarification

    * The restriction that l = 1 and r = N is valid for both operations (both cut and inspect operations).

5. General


    * The testing interface is provided "as is", and we do not endeavour in providing support for it, unfortunately, as per the competition rules.
    * This means that, for example, the testing interface most likely will not work properly for task Weirdtree.

6. Scoring

    * Points are awarded only for correctly solved groups of inputs. If there are partial grading rules for the problem, then the score for an input group will be the lowest among the scores for the particular test inputs contained in the group.
    * The score of a contestant for a task is the sum of the scores obtained for each group of this task. The score obtained for a group is the highest score obtained on this group among all contestant’s submissions for the task.

7. Weirdtree Clarification Subtask 5

    * For subtask 5 what the constraints tells is that:
      1) All 3 types of schedule entries are possible (cut, magic, inspect).
      2) For operation cut, it always holds that l = 1, r = N (no constraint on k).
      3) For operation inspect, it always holds that l = 1, r = N.

8. Last 10 Minutes

    * We removed the constraint to submit at most once per minute per problem.

{{< section title="Original Statements and Translations" >}}

### Day 1

[Gardening (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_gardening.zip)

[Present (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_present.zip)

[Speedrun (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_speedrun.zip)

### Day 2

[NoM (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_nom.zip)

[Paths (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_paths.zip)

[Weirdtree (EN, BG, DE, HE, HU, IT, RO, RU, UK)](/statements_weirdtree.zip)

The editorial, official solutions, testcases, graders and other extras can be found in [solutions and editorial](/solutions).
