# Repositories

{{ repo_count() }} repositories, grouped by role. Release information was last synchronised on {{ releases_generated_at }}.

## Firmware

{{ repo_table(category='firmware') }}

## Tools and applications

{{ repo_table(category='tool', columns=('purpose','status','license','app')) }}

## Device documentation (BOM, assembly)

{{ repo_table(category='device-docs') }}

## Electronics

{{ repo_table(category='hardware') }}

## Mechanics

{{ repo_table(category='mechanics') }}

## Decoders, integrations and platforms

{{ repo_table(category=['decoder','integration','platform','hub']) }}

## Archived

{{ repo_table(category='archive') }}
