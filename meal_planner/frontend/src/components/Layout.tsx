import { NavLink, Outlet } from "react-router-dom";

function navClass(isActive: boolean): string {
  return [
    "flex-1 px-3 py-4 text-center text-sm font-medium",
    isActive ? "text-accent" : "text-ink/70",
  ].join(" ");
}

export function Layout() {
  return (
    <div className="mx-auto flex min-h-screen max-w-lg flex-col">
      <header className="px-4 pt-6 pb-2">
        <p className="text-sm text-ink/60">Home Assistant</p>
        <h1 className="text-2xl font-semibold tracking-tight">Maaltijdplanner</h1>
      </header>
      <main className="flex-1 px-4 pb-24">
        <Outlet />
      </main>
      <nav className="fixed inset-x-0 bottom-0 border-t border-line bg-paper">
        <div className="mx-auto flex max-w-lg">
          <NavLink to="/" end className={({ isActive }) => navClass(isActive)}>
            Overzicht
          </NavLink>
          <NavLink to="/instellingen" className={({ isActive }) => navClass(isActive)}>
            Instellingen
          </NavLink>
        </div>
      </nav>
    </div>
  );
}
