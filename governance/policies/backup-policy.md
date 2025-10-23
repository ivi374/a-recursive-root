# Backup Policy

Backups are performed regularly on all critical data, including the `archive`
and `workspace` directories.  Snapshots should be created using the
`scripts/backup` script and stored in `archive/snapshots`.  Retention
periods and cadence are configured in `cloud/backups.yml`.
