# Class 18: use a coding agent without sharing your real data — video proposal

## Scene 1: The question

You have research data in RCC and want a coding agent to write
the analysis. The safe answer is not to upload the real spreadsheet. Give the
coding agent a small invented example that has the same useful structure.

## Scene 2: Three simple choices

Choose the file in your RCC project, describe the result, and click Make AI
example. RCC creates the question, safe schema, invented rows, expected output,
and prompt as one ready-to-upload ZIP. Ordinary tables do not need a form or a
case-by-case approval.

## Scene 3: Invent every value

RCC creates synthetic rows with obvious labels such as SYN-001 and group_a. It
does not shuffle rows, hash IDs, or replace only names because remaining dates,
free text, and rare combinations can still describe real people. If a safe
fixture cannot be made, the screen offers Use inside RCC instead.

## Scene 4: Ask for general code

Give the invented bundle to the coding agent. Ask for code with input and output
arguments, no network access, no input modification, clear validation, pinned
packages, and a test command. Ask to see the plan first.

## Scene 5: Test inside RCC

Bring the code back to RCC. Inspect it, then run it on the synthetic example.
Check the table, plot, report, and log. For larger work, use an RCC worker.

## Scene 6: Run on the real data

Only after review, point the same code at the real project input inside RCC.
Keep real outputs and revealing error messages inside the approved path. You are
done when the external coding agent has seen only invented data and the real
analysis is reproducible inside RCC.
