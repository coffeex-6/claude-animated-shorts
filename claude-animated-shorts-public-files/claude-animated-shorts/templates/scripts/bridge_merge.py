# Merge sandbox-owned files back into the main bridge folder.
# Usage: python scripts/bridge_merge.py [cam,world,mat,char,post]
# Set REMOTION_PROJECT_ROOT to override automatic project-root discovery.
import os, shutil, sys, time, filecmp

def find_project_root():
    override = os.environ.get("REMOTION_PROJECT_ROOT")
    if override:
        return os.path.abspath(os.path.expanduser(override))
    here = os.path.abspath(os.getcwd())
    for candidate in [here] + [os.path.dirname(here)] * 5:
        if os.path.isfile(os.path.join(candidate, "package.json")) and os.path.isdir(os.path.join(candidate, "src")):
            return candidate
    raise SystemExit("ERROR: Could not find Remotion project root. Run this script from the project folder or set REMOTION_PROJECT_ROOT.")

ROOT = find_project_root()
MAIN = os.path.join(ROOT, "src", "videos", "bridge")
if not os.path.isdir(MAIN):
    raise SystemExit(f"ERROR: main bridge folder not found: {MAIN}")
OWN = {
    "cam": ["story.ts"],
    "world": ["world.ts", "lights.ts", "shade.ts", "grade.ts"],
    "mat": ["paint.ts", "build.ts"],
    "char": ["toon.ts", "cast.ts", "cardshade.ts"],
    "post": ["ink.ts", "Bridge.tsx", "lensblur.ts"],
}
which = sys.argv[1].split(",") if len(sys.argv) > 1 else list(OWN)
unknown = [x for x in which if x not in OWN]
if unknown:
    raise SystemExit("ERROR: unknown sandbox owner(s): " + ", ".join(unknown))
bak = os.path.join(ROOT, "backup", time.strftime("bridge_%Y%m%d_%H%M%S"))
shutil.copytree(MAIN, bak)
print("backup ->", bak)
for box in which:
    src = os.path.join(ROOT, "src", "videos", f"bridge_{box}")
    for name in OWN[box]:
        a, b = os.path.join(src, name), os.path.join(MAIN, name)
        if not os.path.exists(a):
            print(f"  {box}: {name} not in sandbox (skipped)")
            continue
        if os.path.exists(b) and filecmp.cmp(a, b, shallow=False):
            print(f"  {box}: {name} unchanged")
            continue
        shutil.copy2(a, b)
        print(f"  {box}: {name} -> main")
