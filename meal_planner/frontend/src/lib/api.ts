export class ApiClientError extends Error {
  readonly code: string;

  constructor(code: string, message: string) {
    super(message);
    this.code = code;
  }
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const base = document.querySelector("base")?.getAttribute("href") ?? "/";
  const url = new URL(path.replace(/^\//, ""), new URL(base, window.location.href));
  const headers = new Headers(init?.headers);
  headers.set("Accept", "application/json");
  if (init?.body) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(url, { ...init, headers });
  if (!response.ok) {
    let code = "request_failed";
    let message = "Er ging iets mis.";
    try {
      const body = (await response.json()) as { error?: { code?: string; message?: string } };
      code = body.error?.code ?? code;
      message = body.error?.message ?? message;
    } catch {
      message = "Er ging iets mis.";
    }
    throw new ApiClientError(code, message);
  }
  return (await response.json()) as T;
}
