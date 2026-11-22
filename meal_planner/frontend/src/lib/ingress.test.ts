import { describe, expect, it } from "vitest";
import { basenameFromBaseHref } from "./ingress";

describe("basenameFromBaseHref", () => {
  it("uses the ingress path without a trailing slash", () => {
    expect(basenameFromBaseHref("/api/hassio_ingress/Ab12/")).toBe("/api/hassio_ingress/Ab12");
  });

  it("keeps the site root empty", () => {
    expect(basenameFromBaseHref("/")).toBe("");
    expect(basenameFromBaseHref("http://homeassistant.local:8123/")).toBe("");
  });
});
