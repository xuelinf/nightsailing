import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { parseSiteContent } from "./contentParser.js";

const contentMarkdown = readFileSync(new URL("../content/site-content.md", import.meta.url), "utf8");
const { products, siteMeta } = parseSiteContent(contentMarkdown);

test("site metadata is read from the content markdown", () => {
  assert.equal(siteMeta.version, "0.0.4");
  assert.equal(siteMeta.name, "夜航船之书");
  assert.equal(siteMeta.headline, "一册个人 AI 工具目录。");
  assert.match(contentMarkdown, /新产品资料清单/);
});

test("catalog exposes two available products and two planned products", () => {
  assert.equal(products.length, 4);
  assert.equal(products.filter((product) => product.status === "available").length, 2);
  assert.equal(products.filter((product) => product.status === "planned").length, 2);
});

test("available products have download links and planned products do not", () => {
  for (const product of products) {
    if (product.status === "available") {
      assert.match(product.downloadHref, /^\/downloads\/.+\.dmg$/);
    } else {
      assert.equal(product.downloadHref, "");
    }
  }
});

test("AI航行日记 is open source and AI 语音输入 is promised free open source", () => {
  const radar = products.find((product) => product.slug === "ai-sailing-log");
  const voice = products.find((product) => product.slug === "ai-voice-input");

  assert.equal(radar.sourceHref, "https://github.com/xuelinf/vibe-token-usage");
  assert.equal(voice.openSourceLabel, "免费开源");
});

test("every product has enough factual material for the public catalog", () => {
  for (const product of products) {
    assert.match(product.index, /^\d{2}$/);
    assert.ok(product.shortName);
    assert.ok(product.category);
    assert.ok(product.summary.length >= 12);
    assert.ok(product.detail.length >= product.summary.length);
    assert.ok(product.privacy.length >= 12);
    assert.ok(product.visual);
    assert.equal(product.highlights.length, 3);
    assert.equal(product.useCases.length, 3);
    assert.equal(product.materials.length, 3);
    assert.equal(Object.hasOwn(product, "prompt"), false);
    assert.equal(Object.hasOwn(product, "evidence"), false);
  }
});
