import { useEffect, useState, type FormEvent } from "react";
import { apiRequest } from "../lib/api";
import type { HouseholdSettings } from "../types/settings";

export function SettingsPage() {
  const [settings, setSettings] = useState<HouseholdSettings | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    let active = true;
    apiRequest<HouseholdSettings>("api/v1/settings")
      .then((body) => {
        if (active) {
          setSettings(body);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : "Instellingen laden lukt niet.");
        }
      });
    return () => {
      active = false;
    };
  }, []);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!settings) {
      return;
    }
    setSaving(true);
    setSaved(false);
    setError(null);
    try {
      const updated = await apiRequest<HouseholdSettings>("api/v1/settings", {
        method: "PATCH",
        body: JSON.stringify({
          name: settings.name,
          default_servings: settings.default_servings,
          timezone: settings.timezone,
          subtract_pantry: settings.subtract_pantry,
          auto_shopping: settings.auto_shopping,
          preserve_checked: settings.preserve_checked,
          preserve_manual: settings.preserve_manual,
          auto_consume_pantry: settings.auto_consume_pantry,
        }),
      });
      setSettings(updated);
      setSaved(true);
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : "Opslaan lukt niet.");
    } finally {
      setSaving(false);
    }
  }

  if (!settings) {
    return <p className="text-sm text-ink/70">{error ?? "Instellingen laden…"}</p>;
  }

  return (
    <form className="grid gap-4" onSubmit={onSubmit}>
      <label className="grid gap-1 text-sm">
        Naam
        <input
          className="rounded-xl border border-line bg-white px-3 py-3"
          value={settings.name}
          onChange={(event) => setSettings({ ...settings, name: event.target.value })}
        />
      </label>
      <label className="grid gap-1 text-sm">
        Aantal personen
        <input
          className="rounded-xl border border-line bg-white px-3 py-3"
          type="number"
          min={1}
          max={24}
          value={settings.default_servings}
          onChange={(event) =>
            setSettings({ ...settings, default_servings: Number(event.target.value) })
          }
        />
      </label>
      <label className="grid gap-1 text-sm">
        Tijdzone
        <input
          className="rounded-xl border border-line bg-white px-3 py-3"
          value={settings.timezone}
          onChange={(event) => setSettings({ ...settings, timezone: event.target.value })}
        />
      </label>
      <dl className="grid gap-2 rounded-2xl border border-line bg-white p-4 text-sm">
        <div className="flex justify-between gap-4">
          <dt>Taal</dt>
          <dd>Nederlands</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt>Eenheden</dt>
          <dd>Metrisch</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt>Weekstart</dt>
          <dd>Maandag</dd>
        </div>
      </dl>
      <fieldset className="grid gap-3 rounded-2xl border border-line bg-white p-4">
        <legend className="px-1 text-sm font-medium">Boodschappen</legend>
        <Toggle
          label="Voorraad verrekenen"
          checked={settings.subtract_pantry}
          onChange={(checked) => setSettings({ ...settings, subtract_pantry: checked })}
        />
        <Toggle
          label="Lijst automatisch bijwerken"
          checked={settings.auto_shopping}
          onChange={(checked) => setSettings({ ...settings, auto_shopping: checked })}
        />
        <Toggle
          label="Afgevinkte artikelen behouden"
          checked={settings.preserve_checked}
          onChange={(checked) => setSettings({ ...settings, preserve_checked: checked })}
        />
        <Toggle
          label="Handmatige artikelen behouden"
          checked={settings.preserve_manual}
          onChange={(checked) => setSettings({ ...settings, preserve_manual: checked })}
        />
        <Toggle
          label="Voorraad afboeken na het koken"
          checked={settings.auto_consume_pantry}
          onChange={(checked) => setSettings({ ...settings, auto_consume_pantry: checked })}
        />
      </fieldset>
      {error ? <p className="text-sm text-red-800">{error}</p> : null}
      {saved ? <p className="text-sm text-accent">Opgeslagen.</p> : null}
      <button
        className="rounded-xl bg-accent px-4 py-3 font-medium text-white disabled:opacity-60"
        type="submit"
        disabled={saving}
      >
        {saving ? "Opslaan…" : "Opslaan"}
      </button>
    </form>
  );
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}) {
  return (
    <label className="flex items-center justify-between gap-4 text-sm">
      <span>{label}</span>
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
    </label>
  );
}
