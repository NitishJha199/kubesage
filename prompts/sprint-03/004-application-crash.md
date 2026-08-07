# Sprint 3 - Application Crash Knowledge

## Goal

Teach KubeSage to recognize generic application crashes.

## Cursor Prompt

You are working on the KubeSage project.

Architecture rules:

- Keep the existing Knowledge architecture.
- Use the existing Knowledge model.
- No diagnosis logic.
- Only create knowledge entries.

Task:

Create a new knowledge entry named APPLICATION_CRASH.

Fields:

- reason = "Error"
- issue = "ApplicationCrash"
- severity = "CRITICAL"
- confidence = 0.90

Description:

The container terminated because the application exited with an error.

Recommendation:

- Inspect container logs.
- Verify startup configuration.
- Validate environment variables.
- Check mounted volumes.
- Verify required dependencies.

Update the registry to include the new knowledge entry.

## Outcome

Application crash knowledge added.
