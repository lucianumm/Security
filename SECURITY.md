# Security Policy

## Scope

This policy covers this repository's security-auditor skill, scripts, schemas, CI examples and
distribution files. It does not authorize testing any application that uses the skill or any
external service.

## Reporting a vulnerability

Please report a suspected vulnerability privately through GitHub's “Report a vulnerability” flow
on this repository's Security tab. Include the affected path or release, a concise impact statement,
and a safe reproduction using synthetic data. Do not include credentials, customer data or a
destructive proof of concept. If private reporting is unavailable, contact the repository owner
through the public GitHub profile and request a private reporting channel; do not publish exploit
details before coordinated disclosure.

There is no public bug-bounty commitment or guaranteed response time. The maintainer will assess
reports and coordinate a fix and disclosure when feasible.

## Safe use

The skill is defensive and must only be used on systems the operator owns or is authorized to
assess. Dynamic tests require explicit authorization, a controlled local or staging target, and
bounded non-destructive requests. Discovered credentials must never be used to authenticate.
