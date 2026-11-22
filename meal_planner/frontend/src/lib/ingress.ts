export function basenameFromBaseHref(href: string): string {
  const url = new URL(href, "http://local.invalid");
  let path = url.pathname;
  if (path.length > 1 && path.endsWith("/")) {
    path = path.slice(0, -1);
  }
  return path === "/" ? "" : path;
}

export function currentBasename(): string {
  const href = document.querySelector("base")?.href ?? "/";
  return basenameFromBaseHref(href);
}
