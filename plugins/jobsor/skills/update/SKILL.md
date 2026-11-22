---
name: update
description: Bring a JOBSOR user's setup up to date after the plugin was updated, running only the setup steps that are new since their profile was made. Use when the user types /jobsor:update, says "update JOBSOR", "what's new in JOBSOR", or when start or the round says the profile is older than the plugin.
---

# Update JOBSOR

The plugin can change after the user set it up. This skill runs only what is new, so the user never redoes setup.

## What to do

1. **Find the two versions.**
   - The plugin's version: the `version` in this plugin's `.claude-plugin/plugin.json` (latest entry in `references/changes.md` if the
     file cannot be read).
   - The profile's version: the "Plugin version:" line in the JOBSOR profile. No such line means the profile was made before 0.2.8:
     treat it as 0.2.7. If there is no profile at all, say so and run the setup skill instead; stop here.

2. **If they are the same,** say "JOBSOR is up to date (version X). Nothing to do." and stop.

3. **Find what is new.** Read `references/changes.md` and take every entry newer than the profile's version, oldest first. Do not list
   them to the user; just do them.

4. **Run each Step in order,** one at a time, exactly as its entry says (most point to a setup skill step: follow that step in the
   setup skill, but only that step). Change only what the step is about; never touch confirmed facts, roles, templates or other answers
   unless the step says so. If the user says "skip", skip it and note it.

5. **Save.** Set the profile's "Plugin version:" line to the plugin's version (add the line under "About me" if missing). Add a Log row
   to the tracker: today's date, "Updated to X: <steps done>; skipped: <steps skipped or none>".

6. **Report** in three lines at most: version now, steps done, anything the user still has to do (for example "turn on Naukri alerts
   for <role>").

## Rules
- **Shared rules:** follow `skills/round/references/shared-rules.md` (read it once per run; a round has already read it).
