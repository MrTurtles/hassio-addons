import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { currentBasename } from "./lib/ingress";
import { Dashboard } from "./pages/Dashboard";
import { SettingsPage } from "./pages/Settings";

export function App() {
  return (
    <BrowserRouter basename={currentBasename()}>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="instellingen" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
