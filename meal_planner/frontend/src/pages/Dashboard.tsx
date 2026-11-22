export function Dashboard() {
  return (
    <section className="grid gap-3">
      <article className="rounded-2xl border border-line bg-white p-4">
        <h2 className="text-sm font-medium text-ink/60">Vandaag</h2>
        <p className="mt-1 text-lg">Nog niet gepland</p>
      </article>
      <article className="rounded-2xl border border-line bg-white p-4">
        <h2 className="text-sm font-medium text-ink/60">Morgen</h2>
        <p className="mt-1 text-lg">Nog niet gepland</p>
      </article>
      <p className="px-1 text-sm leading-6 text-ink/70">
        Recepten, het weekmenu en de boodschappen komen hierna. Een maaltijd kun je
        later ook in de Home Assistant-agenda plannen.
      </p>
    </section>
  );
}
