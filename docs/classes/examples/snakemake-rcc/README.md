# RCC Snakemake class example

This ready-now example creates only synthetic text. Copy the whole directory
into an approved shared project path, inspect it, and begin with a dry run:

```bash
snakemake --dry-run --printshellcmds
snakemake --profile IKIM --jobs 4
```

The managed `IKIM` profile submits rule jobs through Slurm. Do not replace it
with copied historic profile settings.
