# ADR 0002: Container Boundaries

Date: 2025‑10‑23

## Status

Accepted

## Context

To support modularity, we need to decide how to define container
boundaries for our services.

## Decision

Each major component will run in its own container built from a
language‑specific base defined in `containers/languages`.

## Consequences

Clear isolation of components; increased operational overhead.
