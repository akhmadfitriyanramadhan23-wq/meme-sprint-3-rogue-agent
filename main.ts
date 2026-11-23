// meme-sprint-3-rogue-agent
// Entry program: copies the meme image to /output/entry.png.
// The image itself is drawn by tools/make-image.py (PIL, fixed seed,
// fully procedural); this program only ships the finished file.
// Node 22, stdlib only, no network. Deterministic: two runs write
// byte-identical output (entry.png sha256 ac2f7486...).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const dst = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log("wrote", dst);
