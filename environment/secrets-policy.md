# Secrets Policy

This document describes how secret values are managed within this
cartridge.  Secret environment variables should be defined in
`.env` files which are excluded from version control.  Public defaults
should be provided in `.env.example`.  Use a vault or secret manager to
store and rotate sensitive values.
