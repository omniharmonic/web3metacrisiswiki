import { FullSlug, isRelativeURL, resolveRelative, simplifySlug } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import { write } from "./helpers"
import { BuildCtx } from "../../util/ctx"
import { VFile } from "vfile"
import path from "path"

function toTitleCaseSegment(seg: string): string {
  if (seg.length === 0) return seg
  return seg.charAt(0).toUpperCase() + seg.slice(1).toLowerCase()
}

function generateCaseVariants(slug: FullSlug): FullSlug[] {
  // do not touch root index pages
  if (slug === ("index" as FullSlug)) return []
  const segments = slug.split("/")
  // create all-lowercase variant
  const lower = segments.map((s) => s.toLowerCase()).join("/") as FullSlug
  // create Title-Case-per-segment variant
  const title = segments.map((s) => toTitleCaseSegment(s)).join("/") as FullSlug
  const variants = new Set<FullSlug>()
  variants.add(lower)
  variants.add(title)
  return Array.from(variants)
}

async function* emitRedirect(ctx: BuildCtx, fromSlug: FullSlug, toSlug: FullSlug) {
  const redirUrl = resolveRelative(fromSlug, toSlug)
  yield write({
    ctx,
    content: `
      <!DOCTYPE html>
      <html lang="en-us">
      <head>
      <title>${toSlug}</title>
      <link rel="canonical" href="${redirUrl}">
      <meta name="robots" content="noindex">
      <meta charset="utf-8">
      <meta http-equiv="refresh" content="0; url=${redirUrl}">
      </head>
      </html>
      `,
    slug: fromSlug,
    ext: ".html",
  })
}

async function* processFile(ctx: BuildCtx, file: VFile) {
  const ogSlug = simplifySlug(file.data.slug!)

  // frontmatter-provided aliases
  for (const aliasTarget of file.data.aliases ?? []) {
    const aliasTargetSlug = (
      isRelativeURL(aliasTarget)
        ? path.normalize(path.join(ogSlug, "..", aliasTarget))
        : aliasTarget
    ) as FullSlug

    if (aliasTargetSlug !== ogSlug) {
      yield* emitRedirect(ctx, aliasTargetSlug, ogSlug)
    }
  }

  // automatically add case-variant redirects to make wikilinks case-insensitive
  for (const variant of generateCaseVariants(ogSlug)) {
    if (variant !== ogSlug) {
      yield* emitRedirect(ctx, variant, ogSlug)
    }
  }
}

export const AliasRedirects: QuartzEmitterPlugin = () => ({
  name: "AliasRedirects",
  async *emit(ctx, content) {
    for (const [_tree, file] of content) {
      yield* processFile(ctx, file)
    }
  },
  async *partialEmit(ctx, _content, _resources, changeEvents) {
    for (const changeEvent of changeEvents) {
      if (!changeEvent.file) continue
      if (changeEvent.type === "add" || changeEvent.type === "change") {
        // add new ones if this file still exists
        yield* processFile(ctx, changeEvent.file)
      }
    }
  },
})
