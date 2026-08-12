# Expected output

The program should create an output directory containing:

- `summary.csv` with one row per group;
- `measurement_a.png` with labelled axes and groups;
- `REPORT.md` explaining the result and quality-control counts; and
- `run.log` containing the command, package versions, and completion status but
  no input rows.

It should fail clearly when a required column is missing and must not modify the
input file.
