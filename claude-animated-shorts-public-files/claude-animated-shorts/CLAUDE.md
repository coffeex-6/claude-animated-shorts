# Afran's Permanent Video Workflow

This file is the project-level source of truth. Read it at the start of every new Claude Code session. Also read `SKILL.md` and `references/USER_STYLE_LOCK.md`.

## Non-negotiable workflow: script first, voice second, video third

1. **Start by proposing a voice-over script only.** Do not create the full scene, characters, animation, music or final render yet.
2. The script must be original, fact-checked when factual, suitable for a YouTube Short, and written in natural spoken English unless Afran requests another language.
3. Include an estimated duration and approximate word count. Keep the narration clear and visual. Do not pad the script to hit a duration.
4. Present the complete script to Afran and wait for approval or edits.
5. After approval, ask Afran to record/generate the narration and upload the final audio file, normally `voice.wav`.
6. Do not start final animation or final rendering until Afran supplies the approved voice file.
7. Once audio is uploaded, inspect its actual duration, sample rate, channel count and audio quality. Do not assume the duration from an earlier message.
8. Generate word-level timestamps from the supplied voice using an available aligner/transcription tool. Save them as `voice/words.json`. Manually correct transcription mistakes and check that every word has sensible start/end times.
9. Match the Remotion composition duration exactly to the supplied voice duration. At 30 fps, `TOTAL = round(duration_seconds * 30)`. Make the final frame count and audio mux duration agree. Never silently truncate, stretch, speed up or pad the narration.
10. Create a storyboard and shot plan from the approved script and actual word timings. The visual reaction should land on or just before the corresponding spoken word.
11. Build original characters and a detailed 3D toon environment using `references/USER_STYLE_LOCK.md` and the four unchanged reference images in `references/user-style/`.
12. Render low-resolution stills or short previews first. Inspect every scene for style consistency, character continuity, environment detail, lighting, contrast, glow, shadows and framing.
13. Fix all visual and technical problems before rendering the full-resolution video.
14. Build original music and sound effects that fit the actual story and exact duration. Keep narration clear and dominant. Do not reuse the bridge short's marching soundtrack or its shot-specific sound cues unless the new story genuinely calls for them.
15. Render the final vertical MP4 at 1440x2560, 30 fps, unless Afran explicitly requests a different output.
16. Verify the finished MP4 with ffprobe or equivalent: duration, resolution, frame rate, audio presence, audio/video sync and successful playback.
17. Deliver the final MP4 and any useful project files. Report any unresolved limitation honestly.

## Required response at the start of every new project

Give Afran 3-5 original topic ideas only if he has not supplied a topic. If he has supplied a topic, write the script directly. Always give the full voice-over script first. End by asking for approval or changes. Do not ask him to upload voice before the script is approved.

## Persistent preferences

- Call the user Afran only if needed; casual, direct language is preferred.
- The target visual style is fixed by `references/USER_STYLE_LOCK.md`. Do not drift into photorealism, anime, Pixar-like 3D humans or flat 2D backgrounds.
- Keep the supplied style reference images unchanged.
- Build rich, dimensional environments with suitable houses/buildings, trees/plants, clouds/sky, streets/floors, furniture and story props.
- Characters should use simple round white faces, dark outlines, minimal expressive features and thin dark limbs, with story-specific clothes and accessories.
- Match the reference lighting: clear contrast, bright readable subjects, warm key light, cool shadows, subtle controlled glow/bloom, depth of field and grounded contact shadows.
- Default to no subtitles, no intro logo and no outro unless requested.
- Do not claim a render is complete until the actual output file has been produced and verified.

## Duration and audio safety

The files under `templates/audio/` are a bespoke soundtrack implementation for the example bridge story. Its event timings, music sections, camera-distance automation and shot map are not a universal soundtrack for every new video. Rebuild the audio timeline and cues for each new story.

The bridge example's timeline is 67.5 seconds. It must never be used unchanged for a different narration length. In particular, a 75.2-second voice must produce a 75.2-second composition and a newly designed 75.2-second soundtrack. Do not simply change one duration constant while leaving the old shot/event schedule intact.

If a word aligner is unavailable, explain the limitation and ask before using an alternate alignment method. Never invent word timings.
