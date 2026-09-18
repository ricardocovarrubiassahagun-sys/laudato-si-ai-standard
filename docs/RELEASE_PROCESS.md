# Release process

This document describes a lightweight release process for maintainers.

## Before a release

1. Open or link the public proposal for material standard changes.
2. Update tests and benchmark cases where behavior changes.
3. Run CI successfully.
4. Update `CHANGELOG.md`.
5. Update version numbers consistently.
6. Review licensing and attribution notices.
7. Confirm the independence notice remains accurate.
8. Review documentation links and quickstart commands.

## Release

1. Create a version tag using semantic versioning for the reference implementation.
2. Publish a GitHub Release with a concise summary and migration notes.
3. Attach or link reproducible benchmark information when relevant.
4. For stable citation, archive the release in a persistent repository such as Zenodo and update `CITATION.cff` with the DOI when available.

## After a release

1. Verify the CI badge and installation instructions.
2. Verify release links.
3. Announce through community channels without implying third-party endorsement.
4. Record known limitations and follow-up work.

## Standard vs. implementation

Changes to the written standard and changes to the reference implementation should be distinguished clearly in release notes.
