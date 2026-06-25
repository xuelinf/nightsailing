import test from "node:test";
import assert from "node:assert/strict";
import { products, siteMeta } from "./products.js";

test("site metadata starts at version 0.0.2", () => {
  assert.equal(siteMeta.version, "0.0.2");
  assert.equal(siteMeta.name, "夜航船之书");
  assert.match(siteMeta.headline, /AI 工具/);
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

test("every product has enough material for a showcase detail page", () => {
  for (const product of products) {
    assert.match(product.index, /^\d{2}$/);
    assert.ok(product.shortName);
    assert.ok(product.manifesto.length >= 12);
    assert.ok(product.detail.length >= product.summary.length);
    assert.ok(product.visual);
    assert.equal(product.scenes.length, 3);
    assert.equal(product.mediaSlots.length, 3);
  }
});
